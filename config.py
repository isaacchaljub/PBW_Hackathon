import os

class Config:
    DEBUG = False
    TESTING = False
    DATABASE = 'solar_crowdfunding.db'
    XRPL_CLIENT_URL = "https://s.altnet.rippletest.net:51234"  # Testnet

class ProductionConfig(Config):
    ENV = 'production'
    # Uncomment and adjust for mainnet in production
    # XRPL_CLIENT_URL = "https://xrplcluster.com"

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    DEBUG = True
