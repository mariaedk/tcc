"""
@author maria
date: 2025-05-25
"""
from dotenv import load_dotenv
import os

load_dotenv()

FIREBIRD_PATH = os.getenv("FIREBIRD_PATH")
FIREBIRD_USER = os.getenv("FIREBIRD_USER")
FIREBIRD_PASSWORD = os.getenv("FIREBIRD_PASSWORD")

API_URL = os.getenv("API_URL")
AUTH_URL = os.getenv("AUTH_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

SENSOR_VAZAO1_ID = int(os.getenv("SENSOR_VAZAO1_ID"))
SENSOR_VAZAO2_ID = int(os.getenv("SENSOR_VAZAO2_ID"))
UNIDADE_ID = int(os.getenv("UNIDADE_ID"))
TIPO_MEDICAO = os.getenv("TIPO_MEDICAO", "INST")

BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))
