import json
import os
import urllib3

http = urllib3.PoolManager()

#ReadMe This function ingests a Launch Darkly notification via webhook, translates it into readable fashion by Komodor and sends it to the Komodor Events tab
#Requirements: Create a lambda with the below functions
#Create a lambda function URL to give to Launch Darkly https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html#create-url-console
#Feed that to Launch Darkly to send a webhook to it when events trigger
#Insert your own Komodor API key as a value on line 14 or as a value from vault or other source


KOMODOR_API_KEY = "f11f4ed1-b9c2-4dc2-983c-4f0be53bc98c"
KOMODOR_API_URL = "https://api.komodor.com/mgmt/v1/events"

def lambda_handler(event, context):

    console.log("Received event: " + json.dumps(event))
    # LaunchDarkly sends the payload in the raw body
    body = json.loads(event.get("body", "{}"))

    # Prefer Event/event from LD, fall back to default
    event_type = body.get("Event") or body.get("event") or "launchdarkly-alert"

    # Map webhook fields → Komodor event
    komodor_event = {
        "eventType": event_type,
        "summary": body.get("AlertName", "LaunchDarkly Alert"),
         "scope": {
            "clusters": [],
            "servicesNames": [],
            "namespaces": []
        },
        "severity": "information",
        "details": body  # dump entire payload as-is
    }

    encoded = json.dumps(komodor_event).encode("utf-8")

    # Send to Komodor
    resp = http.request(
        "POST",
        KOMODOR_API_URL,
        body=encoded,
        headers={
            "Content-Type": "application/json",
            "x-api-key": KOMODOR_API_KEY
        }
    )

    return {
        "statusCode": resp.status,
        "body": resp.data.decode("utf-8")
    }


