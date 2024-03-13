import requests
url = "http://api.defterbeyan.gov.tr/rs/api/sistemvarliklari/getcurrent"
""  
response = requests.get(url)

"""if response.status_code == 200:
    data = response.json()  # API yanıtını JSON formatına dönüştürün
    print(data)
else:
    print("İstek başarısız. HTTP Hata Kodu:", response.status_code)"""
x = {
  "status": 0,
  "statusMessage": "string",
  "requestIdentifier": "string",
  "errorCode": "string",
  "errorMessage": "string",
  "warningMessage": "string",
  "resultContainer": {
    "id": "string",
    "deleted": False,
    "baslangicTarihi": "2024-03-13 17:23:07",
    "bitisTarihi": "2024-03-13 17:23:07",
    "v": 0
  }
}
response = requests.post(url, json=x)  # Veriyi JSON formatında gönderin
print(response.status_code)  # HTTP yanıt kodu
print(response.text) 
if response.status_code == 201:  # İstek başarılıysa
    print("Veri başarıyla gönderildi.")
else:
    print("İstek başarısız. HTTP Hata Kodu:", response.status_code)