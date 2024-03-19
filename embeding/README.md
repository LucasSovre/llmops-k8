Auteur : Lucas SOVRE

## Prérequis

- Python 3.10
- Docker
- Accès à une instance Redis

## Installation

1. Clonez le dépôt Git :
```bash
docker build -t embbeding-worker .
```

## Utilisation

Pour lancer le worker, exécutez :

```bash
docker run -d --name embbeding-worker embbeding-worker
```

Assurez-vous de configurer les variables d'environnement nécessaires, notamment REDIS_HOST et MODEL_NAME, pour pointer vers votre instance Redis et définir le nom du modèle utilisé.

## Configuration

Vous pouvez configurer le worker en ajustant les variables d'environnement suivantes :

- REDIS_HOST : l'hôte de votre instance Redis (par défaut : localhost).
- MODEL_NAME : le nom du modèle à utiliser (par défaut : embeding_e5).
- LOG_LEVEL : le niveau de journalisation (par défaut : INFO).

## Arrêt propre

Le worker est configuré pour gérer les signaux SIGINT et SIGTERM pour un arrêt propre. Vous pouvez arrêter le conteneur Docker en utilisant :

```shell
docker stop embbeding-worker
```
