from datetime import datetime
from sqlalchemy import BigInteger, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas import EditableTextSchema
from src.database.connection import Base, async_session_maker


class EditableText(Base):
    __tablename__ = "editable_texts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name_button: Mapped[str] = mapped_column(nullable=False)
    identifier: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,  
        onupdate=datetime.now,  
    )

    @classmethod
    async def get_text(cls, identifier: str) -> EditableTextSchema:
        async with async_session_maker() as session:
            text_record = await session.execute(select(cls).where(cls.identifier == identifier))
            text = text_record.scalars().first()
            return EditableTextSchema(
                id=text.id,
                name_button=text.name_button,
                identifier=text.identifier,
                content=text.content,
                created_at=text.created_at,
                updated_at=text.updated_at,
            ) if text else None

    @classmethod
    async def update_text(cls, identifier: str, new_content: str):
        async with async_session_maker() as session:
            result = await session.execute(select(cls).where(cls.identifier == identifier))
            text_record = result.scalars().first()

            if text_record:
                text_record.content = new_content
                text_record.updated_at = datetime.now()
            else:
                new_record = cls(identifier=identifier, content=new_content)
                session.add(new_record)

            await session.commit()
            
    @classmethod
    async def get_all_texts(cls):
        async with async_session_maker() as session:
            result = await session.execute(select(cls))
            return result.scalars().all()