from typing import Optional

from pydantic import UUID4, BaseModel


class BaseUser(BaseModel):
    id: str
    referer_id: Optional[str] = "0"

class UserIn(BaseUser):
    pass

class UserOut(BaseUser):
    processing_balance: int
    referal_balance: int
