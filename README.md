# ResumeAI - Plateforme SaaS d'Analyse de CV

Une application SaaS (Software as a Service) complète et prête pour la production, conçue pour analyser les curriculum vitae en utilisant une combinaison puissante d'extraction basée sur des règles et d'intelligence artificielle avancée (OpenAI).

## 🚀 Résumé Professionnel du Projet

**ResumeAI** est une plateforme moderne permettant aux développeurs, candidats et recruteurs d'évaluer instantanément les compétences, la profondeur technique et l'expérience présentes dans un CV. 

Grâce à une **architecture hybride unique**, l'application combine un **moteur de scoring multidimensionnel** (basé sur des règles strictes) et l'analyse contextuelle de l'**IA générative** pour fournir un retour constructif, identifier les forces et faiblesses, et générer un bilan précis.

Ce projet met en avant des compétences avancées en ingénierie logicielle (Full-Stack) et a été architecturé pour la **performance, la sécurité et la scalabilité** :

- **Sécurité & Authentification JWT :** Système complet d'inscription et de connexion sécurisé via JSON Web Tokens (JWT) et hachage de mots de passe (bcrypt) avec gestion de routes protégées côté React.
- **Traitement Asynchrone (Background Tasks) :** Les requêtes complexes à l'IA sont gérées en arrière-plan. Le client utilise un mécanisme de *polling* pour interroger le statut de son analyse, garantissant une expérience utilisateur (UX) fluide, sans blocage ni timeout.
- **Base de Données Relationnelle :** Persistance des données utilisateurs et de l'historique des analyses via **PostgreSQL** (NeonDB) et **SQLAlchemy**.
- **Gestion de Quotas (SaaS) :** Implémentation d'un système de limitation côté serveur (ex: 5 analyses par jour) propre au modèle économique SaaS.
- **Interface Utilisateur Premium (UI/UX) :** Design SaaS ultra-moderne adoptant la tendance *Glassmorphism*, avec un mode sombre immersif, des micro-animations fluides, une page d'atterrissage optimisée pour la conversion, et un tableau de bord analytique détaillé.

## 🛠️ Stack Technique

**Backend (API & Intelligence Artificielle) :**
- **Langage :** Python 3
- **Framework :** FastAPI (Framework API asynchrone ultra-rapide)
- **Base de données & ORM :** PostgreSQL, SQLAlchemy, Alembic (Migrations)
- **Sécurité :** Passlib, python-jose (JWT), Pydantic (Validation des schémas)
- **IA & Traitement :** OpenAI SDK, PyPDF (Extraction textuelle)

**Frontend (Client Web & UI) :**
- **Framework :** React.js (Vite)
- **Styling :** Tailwind CSS (Utilitaires & UI Responsive)
- **Réseau :** Axios (Intercepteurs HTTP pour les requêtes authentifiées)
- **Navigation :** React Router DOM (Navigation Single-Page et routes protégées)
- **Composants :** Lucide React (Icônes SVG vectorielles)

## ⚙️ Instructions d'Installation & Lancement

### Backend

1. Naviguez vers le dossier `backend`.
2. Créez un environnement virtuel : `python -m venv venv`.
3. Activez l'environnement : 
   - Windows : `venv\Scripts\activate`
   - Mac/Linux : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`.
5. Configurez vos variables d'environnement dans un fichier `.env` :
   - `OPENAI_API_KEY` (Votre clé API OpenAI)
   - `DATABASE_URL` (Votre connexion PostgreSQL, ex: NeonDB)
   - `JWT_SECRET` (Une chaîne de caractères secrète)
6. Démarrez le serveur FastAPI : `python -m uvicorn app.main:app --reload`.

### Frontend

1. Naviguez vers le dossier `frontend`.
2. Installez les dépendances JavaScript : `npm install`.
3. Lancez le serveur de développement : `npm run dev`.
4. Ouvrez `http://localhost:5173` dans votre navigateur.

## 🧠 Architecture & Flux de Données

1. **Authentification :** L'utilisateur s'inscrit ou se connecte. Le backend retourne un token JWT qui est stocké de manière sécurisée côté client (intercepteurs Axios).
2. **Extraction PDF :** L'utilisateur upload un CV. Le frontend appelle de manière sécurisée l'endpoint `POST /extract-text` qui extrait le contenu brut.
3. **Moteur Hybride Asynchrone :** Le texte est transmis à `POST /analyze-cv`. L'API répond par un code `202 Accepted` avec un `job_id` et délègue le travail au moteur d'IA en arrière-plan.
4. **Polling Réactif :** Le client interroge `GET /analysis-status/{job_id}` à intervalles réguliers. L'UI affiche un état de chargement interactif.
5. **Restitution (Dashboard) :** Une fois le statut à `completed`, les résultats sont sauvegardés en base de données et l'utilisateur est redirigé vers un tableau de bord complet affichant son score, ses compétences, et le retour qualitatif de l'IA.
