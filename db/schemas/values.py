def value_schema (value) -> dict:

    return {"id":str(value["_id"]),
            "max_value":value["max_value"],
            "actual_value":value["actual_value"]
            }

def values_schema (values)->list:
    return [value_schema(value) for value in values]