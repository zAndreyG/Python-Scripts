import requests
from bs4 import BeautifulSoup
import smtplib
import time

# URL do Produto
URL = 'https://www.amazon.com.br/Call-Duty-Modern-Warfare-PlayStation/dp/B07YNG9DKB/ref=sr_1_4?keywords=jogo+Call+Of+Duty%3A+Modern+Warfare&qid=1572103624&sr=8-4'

# User Agent (Para descobrir qual o seu,  basta pesquisar "user agent" no google)
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

# Função que traz o preço do produto e o compara com o valor "alvo"
def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Título do Produto
    title = soup.find(id="productTitle").get_text().strip()
    # Preço do Produto
    price = soup.find(id="priceblock_ourprice").get_text()

    # Ajusta o valor (em Real Brasileiro) do produto para Float no padrão Python
    converted_price = float(price[2:8].replace(",", "."))

    # Verifica se o preço atual do produto é <= ao preço alvo
    # Se a condição for satisfeita, envia um email ao usuário
    if converted_price <= 180.0:
        send_email(title)

    """ # Teste
    if converted_price < 250.0:
        send_email(title)
    
    print(converted_price) """

# Função que envia o email para o usuário
def send_email(title):
    # Gerencia a conexão com o servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Faz login na conta de email que envia o Email
    server.login('examplegmail.com', 'password')

    # Assunto do Email
    subject = f'O preco de {title[0:27]} caiu!'

    # Corpo do Email
    body = 'De uma olhada na pagina da amazon: ' + URL

    # Conteúdo total do Email
    msg = f"Subject: {subject}\n\n{body}"

    # Envia o Email
    server.sendmail(
        'examplegmail.com',  #Conta de email que envia
        'example2gmail.com', #Conta de email que recebe
        msg                  #Conteúdo do email
    )
    print("Email enviado!")

    # Finaliza conexão com o servidor
    server.quit()

# Add tempo de espera até a próxima execução
while True:
    check_price()
    time.sleep(86400) #(60 * 60) * 24 = 1 dia
