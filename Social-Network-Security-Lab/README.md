# Social Network Security Lab

Shortened, organised programs based on the six experiments in the Social Network Security Lab Record.

## Experiments

1. **Experiment 1 – Social Media Application**: Flask + SQLite. Run `app.py` to start the app; run `test_app.py` to test the routes.
2. **Experiment 2 – Network Model using Neo4j**: Run `network.cypher` in Neo4j Browser.
3. **Experiment 3 – Read and Write Graph Database**: Run `queries.cypher` in Neo4j Browser. `neo4j_rw.py` demonstrates the Python driver.
4. **Experiment 4 – Friend of Friends**: Run `friend_of_friends.cypher` in Neo4j Browser.
5. **Experiment 5 – Secure Search**: Run `secure_search.py`.
6. **Experiment 6 – Security and Privacy Detector**: Run `detector.py`.

## Python dependencies

```bash
pip install flask werkzeug neo4j
```

Experiments 2–4 require a running Neo4j database. For Experiment 3, update the Neo4j password in `neo4j_rw.py`.

**Important:** These are lab/practice examples. The hard-coded Flask secret key and sample Neo4j password must be replaced for real applications. Experiment 1's `init_db()` resets the three SQLite tables each time `app.py` starts, so it is intended for demonstration, not production.
