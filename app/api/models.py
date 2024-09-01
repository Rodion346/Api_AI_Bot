from email.policy import default

from sqlalchemy.orm import Mapped, mapped_column

from app.api.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(primary_key=True)
    processing_balance: Mapped[int] = mapped_column(default=0)
    referal_balance: Mapped[int] = mapped_column(default=0)
    referer_id: Mapped[str] = mapped_column(default="0")


class Application(Base):
    __tablename__ = 'application'
    id: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(default=0)
    to_address: Mapped[str] = mapped_column(default="0")
    bank: Mapped[str] = mapped_column(default='0')