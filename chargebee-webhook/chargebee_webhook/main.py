import os
import json
from oep_core.aws import add_to_queue
from oep_core.http_codes import HTTP_OK

CHARGEBEE_WEBHOOK_QUEUE = os.environ.get('CHARGEBEE_WEBHOOK_QUEUE')


def handler(event, context):
    """
    We forward all messages to SQS and return 200 to Chargebee. If they get enough failed webhook
    responses, they will disable sending them. This keeps the webhooks coming and we have access to
    any payload after the fact if we need to manually process something after a failure later in the
    pipeline.
    """
    print(f'Context: {context}')
    print(f'Event: {event}')
    try:
        request = event.get('body')
        body = json.loads(request)
        add_to_queue(CHARGEBEE_WEBHOOK_QUEUE, body)
    except Exception as exc:
        print(f"Something unexpected went wrong: {exc}")
    finally:
        return dict(statusCode=HTTP_OK)
