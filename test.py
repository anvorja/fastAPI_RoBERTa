import requests

url = "http://localhost:8015/get_bio"
texto = "Paciente que recibe tratamiento con Cisplatino + Pemetrexed y radioterapia en julio de 2014."
response = requests.post(url, json={"text": texto})
resultado = response.json()
print(resultado)

# El resultado tendrá este formato:
# {
#     "bio_format": [
#         {"token": "Paciente", "tag": "O"},
#         {"token": "que", "tag": "O"},
#         {"token": "recibe", "tag": "O"},
#         {"token": "tratamiento", "tag": "O"},
#         {"token": "con", "tag": "O"},
#         {"token": "Cisplatino", "tag": "B-DRUG"},
#         ...
#     ],
#     "original_text": "Paciente que recibe..."
# }
