import requests
import os

ID_UFF = 'https://app.uff.br/iduff/login.uff'
HISTORY = 'https://app.uff.br/iduff/privado/declaracoes/private/historico.uff?conversationPropagation=none'

cookie = requests.get(ID_UFF).headers['Set-Cookie']
ID_UFF_LOGIN = os.environ.get('ID_UFF_LOGIN')
ID_UFF_PASSWORD = os.environ.get('ID_UFF_PASSWORD')
HEADER = {
    'Cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.145 Safari/537.36 Vivaldi/2.6.1566.49 '
}

payload = {
    'login': 'login',
    'login:id': ID_UFF_LOGIN,
    'login:senha': ID_UFF_PASSWORD,
    'login:btnLogar': 'Logar',
    'javax.faces.ViewState': 'j_id1'
}

sms_code = requests.post(ID_UFF,
                         data=payload,
                         headers=HEADER)

print(requests.get(HISTORY,
                   headers=HEADER).text)
