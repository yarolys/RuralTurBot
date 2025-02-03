from datetime import datetime
from sqlalchemy import BigInteger, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas import EntertainmentSchema  # Подключаем схему
from src.database.connection import Base, async_session_maker


class Entertainment(Base):
    __tablename__ = 'entertainment'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # Название развлечения
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Описание
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())  # Дата создания
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now()
    )  # Дата обновления

    @classmethod
    async def add_entertainment(cls, name: str, description: str):
        """
        Добавляет новое развлечение в базу данных.
        """
        async with async_session_maker() as session:
            existing_entertainment = await session.execute(select(cls).where(cls.name == name))
            if existing_entertainment.scalars().first():
                return False  # Уже существует
            session.add(cls(name=name, description=description))
            await session.commit()
            return True

    @classmethod
    async def delete_entertainment(cls, entertainment_id: int):
        """
        Удаляет развлечение по его ID.
        """
        async with async_session_maker() as session:
            entertainment = await session.get(cls, entertainment_id)
            if entertainment:
                await session.delete(entertainment)
                await session.commit()
                return True
            return False  # Развлечение не найдено

    @classmethod
    async def get_entertainment(cls, entertainment_id: int) -> EntertainmentSchema:
        """
        Возвращает информацию о развлечении по его ID.
        """
        async with async_session_maker() as session:
            entertainment = await session.get(cls, entertainment_id)
            return EntertainmentSchema(
                id=entertainment.id,
                name=entertainment.name,
                description=entertainment.description,
                created_at=entertainment.created_at,
                updated_at=entertainment.updated_at
            ) if entertainment else None

    @classmethod
    async def get_all_entertainment(cls) -> list[EntertainmentSchema]:
        """
        Возвращает список всех развлечений.
        """
        async with async_session_maker() as session:
            entertainment_list = await session.execute(select(cls))
            return [
                EntertainmentSchema(
                    id=entertainment.id,
                    name=entertainment.name,
                    description=entertainment.description,
                    created_at=entertainment.created_at,
                    updated_at=entertainment.updated_at
                ) for entertainment in entertainment_list.scalars()
            ]
