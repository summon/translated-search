import six
import html

from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

# max number of text segments that can be passed to translate method (See https://cloud.google.com/translate/docs/reference/rest/v2/translate#query-parameters)
MAX_NUM_SEGMENTS = 128


class GoogleTranslate:
    def __init__(self, credentials=None):

        g_credentials = None
        if credentials:
            g_credentials = service_account.Credentials.from_service_account_file(credentials)
        self.translate_client = translate.Client(credentials=g_credentials)

    def translate_text(self, source_language, target_language, text):
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = self.translate_client.translate(text, source_language=source_language, target_language=target_language)
        return html.unescape(result["translatedText"])

    def translate_list(self, source_language, target_language, list_of_text):
        result = []
        for chunk in self.divide_chunks(list_of_text, MAX_NUM_SEGMENTS):
            result += self.translate_client.translate(chunk, source_language=source_language, target_language=target_language)
        return list(map(lambda n: html.unescape(n["translatedText"]), result))

    def divide_chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]
