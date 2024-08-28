from sqlalchemy.orm import Mapped, mapped_column

from app.api.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(default=0)
    referer_id: Mapped[int]