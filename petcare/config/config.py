import os


class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get("PETCARE_DB_URI")


class DevelopmentConfig(Config):
    DEBUG = True
