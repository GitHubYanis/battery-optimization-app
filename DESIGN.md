## Objectifs

Microservice de planification de batterie sur 24 heures pour minimiser le coût d'électricité. Le service expose trois endpoints `/health`, `/optimize`, `/visualize`, optimise un planning horaire et retourne des données de visualisation pour Plotly.

## Contraintes

**Physiques**
- L’état de charge (SoC) doit toujours rester entre 0 et la capacité 
- La charge/décharge doit rester dans les limites de puissance maximales 
- Pas de charge et décharge simultanées dans la même heure 
- La mise à jour du SoC doit tenir compte du rendement 
- Les 24 heures doivent être réalisables 


**Technologie/Techniques**
- Backend Python, frontend React + TypeScript, visualisation Plotly
- Authentification par clé API, rate limiting par clé
- Déploiement via Dockerfile vers une URL cloud publique
- Au moins un paramètre de production via variable d'environnement

## Choix de conception

**Algorithme d'optimisation** — Basée sur la médiane des prix : charge la batterie aux heures moins dispendieuses et se décharge aux heures plus dispendieuses.

**Backend** — FastAPI et Pydantic pour la validation, `x-api-key` pour l'authentification, rate limiting en mémoire par clé (compteur perdu au redémarrage).

**Visualisation** — Objets Plotly complets (`{ data, layout }`) générés côté backend. Le frontend ne contient très peu de logique (aucune logique métier).

**Déploiement** — Conteneur Docker déployé sur Azure Container Apps. Variables d'environnement utilisée : `API_KEY`, `RATE_LIMIT`.