from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
import os

settings = get_settings()

# Afficher les informations d'environnement pour le débogage
print(f"Environnement : {settings.ENV}")
print(f"Variables d'environnement disponibles : {list(os.environ.keys())}")

# Priorité à l'URL de la base de données fournie par Render
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print(f"URL de base de données depuis settings : {SQLALCHEMY_DATABASE_URL}")

# Vérifier si l'URL est disponible directement dans les variables d'environnement
if not SQLALCHEMY_DATABASE_URL or SQLALCHEMY_DATABASE_URL == "":
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "")
    print(f"URL de base de données depuis os.environ : {SQLALCHEMY_DATABASE_URL}")

# Si l'URL n'est toujours pas disponible, on peut la construire manuellement
if not SQLALCHEMY_DATABASE_URL or SQLALCHEMY_DATABASE_URL == "":
    # Informations de connexion spécifiques à Render
    DB_HOST = os.environ.get("DB_HOST", "dpg-cvjafemr433s73islr0-a")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "flashfrdb")
    DB_USER = os.environ.get("DB_USER", "flashfrdbuser")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"URL de base de données construite manuellement : {SQLALCHEMY_DATABASE_URL}")

# Correction du préfixe pour PostgreSQL
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"URL de base de données après correction du préfixe : {SQLALCHEMY_DATABASE_URL}")

print(f"URL finale de connexion à la base de données : {SQLALCHEMY_DATABASE_URL}")

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
