// Experiment 2: Create a social network in Neo4j

// Create five people and four friendship relationships
CREATE (alice:Person {name:'Alice', age:21, city:'Nagercoil'}),
       (bob:Person {name:'Bob', age:22, city:'Chennai'}),
       (carol:Person {name:'Carol', age:20, city:'Madurai'}),
       (david:Person {name:'David', age:23, city:'Kanyakumari'}),
       (eve:Person {name:'Eve', age:21, city:'Tirunelveli'}),
       (alice)-[:FRIENDS_WITH {since:2020}]->(bob),
       (bob)-[:FRIENDS_WITH {since:2021}]->(carol),
       (carol)-[:FRIENDS_WITH {since:2022}]->(david),
       (alice)-[:FRIENDS_WITH {since:2023}]->(eve);

// Display the whole graph
MATCH (n) RETURN n;

// List all users
MATCH (p:Person)
RETURN p.name AS name, p.age AS age, p.city AS city;

// List all friendships
MATCH (a:Person)-[r:FRIENDS_WITH]->(b:Person)
RETURN a.name AS person, b.name AS friend, r.since AS since;
