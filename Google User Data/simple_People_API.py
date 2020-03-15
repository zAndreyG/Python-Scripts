from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

# Se modificar as permissões, delete o arquivo token.pickle.
PERMISSIONS = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/user.emails.read',
    'https://www.googleapis.com/auth/user.birthday.read',
    'https://www.googleapis.com/auth/user.addresses.read',
    'https://www.googleapis.com/auth/user.phonenumbers.read'
    ]

ME = 'me'
ACCOUNT_ID = '113270844035142685878' #ID de minha conta google

USER_INFO = ['names', 'birthdays', 'genders', 'photos', 'phoneNumbers', 'emailAddresses', 'locales', 'addresses']

def main():
    creds = None
    # O arquivo token.pickle guarda os tokens de acesso do usuário, e é criado
    # automaticamente quando a autorização é feita pela primeira vez.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Se não há credenciais (válidas) disponíveis, leva o usário para fazer login e conceder permissões.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', PERMISSIONS)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para uma próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Chama a People API
    results = service.people().get(
        resourceName='people/' + ME,
        personFields='names,birthdays,genders,photos,locales,emailAddresses,addresses').execute()

    print('--------------- RESULTS ---------------')
    print(results)

    for index, val in enumerate(USER_INFO):
        if USER_INFO[index] in results:
            df_info = pd.DataFrame.from_dict(results[USER_INFO[index]])
            print('\n--------------- ' + USER_INFO[index].upper() + ' ---------------')
            print(df_info)
    # OU
    """ if 'names' in results:
        df_names = pd.DataFrame.from_dict(results['names'])
        print('\n--------------- NAMES ---------------')
        print(df_names)

    if 'birthdays' in results:
        df_birthdays = pd.DataFrame.from_dict(results['birthdays'])
        print('\n--------------- BIRTHDAYS ---------------')
        print(df_birthdays)

    if 'genders' in results:
        df_genders = pd.DataFrame.from_dict(results['genders'])
        print('\n--------------- GENDERS ---------------')
        print(df_genders)
    
    if 'phoneNumbers' in results:
        df_phoneNumbers = pd.DataFrame.from_dict(results['phoneNumbers'])
        print('\n--------------- PHONE NUMBERS ---------------')
        print(df_phoneNumbers)

    if 'emailAddresses' in results:
        df_emailAddresses = pd.DataFrame.from_dict(results['emailAddresses'])
        print('\n--------------- EMAIL ADDRESSES ---------------')
        print(df_emailAddresses)

    if 'locales' in results:
        df_locales = pd.DataFrame.from_dict(results['locales'])
        print('\n--------------- LOCALES ---------------')
        print(df_locales)

    if 'addresses' in results:
        df_addresses = pd.DataFrame.from_dict(results['addresses'])
        print('\n--------------- ADDRESSES ---------------')
        print(df_addresses) """

if __name__ == '__main__':
    main()