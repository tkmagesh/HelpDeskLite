from sqlalchemy.exc import IntegrityError

from helpdesk_lite.database import db
from helpdesk_lite.models import User
from helpdesk_lite.validators import validate_user_payload


class UserService:
    def create_user(self, name, email):
        errors = validate_user_payload(name, email)
        if errors:
            return None, errors

        user = User(name=name.strip(), email=email.strip())
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None, ["A user with that email already exists."]

        return user, []

    def list_users(self):
        # TODO pagination: this loads every user, which is fine for training data.
        return User.query.order_by(User.name.asc()).all()

    def get_user(self, user_id):
        if not user_id:
            return None
        return db.session.get(User, int(user_id))

    def count_users(self):
        return User.query.count()
