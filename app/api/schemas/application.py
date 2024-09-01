from typing import Optional

from pydantic import UUID4, BaseModel


class BaseApplication(BaseModel):
    id: str

class ApplicationIn(BaseApplication):
    amount: int
    to_address: str
    bank: str

