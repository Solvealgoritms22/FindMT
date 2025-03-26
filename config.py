import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_LOGIN = os.getenv("SMTP_LOGIN")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")
LOGO_PATH = os.getenv("LOGO_PATH")
# Convertir la variable ALLOWED_PROVINCIAS en una lista de enteros.
ALLOWED_PROVINCIAS = [int(x.strip()) for x in os.getenv("ALLOWED_PROVINCIAS", "41,190,42").split(",")]

# Datos para solicitar el token
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT", "https://empleateya.mt.gob.do/idp/connect/token")
INTERMEDIATE_BASE_URL = os.getenv("INTERMEDIATE_BASE_URL")
