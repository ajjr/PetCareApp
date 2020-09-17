import petcare.models.db_session as db
from petcare.models.user import User


def get_user(uid: str) -> object:
    """

    @rtype: petcare.models.User
    """
    return db.get_db_obj(uid, User)
