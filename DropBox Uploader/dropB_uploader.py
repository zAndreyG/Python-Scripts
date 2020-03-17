# Pré requisitos:
# 1.Instale o sdk do DropBox para poder utilizar sua API
# MAC e Linux: $ sudo pip install dropbox
#
# Windows: pip install dropbox
#
# Por padrão o sdk do DropBox é baseado no Python 3.5
# Então é recomendado utilizar esta versão, porém também é funcional na versão 3.7
#
# 2. Crie um aplicativo no DropBox App Console (https://www.dropbox.com/developers/apps), o qual será validado
# e utilizado para fazer o upload do arquivo utilizando a API do dropbox. É necessário um token de acesso para se
# conectar ao dropbox antes de realizar operações em pastas ou arquivos.

import sys
import dropbox
import datetime as dt
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

def get_today():
    today = dt.date.today().strftime('%Y_%m_%d')
    return today

today = get_today()

# Access token da conta
TOKEN = 'TOKEN_API'

# Diretório do arquivo local
LOCALFILE = 'D:/Users/CSV_Files/' + today + '_users.csv'

# Mantenha a '/' antes do diretório do arquivo no DropBox
BACKUPPATH = '/Users/' + today + '_users.csv'


# Faz o upload do arquivo indicado na variável LOCALFILE para o Dropbox
def backup():
    with open(LOCALFILE, 'rb') as f:
        # Usa-se o WriteMode=overwrite para assegurar que as configurações do arquivo
        # estão cofiguradas para upload
        print("Fazendo upload de " + LOCALFILE + " para o Dropbox como " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # Checa se o usuário tem espaço livre o sufciente no DropBox para fazer upload do arquivo
            if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERRO: Não é possível fazer Upload. Espaço insuficiente.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# Função para checar detalhes dos arquivos no diretório do Upload
def checkComponents():
    print("Checando componentes:")
    for entry in dbx.files_list_folder('').entries:
        print('-->', entry.name)

if __name__ == '__main__':
    # Checa se há um Token de acesso para ser utilizado
    if (len(TOKEN) == 0):
        sys.exit("ERRO: Parece não haver nenhum Token de Acesso.")

    # Instancia uma classe DropBox, para fazer requisições para a API
    print("Criando um Objeto DropBox...")
    dbx = dropbox.Dropbox(TOKEN)

    # Checa se o token de acesso é válido
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "ERRO: Token de acesso inválido, tente gerar um novo token de acesso a partir do App Console na página web do DropBox.")

    try:
        checkComponents()
    except ApiError as err:
        sys.exit("Erro enquanto checando componentes.")

    print("\n----- Upload -----")
    # Faz upload do arquivo como um backup do mesmo no DropBox
    backup()

    print("Upload realizado com Sucesso!")