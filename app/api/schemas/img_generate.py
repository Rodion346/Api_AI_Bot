from pydantic import UUID4, BaseModel
from app.config import APIKEY_CLOTHOFF

class Clot(BaseModel):
    pass


class ClotIn(Clot):
    age: str
    breast_size: str
    body_type: str
    butt_size: str
    cloth: str
    id_gen: str
    webhook: str = "https://rodion346-api-ai-bot-5bab.twc1.net/webhook"