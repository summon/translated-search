import logging
import logging.handlers
import sys
import datetime

LOGGING_LEVEL = logging.DEBUG
LOGGING_BASE = '/tmp'

SUMMON_API_HOST = 'api.summon.serialssolutions.com'

# Google credentials
GOOGLE_CRED_JSON_FILE = ''

# Summon Credentials
SUMMON_ACCESS_ID = ''
SUMMON_API_KEY = ''


supported_languages = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese': 'zh',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'French': 'fr',
    'German': 'de',
    'Hebrew': 'he',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Latin': 'la',
    'Lithuanian': 'lt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk'
}

#
# Utility method to set up some nice logging
#
def set_logger(level, name_addition = ''):
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s:%(lineno)d: %(message)s")
    root_logger = logging.getLogger()

    # Remove any old handlers
    for hdlr in root_logger.handlers[:]:  # remove all old handlers
        root_logger.removeHandler(hdlr)

    file_name = sys.argv[0].split('/')[-1].split('.')[0]
    date_stamp = str(datetime.datetime.now()).lower().replace(' ', '_').replace(':', '_').replace('.', '_')
    file_handler = logging.handlers.RotatingFileHandler('{0}/{1}-{2}-{3}.log'.format(LOGGING_BASE, file_name, name_addition, date_stamp), maxBytes=10 * 1024 * 1024, backupCount=5, delay=1)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


set_logger(LOGGING_LEVEL)
