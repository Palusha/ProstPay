import datetime

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


Base = declarative_base()


class User(Base):
    """
    A simple user sqlalchemy model
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    username: Mapped[str]
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


class UserDTO(BaseModel):
    """
    A simple user representation pydantic model
    """

    id: int
    firstname: str
    lastname: str
    username: str
    create_date: datetime.datetime = datetime.datetime.utcnow()


class UserManager:
    async def get(self, user_id: int) -> UserDTO:
        # used a not existing function because we need to assume that we have get_async_session function implemented
        async with get_async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            await session.commit()
        return UserDTO.model_validate(result.scalar_one_or_none(), from_attributes=True)

    async def add(self, user: UserDTO) -> None:
        # used a not existing function because we need to assume that we have get_async_session function implemented
        async with get_async_session() as session:
            session.add(User(**user.model_dump()))
            await session.commit()
