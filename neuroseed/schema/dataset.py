
DATASET_SCHEMA = {
    "type": "object",
    "properties": {
        "is_public": {"type": "boolean"},
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "category": {
            "type": "string",
            "maxLength": 64
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 64
            },
            "uniqueItems": True
        }
    },
    "required": ["title"],
    "additionalProperties": False
}