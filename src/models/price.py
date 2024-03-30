import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column


from db.db import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    gpu_id: Mapped[int] = mapped_column(ForeignKey("gpus.id"))
    price: Mapped[float]
    time: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
