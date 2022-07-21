import time
import uuid



query_database = {
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
                    "database": {
                        "database": "system",
                        "table": "os_version"
                    }
                }
            }
        }
    }
}

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


query_sbom = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {

                "target": {
                    "sbom": {}
                     }
            }
        }
    }
}

deny_ipv4_connection = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {
                "action": "deny",
                "target": {
                    "ipv4_connection": {}
                     }
            }
        }
    }
}