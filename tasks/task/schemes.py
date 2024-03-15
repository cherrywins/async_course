tasks_stream_schema_v1 = {
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
            "task_id": {
            "type": "string"
            },
            "assignee_id": {
            "type": "string"
            },
            "cost": {
            "type": "number"
            },
            "reward": {
            "type": "number"
            }
        },
        "required": ["task_id", "assignee_id", "cost", "reward"]
        }
    },
    "required": ["metadata", "data"]
}


tasks_complete_schema_v1 = {
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
            "task_id": {
            "type": "string"
            },
        },
        "required": ["task_id"]
        }
    },
    "required": ["metadata", "data"]
}

tasks_assign_schema_v1 = {
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
            "task_id": {
            "type": "string"
            },
            "assignee_id": {
            "type": "string"
            },
        },
        "required": ["task_id", "assignee_id"]
        }
    },
    "required": ["metadata", "data"]
}
