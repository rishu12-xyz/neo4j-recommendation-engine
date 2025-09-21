# Neo4j Recommendation Engine

## Overview
This project demonstrates how to build a collaborative filtering recommendation system using Neo4j graph database. We model users, products, and purchase relationships as a graph to find similar users and generate product recommendations based on shared purchasing behavior.

## Graph Model
- `(:User {name: string})` - Users in the system
- `(:Product {name: string})` - Products available for purchase  
- `(:User)-[:PURCHASED]->(:Product)` - Purchase relationships between users and products

## Data Setup
```cypher
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create sample data
CREATE 
  // Users
  (alice:User {name:"Alice"}),
  (bob:User {name:"Bob"}),
  (carol:User {name:"Carol"}),
  (dave:User {name:"Dave"}),
  
  // Products
  (laptop:Product {name:"Laptop"}),
  (phone:Product {name:"Phone"}),
  (headphones:Product {name:"Headphones"}),
  (keyboard:Product {name:"Keyboard"}),
  (mouse:Product {name:"Mouse"}),
  
  // Purchase relationships
  (alice)-[:PURCHASED]->(laptop),
  (alice)-[:PURCHASED]->(keyboard),
  (bob)-[:PURCHASED]->(laptop),
  (bob)-[:PURCHASED]->(phone),
  (carol)-[:PURCHASED]->(laptop),
  (carol)-[:PURCHASED]->(headphones),
  (dave)-[:PURCHASED]->(keyboard),
  (dave)-[:PURCHASED]->(mouse);
```

## Recommendation Query
### Collaborative Filtering Algorithm
```cypher
// Find products to recommend to Alice based on similar users
MATCH (alice:User {name:"Alice"})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
WHERE alice <> similarUser
MATCH (similarUser)-[:PURCHASED]->(rec:Product)
WHERE NOT (alice)-[:PURCHASED]->(rec)
RETURN rec.name AS RecommendedProduct, 
       COUNT(*) AS score,
       COLLECT(DISTINCT similarUser.name) AS RecommendedBy
ORDER BY score DESC;
```

### Graph Visualization Query
```cypher
// Show recommendation network as connected graph
MATCH (alice:User {name:"Alice"})-[r1:PURCHASED]->(commonProduct:Product)<-[r2:PURCHASED]-(similarUser:User)-[r3:PURCHASED]->(rec:Product)
WHERE alice <> similarUser AND NOT (alice)-[:PURCHASED]->(rec)
RETURN alice, r1, commonProduct, r2, similarUser, r3, rec;
```

## How It Works
1. **Find Similar Users**: Identify users who purchased the same products as the target user
2. **Discover New Products**: Find products that similar users bought but the target user hasn't
3. **Score Recommendations**: Count how many similar users bought each recommended product
4. **Rank Results**: Order recommendations by popularity among similar users

## Running Locally
1. Start a free [Neo4j AuraDB](https://neo4j.com/cloud/aura/) instance
2. Run the data setup query to create sample data
3. Execute recommendation queries in Neo4j Browser
4. Switch to Graph view to visualize the recommendation network
5. (Optional) Use Neo4j drivers to integrate with your application

## Sample Output
For user **Alice** (who bought Laptop and Keyboard), the system recommends:

| RecommendedProduct | Score | RecommendedBy |
|-------------------|-------|---------------|
| Phone | 1 | ["Bob"] |
| Headphones | 1 | ["Carol"] |
| Mouse | 1 | ["Dave"] |

## Use Cases
- **E-commerce**: Product recommendations based on purchase history
- **Content Platforms**: Suggest movies, books, or articles
- **Social Networks**: Friend or content recommendations
- **Music Streaming**: Recommend songs or artists

## Next Steps
- Add product categories and user demographics
- Implement content-based filtering using product features
- Add rating relationships for more sophisticated recommendations
- Scale with real-world datasets using graph algorithms
