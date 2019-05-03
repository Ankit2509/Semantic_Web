import json
import requests
data={}
dictn={}
js=[]
data["arr"]=[1,2,3,4,5]


data["barr"]=["aa","bb","cc"]
js.append(data)
dictn["res"]=js
# r = requests.post('http://0db34979.ngrok.io/backend.py', json=json.dumps(js))
print(json.dumps(dictn))