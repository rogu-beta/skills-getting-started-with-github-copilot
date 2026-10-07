def test_student_can_unregister_from_activity(client):
    email = "michael@mergington.edu"

    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregistering_unknown_participant_returns_not_found(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_student_can_sign_up_again_after_unregistering(client):
    email = "michael@mergington.edu"

    client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }