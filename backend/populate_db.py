import logging
import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Progression, Objective, Sequence, Session as SessionModel, Resource, User # Import des modèles principaux
from models.resource import ResourceType # Import de l'Enum depuis son module spécifique
from models.association_tables import session_objective_association, sequence_objective_association # Table Progression-Sequence non définie ici

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_existing_data(db: Session):
    """Supprime les données existantes (sauf utilisateurs)."""
    logger.info("Suppression des anciennes données (sauf utilisateurs)...")
    try:
        # Supprimer les liens où les tables d'association sont explicitement définies
        db.execute(session_objective_association.delete()) # Nom corrigé
        db.execute(sequence_objective_association.delete()) # Nom corrigé
        # db.execute(progression_sequence_association.delete()) # Cette table n'est pas définie ici
        db.commit()
        # La suppression en cascade devrait gérer les liens Progression-Sequence lors de la suppression des Progressions/Sequences
        db.query(Resource).delete(synchronize_session=False)
        db.query(SessionModel).delete(synchronize_session=False)
        db.query(Sequence).delete(synchronize_session=False)
        db.query(Objective).delete(synchronize_session=False)
        db.query(Progression).delete(synchronize_session=False)
        db.commit()
        logger.info("Anciennes données supprimées.")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression des anciennes données: {e}")
        db.rollback()
        raise # Propage l'erreur pour arrêter le script

