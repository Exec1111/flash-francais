"""
Script d'initialisation de la base de données pour Render.
Ce script crée les tables nécessaires et applique les migrations Alembic.
"""
import os
import sys
import logging
import traceback
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from database import engine, Base, SessionLocal
from models.user import User, UserRole  # Import direct du modèle User
from security import get_password_hash

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initialise la base de données en créant les tables et en appliquant les migrations.
    """
    try:
        logger.info("Initialisation de la base de données...")
        
        # Vérifier si la connexion à la base de données fonctionne
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info(f"Connexion à la base de données réussie: {result.fetchone()}")
        
        # Créer les tables directement avec SQLAlchemy
        logger.info("Création des tables avec SQLAlchemy...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables créées avec succès.")
        
        # Exécuter les migrations Alembic
        logger.info("Application des migrations Alembic...")
        try:
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations Alembic appliquées avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'application des migrations Alembic: {e}")
            logger.error(traceback.format_exc())
            # Continuer malgré l'erreur, car les tables ont déjà été créées avec SQLAlchemy
        
        # Vérifier que les tables ont été créées
        try:
            with engine.connect() as conn:
                tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                table_list = [table[0] for table in tables]
                logger.info(f"Tables dans la base de données: {table_list}")
                
                # Vérifier si la table users existe
                if 'users' in table_list:
                    logger.info("La table 'users' existe dans la base de données.")
                else:
                    logger.warning("La table 'users' n'existe pas dans la base de données!")
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des tables: {e}")
            logger.error(traceback.format_exc())
        
        # Créer un utilisateur de test
        create_test_user()
        
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        logger.error(traceback.format_exc())
        return False

def create_test_user():
    """
    Crée un utilisateur de test dans la base de données.
    """
    db = SessionLocal()
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            logger.info("L'utilisateur de test existe déjà.")
            return existing_user
        
        # Créer un nouvel utilisateur
        hashed_password = get_password_hash("password123")
        test_user = User(
            email="test@example.com",
            first_name="Utilisateur",
            last_name="Test",
            hashed_password=hashed_password,
            role=UserRole.TEACHER,
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        logger.info(f"Utilisateur de test créé avec succès: {test_user.email}")
        logger.info("Email: test@example.com")
        logger.info("Mot de passe: password123")
        return test_user
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'utilisateur de test: {e}")
        logger.error(traceback.format_exc())
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    try:
        logger.info("Démarrage du script d'initialisation de la base de données...")
        success = init_db()
        if success:
            logger.info("Initialisation de la base de données terminée avec succès.")
            sys.exit(0)
        else:
            logger.error("Échec de l'initialisation de la base de données.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur non gérée: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
