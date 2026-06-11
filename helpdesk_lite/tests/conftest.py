import pytest

from helpdesk_lite.app import create_app
from helpdesk_lite.config import TestConfig
from helpdesk_lite.database import db


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_user(app):
    from helpdesk_lite.services.user_service import UserService

    user, errors = UserService().create_user("Ada Lovelace", "ada@example.com")
    assert errors == []
    return user


@pytest.fixture()
def sample_issue(app):
    from helpdesk_lite.services.issue_service import IssueService

    issue, errors = IssueService().create_issue(
        "Printer is jammed", "The third floor printer is jammed.", "Grace", "high"
    )
    assert errors == []
    return issue
