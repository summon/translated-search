# Translated Search
This is the 2023 CDI Hackathon Project combining the Summon API with Google Translate.  It is open sourced to provide an API Integration example.

## Installation
This assumes you are using system python 3 to seed a virtual environment.  Adjust accordingly for different scenarios.
* cd into your desired install location
* git clone https://github.com/summon/translated-search.git
* cd translated-search
* python3 -m venv venv 
* source venv/bin/activate
* python3 -m pip install -r requirements.txt
* edit settings.py and set proper values for:
  * SUMMON_ACCESS_ID
  * SUMMON_API_KEY
  * GOOGLE_CRED_JSON_FILE

## Running
* cd into your translated-search installation
* ./venv/bin/flask --app translatedsearch run
* your local application should now be running at http://127.0.0.1:5000

## Variable details
#### SUMMON_ACCESS_ID
This is the short name associated with your institution.  Examples: uc, duke.

#### SUMMON_API_KEY
This is the secret key given to your institution upon implementation.  If you need this, contact support.

#### GOOGLE_CRED_JSON_FILE
This is a reference to the Google API credentials file created through Google's system.

#### Creating a Google API credenials file
NOTE: using the Google API is not free.  The instructions below are from when we did our hackathon.  Google's systems change frequently, so these could be out of date.
1. Go to https://cloud.google.com/translate/docs/setup
2. Click on "Go to project selector"
3. Create a project "Translated Search"
4. Go to the project "Translated Search"
5. Click "Go to the API overview"
6. Click "ENABLE APIS and SERVICES" and search " translation"
7. Select "Cloud Translation API" and click "ENABLE"
8. Click "CREATE CREDENTIALS", select "Application Data", "No I'm not using (GCE, etc.)", "Next"
9. Type in Service Account Name, etc., "Create and Continue". Click "Done"
10. Go to the APIs page (https://console.cloud.google.com/apis/credentials) select project "Translated Search"
11. Click on Credentials 
12. Click on the email address under "Service Accounts"
13. Go to "Keys", click "Add Key"→"Create New Key", select "JSON" → This will download an API credentials json file 
14. Move the json file somewhere reasonable