import pandas as pd
import buscacep
import requests

# Verifica a presença de uma 'key' dentro do dicionário
def validate_presence(key, data):
    if key in data['wind']:
        return True
    else: return False

# Busca informações climáticas da cidade inserida
def get_weather_info(city_name):

    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=9d66e215a6ea07817c0a3ee7e6cb5b13&q='

    language = '&lang=pt_br'
    units = '&units=metric' # Para retornar CELSIUS

    url = api_address + city_name + units + language

    # Tenta consultar informações do clima
    try:
        response = requests.get(url).json()

        # O JSON vindo da API é um pouco bagunçado e mal organizado
        # aqui é feita uma organização destas informações
        weather_info = {
            'nome_cidade':  response['name'],
            'pais':         response['sys']['country'],

            #'clima_id':     response['weather'][0]['id'],
            'predominio':   response['weather'][0]['main'],
            'descricao':    response['weather'][0]['description'],
            'temperatura':  response['main']['temp'],
            'sens_termica': response['main']['feels_like'],
            'minima':       response['main']['temp_min'],
            'maxima':       response['main']['temp_max'],
            'humidade':     response['main']['humidity'],
            'pressao_atm':  response['main']['pressure'],
            'vento_vel':    response['wind']['speed'],
            'vento_dir':    validate_presence('deg', response) == True and response['wind']['deg'] or None,  # IF Ternário
            #'icone':        response['weather'][0]['icon'],

            'sol_nascer':   response['sys']['sunrise'],
            'sol_por':      response['sys']['sunset'],
            'porc_nuvens':  response['clouds']['all'],

            'longitude':    response['coord']['lon'],
            'latitude':     response['coord']['lat'],

            'fuso_horario': response['timezone'],

            'base':         response['base'],

            'date_time':    response['dt'],
            
            'cidade_id':    response['id'],
            'code_request': response['cod']
        }

        dt_info = pd.Series(weather_info)
        return dt_info

    except Exception as e:
        print('Ocorreu um erro ao consultar clima: ', e)

    
    #print('\n---------------INFO CLIMÁTICAS---------------')
    #print(dt_info)

# Busca por informações da localidade utilizando o CEP
def get_cep_info(cep):
    response = buscacep.busca_cep_correios_as_dict(cep)
    return response
    #cep_info = pd.Series(response)
    #print(cep_info)

# Printa as Informações no Terminal
def show_info(info):
    print('\n----------INFORMAÇÕES CLIMÁTICAS----------')
    print(info)

if __name__ == "__main__":

    print('Para consultar o clima com CEP, insira apenas os números. \nOu insira o nome da cidade que deseja.')
    data = input('Cep ou cidade: ')

    # Verifica se a entrada é um INTEIRO
    try:
        int(data)

        # Tenta obter informações da localização através do CEP
        try:
            cep_info = get_cep_info(data)

            city_name = cep_info['localidade'][:-3]
            cep_info.pop('localidade')

            weather_info = get_weather_info(city_name)
            complete_info = {**cep_info, **weather_info}
            dt_info = pd.Series(complete_info)

            show_info(dt_info)
        except Exception as e:
            print('Ocorreu um erro: ', e)

    except:
        weather_info = get_weather_info(data)
        show_info(weather_info)