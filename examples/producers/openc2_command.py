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


query_sbom = {
    "headers": {
        "request_id": str(uuid.uuid4()),
        "created": round(time.time() * 1000),
        "from": "Producer1"
    },
    "body": {
        "openc2": {
            "request": {
                "action":"query",
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


deny_file_by_hash = {

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
                    "file": {
                        "hashes": {
                            "sha256": "0a73291ab5607aef7db23863cf8e72f55bcb3c273bb47f00edf011515aeb5894"
                        }
                    }
                },
                "actuator": {
                    "er": {}
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