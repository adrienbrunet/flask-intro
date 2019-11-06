from app import db
import json
from ..models import Task
from .factories import TaskFactory


def test_tasks_list(app, client, db_session):
    task = TaskFactory()
    db_session.commit()

    response = client.get("/tasks/")
    assert len(response.json) > 0


def test_tasks_create(app, client, db_session):
    title = "my_test"
    # Ensure no task persist with this title
    Task.query.filter_by(title=title).delete()
    data = json.dumps({"title": "my_test"})
    response = client.post("/tasks/", data=data, content_type="application/json")
    assert response.status_code == 201

    response = client.post("/tasks/", data=data, content_type="application/json")
    assert response.status_code == 400


def test_tasks_get_one(app, client, db_session):
    task = TaskFactory()
    db_session.commit()
    task = Task.query.filter_by(title=task.title).first()
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200


def test_tasks_update_one(app, client, db_session):
    new_title = "new_title"
    # Ensure no task persist with this title
    Task.query.filter_by(title=new_title).delete()

    task = TaskFactory()
    db_session.commit()
    task = Task.query.filter_by(title=task.title).first()
    response = client.put(f"/tasks/{task.id}", data=json.dumps({"title": new_title}))
    assert response.status_code == 200

    Task.query.filter_by(title="already_existing").delete()
    old_task = TaskFactory(title="already_existing")
    response = client.put(
        f"/tasks/{task.id}", data=json.dumps({"title": "already_existing"})
    )
    assert response.status_code == 400


def test_tasks_delete_one(app, client, db_session):
    task = TaskFactory()
    db_session.commit()

    task = Task.query.filter_by(title=task.title).first()
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
