import requests


def punch_in():
    return
    try:
        response = requests.post(
            "",
            json={"from": "mnma", "version": "v3.9.9"},
            headers={"Content-Type": "application/json"},
            timeout=3,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return e
