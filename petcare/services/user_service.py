from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt as crypto

import petcare.models.db_session as db
from petcare.models.user import User

CRYPTO_ROUNDS = 200000


def get_user(user_id: str) -> User:
    return db.get_db_obj(user_id, User)


def get_user_by_username_or_email(username: str, email: str) -> Optional[User]:
    session = db.create_session()
    return session.query(User).filter(User.username == username).first() \
           or session.query(User).filter(User.email == email).first()


def authenticate(username: str, password: str) -> Optional[User]:
    session = db.create_session()

    user = session.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not crypto.verify(password, user.password):
        return None

    return user


def create_user(username: str, name: str, email: str, password: str) -> Optional[User]:
    if get_user_by_username_or_email(username, email):
        return None

    user = User()
    user.username = username
    user.email = email
    user.name = name
    user.password = crypto.encrypt(password, rounds=CRYPTO_ROUNDS)

    session = db.create_session()
    session.add(user)
    session.commit()

    return user
