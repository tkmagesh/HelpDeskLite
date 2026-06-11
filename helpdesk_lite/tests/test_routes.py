def test_dashboard_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_create_user_route(client):
    response = client.post(
        "/users/new",
        data={"name": "Katherine Johnson", "email": "kj@example.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Katherine Johnson" in response.data


def test_create_issue_route(client):
    response = client.post(
        "/issues/new",
        data={
            "title": "Keyboard missing",
            "description": "No keyboard at desk 42.",
            "reporter_name": "Pat",
            "priority": "medium",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Keyboard missing" in response.data


def test_issue_list_route_searches(client):
    client.post(
        "/issues/new",
        data={
            "title": "VPN outage",
            "description": "VPN is down.",
            "reporter_name": "Pat",
            "priority": "high",
        },
    )

    response = client.get("/issues/?q=VPN")

    assert response.status_code == 200
    assert b"VPN outage" in response.data


def test_add_comment_route(client):
    create_response = client.post(
        "/issues/new",
        data={
            "title": "Mouse issue",
            "description": "Mouse scroll wheel sticks.",
            "reporter_name": "Pat",
            "priority": "low",
        },
        follow_redirects=False,
    )
    issue_location = create_response.headers["Location"]
    issue_id = issue_location.rstrip("/").split("/")[-1]

    response = client.post(
        f"/issues/{issue_id}/comments",
        data={"author_name": "Pat", "body": "Adding more context."},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Adding more context." in response.data
