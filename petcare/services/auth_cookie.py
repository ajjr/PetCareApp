import hashlib
from typing import Optional

from flask import Response
from flask import Request

auth_cookie_name = "petcare_user"


def set_auth(response: Response, user_id: int):
    hash_val = _hash_text(str(user_id))
    response.set_cookie(auth_cookie_name, f"{user_id}:{hash_val}",
                        secure=False, httponly=True, samesite='Lax')


def _hash_text(text: str) -> str:
    text = "salt_" + text + "_text"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def get_auth(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None

    val = request.cookies[auth_cookie_name]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]

    if hash_val != _hash_text(user_id):
        return None

    return int(user_id)


def logout(response: Response):
    response.delete_cookie(auth_cookie_name)
