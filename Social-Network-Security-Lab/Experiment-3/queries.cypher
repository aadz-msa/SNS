// Experiment 3: Read and write data in Neo4j

// CREATE: add Frank
CREATE (:Person {name:'Frank', age:22, city:'Chennai'});

// SET: update Frank's age
MATCH (p:Person {name:'Frank'})
SET p.age = 23;

// READ: display Frank
MATCH (p:Person {name:'Frank'})
RETURN p.name, p.age, p.city;

// CREATE: connect Eve and Frank
MATCH (a:Person {name:'Eve'}), (f:Person {name:'Frank'})
CREATE (a)-[:FRIENDS_WITH {since:2025}]->(f);

// READ: display all people
MATCH (p:Person)
RETURN p.name AS name, p.age AS age
ORDER BY name;

// DELETE: delete Frank and his relationships
MATCH (p:Person {name:'Frank'})
DETACH DELETE p;
