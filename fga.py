
import requests
import json

# auth/login endpoint için gerekli bilgiler
login_url = 'https://api.defterbeyan.gov.tr/auth/login'
api_key = 'mRUhlKbkYFWhc3EylDtV'
api_secret = 'M9w2mcjm09djXF2i7Vle0EpbhWv0Uh'
login_type = 'ENTEGRATOR'

# auth/login endpoint için isteği oluşturma
login_data = {
    'apiKey': api_key,
    'apiSecret': api_secret,
    'loginType': login_type
}

# JSON formatına dönüştürme
login_json_data = json.dumps(login_data)

# auth/login endpoint'e POST isteği gönderme
response = requests.post(login_url, data=login_json_data)
print(response.text)
# Cevap kontrolü ve token alma
if response.status_code == 200:
    token = response.json().get('token')
    print(f"Başarıyla oturum açıldı. Token: {token}")

    # auth/authorizewith endpoint için gerekli bilgiler
    authorizewith_url = 'https://api.defterbeyan.gov.tr/auth/authorizewith'
    smm_api_key = 'mRUhlKbkYFWhc3EylDtV'
    smm_api_secret = 'M9w2mcjm09djXF2i7Vle0EpbhWv0Uh'
    smm_login_type = 'API'

    # auth/authorizewith endpoint için isteği oluşturma
    authorizewith_data = {
        'apiKey': smm_api_key,
        'apiSecret': smm_api_secret,
        'loginType': smm_login_type
    }

    # JSON formatına dönüştürme
    authorizewith_json_data = json.dumps(authorizewith_data)

    # auth/authorizewith endpoint'e POST isteği gönderme
    auth_response = requests.post(authorizewith_url, data=authorizewith_json_data, headers={'Token': token})

    # Cevap kontrolü ve yeni token alma
    if auth_response.status_code == 200:
        new_token = auth_response.json().get('token')
        print(f"Yeni token başarıyla alındı. Yeni Token: {new_token}")
    else:
        print("Token alınamadı.")
else:
    print("Oturum açılamadı.")
