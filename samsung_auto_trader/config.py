import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env files from the package and repository root if present.
load_dotenv(Path(__file__).parent / '.env')
load_dotenv(Path(__file__).parent.parent / '.env')

class Config:
    BASE_URL = 'https://openapivts.koreainvestment.com:29443'  # Mock trading URL

    def __init__(self):
        raw_account = os.getenv('GH_ACCOUNT', '')
        self.account = self._clean_env_value(raw_account)
        self.appkey = self._clean_env_value(os.getenv('GH_APPKEY', ''))
        self.appsecret = self._clean_env_value(os.getenv('GH_APPSECRET', ''))
        self.base_url = self.BASE_URL
        self.token_cache_file = Path(__file__).parent / 'token_cache.json'

        print(
            f"GH_ACCOUNT raw={repr(raw_account)} "
            f"raw_len={len(raw_account)} "
            f"cleaned={repr(self.account)} "
            f"cleaned_len={len(self.account)}"
        )

    @staticmethod
    def _clean_env_value(value: str) -> str:
        return value.strip().strip('"\'"').replace(' ', '').replace('\n', '').replace('\r', '')

    def validate(self):
        missing = [name for name, value in [
            ('GH_ACCOUNT', self.account),
            ('GH_APPKEY', self.appkey),
            ('GH_APPSECRET', self.appsecret)
        ] if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        if len(self.account) < 9:
            raise ValueError(
                f"GH_ACCOUNT appears too short ({len(self.account)} chars); "
                "expected account number plus product code."
            )

    @property
    def cano(self) -> str:
        return self.account[:8]

    @property
    def acnt_prdt_cd(self) -> str:
        return self.account[8:]