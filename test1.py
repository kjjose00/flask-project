import requests

web='http://127.0.0.1:5000/'
response=requests.get(web+"hello/jesus")
print(response.json())