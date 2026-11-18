# Experiment 5: Secure search in social media
import sqlite3
import re

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    bio TEXT,
    searchable INTEGER,
    pwd TEXT
);

INSERT INTO users VALUES
(1, 'alice', 'Loves hiking', 1, 'hash_a'),
(2, 'alan', 'Photographer', 1, 'hash_b'),
(3, 'albert', 'Private account', 0, 'hash_c'),
(4, 'bob', 'Chess player', 1, 'hash_d');
""")


def insecure_search(term):
    # Vulnerable: SQL is built by joining user input into the query.
    query = (
        "SELECT username, bio FROM users "
        "WHERE searchable=1 AND username LIKE '%" + term + "%'"
    )
    return con.execute(query).fetchall()


def sanitize(term):
    term = term.strip()[:30]
    if not re.fullmatch(r"[A-Za-z0-9_ .-]*", term):
        raise ValueError("invalid characters in search term")
    return term


def secure_search(term):
    term = sanitize(term)
    query = (
        "SELECT username, bio FROM users "
        "WHERE searchable=1 AND username LIKE ?"
    )
    return con.execute(query, ("%" + term + "%",)).fetchall()


attack = "zzz' OR '1'='1' --"

print("Normal search 'al' ->", secure_search("al"))
print("\n[INSECURE] attack ->", insecure_search(attack))

try:
    print("[SECURE] attack ->", secure_search(attack))
except ValueError as error:
    print("[SECURE] attack -> blocked:", error)

union_attack = "x' UNION SELECT username, pwd FROM users --"
print("\nUnion attack (insecure) ->", insecure_search(union_attack))

try:
    secure_search(union_attack)
except ValueError as error:
    print("Union attack (secure) -> blocked:", error)

visible = any(
    username == "albert" for username, bio in secure_search("albert")
)
print("\nPrivate user 'albert' visible in secure search?", visible)
