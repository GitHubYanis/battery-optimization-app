# Application d'Optimisation de Batterie

Microservice qui planifie l'utilisation d'une batterie sur 24 heures pour minimiser le coût d'électricité.

## Accès
Lien de l'application déployée: https://battery-api.proudcliff-6f07144c.canadacentral.azurecontainerapps.io/

## Prérequis

- Python 3.11+
- Node.js 18+
- Docker Desktop


## Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
```

Crée un fichier `.env` dans `backend/` :
```
API_KEY=your-secret-key
RATE_LIMIT=100
```

### Frontend
```bash
cd frontend
npm install
```

Crée un fichier `.env.development` dans `frontend/` :
```
VITE_API_URL=http://localhost:8000
VITE_API_KEY=your-secret-key
```


## Exécution locale

### Backend
```bash
cd backend
uvicorn main:app --reload
```
API disponible sur `http://localhost:8000`
Documentation sur `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm run dev
```
Interface disponible sur `http://localhost:5173`


## Déploiement (Azure)

### 1. Build et push l'image Docker
```bash
docker build -t battery-api .
docker tag battery-api <registry>.azurecr.io/battery-api
az acr login --name <registry>
docker push <registry>.azurecr.io/battery-api
```

### 2. Variables d'environnement Azure
Dans Azure Container Apps → Settings → Environment variables :
```
API_KEY=your-secret-key
RATE_LIMIT=100
```

### 3. Variables d'environnement frontend
Crée `frontend/.env.production` avant le build :
```
VITE_API_URL=https://your-app.azurecontainerapps.io
VITE_API_KEY=your-secret-key
```
