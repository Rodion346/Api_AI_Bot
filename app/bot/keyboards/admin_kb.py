import requests

url = "https://public-api.clothoff.io/position"

payload = { "id_gen": "2" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "f5406795d2baab5be031ca82f3ebe1f50da871c3"
}

response = requests.post(url, json=payload, headers=headers)

print(response)