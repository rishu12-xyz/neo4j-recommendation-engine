// Create sample data manually
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

// Alternative: Load data from CSV (uncomment to use)
/*
LOAD CSV WITH HEADERS FROM 'file:///sample_data.csv' AS row
MERGE (u:User {name: row.user_name})
MERGE (p:Product {name: row.product_name})
MERGE (u)-[:PURCHASED]->(p);
*/

// Verify data loaded correctly
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN u.name AS User, p.name AS Product
ORDER BY User, Product;

// Basic recommendation query - Get recommendations for a specific user
MATCH (target:User {name:"Alice"})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
WHERE target <> similarUser
MATCH (similarUser)-[:PURCHASED]->(rec:Product)
WHERE NOT (target)-[:PURCHASED]->(rec)
RETURN rec.name AS RecommendedProduct, 
       COUNT(*) AS score,
       COLLECT(DISTINCT similarUser.name) AS RecommendedBy
ORDER BY score DESC;

// Generic recommendation function (replace 'Alice' with any username)
MATCH (target:User {name:$username})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
WHERE target <> similarUser
MATCH (similarUser)-[:PURCHASED]->(rec:Product)
WHERE NOT (target)-[:PURCHASED]->(rec)
RETURN rec.name AS RecommendedProduct, 
       COUNT(*) AS score,
       COLLECT(DISTINCT similarUser.name) AS RecommendedBy
ORDER BY score DESC
LIMIT $limit;

// Graph visualization query - Show recommendation network
MATCH (alice:User {name:"Alice"})-[r1:PURCHASED]->(commonProduct:Product)<-[r2:PURCHASED]-(similarUser:User)-[r3:PURCHASED]->(rec:Product)
WHERE alice <> similarUser AND NOT (alice)-[:PURCHASED]->(rec)
RETURN alice, r1, commonProduct, r2, similarUser, r3, rec;

// Find all similar users for a given user
MATCH (target:User {name:"Alice"})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
WHERE target <> similarUser
RETURN target.name AS TargetUser,
       similarUser.name AS SimilarUser,
       COLLECT(commonProduct.name) AS SharedProducts,
       SIZE(COLLECT(commonProduct.name)) AS SharedCount
ORDER BY SharedCount DESC;

// Get user's purchase history
MATCH (u:User {name:"Alice"})-[:PURCHASED]->(p:Product)
RETURN u.name AS User, COLLECT(p.name) AS PurchasedProducts;

// Find most popular products
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN p.name AS Product, COUNT(u) AS PurchaseCount
ORDER BY PurchaseCount DESC;