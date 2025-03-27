# Flash Français

Application d'apprentissage du français utilisant des flashcards.

## Structure du Projet

```
flash-francais/
├── frontend/           # Application React
├── backend/           # API Python
└── docker/            # Configuration Docker
```

## Prérequis

- Node.js >= 16
- Python >= 3.8
- PostgreSQL >= 13
- Docker (optionnel)

## Installation

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Sur Windows
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Démarrage

### Backend

```bash
cd backend
source venv/Scripts/activate  # Sur Windows
python -m uvicorn app.py:app --reload
```

L'API sera disponible sur http://localhost:8000
Documentation Swagger : http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm start
```

Le frontend sera disponible sur http://localhost:3000

## Base de données

PostgreSQL est utilisé comme base de données.
Configuration dans le fichier `.env` :

```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/flash_francais
```

## Déploiement

L'application est déployée sur Render.com.
La configuration du déploiement se trouve dans le fichier `render.yaml`.
