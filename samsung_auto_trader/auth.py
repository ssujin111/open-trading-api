import json
import os
from datetime import datetime, date
from typing import Optional, Dict, Any
from api_client import APIClient
from logger import logger

class Auth:
    def __init__(self, config, api_client: APIClient):
        self.config = config
        self.api_client = api_client
        self.token: Optional[str] = None
        self.token_date: Optional[date] = None

    def get_token(self) -> str:
        today = date.today()
        if self.token and self.token_date == today:
            logger.info("Reusing cached token")
            return self.token

        # Load from cache if exists
        if os.path.exists(self.config.token_cache_file):
            with open(self.config.token_cache_file, 'r') as f:
                cache = json.load(f)
                if cache.get('date') == str(today):
                    self.token = cache['token']
                    self.token_date = today
                    logger.info("Loaded token from cache")
                    return self.token

        # Authenticate
        data = {
            "grant_type": "client_credentials",
            "appkey": self.config.appkey,
            "appsecret": self.config.appsecret
        }
        response = self.api_client.post('/oauth2/tokenP', data)
        self.token = response['access_token']
        self.token_date = today

        # Cache
        with open(self.config.token_cache_file, 'w') as f:
            json.dump({'token': self.token, 'date': str(today)}, f)
        logger.info("New token obtained and cached")
        return self.token