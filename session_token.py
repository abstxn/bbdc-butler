'''
Provides methods to obtain valid session tokens.
'''

import requests
import json

cache_token_dir = './secrets/cached-token'
cache_login_dir = './secrets/login-info'

def cache_read() -> str:
    file = open(cache_token_dir, 'r')
    return file.readline().rstrip()

def cache_write(token: str):
    file = open(cache_token_dir, 'w')
    file.write(token)

def is_valid(token: str) -> bool:
    cookies = {
        'bbdc-token': token,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': token,
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
    response = requests.post(
        'https://booking.bbdc.sg/bbdc-back-service/api/account/getUserProfile',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return json.loads(response.text)['success']

def login() -> str:
    file = open(cache_login_dir, 'r')
    lines = file.readlines()
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
        'userId': lines[0].rstrip(),
        'userPass': lines[1].rstrip()
    }
    response = requests.post(url, headers=headers, json=json_payload)
    token = json.loads(response.text)['data']['tokenContent']
    return token

def get() -> str:
    curr_token = cache_read()
    while not is_valid(curr_token):
        curr_token = login()
    return curr_token