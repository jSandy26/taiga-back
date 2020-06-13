import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError
from taiga.projects.models import Project, TaskStatus


slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)


def send_slack_notification(request, obj):
    try:
        old_status = obj.status
        new_status_id = request.DATA.get('status', None)
        new_status = TaskStatus.objects.get(pk=new_status_id)
        task_id = obj.ref
        task_name = obj.subject

        response = client.chat_postMessage(
            channel="U015GFCDKBN",
            text=f"status for the task {task_id} - {task_name} changed from {old_status.name} to {new_status.name}"
            # text="hello there"
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'