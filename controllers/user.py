from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt

def create_user(username: str, password: str, db) -> None:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.execute(
        text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)"),
        {"username": username, "password_hash": password_hash}
    )
    db.commit()


def login_user(username: str, password: str, db) -> tuple:
    result = db.execute(
        text("SELECT username, password_hash FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()

    # Same error for both cases — don't reveal which one failed
    if not result:
        return (False, "Invalid username or password")

    if not bcrypt.checkpw(password.encode(), result[1].encode()):
        return (False, "Invalid username or password")

    return (True, "Login successful")