import requests
import json
from bs4 import BeautifulSoup 
req = requests.get('http://localhost:8080/data')
soup = BeautifulSoup(req.content, 'html.parser')

data = json.loads(soup.text)

for i in range(len(data)):
    print(data[i]['stacja'])
    
