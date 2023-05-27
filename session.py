import json
from dotenv import dotenv_values, set_key
from query import getUserProfile, loginRequest

login = dotenv_values('env/login.env')
USERNAME = login['USERNAME']
PASSWORD = login['PASSWORD']
TOKEN = dotenv_values('env/session.env')['TOKEN']

def save_token(token: str):
    print(f'Saving new token: {token}')
    set_key('env/session.env', 'TOKEN', token)

def is_valid(token: str) -> bool:
    print(f'Checking if token is valid: {token}')
    response = getUserProfile.send_using(token)
    if json.loads(response.text)['success']:
        print(f'The token {token} is valid')
        return True
    else:
        print(f'The token {token} is NOT valid')
        return False

def login() -> str:
    print('Attempting to login...')
    response = loginRequest.send_using(USERNAME, PASSWORD)
    print(response.text)
    token = json.loads(response.text)['data']['tokenContent']
    print(f'Logged in. Session token: {token}')
    return token

def get_token() -> str:
    curr_token = TOKEN
    while not is_valid(curr_token):
        curr_token = login()
    save_token(curr_token)
    return curr_token