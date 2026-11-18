# Experiment 1: Secure Social Media Application (Flask + SQLite)
import sqlite3
from flask import Flask, request, session, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret"
DB = "social.db"


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    connection = g.pop("db", None)
    if connection:
        connection.close()


def init_db():
    connection = sqlite3.connect(DB)
    connection.executescript("""
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS posts;
    DROP TABLE IF EXISTS follows;

    CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        pwd TEXT
    );

    CREATE TABLE posts(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        body TEXT,
        visibility TEXT DEFAULT 'public'
    );

    CREATE TABLE follows(
        follower INTEGER,
        followee INTEGER
    );
    """)
    connection.commit()
    connection.close()


@app.post("/register")
def register():
    username = request.form["username"]
    password = request.form["password"]

    if len(password) < 8:
        return jsonify(error="password too short"), 400

    try:
        db().execute(
            "INSERT INTO users(username, pwd) VALUES(?, ?)",
            (username, generate_password_hash(password))
        )
        db().commit()
    except sqlite3.IntegrityError:
        return jsonify(error="username taken"), 409

    return jsonify(msg="registered")


@app.post("/login")
def login():
    user = db().execute(
        "SELECT * FROM users WHERE username=?",
        (request.form["username"],)
    ).fetchone()

    if user and check_password_hash(user["pwd"], request.form["password"]):
        session["uid"] = user["id"]
        return jsonify(msg="login ok")

    return jsonify(error="invalid credentials"), 401


@app.post("/post")
def create_post():
    if "uid" not in session:
        return jsonify(error="login required"), 401

    db().execute(
        "INSERT INTO posts(user_id, body, visibility) VALUES(?, ?, ?)",
        (
            session["uid"],
            request.form["body"],
            request.form.get("visibility", "public")
        )
    )
    db().commit()
    return jsonify(msg="posted")


@app.post("/follow/<int:uid>")
def follow(uid):
    if "uid" not in session:
        return jsonify(error="login required"), 401

    db().execute(
        "INSERT INTO follows VALUES(?, ?)",
        (session["uid"], uid)
    )
    db().commit()
    return jsonify(msg="following")


@app.get("/feed")
def feed():
    if "uid" not in session:
        return jsonify(error="login required"), 401

    rows = db().execute("""
        SELECT u.username, p.body, p.visibility
        FROM posts p JOIN users u ON u.id = p.user_id
        WHERE p.user_id = ?
           OR p.visibility = 'public'
           OR (p.visibility = 'followers'
               AND p.user_id IN (
                   SELECT followee FROM follows WHERE follower = ?
               ))
    """, (session["uid"], session["uid"])).fetchall()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
