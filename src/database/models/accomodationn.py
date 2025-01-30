from datetime import datetime
from sqlalchemy import BigInteger, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas import AccomodationSchema  # Создадим схему для туров
from src.database.connection import Base, async_session_maker


class Accomodation(Base):
    __tablename__ = 'accomodation'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # Название тура
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Описание тура
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())  # Время создания
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now()
    )  

    @classmethod
    async def add_accomodation(cls, name: str, description: str):
        """
        Добавляет новую точку проживания в базу данных.
        """
        async with async_session_maker() as session:
            existing_accomodation = await session.execute(select(cls).where(cls.name == name))
            if existing_accomodation.scalars().first():
                return False 
            session.add(cls(name=name, description=description))
            await session.commit()
            return True

    @classmethod
    async def delete_accomodation(cls, tour_id: int):
        """
        Удаляет точку проживания по его ID.
        """
        async with async_session_maker() as session:
            tour = await session.get(cls, tour_id)
            if tour:
                await session.delete(tour)
                await session.commit()
                return True
            return False  # Тур не найден

    @classmethod
    async def get_accomodation(cls, tour_id: int) -> AccomodationSchema:
        """
        Возвращает информацию о проживании по его ID.
        """
        async with async_session_maker() as session:
            tour = await session.get(cls, tour_id)
            return AccomodationSchema(
                id=tour.id,
                name=tour.name,
                description=tour.description,
                created_at=tour.created_at,
                updated_at=tour.updated_at
            ) if tour else None

    @classmethod
    async def get_all_accomodation(cls) -> list[AccomodationSchema]:
        """
        Возвращает список всех проживаний.
        """
        async with async_session_maker() as session:
            tours = await session.execute(select(cls))
            return [
                AccomodationSchema(
                    id=tour.id,
                    name=tour.name,
                    description=tour.description,
                    created_at=tour.created_at,
                    updated_at=tour.updated_at
                ) for tour in tours.scalars()
            ]