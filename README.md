# celosia_bot 🌺
A small Telegram bot written for Python 3.  Currently support a very small set of commands.

## Python Module Requirements:
* telepot
* urllib.request
* urllib.parse
* json
* psutil
* requests
* re

All modules can be installed via pip3.

## Currently Supported Commands:
* **!echo**: echos whatever follows back to the user or group chat
* **!newpoll**: creates a strawpoll and returns the link (usage available with !help)
* **!serverstats**: uses psutil to return information on processor and memory usage
* **!time**: returns the time (currently only EST)
* **!whereyouat**: the bot uses its current public IP to determine location
* **!yt**: uses any further inputs as a query for a YouTube search then returns a list of the top 3 results
* **!ytlucky**: basically the same as !yt but only returns the top result
