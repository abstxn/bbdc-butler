# Standard Modules
import json
import sys

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
        else:
            # Read the session token and user's name from the response data
            self.sessionToken = self.loginResponseData['data']['tokenContent']
            # self.userName = self.loginResponseData['data']['?']
            print(f"Successfully logged in as {self.userName}.")
    
    def queryTheorySlots(self, type, month):
        cookies = {
            'bbdc-token': self.sessionToken
        }
        headers = {
            'Authorization': self.sessionToken,
            'Connection': 'keep-alive',
        }
        json = {
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
            json=json
        )
        print(json.dumps(json.loads(response.text)))

# telegramBot = telegram.Bot(token=teleBotToken)

isLogin = 'n'
while isLogin != 'y':
    isLogin = input("Would you like to log in? (y/n) > ")
    if isLogin == 'n':
        print("Quitting BBDC Booky - Bye!")
        sys.exit()
    print("Please enter 'y' for yes, or 'n' for no.")

tryAgain = 'y'
while tryAgain == 'y':
    session = Session()
    if not session.login():
        tryAgain = input("Error logging in. Try again? (y/n) > ")
        while not (tryAgain == 'y' or tryAgain == 'n'):
            tryAgain = input("Please enter 'y' for yes, or 'n' for no. > ")
        if tryAgain == 'n':
            print("Quitting BBDC Booky - Bye!")
            sys.exit()

userInput = ''
while userInput != 'exit':
# Type: FTE, FTP, etc.
    userInput = input("Enter type of theory lesson to find this month (FTE/FTP) > ")
    session.queryTheorySlots(userInput, 'feb')