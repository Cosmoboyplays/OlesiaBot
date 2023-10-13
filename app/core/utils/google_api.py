from pprint import pprint

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1XhRK4NusW8uAqMTu6Bhp-JsIxpjPZfSCBWebmwxjw18'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

# values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
#                                              range="'Лист1'!A1:E300",         # формат "'Лист2'!A1:E10"
#                                              majorDimension='ROWS'
#                                              ).execute()

# pprint(values)
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheet_id=spreadsheet_id,
#     body={
#         'valueInputOption': 'USER_ENTERED',
#         'deta':[]
#     }
