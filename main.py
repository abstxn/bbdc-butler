# Standard Modules
import json
import sys
import time
import asyncio

# 3rd-party Modules
import requests
import telegram

monthToInt = {
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
Opens the config file to read important details.
'''
secrets = dict()
with open('.config') as configFile:
    lines = configFile.readlines()
    for line in lines:
        if line[:1] == '#':
            continue
        pair = line.split('::')
        secrets[pair[0]] = pair[1].rstrip()
# Declare details as global variables
userId = secrets['userId']
userPass = secrets['userPass']
teleBotToken = secrets['teleBotToken']
teleId = secrets['teleId']


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
            'releasedSlotMonth': f'2023{monthToInt[month]}',
        }
        response = requests.post(
            'https://booking.bbdc.sg/bbdc-back-service/api/booking/theory/listTheoryLessonByDate',
            cookies=cookies,
            headers=headers,
            json=json_data
        )
        return json.loads(response.text)

class BookingSlot:
    date = None
    startTime = None
    endTime = None
    slotType = None

    def __init__(self, date, startTime, endTime, slotType) -> None:
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.slotType = slotType
    
    def __str__(self) -> str:
        return f"On {self.date}, start {self.startTime}, end {self.endTime}."


telegramBot = telegram.Bot(token=teleBotToken)
async def notifySlot(slot):
    await telegramBot.send_message(chat_id=teleId, text=f"Slot found: {slot}")

isLogin = 'n'
while isLogin != 'y':
    isLogin = input("Would you like to log in? (y/n) > ")
    if isLogin == 'n':
        print("Quitting BBDC Booky - Bye!")
        sys.exit()
    elif isLogin != 'y':
        print("Please enter 'y' for yes, or 'n' for no.")

tryAgain = 'y'
while tryAgain == 'y':
    session = Session()
    isSuccess = session.login()
    if not isSuccess:
        tryAgain = input("Error logging in. Try again? (y/n) > ")
        if tryAgain == 'n':
            print("Quitting BBDC Booky - Bye!")
            sys.exit()
        elif tryAgain == 'y':
            continue
        else:
            print("Did not enter y/n. Quitting program - Bye!")
            sys.exit()
    else:
        print(f"Successfully logged in as {session.userName}.")
        break

targetDate = '2023-02-24 00:00:00'

async def queryLoop():
    while True:
    # Type: FTE, FTP, etc.
        '''
        userInput = input("Enter type of theory lesson to find this month (FTE/FTP) > ")
        if userInput == 'exit':
            print("Quitting BBDC Booky - Bye!")
            sys.exit()
        '''
        slotsData = session.queryTheorySlots('FTP', 'feb')
        slotsFound = list()
        for date, slots in slotsData['data']['releasedSlotListGroupByDay'].items():
            for slot in slots:
                slotsFound.append(BookingSlot(slot['slotRefDate'], slot['startTime'], slot['endTime'], 'FTP'))
        slotsFound = sorted(slotsFound, key=lambda x: x.startTime)
        slotsFound = sorted(slotsFound, key=lambda x: x.date)
        print("--- Slots found: ---")
        for slot in slotsFound:
            if slot.date == targetDate:
                await notifySlot(slot)
            print(slot)
        time.sleep(60)

asyncio.run(queryLoop())