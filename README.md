# Neo4j Recommendation Engine

## Overview
This project demonstrates how to build a simple recommendation system using Neo4j.  
We model users, products, and purchases as a graph and query similar-user behavior to generate recommendations.

## Graph Model
- `(:User)`
- `(:Product)`
- `(:User)-[:PURCHASED]->(:Product)`

## Example Cypher Query
```cypher
MATCH (u:User {name:"Alice"})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:User)-[:PURCHASED]->(rec:Product)
WHERE NOT (u)-[:PURCHASED]->(rec)
RETURN rec, COUNT(*) AS score
ORDER BY score DESC
LIMIT 5;
```

## Running Locally
1. Start a free [Neo4j AuraDB](https://neo4j.com/cloud/aura/).
2. Import `data/sample_data.csv` using `LOAD CSV`.
3. Run queries from `queries/recommendations.cypher`.
4. (Optional) Use `app/app.py` to run queries from Python.

## Sample Output
For user *Alice*, recommendations might look like:
- "Tablet"
- "Headphones"
