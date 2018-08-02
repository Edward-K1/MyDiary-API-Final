class Config:
    DEBUG = True


class DevelopmentConfig(Config):
    DATABASE_URL = "postgresql://postgres:postgres@localhost/mydiary"


class TestingConfig(Config):
    DATABASE_URL = "postgresql://postgres:postgres@localhost/mydiary_test"


class ProductionConfig(Config):
    DATABASE_URL = "postgresql://postgres:postgres@localhost/mydiary"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
