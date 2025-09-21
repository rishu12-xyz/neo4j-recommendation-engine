// Cypher query for recommendations
MATCH (u:User {name:"Alice"})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:User)-[:PURCHASED]->(rec:Product)
WHERE NOT (u)-[:PURCHASED]->(rec)
RETURN rec, COUNT(*) AS score
ORDER BY score DESC
LIMIT 5;
