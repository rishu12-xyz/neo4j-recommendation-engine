"""
Neo4j Recommendation Engine - Python Application
Demonstrates collaborative filtering recommendations using Neo4j graph database
"""

from neo4j import GraphDatabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your Aura credentials
URI = "neo4j+s://<your-database-id>.databases.neo4j.io"
AUTH = ("neo4j", "<your-password>")

class RecommendationApp:
    """
    A recommendation engine using Neo4j graph database
    """

    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        """Close the database connection"""
        self.driver.close()

    def setup_data(self):
        """Create sample data in the database"""
        query = '''
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
        '''
        
        with self.driver.session() as session:
            session.run(query)
            logger.info("Sample data created successfully")

    def get_recommendations(self, username, limit=5):
        """
        Get product recommendations for a user based on collaborative filtering
        
        Args:
            username (str): Name of the user to get recommendations for
            limit (int): Maximum number of recommendations to return
            
        Returns:
            list: List of dictionaries containing recommendation details
        """
        query = '''
        MATCH (target:User {name:$username})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
        WHERE target <> similarUser
        MATCH (similarUser)-[:PURCHASED]->(rec:Product)
        WHERE NOT (target)-[:PURCHASED]->(rec)
        RETURN rec.name AS product, 
               COUNT(*) AS score,
               COLLECT(DISTINCT similarUser.name) AS recommendedBy
        ORDER BY score DESC
        LIMIT $limit
        '''
        
        with self.driver.session() as session:
            result = session.run(query, username=username, limit=limit)
            recommendations = []
            for record in result:
                recommendations.append({
                    'product': record['product'],
                    'score': record['score'],
                    'recommended_by': record['recommendedBy']
                })
            return recommendations

    def get_user_purchases(self, username):
        """
        Get a user's purchase history
        
        Args:
            username (str): Name of the user
            
        Returns:
            list: List of purchased products
        """
        query = '''
        MATCH (u:User {name:$username})-[:PURCHASED]->(p:Product)
        RETURN COLLECT(p.name) AS products
        '''
        
        with self.driver.session() as session:
            result = session.run(query, username=username)
            record = result.single()
            return record['products'] if record else []

    def find_similar_users(self, username):
        """
        Find users similar to the given user based on shared purchases
        
        Args:
            username (str): Name of the user
            
        Returns:
            list: List of similar users with shared products
        """
        query = '''
        MATCH (target:User {name:$username})-[:PURCHASED]->(commonProduct:Product)<-[:PURCHASED]-(similarUser:User)
        WHERE target <> similarUser
        RETURN similarUser.name AS user,
               COLLECT(commonProduct.name) AS sharedProducts,
               SIZE(COLLECT(commonProduct.name)) AS sharedCount
        ORDER BY sharedCount DESC
        '''
        
        with self.driver.session() as session:
            result = session.run(query, username=username)
            similar_users = []
            for record in result:
                similar_users.append({
                    'user': record['user'],
                    'shared_products': record['sharedProducts'],
                    'shared_count': record['sharedCount']
                })
            return similar_users

    def get_popular_products(self, limit=10):
        """
        Get most popular products across all users
        
        Args:
            limit (int): Maximum number of products to return
            
        Returns:
            list: List of popular products with purchase counts
        """
        query = '''
        MATCH (u:User)-[:PURCHASED]->(p:Product)
        RETURN p.name AS product, COUNT(u) AS purchaseCount
        ORDER BY purchaseCount DESC
        LIMIT $limit
        '''
        
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            popular_products = []
            for record in result:
                popular_products.append({
                    'product': record['product'],
                    'purchase_count': record['purchaseCount']
                })
            return popular_products


def main():
    """Main function to demonstrate the recommendation system"""
    app = RecommendationApp(URI, AUTH)
    
    try:
        # Setup sample data
        print("Setting up sample data...")
        app.setup_data()
        
        # Test user
        username = "Alice"
        
        # Get user's current purchases
        purchases = app.get_user_purchases(username)
        print(f"\n{username}'s current purchases: {purchases}")
        
        # Get recommendations
        recommendations = app.get_recommendations(username)
        print(f"\nRecommendations for {username}:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['product']} (Score: {rec['score']}, Recommended by: {rec['recommended_by']})")
        
        # Find similar users
        similar_users = app.find_similar_users(username)
        print(f"\nUsers similar to {username}:")
        for user in similar_users:
            print(f"- {user['user']}: {user['shared_count']} shared products {user['shared_products']}")
        
        # Get popular products
        popular = app.get_popular_products(5)
        print(f"\nMost popular products:")
        for product in popular:
            print(f"- {product['product']}: {product['purchase_count']} purchases")
            
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        app.close()


if __name__ == "__main__":
    main()