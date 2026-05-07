# 🪴 Gardening-Scraping

Scraper Scrapy pour extraire les catégories et produits de bricodepot.fr, avec stockage dans une base de données PostgreSQL via SQLAlchemy.

---

## 📁 Structure du projet

```
Gardening-Scraping/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                        ← à créer depuis .env.example
├── .env.example
└── src/
    ├── main.py
    └── app/
        └── gardening_scraper/
            ├── spiders/
            │   ├── categoryspider.py
            │   └── pagelist_spider.py
            ├── __init__.py
            ├── database.py
            ├── items.py
            ├── middlewares.py
            ├── models.py
            ├── pipelines.py
            └── settings.py
```

---

## ⚙️ Prérequis

- Docker ou [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et **lancé**
- Python 3.11+

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd Gardening-Scraping
```

### 2. Créer l'environnement virtuel

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD)**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

**macOS / Linux**
```bash
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

**Windows (CMD)**
```cmd
copy .env.example .env
```

Édite `.env` avec tes valeurs :

```env
POSTGRES_DB=gardening
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ton_mot_de_passe
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

> ⚠️ `.env` ne doit jamais être commité. Vérifie qu'il est dans `.gitignore`.

---

## 🐳 Lancer la base de données avec Docker

### 1. Démarrer Docker Desktop

| OS | Action |
|----|--------|
| macOS | Lance Docker Desktop depuis le Launchpad — attends la baleine 🐳 dans la barre de menu |
| Windows | Lance Docker Desktop depuis le menu Démarrer — attends la baleine 🐳 dans la barre des tâches |
| Linux | Docker tourne en service système — vérifie avec `sudo systemctl status docker` |

**Linux uniquement — démarrer le service si nécessaire :**
```bash
sudo systemctl start docker
# Optionnel : démarrer automatiquement au boot
sudo systemctl enable docker
```

### 2. Démarrer le conteneur PostgreSQL

```bash
docker compose up -d postgres-api
```

### 3. Vérifier que PostgreSQL est prêt

```bash
docker compose ps
# Le statut doit afficher "healthy" pour postgres-api
```

---

## 🗄️ Initialiser la base de données

Les tables sont créées automatiquement à partir des modèles SQLAlchemy.

**macOS / Linux**
```bash
cd src/app
python3 -m gardening_scraper.database
```

**Windows**
```powershell
cd src\app
python -m gardening_scraper.database
```

Vérifie que les tables ont bien été créées :

```bash
docker compose exec postgres-api psql -U postgres -d gardening -c "\dt"
```

Tu dois voir les tables `categories` et `product`.

---

## 🕷️ Lancer les spiders

Place-toi dans `src/app/` (venv activé) :

**macOS / Linux**
```bash
cd src/app
```

**Windows**
```powershell
cd src\app
```

### Spider catégories

Scrape toutes les catégories et sous-catégories du site.

```bash
scrapy crawl categories
```

Génère également un fichier `categories.csv`.

### Spider produits

Scrape les produits d'une page de liste.

```bash
scrapy crawl pagelist_spider
```

---

## 🔍 Vérifier les données en base

```bash
docker compose exec postgres-api psql -U postgres -d gardening
```

Quelques requêtes utiles :

```sql
SELECT count(*) FROM categories;
SELECT * FROM categories LIMIT 10;
SELECT count(*) FROM product;
SELECT product_category, count(*) FROM product GROUP BY product_category;
\q
```

Tu peux également utiliser **DBeaver** pour visualiser les données :

| Champ    | Valeur      |
|----------|-------------|
| Host     | `localhost` |
| Port     | `5433`      |
| Database | `gardening` |
| Username | `postgres`  |
| Password | *(celle de ton .env)* |

---

## 🗂️ Schéma de la base de données

```
Table categories
├── id              SERIAL PRIMARY KEY
├── category_name   VARCHAR(255)
├── url             VARCHAR(2048)
├── category_id     VARCHAR(255)
├── parent_category VARCHAR(255)
└── image_url       VARCHAR(2048)

Table product
├── id               SERIAL PRIMARY KEY
├── url              VARCHAR(2048)
├── name             VARCHAR(255) NOT NULL
├── price_euros      FLOAT
├── price_cents      FLOAT
├── price_concat     FLOAT
├── product_id       INTEGER
├── product_code     INTEGER
├── product_category VARCHAR(255)
└── description      TEXT
```

---

## 🐳 Lancer le scraper via Docker

```bash
docker compose build
docker compose run --rm scraper
```

> Le scraper attend que PostgreSQL soit `healthy` avant de démarrer.

---

## 🔧 Commandes utiles

```bash
# Voir les logs PostgreSQL
docker compose logs postgres-api

# Voir les logs du scraper
docker compose logs scraper

# Arrêter les conteneurs (données conservées)
docker compose down

# Arrêter et supprimer les données
docker compose down -v

# Reconstruire l'image après modif du code
docker compose build scraper
```

---

## 🌍 Variables d'environnement

| Variable            | Défaut      | Description                               |
|---------------------|-------------|-------------------------------------------|
| `POSTGRES_DB`       | `gardening` | Nom de la base de données                 |
| `POSTGRES_USER`     | `postgres`  | Utilisateur PostgreSQL                    |
| `POSTGRES_PASSWORD` | —           | Mot de passe                              |
| `POSTGRES_HOST`     | `localhost` | Hôte (`postgres-api` dans Docker)         |
| `POSTGRES_PORT`     | `5433`      | Port exposé sur la machine hôte           |

---

## 📦 Dépendances principales

| Package         | Usage                           |
|-----------------|---------------------------------|
| `scrapy`        | Framework de scraping           |
| `sqlalchemy`    | ORM pour les modèles            |
| `psycopg2`      | Driver PostgreSQL               |
| `python-dotenv` | Chargement des variables `.env` |

---

## ⚡ Workflow complet résumé

**macOS / Linux**
```bash
# 1. Activer le venv
source .venv/bin/activate

# 2. Lancer PostgreSQL
docker compose up -d postgres-api

# 3. Créer les tables
cd src/app
python3 -m gardening_scraper.database

# 4. Lancer un spider
scrapy crawl categories
# ou
scrapy crawl pagelist_spider

# 5. Vérifier les données
docker compose exec postgres-api psql -U postgres -d gardening -c "SELECT count(*) FROM categories;"
```

**Windows (PowerShell)**
```powershell
# 1. Activer le venv
.venv\Scripts\Activate.ps1

# 2. Lancer PostgreSQL
docker compose up -d postgres-api

# 3. Créer les tables
cd src\app
python -m gardening_scraper.database

# 4. Lancer un spider
scrapy crawl categories
# ou
scrapy crawl pagelist_spider

# 5. Vérifier les données
docker compose exec postgres-api psql -U postgres -d gardening -c "SELECT count(*) FROM categories;"
```
