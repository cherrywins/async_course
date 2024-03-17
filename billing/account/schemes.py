account_stream_schema_v1 = {
    "type": "object",
    "properties": {
        "event_name": {
            "type": "string"
        },
        "data": {
        "type": "object",
        "properties": {
            "public_id": {
            "type": "string"
            },
            "email": {
            "type": "string"
            },
            "name": {
            "type": "string"
            },
            "role": {
            "type": "string"
            }
        },
        "required": ["account_id", "email", "name", "role"]
        }
    },
    "required": ["event_name", "data"]
}

account_stream_schema_v2 = {
    "type": "object",
    "properties": {
        "metadata": {
        "type": "object",
        "properties": {
            "version": {
            "type": "integer"
            },
            "event_name": {
            "type": "string"
            },
            "event_uuid": {
            "type": "string",
            "format": "uuid"
            },
            "timestamp": {
            "type": "number"
            }
        },
        "required": ["version", "event_name", "event_uuid", "timestamp"]
        },
        "data": {
        "type": "object",
        "properties": {
            "account_id": {
            "type": "string"
            },
            "email": {
            "type": "string"
            },
            "name": {
            "type": "string"
            },
            "role": {
            "type": "string"
            }
        },
        "required": ["account_id", "email", "name", "role"]
        }
    },
    "required": ["metadata", "data"]
}
