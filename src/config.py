import os

TOKEN = os.getenv("TOKEN", '1649136824:AAEm_hTfTMiYZUxrg4ui0jNuJVndZDULfVQ')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///local.db")