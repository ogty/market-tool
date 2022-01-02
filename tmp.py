import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# NOTE: NOT working!!
with open("./images/totalling_sample.png", "rb") as f:
    auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_KEY_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)

    api.update_status_with_media("2021/12/30", "2021_12_30", file=f)