def populate_database():
    db: Session = SessionLocal()
    try:
        logger.info("Début du peuplement de la base de données...")
        clear_existing_data(db)

        # --- Création des données fictives --- 

        # 1. Objectifs
        objectives_data = [
            ("Comprendre le présent", "Savoir conjuguer les verbes ER"),
            ("Vocabulaire : La nourriture", "Connaître 20 mots courants"),
            ("Grammaire : Les articles", "Différencier un/une/des et le/la/les"),
            ("Exprimer ses goûts", "Utiliser J'aime / Je n'aime pas"),
            ("Passé composé : auxiliaire AVOIR", "Formation avec les verbes réguliers"),
            ("Passé composé : auxiliaire ÊTRE", "Accord du participe passé"),
            ("Imparfait : formation", "Terminaisons et verbes courants"),
            ("Futur simple", "Formation et utilisation"),
            ("Vocabulaire : Les vêtements", "Nommer 15 vêtements"),
            ("Vocabulaire : La famille", "Membres de la famille"),
            ("Prépositions de lieu", "Utiliser sur, sous, dans, devant, derrière"),
            ("Adjectifs possessifs", "Mon, ton, son, notre, votre, leur"),
            ("Négation simple", "Ne...pas"),
            ("Questions simples", "Est-ce que, Qu'est-ce que, Où, Quand"),
            ("Pronoms COD", "Le, la, les, l'"),
            ("Pronoms COI", "Lui, leur"),
            ("Conditionnel présent", "Formation et politesse"),
            ("Subjonctif présent : introduction", "Après il faut que"),
            ("Vocabulaire : Les transports", "Moyens de transport courants"),
            ("Culture : Monuments de Paris", "Identifier 5 monuments")
        ]
        objectives = [Objective(title=t, description=d) for t, d in objectives_data]
        db.add_all(objectives)
        db.commit() # Commit pour obtenir les IDs des objectifs
        logger.info(f"{len(objectives)} Objectifs créés.")
        obj_map = {obj.title: obj for obj in objectives} # Pour accès facile par titre

        # 2. Progressions (créées avant les séquences)
        progressions_data = [
            ("Parcours Débutant A1", "Niveau A1 complet"),
            ("Parcours Intermédiaire A2", "Niveau A2 complet"),
            ("Parcours Avancé B1", "Niveau B1 complet"),
            ("Module : Grammaire Passé", "Focus sur Passé Composé et Imparfait"),
            ("Module : Voyage et Culture", "Préparation et découverte")
        ]
        progressions = [Progression(title=t, description=d) for t, d in progressions_data]
        db.add_all(progressions)
        db.commit() # Commit pour obtenir les IDs des progressions
        logger.info(f"{len(progressions)} Progressions créées.")
        prog_map = {prog.title: prog for prog in progressions} # Pour accès facile
        prog_ids = [p.id for p in progressions]

        # 3. Séquences (créées APRES les progressions, avec progression_id)
        sequences_data = [
            # Titre, Description, Titres Objectifs, Titre Progression Parente (Optionnel)
            ("A1.1 Introduction", "Les bases absolues", ["Comprendre le présent", "Vocabulaire : La nourriture", "Grammaire : Les articles"], "Parcours Débutant A1"),
            ("A1.2 Premiers pas", "Communication simple", ["Exprimer ses goûts", "Adjectifs possessifs", "Négation simple"], "Parcours Débutant A1"),
            ("A2.1 Le passé", "Raconter des événements", ["Passé composé : auxiliaire AVOIR", "Passé composé : auxiliaire ÊTRE", "Imparfait : formation"], "Parcours Intermédiaire A2"),
            ("A2.2 Descriptions", "Décrire des personnes et lieux", ["Vocabulaire : Les vêtements", "Vocabulaire : La famille", "Prépositions de lieu"], "Parcours Intermédiaire A2"),
            ("B1.1 Vers l'autonomie", "Exprimer son opinion", ["Futur simple", "Pronoms COD", "Pronoms COI"], "Parcours Avancé B1"),
            ("B1.2 Structures avancées", "Hypothèses et conditions", ["Conditionnel présent", "Subjonctif présent : introduction"], "Parcours Avancé B1"),
            ("Thème : Voyage", "Préparer un voyage", ["Vocabulaire : Les transports", "Questions simples"], "Module : Voyage et Culture"),
            ("Thème : Culture", "Découverte culturelle", ["Culture : Monuments de Paris"], "Module : Voyage et Culture"),
            # Séquence orpheline pour tester
            ("Orpheline : Adverbes", "Formation des adverbes en -ment", ["Comprendre le présent"], None) 
        ]
        sequences = []
        for title, desc, obj_titles, prog_title in sequences_data:
            seq_objectives = [obj_map[t] for t in obj_titles if t in obj_map]
            current_prog_id = prog_map[prog_title].id if prog_title and prog_title in prog_map else None
            
            # Gérer le cas où la progression parente est None mais que la colonne est NOT NULL
            # Si la colonne EST nullable, current_prog_id = None est ok
            # Si la colonne est NOT NULL, il faut assigner une progression par défaut ou lever une erreur
            # Ici, on choisit une progression aléatoire si prog_title est None et que la colonne semble NOT NULL
            if current_prog_id is None:
                logger.warning(f"Sequence '{title}' n'a pas de progression parente définie. Assignation aléatoire car progression_id semble NOT NULL.")
                current_prog_id = random.choice(prog_ids) # Assignation aléatoire
                # Alternative : lever une erreur si une séquence doit absolument avoir une progression
                # raise ValueError(f"Sequence '{title}' doit avoir une progression parente définie.")
                
            sequences.append(Sequence(title=title, description=desc, objectives=seq_objectives, progression_id=current_prog_id))
            
        db.add_all(sequences)
        db.commit() # Commit pour obtenir les IDs des séquences
        logger.info(f"{len(sequences)} Séquences créées.")
        sequence_ids = [s.id for s in sequences] # Récupérer les IDs des séquences
        
        # 4. Mettre à jour les progressions avec leurs séquences (si nécessaire et si la relation est bidirectionnelle)
        # Si la relation Progression.sequences est définie avec back_populates='progression',
        # SQLAlchemy devrait gérer cela automatiquement. Sinon, on peut le faire manuellement:
        # for prog in progressions:
        #     prog.sequences = [s for s in sequences if s.progression_id == prog.id]
        # db.commit()
        # logger.info("Liens Progression -> Sequences mis à jour.")
        
        # 5. Sessions (comme avant, mais après les objectifs et avec sequence_id)
        if not sequence_ids:
             logger.error("Aucune séquence n'a été créée, impossible de créer des sessions.")
             return # Ou lever une exception
        
        sessions = []
        start_date = date(2024, 1, 10)
        session_titles_templates = [
            "Leçon {}: {}",
            "Révision : {}",
            "Focus sur : {}",
            "Atelier pratique : {}"
        ]
        all_objective_ids = [o.id for o in objectives]
        
        for i in range(50): # Créer 50 sessions
            template = random.choice(session_titles_templates)
            # Utiliser un objectif aléatoire pour le titre pour plus de variété
            random_objective_title = random.choice([o.title for o in objectives]) if objectives else f"Thème {i+1}"
            session_title = template.format(i + 1, random_objective_title)
            session_date = start_date + timedelta(days=random.randint(0, 365*1)) # Dates sur 1 an
            
            # Sélectionne 1 à 3 objectifs aléatoires pour cette session
            num_objectives = random.randint(1, 3)
            session_objectives_ids = random.sample(all_objective_ids, min(num_objectives, len(all_objective_ids)))
            # Récupérer les objets Objective correspondants
            session_objectives = db.query(Objective).filter(Objective.id.in_(session_objectives_ids)).all()
            
            # Assigner un sequence_id valide
            assigned_sequence_id = random.choice(sequence_ids)
            
            sessions.append(SessionModel(
                title=session_title,
                date=session_date,
                objectives=session_objectives,
                sequence_id=assigned_sequence_id # Assignation ici
            ))
            
        db.add_all(sessions)
        db.commit() # Commit pour obtenir les IDs des sessions
        logger.info(f"{len(sessions)} Sessions créées.")
        session_ids = [s.id for s in sessions] # Récupérer les IDs des sessions
        
        # Ressources (une par session pour l'exemple)
        resources = []
        for sess in sessions:
            # Assurer que le type correspond à l'Enum ResourceType défini dans le modèle
            res_type_enum = random.choice(list(ResourceType))
            res_title = f"{res_type_enum.value.capitalize()} pour {sess.title[:30]}..."
            res_url = f"http://example.com/{res_type_enum.value}/{sess.id}" # Générer une URL fictive
            # Utiliser le champ 'description' pour stocker l'URL (faute de champ 'link' ou 'url')
            resources.append(Resource(type=res_type_enum, title=res_title, description=res_url, session_id=sess.id))
        
        db.add_all(resources)
        db.commit()
        logger.info(f"{len(resources)} Ressources créées.")

        logger.info("Peuplement de la base de données terminé avec succès !")

    except Exception as e:
        logger.error(f"Erreur lors du peuplement de la base de données: {e}", exc_info=True) # Ajout trace
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Assurer que les tables existent (au cas où)
    logger.info("Vérification/Création des tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables vérifiées/créées.")
        populate_database()
    except Exception as e:
        logger.critical(f"Impossible de créer les tables ou de peupler la DB: {e}", exc_info=True)
