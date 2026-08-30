from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from syncsphere.main import app
from syncsphere.tasks.documents import TaskDocument, TaskAutomation
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from syncsphere.main import app
from syncsphere.tasks.documents import TaskDocument, TaskAutomation

client = TestClient(app)



def test_tasks_ai_planning_flow(mock_task_coll, mock_slack_coll):
    # Register/Login
    register_payload = {
        "email": "aiadmin@acme.ai",
        "password": "supersecretpassword123!",
        "first_name": "AI",
        "last_name": "User",
        "org_name": "AI Corp",
        "org_slug": "ai-corp"
    }
    client.post("/v1/auth/register", json=register_payload)
    
    resp_login = client.post("/v1/auth/login", json={
        "email": "aiadmin@acme.ai",
        "password": "supersecretpassword123!"
    })
    access_token = resp_login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test /plan-with-ai endpoint
    from syncsphere.ai.domain.value_objects import StructuredOutputResult
    from syncsphere.core.dependency_injection.container import container

    mock_parsed_str = (
        '{"task": {"title": "Draft Gmail", "description": "Draft client email", "assigned_to": "Alice", "priority": "High", "status": "Pending"},'
        ' "integrations": [{"action": "gmail.send_email", "selected": true, "config": {"to": "bob@gmail.com", "subject": "Hi", "body": "Hello"}}]}'
    )

    async def mock_structured_output(*args, **kwargs):
        return StructuredOutputResult(
            success=True,
            raw_output=mock_parsed_str
        )

    # Patch structured output
    container.ai_gateway.structured_output = mock_structured_output

    plan_payload = {"prompt": "Write email to Bob and manually review output"}
    resp_plan = client.post("/v1/tasks/plan-with-ai", json=plan_payload, headers=headers)

    assert resp_plan.status_code == 200

    planned_tasks = resp_plan.json()["data"]

    assert planned_tasks["task"]["title"] == "Draft Gmail"

    # The planner creates the Gmail action plus an approval step
    # because the prompt explicitly requests manual review.
    assert len(planned_tasks["integrations"]) == 2

    actions = [item["action"] for item in planned_tasks["integrations"]]

    assert "gmail.send_email" in actions
    assert "system.approval" in actions

    # Test /confirm-plan endpoint
    mock_task = TaskDocument(
        id="60c72b2f9b1d8e2b8c8b4000",
        org_id="test-org",
        title="Draft Gmail",
        description="Draft client email",
        assigned_to="Alice",
        priority="High",
        status="Pending",
        due_date="2026-08-01",
        automation=TaskAutomation(
            action="gmail.send_email",
            config={"to": "bob@gmail.com", "subject": "Hi", "body": "Hello"},
            status="pending"
        )
    )

    confirm_payload = {
        "tasks": [
            {
                "title": "Draft Gmail",
                "description": "Draft client email",
                "assigned_to": "Alice",
                "priority": "High",
                "status": "Pending",
                "automation": {
                    "action": "gmail.send_email",
                    "config": {"to": "bob@gmail.com", "subject": "Hi", "body": "Hello"}
                }
            }
        ]
    }

    with patch("syncsphere.tasks.documents.TaskDocument.insert", new_callable=AsyncMock) as mock_insert, \
     patch("syncsphere.tasks.documents.TaskDocument.find_one", new_callable=AsyncMock) as mock_find_one, \
     patch("syncsphere.tasks.documents.TaskDocument.save", new_callable=AsyncMock) as mock_save, \
     patch("syncsphere.tasks.documents.TaskDocument.get_motor_collection", create=True), \
     patch("syncsphere.tasks.documents.SlackTokenDocument.get_motor_collection", create=True), \
     patch("syncsphere.workflow.application.action_registry.ACTION_REGISTRY") as mock_action_registry:
         
         mock_insert.return_value = mock_task
         mock_find_one.return_value = mock_task
         mock_save.return_value = mock_task

         mock_gmail_fn = AsyncMock(return_value={"status": "sent"})
         mock_action_registry.get.return_value = mock_gmail_fn
         
         with patch("syncsphere.workflow.application.action_registry.get_action", return_value=mock_gmail_fn), \
              patch("syncsphere.connectors.application.google_token_service.get_valid_google_token", new_callable=AsyncMock) as mock_google_token:
             mock_google_token.return_value = "fake_token"
             
             resp_confirm = client.post("/v1/tasks/confirm-plan", json=confirm_payload, headers=headers)
             assert resp_confirm.status_code == 201
             # confirm_plan kicks off async background execution, wait for it natively or mock_gmail_fn could be called 0 times here in tests depending on event loop.
             # but we'll test the manual endpoint where it's synchronous.

             resp_exec = client.post("/v1/tasks/60c72b2f9b1d8e2b8c8b4000/execute-automation", headers=headers)
             assert resp_exec.status_code == 200
             # Due to BackgroundTasks in confirm-plan, we only guarantee execute_automation's call.
             assert mock_gmail_fn.call_count >= 1
             mock_gmail_fn.assert_called_with(to="bob@gmail.com", subject="Hi", body="Hello", organization_id=mock_task.org_id, user_id=mock_task.created_by_user_id)

def test_tasks_ai_validation_blocked(mock_task_coll):
    # Test Preflight Blocking
    client.post("/v1/auth/register", json={
        "email": "testblocked@acme.ai", "password": "supersecretpassword123!",
        "first_name": "Block", "last_name": "User", "org_name": "AI Corp", "org_slug": "ai-corp2"
    })
    
    resp_login = client.post("/v1/auth/login", json={"email": "testblocked@acme.ai", "password": "supersecretpassword123!"})
    headers = {"Authorization": f"Bearer {resp_login.json()['data']['access_token']}"}

    confirm_payload = {
        "tasks": [{
            "title": "Draft Failed", "description": "Failed email", "assigned_to": "Alice", "priority": "High", "status": "Pending",
            "automations": [
                {"action": "gmail.send_email", "config": {"to": "bob@gmail.com"}},
                {"action": "slack.send_message", "config": {"slack_workspace": "foo"}}
            ]
        }]
    }

    # First test: Both missing
    resp = client.post("/v1/tasks/confirm-plan", json=confirm_payload, headers=headers)
    assert resp.status_code == 403
    err_data = resp.json()["detail"]
    assert err_data["status"] == "authorization_required"
    
    connections = err_data["missing_connections"]
    assert len(connections) == 2
    
    g_conn = next(c for c in connections if c["identifier"] == "google")
    assert g_conn["action_required"] == "connect"
    assert g_conn["connection_status"] == "disconnected"
    
    s_conn = next(c for c in connections if c["identifier"] == "slack")
    assert s_conn["action_required"] == "connect"

    # Second test: Expired Google
    from syncsphere.connectors.application.exceptions import OAuthError
    with patch("syncsphere.connectors.application.google_token_service.get_valid_google_token", side_effect=OAuthError("Token expired and refresh failed. Please reconnect Google")):
        confirm_payload_google_only = {"tasks": [{
            "title": "Draft Failed", "description": "Failed email", "assigned_to": "Alice", "priority": "High", "status": "Pending",
            "automations": [{"action": "gmail.send_email", "config": {"to": "bob@gmail.com"}}]
        }]}
        resp = client.post("/v1/tasks/confirm-plan", json=confirm_payload_google_only, headers=headers)
        assert resp.status_code == 403
        data = resp.json()
        conn = data["detail"]["missing_connections"][0]
        assert conn["action_required"] == "reconnect"
        assert conn["connection_status"] == "expired"
