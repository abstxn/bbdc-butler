import requests
import json

url ='https://booking.bbdc.sg/bbdc-back-service/api/booking/c3practical/checkExistsC3PracticalTrainingSlot'
cookies = {'bbdc-token': None}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': None,
    'JSESSIONID': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJBQ0NfSUQiOiI5NDg5NDYiLCJUUkFfTE9HSU4iOiI5NjdHMDkwODIwMDAiLCJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTMwNTMyNDU0ODkzfQ.2TRNux6TwJU8XZU5IjcpbhuaHIj0y7cR8WKtxorzUeA',
    'Origin': 'https://booking.bbdc.sg',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://booking.bbdc.sg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}
json_payload = {"insInstructorId":""}

def send_using(token: str) -> str:
    cookies['bbdc-token'] = token
    headers['Authorization'] = token
    response = requests.post(url, cookies=cookies, headers=headers, json=json_payload)
    return json.loads(response.text)['message']