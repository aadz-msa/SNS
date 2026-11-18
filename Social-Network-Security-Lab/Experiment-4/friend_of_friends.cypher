// Experiment 4: Find friends of friends in Neo4j

// Friend of Friends of Alice
MATCH (me:Person {name:'Alice'})-[:FRIENDS_WITH]-(f:Person)
      -[:FRIENDS_WITH]-(fof:Person)
WHERE fof <> me
  AND NOT (me)-[:FRIENDS_WITH]-(fof)
RETURN fof.name AS suggestion,
       collect(DISTINCT f.name) AS through_mutual_friend;

// Friend of Friends of Bob
MATCH (me:Person {name:'Bob'})-[:FRIENDS_WITH]-(f:Person)
      -[:FRIENDS_WITH]-(fof:Person)
WHERE fof <> me
  AND NOT (me)-[:FRIENDS_WITH]-(fof)
RETURN fof.name AS suggestion,
       collect(DISTINCT f.name) AS through_mutual_friend;

// Variable-length path version: exactly two hops
MATCH (me:Person {name:'Alice'})-[:FRIENDS_WITH*2]-(fof:Person)
WHERE fof <> me
  AND NOT (me)-[:FRIENDS_WITH]-(fof)
RETURN DISTINCT fof.name AS suggestion;
