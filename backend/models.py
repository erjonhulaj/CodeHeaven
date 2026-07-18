# models.py

from pydantic import BaseModel


class Finding(BaseModel):
    rule: str
    message: str
    severity: str
    line: int | None = None