import requests

def send(endpoint: str, cmd: dict) -> requests.Response:
    """
    """
    headers = {
        "Content-Type": "application/json"
    }

    return requests.post(endpoint, json=cmd, headers=headers, verify=False)
