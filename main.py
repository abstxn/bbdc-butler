# Standard Modules
import json
import sys
import time
import asyncio

# 3rd-party Modules
import requests     # send and receive HTTPS
import telegram     # for Telegram notifications upon slots found

month_to_int = {
    'jan': '01',
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12' 
}

'''
###############################################################################
# Get user login credentials and prepare Telegram bot                         #
###############################################################################
'''

class BBDC_Login_Credentials:

    username = 'NOT_INITIALIZED'
    password = 'NOT_INITIALIZED'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Telegram_Details:

    bot_token = 'NOT_INITIALIZED'
    telegram_UID = 'NOT_INITIALIZED' # see @userinfobot in Telegram

    def __init__(self, bot_token: str, telegram_UID: str):
        self.bot_token = bot_token
        self.telegram_UID = telegram_UID 
    
    @classmethod
    def read_cache(cls):
        try:
            cached_file = open('.telegram', 'r')
            text_lines = cached_file.readlines()
            bot_token = text_lines[0].rstrip()
            telegram_UID = text_lines[1].rstrip()
            return cls(bot_token, telegram_UID)
        except FileNotFoundError:
            print('File containing Telegram details (bot token, user ID) not found. Aborting.')
            exit(1)

class Telegram_Connection:

    telegram_UID: str = None
    bot_instance: telegram.Bot = None

    def __init__(self, telegram_details: Telegram_Details):
        self.telegram_UID = telegram_details.telegram_UID
        self.bot_instance = telegram.Bot(telegram_details.bot_token)
    
    async def send(self, message: str):
        await self.bot_instance.send_message(self.telegram_UID, message)
    
    async def notify_available_slot(self, slot):
        notification = f'Available slot:\n\n{slot}'
        await self.bot_instance.send_message(self.telegram_UID, notification)

# Prepare login credentials
print("Username is the last 4 Characters of your NRIC/FIN and Birthdate (DDMMYYYY).\nExample: \"567A02071990\".")
username = input("Enter username: ")
password = input("Enter password: ")
login_credentials = BBDC_Login_Credentials(username, password)

# Telegram setup
telegram_details = Telegram_Details.read_cache()
telegram_connection = Telegram_Connection(telegram_details)
asyncio.run(telegram_connection.send("Bot online."))

'''
###############################################################################
# Establish a connection with BBDC's website                                  #
###############################################################################
'''

class Login_Request:

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
    json_payload = {}

    def __init__(self, login_credentials: BBDC_Login_Credentials):
        self.json_payload['userId'] = login_credentials.username
        self.json_payload['userPass'] = login_credentials.password
    
    def send(self) -> requests.Response:
        return requests.post(url=self.url, headers=self.headers, json=self.json_payload)

    @staticmethod
    def is_login_success(login_response: requests.Response) -> bool:
        response_json = json.loads(login_response.text)
        return response_json['success']

    @staticmethod
    def extract_session_token(login_response: requests.Response) -> str:
        response_json = json.loads(login_response.text)
        return response_json['data']['tokenContent']

login_request = Login_Request(login_credentials)
login_response = login_request.send()
session_token = None
if Login_Request.is_login_success(login_response):
    print('Login successful.')
    session_token = Login_Request.extract_session_token(login_response)
else:
    response_message = json.loads(login_response.text)['message']
    print('Login unsuccessful.')
    print(f'Error message: \"{response_message}\"')
    exit(1)

'''
###############################################################################
# Making requests with the established session token                          #
###############################################################################
'''

class Practical_Exist_Request:

    NO_SLOT_RELEASED = 'There is no slot released for booking at the moment.'
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

    def __init__(self, session_token):
        print(f'Using session token: {session_token}')
        self.cookies['bbdc-token'] = session_token
        self.headers['Authorization'] = session_token
    
    def send(self) -> requests.Response:
        return requests.post(url=self.url, cookies=self.cookies, headers=self.headers, json=self.json_payload)
    
    @staticmethod
    def is_practical_exist(practical_exist_response: requests.Response):
        response_json = json.loads(practical_exist_response.text)
        response_message = response_json['message']
        if response_message == Practical_Exist_Request.NO_SLOT_RELEASED:
            return False
        else:
            return True

practical_exist_request = Practical_Exist_Request(session_token)
while True:
    practical_exist_response = practical_exist_request.send()
    response_message = json.loads(practical_exist_response.text)['message']
    print(f'{time.strftime("%H:%M:%S", time.localtime())}: {response_message}')
    if response_message != Practical_Exist_Request.NO_SLOT_RELEASED:
        asyncio.run(telegram_connection.send("Available slots detected! GO GO GO!"))
    # if Practical_Exist_Request.is_practical_exist(practical_exist_response):
    #     print('There are slots available for booking!')
    #     break
    time.sleep(5)

