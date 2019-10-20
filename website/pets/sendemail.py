from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from urllib.error import HTTPError
from email.mime.text import MIMEText
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')
  return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message

    except errors.HttpError as error:
        print (f'An error occurred: {error}')
        return None

def service_account_login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    dirname = os.path.dirname(__file__)
    credentials_path = os.path.join(dirname, 'credentials.json')
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service


def sendNotification(nome, user_email, horario, servico):

    EMAIL_FROM = 'petshopdoggis@gmail.com'
    EMAIL_TO = user_email
    EMAIL_SUBJECT = '[ Doggis ] Lembrete de Serviço'
    EMAIL_CONTENT = 'Prezado(a) {0},\n\nGostaríamos de lembrar que às {1} está reservado para o seu pet estar conosco, para {2}.\n\nEsperamos por você e seu pet,\nEquipe Doggis'.format(nome,horario, servico)

    service = service_account_login()
    message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
    sent = send_message(service, 'me', message)
