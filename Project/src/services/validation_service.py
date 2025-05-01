from fastapi import HTTPException, Request


def validate_id(name: str):
    async def dependency(request: Request):
        value = request.query_params.get(name)
        if value is None:
            raise HTTPException(status_code=422, detail=f"Missing required query parameter '{name}'")
        try:
            valid_number_id = int(value)
            if valid_number_id <= 0:
                raise HTTPException(status_code=400, detail=f"{name} must be a positive integer")
            return valid_number_id
        except ValueError:
            raise HTTPException(status_code=400, detail=f"{name} must be a valid integer")
    return dependency
