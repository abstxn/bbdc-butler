import requests

url = 'https://booking.bbdc.sg/bbdc-back-service/api/account/getUserProfile'
cookies = {
    'bbdc-token': None,
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': None,
    'JSESSIONID': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJBQ0NfSUQiOiI5NDg5NDYiLCJUUkFfTE9HSU4iOiI5NjdHMDkwODIwMDAiLCJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTMwNTMyNTI4OTI2fQ._c0kdtnWp5qKXFu_Hg6x8zo1sDkRB5hbh7bUhzQdiZw',
    'Origin': 'https://booking.bbdc.sg',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://booking.bbdc.sg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}
json_data = {}

def send_using(token:str) -> requests.Response:
    cookies['bbdc-token'] = token
    headers['Authorization'] = token
    return requests.post(url, cookies=cookies, headers=headers, json=json_data)
