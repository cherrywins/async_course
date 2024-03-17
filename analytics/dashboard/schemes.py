pay_out_schema_v1 = {
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
            "payout_id": {
                "type": "string"
            },
            "account_id": {
                "type": "string"
            },
            "amount": {
                "type": "number"
            },
            "date": {
                "type": "string"
            },
        },
        "required": ["payout_id", "account_id", "amount", "date"]
        }
    },
    "required": ["metadata", "data"]
}
