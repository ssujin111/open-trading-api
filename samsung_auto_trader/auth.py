import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

from api_client import APIClient
from config import Config
from logger import logger


class Auth:
    def __init__(self, config: Config, api_client: APIClient):
        self.config = config
        self.api_client = api_client
        self.token: Optional[str] = None
        self.token_date: Optional[date] = None
        self.cache_file = Path(self.config.token_cache_file)

    def _load_cached_token(self) -> Optional[Dict[str, str]]:
        if not self.cache_file.exists():
            return None

        try:
            with self.cache_file.open('r', encoding='utf-8') as cache_file:
                return json.load(cache_file)
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning(f"Unable to read token cache: {exc}")
            return None

    def _save_cached_token(self, token: str) -> None:
        try:
            with self.cache_file.open('w', encoding='utf-8') as cache_file:
                json.dump({'token': token, 'date': str(date.today())}, cache_file)
            logger.info('New token obtained and cached')
        except OSError as exc:
            logger.warning(f"Unable to write token cache: {exc}")

    def _fetch_token(self) -> str:
        request_data = {
            'grant_type': 'client_credentials',
            'appkey': self.config.appkey,
            'appsecret': self.config.appsecret,
        }
        response = self.api_client.post('/oauth2/tokenP', request_data)
        token = response.get('access_token')
        if not token:
            raise ValueError('Authentication response did not include access_token')
        return token

    def get_token(self) -> str:
        today = date.today()
        if self.token and self.token_date == today:
            logger.info('Reusing cached token')
            return self.token

        cache = self._load_cached_token()
        if cache and cache.get('date') == str(today) and cache.get('token'):
            self.token = cache['token']
            self.token_date = today
            logger.info('Loaded token from cache')
            return self.token

        self.token = self._fetch_token()
        self.token_date = today
        self._save_cached_token(self.token)
        return self.token
