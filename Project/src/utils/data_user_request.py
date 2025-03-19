from pydantic import BaseModel, field_validator


class DataOfUserRequest(BaseModel):
    user_id: int
    name_pills: str
    limitation_days: int | None
    number_iters: int

    @field_validator("user_id")
    def validate_user_id(cls, user_id: int) -> int:
        if user_id < 0:
            raise ValueError("user_id cannot be negative")
        return user_id

    @field_validator("name_pills")
    def validate_name_pills(cls, name_pills: str) -> str:
        return name_pills.capitalize()

    @field_validator("limitation_days")
    def validate_limitation_days(cls, limit: int | None) -> int | None:
        if limit is not None and limit < 0:
            raise ValueError("limitation_days cannot be negative")
        return limit if (limit != 0) else None

    @field_validator("number_iters")
    def validate_number_iters(cls, number_iters: int) -> int:
        if number_iters <= 0:
            raise ValueError("number_iters cannot be negative or equal 0")
        return number_iters
