from neo4j import GraphDatabase

# Replace with your Aura credentials
URI = "neo4j+s://<your-database-id>.databases.neo4j.io"
AUTH = ("neo4j", "<password>")

class RecommendationApp:

    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def recommend(self, username):
        query = '''
        MATCH (u:User {name:$username})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(other:User)-[:PURCHASED]->(rec:Product)
        WHERE NOT (u)-[:PURCHASED]->(rec)
        RETURN rec.name AS product, COUNT(*) AS score
        ORDER BY score DESC
        LIMIT 5
        '''
        with self.driver.session() as session:
            result = session.run(query, username=username)
            return [record["product"] for record in result]

if __name__ == "__main__":
    app = RecommendationApp(URI, AUTH)
    recs = app.recommend("Alice")
    print("Recommendations for Alice:", recs)
    app.close()
