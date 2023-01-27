from typing import Any
from msal import ConfidentialClientApplication
import requests

CLIENT_ID = '<CLIENT_ID>'
CLIENT_SECRET = '<CLIENT_SECRET>'
DEVICE_ID = '<DEVICE_ID>'
base_url = "https://external.xolta.com"


def get_headers():
    clientId = CLIENT_ID
    clientSecret = CLIENT_SECRET
    scope = ["https://Xolta.onmicrosoft.com/TelemetryAPI/.default"]
    authority = "https://login.microsoftonline.com/145c2c43-a8da-46ab-b5da-1d4de444ed82"
    app = ConfidentialClientApplication(
        clientId, authority=authority, client_credential=clientSecret)
    result = app.acquire_token_silent(scope, account=None)
    if not result:
        result = app.acquire_token_for_client(scope)
    token = result["access_token"]

    return {'Authorization': 'Bearer ' + token}


def get_status():
    response = requests.get(f"{base_url}/api/deviceStatus", headers=get_headers())
    return response.json()


def _go_to_command(command, payload: Any = ""):
    response = requests.post(f"{base_url}/api/SendStateModeCommand",
                             json={"DeviceId": DEVICE_ID, "CommandName": command, "Payload": payload},
                             headers=get_headers())
    return response.json()


def go_to_running():
    return _go_to_command("GoToState_Running")


def go_to_idling():
    return _go_to_command("GoToState_Idling")


def go_to_maxself():
    return _go_to_command("GoToMode_SelfConsumption")


def send_power(time, power):
    return _go_to_command("GoToMode_ExternalControl",
                          {'setPoint': {'1': {'utcTime': time, "batteryActivePower": power}}})


if __name__ == '__main__':

    print(get_status())
