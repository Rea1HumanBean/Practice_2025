

def validate_grpc_id(id_value: int | str) -> int:
    try:
        id_int = int(id_value)
        if id_int <= 0:
            raise ValueError("ID must be a positive integer")
        return id_int
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid ID value: {id_value}. Must be a positive integer") from e
