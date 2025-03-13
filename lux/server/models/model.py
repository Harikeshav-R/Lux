from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lux.server.core.db import Base


class Model(Base):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)

    model_name: Mapped[str] = mapped_column(String, nullable=False)
    base_provider: Mapped[str] = mapped_column(String, nullable=False)
    is_provider: Mapped[bool] = mapped_column(Boolean, nullable=False)
    supports_image_generation: Mapped[bool] = mapped_column(Boolean, nullable=False)
