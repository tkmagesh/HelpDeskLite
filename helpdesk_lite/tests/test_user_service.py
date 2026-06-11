from helpdesk_lite.services.user_service import UserService


def test_create_user_success(app):
    service = UserService()

    user, errors = service.create_user("Grace Hopper", "grace@example.com")

    assert errors == []
    assert user.id is not None
    assert user.name == "Grace Hopper"


def test_create_user_requires_email(app):
    service = UserService()

    user, errors = service.create_user("No Email", "")

    assert user is None
    assert "A valid email is required." in errors


def test_duplicate_email_is_rejected(app):
    service = UserService()
    service.create_user("First", "same@example.com")

    user, errors = service.create_user("Second", "same@example.com")

    assert user is None
    assert errors == ["A user with that email already exists."]


def test_list_users_orders_by_name(app):
    service = UserService()
    service.create_user("Zoe", "zoe@example.com")
    service.create_user("Anna", "anna@example.com")

    users = service.list_users()

    assert [user.name for user in users] == ["Anna", "Zoe"]
