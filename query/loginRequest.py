import requests

url = 'https://booking.bbdc.sg/bbdc-back-service/api/auth/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://booking.bbdc.sg',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://booking.bbdc.sg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}
json_payload = {
    'userId': None,
    'userPass': None
}

def send_using(username:str, password:str) -> requests.Response:
    json_payload['userId'] = username
    json_payload['userPass'] = password
    return requests.post(url, headers=headers, json=json_payload)