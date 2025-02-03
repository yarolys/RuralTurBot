from datetime import datetime
from sqlalchemy import BigInteger, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas import LocalFoodSchema  # Создадим схему для местной кухни
from src.database.connection import Base, async_session_maker


class LocalFood(Base):
    __tablename__ = 'local_foods'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # Название блюда
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Описание блюда
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())  # Время создания
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now()
    )  

    @classmethod
    async def add_local_food(cls, name: str, description: str):
        """
        Добавляет новое блюдо в базу данных.
        """
        async with async_session_maker() as session:
            existing_food = await session.execute(select(cls).where(cls.name == name))
            if existing_food.scalars().first():
                return False 
            session.add(cls(name=name, description=description))
            await session.commit()
            return True

    @classmethod
    async def delete_local_food(cls, food_id: int):
        """
        Удаляет блюдо по его ID.
        """
        async with async_session_maker() as session:
            food = await session.get(cls, food_id)
            if food:
                await session.delete(food)
                await session.commit()
                return True
            return False  # Блюдо не найдено

    @classmethod
    async def get_local_food(cls, food_id: int) -> LocalFoodSchema:
        """
        Возвращает информацию о блюде по его ID.
        """
        async with async_session_maker() as session:
            food = await session.get(cls, food_id)
            return LocalFoodSchema(
                id=food.id,
                name=food.name,
                description=food.description,
                created_at=food.created_at,
                updated_at=food.updated_at
            ) if food else None

    @classmethod
    async def get_all_local_foods(cls) -> list[LocalFoodSchema]:
        """
        Возвращает список всех блюд.
        """
        async with async_session_maker() as session:
            foods = await session.execute(select(cls))
            return [
                LocalFoodSchema(
                    id=food.id,
                    name=food.name,
                    description=food.description,
                    created_at=food.created_at,
                    updated_at=food.updated_at
                ) for food in foods.scalars()
            ]
