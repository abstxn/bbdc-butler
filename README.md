# bbdc-butler

## About

A simple Python script to periodically search for practical training slots at BBDC.

## Notes

- Only works for 3C (manual car), but code can be tweaked for other query types
- Pings the website every 15 seconds to avoid flooding requests

## Logins/Tokens/API Keys

`bbdc-butler` uses the `python-dotenv` module to load secrets that are needed
for logins and authentication. The directory structure should be as such:

```
./
    app.py
    session.py
    tele.py
    message.py
    query/
        checkExists.py
        getUserProfile.py
        loginRequest.py
    env/
        login.env
        session.env
        tele.env
```

- `login.env`: contains your BBDC username and password
- `session.env`: contains the last working session token (cache)
    - This exists to avoid unnecessary re-negotiation via login when restarting the script.
- `tele.env`: contains your Telegram bot's API key and your Telegram user ID (see @userinfobot on Telegram)

# To-do's

- [ ] Use `python-dotenv` to handle secrets
- [ ] Use `os/path` to allow execution from any directory