'''
Encapsulates a login session.
On initialization, logs in to the server, and saves the response.
Important Variables:
    loginResponse: The HTTP response given by the server upon login.
    sessionToken: Key to be used in subsequent requests in this session.
    userName: Name of the user that the script is logged in as.
'''
class Session:
    
    # Returns True if successful
    def login(self) -> bool:
        # Set up login HTTP request
        loginUrl = 'https://booking.bbdc.sg/bbdc-back-service/api/auth/login'
        loginHeaders = {
            'Connection': 'keep-alive'
        }
        loginJson = {
            'userId': userId,
            'userPass': userPass
        }
        # Send login request and read the response
        self.loginResponse = requests.post(loginUrl, headers=loginHeaders, json=loginJson)
        # Convert the text of the Response object (JSON) into a dict
        self.loginResponseData = json.loads(self.loginResponse.text)
        if not self.loginResponseData['success']:
            print(self.loginResponseData['message'])
            return False
        else:
            # Read the session token and user's name from the response data
            self.sessionToken = self.loginResponseData['data']['tokenContent']
            self.userName = self.loginResponseData['data']['username']
            return True
    
    def queryTheorySlots(self, type, month) -> dict:
        cookies = {
            'bbdc-token': self.sessionToken
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': self.sessionToken,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'bbdc-token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTY3NjkzNjQ1NH0.k6Dhyk8WO7rXOyne-ScY0-_KyEt_1rcctI62zWsec4w',
            'DNT': '1',
            'JSESSIONID': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJBQ0NfSUQiOiI5NDg5NDYiLCJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTMwNTI1ODY4ODc0fQ.7hUw388BZ8761PYpYXdSNlhvkwEbSFEAUrxCwCx1WKU',
            'Origin': 'https://booking.bbdc.sg',
            'Referer': 'https://booking.bbdc.sg/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="24", "Chromium";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-gpc': '1'
        }
        json_data = {
            'courseType': '3C',
            'theoryType': type,
            'stageSubNo': '0',
            'language': 'English',
            'releasedSlotMonth': f'2023{month_to_int[month]}',
        }
        response = requests.post(
            'https://booking.bbdc.sg/bbdc-back-service/api/booking/theory/listTheoryLessonByDate',
            cookies=cookies,
            headers=headers,
            json=json_data
        )
        return json.loads(response.text)

    def queryFTTSlots(self, month) -> dict:
        import requests
        cookies = {
            'bbdc-token': self.sessionToken,
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': self.sessionToken,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'bbdc-token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTY3NzU1NDYyNX0.oSW6uDF_BJnxBmdkOIi0txOPc_bqgcrz0Q-LFsZRsm4',
            'DNT': '1',
            'JSESSIONID': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJBQ0NfSUQiOiI5NDg5NDYiLCJpc3MiOiJCQkRDIiwiTlJJQyI6IlQwMDI2OTY3RyIsImV4cCI6MTMwNTI2NDg3MDU0fQ.Isd0IOy6E7lTuHGM0_wUevdVbKi3Rhd1ZzkoWPEotZQ',
            'Origin': 'https://booking.bbdc.sg',
            'Referer': 'https://booking.bbdc.sg/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="24", "Chromium";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-gpc': '1',
        }

        json_data = {
            'courseType': '3C',
            'testType': 'FTT',
            'language': 'English',
            'viewOnly': False,
        }

        response = requests.post(
            'https://booking.bbdc.sg/bbdc-back-service/api/booking/test/listTheoryTestSlotWithMaxCap',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        return json.loads(response.text)

class BookingSlot:
    type = None
    date = None
    startTime = None
    endTime = None
    slotType = None

    def __init__(self, type, date, startTime, endTime, slotType) -> None:
        self.type = type
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.slotType = slotType
    
    def __str__(self) -> str:
        return f"{self.type}: {self.date}, start {self.startTime}, end {self.endTime}."


'''
targetDates = ['2023-03-23 00:00:00']
targetTypes = ['FTP']


# Execute search based on user inputs
async def queryLoop():
    while True:
        for type in targetTypes:
            slotsData = session.queryTheorySlots(type, 'mar')
            slotsFound = list()
            if slotsData['data']['releasedSlotListGroupByDay'] == None:
                continue
            for date, slots in slotsData['data']['releasedSlotListGroupByDay'].items():
                for slot in slots:
                    slotsFound.append(BookingSlot(type, slot['slotRefDate'], slot['startTime'], slot['endTime'], 'FTP'))
            slotsFound = sorted(slotsFound, key=lambda x: x.startTime)
            slotsFound = sorted(slotsFound, key=lambda x: x.date)
            print("--- Slots found: ---")
            for slot in slotsFound:
                if slot.date in targetDates:
                    print("SLOT FOUND!!!!!!!!!!!!")
                    await notifySlot(slot)
                print(slot)
        time.sleep(15)

asyncio.run(queryLoop())
'''