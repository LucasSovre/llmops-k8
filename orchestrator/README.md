Auteur : Lucas SOVRE

Auteur : Lucas SOVRE

## Prérequis

- Python 3.10
- Docker
- Accès à une instance Redis
- Accès à une base mongo

## Installation

1. Clonez le dépôt Git :
```bash
docker build -t orchestrator .
```

## Utilisation

Pour lancer le serveur, exécutez :

```bash
docker run -d --name orchestrator orchestrator
```

Assurez-vous de configurer les variables d'environnement nécessaires.

## Configuration

Vous pouvez configurer le serveur en ajustant les variables d'environnement suivantes :

- REDIS_HOST=redis (par défaut : localhost)
- MONGO_HOST=mongo (par défaut : localhost)
- MONGO_USER=admin (par défaut : admin)
- MONGO_PASSWORD=admin (par défaut : admin)