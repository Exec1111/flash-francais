from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
import os

settings = get_settings()

# Priorité à l'URL de la base de données fournie par Render
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Si l'URL n'est pas disponible, on peut la construire manuellement
if not SQLALCHEMY_DATABASE_URL or SQLALCHEMY_DATABASE_URL == "":
    # Informations de connexion spécifiques à Render
    DB_HOST = "dpg-cvjafemr433s73islr0-a"
    DB_PORT = "5432"
    DB_NAME = "flashfrdb"
    DB_USER = os.getenv("DB_USER", "flashfrdbuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Correction du préfixe pour PostgreSQL
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connexion à la base de données : {SQLALCHEMY_DATABASE_URL}")

# Configuration des paramètres de connexion en fonction de l'environnement
connect_args = {}
if settings.ENV == "production":
    # En production (Render), on utilise SSL
    connect_args["sslmode"] = "require"
    pool_size = 5
    max_overflow = 2
    pool_timeout = 30
    pool_recycle = 1800
else:
    # En développement local, pas de SSL
    pool_size = 5
    max_overflow = 2
    pool_timeout = 30
    pool_recycle = 1800

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=pool_size,
    max_overflow=max_overflow,
    pool_timeout=pool_timeout,
    pool_recycle=pool_recycle,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
