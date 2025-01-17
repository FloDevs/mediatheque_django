# mediatheque_django
# README - Lancer le projet Django

## Description du projet
Ce projet Django est une application de gestion permettant de gérer une médiatheque.

Ce guide détaille les étapes nécessaires pour configurer et exécuter l'application sur votre machine locale.

---

## Prérequis
Avant de commencer, assurez-vous que votre système dispose des éléments suivants :

- **Python** (version 3.8 ou supérieure)
- **pip** (inclus avec Python)
- **Un gestionnaire de base de données** (SQLite inclus par défaut, ou PostgreSQL/MySQL si configuré)
- **Git** (facultatif, pour cloner le projet depuis un dépôt GitHub)

---

## Installation et configuration

### 1. **Cloner le projet**

Commencez par cloner le dépôt Git de l'application :

```bash
git clone https://github.com/FloDevs/mediatheque_django.git
cd mediatheque_django 
cd mediatheque_django 
```
Faite bien 2 fois le changement de dossier
---

### 2. **Créer et activer un environnement virtuel**

Créez un environnement virtuel pour isoler les dépendances du projet :

```bash
python -m venv env
```

Activez l'environnement virtuel :

- **Windows** :
  ```bash
  .\env\Scripts\activate

  ```
- **macOS/Linux** :
  ```bash

  source env/bin/activate

  ```

---

### 3. **Installer les dépendances**

Installez les dépendances nécessaires à l'exécution du projet en utilisant le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```
---

### 4. **Configurer la base de données**


Exécutez les migrations pour configurer les tables nécessaires à l'application :

```bash
python manage.py migrate
```
Ceci devrait créer automatiquement une base de données 'db.sqlite3'

Pour importer des données test qui ont déja été établi :

```bash

python manage.py loaddata app_bibliothecaire/data/data_bdd.json

```
---

### 5. **Créer un super utilisateur (optionnel)**

Normalement un super utilisateur à déja été intégré à la base de données , ces informations de connexion sont les suivantes :

 ### user = admin_mediatheque
 ### password = password_mediatheque

Avec ceci vous pourrez accéder à l'interface d'administration et à l'application des bibliothecaires, 

si ca ne fonctionne pas créez un super utilisateur :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour définir un nom d'utilisateur, un e-mail et un mot de passe.

---

### 6. **Lancer le serveur de développement**

Démarrez le serveur Django :

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse suivante :

[http://127.0.0.1:8000](http://127.0.0.1:8000)

---



## Informations supplémentaires

### Désactiver l'environnement virtuel

Pour quitter l'application faite un CTRL+c (Break)

Pour quitter l'environnement virtuel après utilisation, exécutez :

```bash
deactivate
```

## Auteur

FloDevs

---



