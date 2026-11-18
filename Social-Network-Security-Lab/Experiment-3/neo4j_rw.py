# Experiment 3: Read and write using the Neo4j Python driver
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"  # Replace with your Neo4j database password

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def add_person(tx, name, age, city):
    tx.run(
        "MERGE (p:Person {name:$name}) SET p.age=$age, p.city=$city",
        name=name, age=age, city=city
    )


def add_friend(tx, a, b, since):
    tx.run(
        "MATCH (x:Person {name:$a}), (y:Person {name:$b}) "
        "MERGE (x)-[r:FRIENDS_WITH]->(y) SET r.since=$since",
        a=a, b=b, since=since
    )


def get_friends(tx, name):
    result = tx.run(
        "MATCH (:Person {name:$name})-[:FRIENDS_WITH]-(f) "
        "RETURN f.name AS friend ORDER BY friend",
        name=name
    )
    return [record["friend"] for record in result]


with driver.session() as session:
    session.execute_write(add_person, "Frank", 22, "Chennai")
    session.execute_write(add_friend, "Eve", "Frank", 2025)

    print("Frank added and linked with Eve")
    print("Friends of Alice:", session.execute_read(get_friends, "Alice"))
    print("Friends of Eve :", session.execute_read(get_friends, "Eve"))

driver.close()
