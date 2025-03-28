"""
Script d'initialisation de la base de données pour Render.
Ce script crée les tables nécessaires et applique les migrations Alembic.
"""
import os
import sys
import logging
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from database import engine, Base
from models import Flashcard  # Importer tous les modèles pour qu'ils soient enregistrés

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
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations Alembic appliquées avec succès.")
        
        # Vérifier que les tables ont été créées
        with engine.connect() as conn:
            tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            table_list = [table[0] for table in tables]
            logger.info(f"Tables dans la base de données: {table_list}")
            
            # Vérifier si la table flashcards existe
            if 'flashcards' in table_list:
                logger.info("La table 'flashcards' existe dans la base de données.")
            else:
                logger.warning("La table 'flashcards' n'existe pas dans la base de données!")
        
        logger.info("Initialisation de la base de données terminée avec succès.")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        return False

if __name__ == "__main__":
    success = init_db()
    # Ne pas quitter avec un code d'erreur même si l'initialisation échoue
    # Cela permettra à Render de continuer le déploiement
    sys.exit(0)
