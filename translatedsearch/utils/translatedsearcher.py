import json
from iso639 import languages

from translatedsearch.utils.summonapi import SummonAPI
from translatedsearch.utils.googletranslate import GoogleTranslate
from translatedsearch import settings

"""
Translated Search Backend
"""

class TranslatedSearcher():
    def __init__(self):
        self.google = GoogleTranslate(settings.GOOGLE_CRED_JSON_FILE)
        self.api = SummonAPI()
        self.default_fields = ["Title", "Subtitle", "Author", "PublicationTitle", "PublicationDate",
                               "ContentType", "Language", "ISSN", "ISBN", "ParticipantIDs", "DOI", "URI"]
        self.default_fields_with_abstract =  ["Title", "Subtitle", "Author", "PublicationTitle", "PublicationDate", "Abstract",
                               "ContentType", "Language", "ISSN", "ISBN", "ParticipantIDs", "DOI"]
        self.translatable_fields = {"Title", "Subtitle", "Author", "PublicationTitle", "Abstract"}
        self.user_lang = "en"

    def q_translate(self, lang, qstr):
        """Transate q parameter only"""
        tqstr = self.google.translate_text(self.user_lang, lang, qstr)
        return tqstr

    def add_to_fvf(self, params, value):
        if "s.fvf" in params:
            params["s.fvf"].append(value)
        else:
            params["s.fvf"] = [value,]
        return params

    def search(self, lang, qstr, params, translateQuery=True):
        """Translate qstr to the language specified in lang, and issue query to Summon API"""
        if translateQuery:
            qstr = self.google.translate_text(self.user_lang, lang, qstr)

        all_params = {"s.q":qstr}
        if params != None:
            all_params.update(params)
        response_text = self.api.search(all_params)
        return json.loads(response_text)

    def tsearch(self, lang, qstr, journalArticlesOnly=False, langFilter=True, includeAbstract=False, translateQuery=True, numResults=50, returncsv=True):
        """Issue translated search and return translated results in csv
           - langFilter : if True, apply language facet filter
           - includeAbstract : if True, include translated Abstract in results
           - journalArticlesOnly : if True, return journal articles only
           - translateQuery : if True, translate query (set it to False if it has already been translated)
           - numResults : number of results
        """
        params = {}
        if langFilter:
            lang_full = languages.get(alpha2=lang).name
            params = self.add_to_fvf(params, "Language," + lang_full + ",f")
        if includeAbstract:
            fields = self.default_fields_with_abstract
            params["s.fl"] = ",".join(self.default_fields_with_abstract)
        else:
            fields = self.default_fields
            params["s.fl"] = ",".join(self.default_fields)
        if journalArticlesOnly:
            params = self.add_to_fvf(params, "ContentType,Journal Article,f")
        else:
            params = self.add_to_fvf(params, "Language," + lang_full + ",f") 

        params["s.ps"] = numResults

        results = self.search(lang, qstr, params, translateQuery=translateQuery)

        record_count = 0
        translated_query = ''
        try:
            record_count = results.get('recordCount', 0)
            translated_query = results.get('query', {}).get('textQueries', [{}])[0].get('textQuery', '')
        except:
            pass

        lines = self.json_to_lists(results, fields)
        lines_trans = self.translate_fields(lang, lines, self.translatable_fields)

        if returncsv:
            return self.lists_to_csv(lines_trans)
        else:
            return {'lines': lines_trans, 'record_count': record_count, 'translated_query': translated_query}

    def translate_fields(self, lang, lists, fieldsToTranslate):
        out = []
        fields = lists[0]
        translate_positions = set()
        fields_out = []
        i = 0
        for field in fields:
            fields_out.append(field)
            if field in fieldsToTranslate:
                translate_positions.add(i)
                fields_out.append(field + "_trans")
            i += 1
        out.append(fields_out)

        # first pass - create a list of field values to translate
        to_translate = []
        for line in lists[1:]:
            i = 0
            for field_value in line:
                if i in translate_positions:
                    to_translate.append(field_value)
                i += 1

        # translate
        translated_field_values = self.google.translate_list(lang, self.user_lang, to_translate)

        # second pass - merge in translated field values
        pos = 0
        for line in lists[1:]:
            i = 0
            line_out = []
            for field_value in line:
                line_out.append(field_value)
                if i in translate_positions:
                    line_out.append(translated_field_values[pos])
                    pos += 1
                i += 1
            out.append(line_out)

        return out

    def json_to_lists(self, results, fields):
        """Convert results in json to result list of field value lists"""
        lines = []

        # 1st line is a header
        lines.append(fields)
        
        for document in results["documents"]:
            line = []
            for field in fields:
                if field in document:
                    obj = document[field]
                    if isinstance(obj, list):
                        line.append(obj[0])
                    else:
                        line.append(document[field])
                else:
                    line.append("")
            lines.append(line)
        return lines

    def lists_to_csv(self, lists):
        """Convert result lists to csv"""
        out = []
        rank = 0
        for line in lists:
            if rank == 0:
                line2 = ["Rank",]
            else:
                line2 = [str(rank),]                
            rank += 1
            for item in line:
                line2.append(self.normalize_entry(item))
            out.append(",".join(line2))
        return "\n".join(out)

    def normalize_entry(self, entry):
        entry = entry.replace("\"", "'")
        return "\""+entry+"\""
            
    def pprint(self, response):
        print(json.dumps(response, indent=2, ensure_ascii=False))
