import time
import uuid

query_features = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {
                "action": "query",
                "target": {
                    "features": ["profiles"]
                }
            }
        }
    }
}

query_features_silent = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {
                "action": "query",
                "target": {
                    "features": ["profiles"]
                },
                "args": {
                    "response_requested" : "none"
                }
            }
        }
    }
}




set_account_status_enabled = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {
                "action": "set",
                "target": {
                    "account": {
                        "uid" : "S-1-5-21-7375663-6890924511-1272660413-2944159"
                        }
                },
                "args": {
                    "account_status" : "enabled",
                    "response_requested": "status"
                },
                "actuator": {
                    "er": {}
                }
            }
        }
    }
}