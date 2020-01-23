from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()




# *****************************************************************************************************
    # google calendars
    # def google_calendar_connection():
    #     """
    #     This method used for connect with google calendar api.
    #     """
        
    #     flags = tools.argparser.parse_args([])
    #     FLOW = OAuth2WebServerFlow(
    #         client_id='159469339586-udev46bnddnlifq04ah7i29gooa0h1l8.apps.googleusercontent.com',
    #         client_secret='vzAeRp_t1f_GK4-ys0HN89vX',
    #         scope='https://www.googleapis.com/auth/calendar',
    #         user_agent='quickstart'
    #         )
    #     storage = Storage('calendar.dat')
    #     credentials = storage.get()
    #     if credentials is None or credentials.invalid == True:
    #         credentials = tools.run_flow(FLOW, storage, flags)
        
    #     # Create an httplib2.Http object to handle our HTTP requests and authorize it
    #     # with our good Credentials.
    #     http = httplib2.Http()
    #     http = credentials.authorize(http)
    #     service = discovery.build('calendar', 'v3', http=http)
        
    #     return service


    # def form_valid(self, e_form):
    #     """
    #     This method used for add event in google calendar.
    #     """
        
    #     service = self.google_calendar_connection()
        
    #     event = {
    #         'summary': "",
    #         'location': "london",
    #         'description': "anything",
    #         'start': {
    #             'date': "2015-09-02",
    #         },
    #         'end': {
    #             'date': "2015-09-02",
    #         },
    #     }
        
    #     event = service.events().insert(calendarId='primary', body=event).execute()
        
    #     return CreateView.form_valid(self, e_form) 

    # ***************************************************************************************************