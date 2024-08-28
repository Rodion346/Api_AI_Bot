from typing import Optional

from pydantic import UUID4, BaseModel


class BaseUser(BaseModel):
    id: str

class UserIn(BaseUser):
    referer_id: Optional[int] = 0

class UserOut(BaseUser):
    balance: int
