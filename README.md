# Test technique LLMOPS

Auteur : Lucas SOVRE

### Description de la stack :

Pour une bonne orchestration des demandes, nous utilisons Redis list comme message brokers.
Pour permettre au client de recuperer la réponse à sa requête, on utilise le Server Side Event et Redis pub/sub, cela permet de drastiquement réduire le nombre de requêtes, en comparaison avec un refetch régulier.

```mermaid
sequenceDiagram
    client->>+orchestrateur: POST ai request
    orchestrateur->>redis:push new task in queue
    orchestrateur->>-client:task schedule, wait for SSE with dedicated chanel_id
    redis->>llm: pop element in queue
    llm->>redis: return inference result in inference_end channel
    redis->>orchestrateur: consume inference_end channel
    orchestrateur->>client:send back inference result by SSE
```

Avec l'architecture state-less décrite ci-dessous, on peut déployer autant d'orchestrateurs et de workers que nécessaire, nous avons une scalabilité horizontale quasiment infinie :

![plot](./doc/architecture.png)
