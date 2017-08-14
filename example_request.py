import requests


url = 'http://127.0.0.1:5000/segment'
payload = {'text': ''}
with open('./data/example.txt') as f:
    payload['text'] = f.read()

r = requests.post(url, data=payload)
print(r.text)
