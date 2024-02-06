from AlinaXIQ.core.bot import Alina
from AlinaXIQ.core.dir import dirr
from AlinaXIQ.core.git import git
from AlinaXIQ.core.userbot import Userbot
from AlinaXIQ.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Alina()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
