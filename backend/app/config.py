class Config:
    SECRET_KEY = "supersecretkey-1234"
    SQLALCHEMY_DATABASE_URI = "sqlite:///quiz_master.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwtsecret-1234"