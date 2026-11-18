# Experiment 1: Test the Social Media Application
import app
import sqlite3

app.init_db()


def client():
    return app.app.test_client()


alice = client()
bob = client()
carol = client()

print("REGISTER alice :", alice.post(
    "/register", data=dict(username="alice", password="alice@1234")
).get_json())

print("REGISTER bob   :", bob.post(
    "/register", data=dict(username="bob", password="bob@12345")
).get_json())

print("REGISTER carol :", carol.post(
    "/register", data=dict(username="carol", password="123")
).get_json())

print("DUPLICATE alice:", client().post(
    "/register", data=dict(username="alice", password="alice@1234")
).get_json())

print("LOGIN wrong pwd:", client().post(
    "/login", data=dict(username="alice", password="x")
).get_json())

print("LOGIN alice    :", alice.post(
    "/login", data=dict(username="alice", password="alice@1234")
).get_json())

print("LOGIN bob      :", bob.post(
    "/login", data=dict(username="bob", password="bob@12345")
).get_json())

print("POST public    :", alice.post(
    "/post", data=dict(body="Hello world", visibility="public")
).get_json())

print("POST followers :", alice.post(
    "/post", data=dict(body="Family photos", visibility="followers")
).get_json())

print("POST private   :", alice.post(
    "/post", data=dict(body="My diary", visibility="private")
).get_json())

print("FEED bob (not following):",
      [p["body"] for p in bob.get("/feed").get_json()])

print("BOB follows alice:", bob.post("/follow/1").get_json())

print("FEED bob (following):",
      [p["body"] for p in bob.get("/feed").get_json()])

print("FEED alice (owner):",
      [p["body"] for p in alice.get("/feed").get_json()])

print("FEED anonymous:", client().get("/feed").get_json())

password_hash = sqlite3.connect("social.db").execute(
    "SELECT pwd FROM users WHERE id=1"
).fetchone()[0]
print("STORED PASSWORD:", password_hash[:45] + "...")
