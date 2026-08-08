from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from celery import Celery
import redis


db = SQLAlchemy()

jwt = JWTManager()

cors = CORS()

migrate = Migrate()

bcrypt = Bcrypt()

# Celery
celery = Celery(__name__)

# Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)