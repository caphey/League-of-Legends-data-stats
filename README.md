# League of Legends Data Stats

Ce projet est une application web qui utilise l'API de Riot Games pour récupérer et afficher des statistiques sur les joueurs de League of Legends.

![Capture d'écran de l'application](/static/img/background.jpeg)
![Capture d'écran de l'application](/static/img/screenshot.jpeg)

## Structure du projet

Le projet est structuré comme suit :

- `main.py` : Le point d'entrée de l'application. Il contient le code du serveur Flask et les routes.
- `riot.py` : Ce fichier contient les fonctions qui interagissent avec l'API de Riot Games.
- `static/` : Ce dossier contient les fichiers statiques tels que les images et les fichiers CSS.
- `templates/` : Ce dossier contient les fichiers HTML qui sont rendus par le serveur Flask.

## Comment exécuter le projet

1. Assurez-vous d'avoir installé Python et Flask.
2. Exécutez le serveur Flask avec la commande suivante :

```bash
python main.py
```

Ouvrez votre navigateur et accédez à http://localhost:5000.

## Fonctionnalités
* Récupération des données du joueur à partir de son nom de jeu et de sa ligne de tag.
* Affichage des 3 champions les plus joués par le joueur.
* Affichage du niveau du joueur.
* Affichage des statistiques des trois derniers matchs du joueur.
* Affichage du pourcentage de victoires et de défaites du joueur.
* Affichage du CS par minute du joueur.

## Technologies utilisées
* Python
* HTML/CSS
* Chart.js
* Flask
* MongoDB / NoSQL