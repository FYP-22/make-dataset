import os
import requests
import json

API_KEY = "ba894ade069d32d7a0ee19d8bfa35ca361fbae84f620efc2b7b89e9e760d8b5d"

FILES = 'apks/'
dirc = os.listdir(FILES)
files = dirc[0]
payload = {"file": open(FILES + files, "rb")}
def upload_files():
    url = "https://www.virustotal.com/api/v3/files"
    response = requests.request("POST", url, data=payload, headers={
        "Accept": "application/json",
        "Content-Type": "multipart/form-data",
        "x-apikey": API_KEY,
    })
    print(response.text)
    return response


data = upload_files()
print(data)

