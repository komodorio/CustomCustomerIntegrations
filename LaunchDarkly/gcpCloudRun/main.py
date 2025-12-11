import json
import os
import urllib3

KOMODOR_API_KEY = os.environ.get(
    "KOMODOR_API_KEY",
    "<Komodor API Key Here>",
)

KOMODOR_API_URL = "https://api.komodor.com/mgmt/v1/events"

http = urllib3.PoolManager()


def darkly_to_komodor(request):
    print("Received request from LaunchDarkly")

    # Outer body (what Cloud Run receives)
    outer = request.get_json(silent=True) or {}
    print(f"Outer body: {outer}")

    # LD puts the real payload as a JSON string in "body"
    ld_payload = outer
    if "body" in outer:
        inner = outer.get("body")
        if isinstance(inner, str):
            try:
                ld_payload = json.loads(inner)
            except Exception as e:
                print(f"Failed to parse inner body JSON: {e}")
                ld_payload = {}
        elif isinstance(inner, dict):
            ld_payload = inner

    print(f"LD payload: {ld_payload}")

    # Now work off the real LD payload
    event_type = ld_payload.get("Event") or ld_payload.get("event") or "launchdarkly-alert"

    komodor_event = {
        "eventType": event_type,
        "summary": ld_payload.get("AlertName", "LaunchDarkly Alert"),
        "scope": {
            "clusters": [],
            "servicesNames": [],
            "namespaces": []
        },
        "severity": "information",
        "details": ld_payload,  # dump LD payload into details
    }

    encoded = json.dumps(komodor_event).encode("utf-8")

    try:
        resp = http.request(
            "POST",
            KOMODOR_API_URL,
            body=encoded,
            headers={
                "x-api-key": KOMODOR_API_KEY,
                "Content-Type": "application/json",
            },
        )
    except Exception as e:
        print(f"Error calling Komodor: {e}")
        return (
            json.dumps({"error": "Failed to call Komodor", "details": str(e)}),
            500,
            {"Content-Type": "application/json"},
        )

    return (
        json.dumps({
            "statusCode": resp.status,
            "body": resp.data.decode("utf-8"),
        }),
        resp.status,
        {"Content-Type": "application/json"},
    )


