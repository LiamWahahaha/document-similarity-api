import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""

    @staticmethod
    def get_env_variable(name, default=""):
        try:
            return os.environ[name]
        except KeyError:
            return default


class ProductionConfig(Config):
    """Production configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
