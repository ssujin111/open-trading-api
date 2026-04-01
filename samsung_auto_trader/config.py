import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.account = os.getenv('GH_ACCOUNT')
        self.appkey = os.getenv('GH_APPKEY')
        self.appsecret = os.getenv('GH_APPSECRET')
        self.base_url = 'https://openapivts.koreainvestment.com:29443'  # Mock trading URL
        self.token_cache_file = 'token_cache.json'

    def validate(self):
        if not all([self.account, self.appkey, self.appsecret]):
            raise ValueError("Missing required environment variables: GH_ACCOUNT, GH_APPKEY, GH_APPSECRET")

    @property
    def cano(self) -> str:
        return self.account[:8]

    @property
    def acnt_prdt_cd(self) -> str:
        return self.account[8:]