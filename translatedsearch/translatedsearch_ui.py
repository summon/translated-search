import logging

from translatedsearch import settings
from flask import Blueprint, render_template, request, Response

from translatedsearch.utils.translatedsearcher import TranslatedSearcher

bp = Blueprint('translatedsearch', __name__)

NUM_RESULTS = 50
TRANSLATE_QUERY = True
INCLUDE_ABSTRACTS = False
LANG_FILTER = True
JOURNAL_ONLY = True


@bp.route('/', methods=('GET', 'POST'))
def index():
    data = None
    csv = False
    search = ''
    language = ''
    if request.method == 'POST':
        action = request.values.get('action', '')
        search = request.form['search']
        language = request.form['target_language']
        logging.debug('Search: {0}'.format(search))
        logging.debug('Target Language: {0}'.format(language))

        ts = TranslatedSearcher()

        csv = False
        if action == 'download':
            csv = True

        data = ts.tsearch(settings.supported_languages.get(language),
                          search,
                          journalArticlesOnly=JOURNAL_ONLY,
                          langFilter=LANG_FILTER,
                          includeAbstract=INCLUDE_ABSTRACTS or csv,
                          translateQuery=TRANSLATE_QUERY,
                          numResults=NUM_RESULTS,
                          returncsv=csv)

    if csv:
        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=translated_search.csv"})

    return render_template('index.html', search=search, language=language, languages=settings.supported_languages.keys(), data=data)
