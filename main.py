import requests
import os
import csv

from bs4 import BeautifulSoup

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

requests.post(ID_UFF, data=payload, headers=HEADER)

history = requests.get(HISTORY, headers=HEADER).text

soup = BeautifulSoup(history, 'html.parser')

html_selection = soup.select("#historico\:tblDisciplinasHistorico")[0]

columns = html_selection.select('span')
lines = html_selection.find_all('tr')

weights = []
weighted_scores = []
with open('grades.csv', mode='w', newline='') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow([column.text for column in columns])
    for line in lines:
        line_elements = []
        for element in line.find_all('td'):
            line_elements.append(element.text.strip())
        if len(line_elements) != 0:
            score = float(line_elements[4])
            weight = int(line_elements[7])
            if score < 6:
                vs = float(line_elements[5])
                score = (score + vs)/2
                
            weights.append(weight)
            weighted_scores.append(score * weight)
            
            file_writer.writerow(line_elements)
            
    cr = sum(weighted_scores)/sum(weights)
    file_writer.writerow([])
    file_writer.writerow(["CR", cr])
