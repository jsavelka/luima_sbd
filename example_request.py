import chardet
import requests


url = 'http://127.0.0.1:5000/dev2'
# url = 'http://127.0.0.1:5000/offsets'
#payload = {'text': ''}
#file_name = './data/example.txt'

#raw = open(file_name, 'rb').read()
#enc = chardet.detect(raw)['encoding']

#with open(file_name, mode='r', encoding=enc) as f:
#    payload['text'] = f.read()

#r = requests.post(url, data=payload)
r = requests.post(url, data={'msg': 'hello'})