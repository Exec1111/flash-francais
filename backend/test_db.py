import psycopg2
from config import get_settings

settings = get_settings()

def test_connection():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(settings.DATABASE_URL)
        
        # Création d'un curseur
        cur = conn.cursor()
        
        # Exécution d'une requête simple
        cur.execute('SELECT version();')
        
        # Récupération du résultat
        version = cur.fetchone()
        print("Connexion réussie !")
        print(f"Version PostgreSQL : {version[0]}")
        
        # Lister les tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print("\nTables dans la base de données :")
        for table in tables:
            print(f"- {table[0]}")
        
    except Exception as e:
        print(f"Erreur de connexion : {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_connection()
