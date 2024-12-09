import os
from typing import Dict, Any

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'library.db'
    ITEMS_PER_PAGE = 10
    TOKEN_EXPIRATION = 24 * 3600  # 24 hours in seconds

    @staticmethod
    def to_dict() -> Dict[str, Any]:
        return {
            'SECRET_KEY': Config.SECRET_KEY,
            'DATABASE_PATH': Config.DATABASE_PATH,
            'ITEMS_PER_PAGE': Config.ITEMS_PER_PAGE,
            'TOKEN_EXPIRATION': Config.TOKEN_EXPIRATION
        } 