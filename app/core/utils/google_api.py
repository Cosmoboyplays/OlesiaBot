import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from app.core.utils.newletters import NewsletterManager

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1XhRK4NusW8uAqMTu6Bhp-JsIxpjPZfSCBWebmwxjw18'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)


class GoogleTable():
    def __init__(self) -> None:
        pass

    def append_user(self, s: list, sheet_name=None):
        if sheet_name is None:
            newsletter_manager = NewsletterManager()
            sheet_name = newsletter_manager.get_list_name()

        service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                               range=f"{sheet_name}!A2",
                                               valueInputOption="USER_ENTERED",
                                               body={"values": s}
                                               ).execute()

    def check_sheet(self, sheet_name):
        '''Checking a sheet in the table'''
        try:
            response = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=sheet_name).execute()
            return True
        except Exception as e:
            return False

    def get_data(self, sheet_range):
        return service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_range,  # формат "'Лист2'!A1:E10"
                                                   majorDimension='ROWS'
                                                   ).execute()

    def batchUpdate(self, sheet_range, values):
        return service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                           body={"valueInputOption": "USER_ENTERED",
                                                                 "data": [
                                                                     {"range": sheet_range,
                                                                      "majorDimension": "ROWS",
                                                                      # сначала заполнять ряды, затем столбцы (т.е.
                                                                      # самые внутренние списки в values - это ряды)
                                                                      "values": values}
                                                                 ]
                                                                 }).execute()

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
