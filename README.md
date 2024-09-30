# League of Legends Data Stats

Ce projet est une application web qui utilise l'API de Riot Games pour récupérer et afficher des statistiques détaillées sur les joueurs de League of Legends.

![Capture d'écran de l'application](/static/img/background.jpeg)
![Capture d'écran de l'application](/static/img/screensho.jpeg)

## Structure du projet

Le projet est structuré comme suit :

- `main.py` : Point d'entrée de l'application. Contient le code du serveur Flask et les routes.
- `riot.py` : Contient les fonctions qui interagissent avec l'API de Riot Games.
- `config.py` : Gère la configuration de l'application et les variables d'environnement.
- `static/` : Contient les fichiers statiques (images, CSS, JavaScript).

- `css/` : Fichiers CSS (`index.css`, `style.css`).
- `js/` : Fichiers JavaScript (`script.js` pour les graphiques).
- `img/` : Images utilisées dans l'application.
- `templates/` : Contient les fichiers HTML (`index.html`, `result.html`).

## Comment exécuter le projet

1. Assurez-vous d'avoir installé Python et Flask.
2. Exécutez le serveur Flask avec la commande suivante :

```bash
python main.py
```

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/caphey/league-of-legends-data-stats.git
cd league-of-legends-data-stats
```

2. Créez un fichier `.env` à la racine du projet et ajoutez vos variables d'environnement :
```bash
SECRET_KEY=votre_clé_secrète
RIOT_API_KEY=votre_clé_api_riot
MONGODB_URI=votre_uri_mongodb
FLASK_DEBUG=True  # ou False en production
```

## Comment exécuter le projet

1. Assurez-vous d'avoir bien installé python et que la clé de l'API soit encore fonctionnelle
2. Exécutez le serveur Flask :
```bash
python main.py
```

Ouvrez votre navigateur et accédez à `http://localhost:5000`.

## Fonctionnalités
* Récupération des données du joueur à partir de son nom de jeu et de sa ligne de tag.
* Affichage des 3 champions les plus joués par le joueur.
* Affichage du niveau du joueur.
* Affichage des statistiques des trois derniers matchs du joueur.
* Affichage du pourcentage de victoires et de défaites du joueur.
* Affichage du CS par minute du joueur.

## Technologies utilisées
- Backend : Python, Flask
- Frontend : HTML, CSS, JavaScript
- Visualisation de données : Chart.js
- API : Riot Games API

## Structure du projet
![Capture d'écran de l'application](/static/img/structure.png)
