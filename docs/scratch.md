# 2023-05-07

- directly enter login credentials instead of storing it in a file
- storing Telegram details (bot token, user ID) in untracked file

All a "connection" to the server is (in this case), is a single session token. Having this session token comes first. With the token, we can then make other HTTP requests, and read responses.

- trouble using gpg to verify python-telegram-bot module, might have to move to another module like python-pyrogram
    - fixed with pinned comment: "https://aur.archlinux.org/packages/python-telegram-bot"

- did abstracting over several details
- since I could not extract a legitmate practical slot API call from the website (no slots available), the temporary solution is to loop the bot until slots are found
    - when slots found, quickly fetch a legitmate request to work on proper request