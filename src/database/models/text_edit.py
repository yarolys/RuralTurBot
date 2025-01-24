from datetime import datetime, timezone
from sqlalchemy import BigInteger, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.schemas import EditableTextSchema
from src.database.connection import Base, async_session_maker


class EditableText(Base):
    __tablename__ = "editable_texts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @classmethod
    async def get_text(cls, identifier: str) -> EditableTextSchema:
        async with async_session_maker() as session:
            text_record = await session.execute(select(cls).where(cls.identifier == identifier))
            text = text_record.scalars().first()
            return EditableTextSchema(
                id=text.id,
                identifier=text.identifier,
                content=text.content,
                created_at=text.created_at,
                updated_at=text.updated_at,
            ) if text else None

    @classmethod
    async def update_text(cls, identifier: str, new_content: str):
        async with async_session_maker() as session:
            text_record = await session.execute(select(cls).where(cls.identifier == identifier))
            text = text_record.scalars().first()
            if text:
                text.content = new_content
                text.updated_at = datetime.now(timezone.utc)
            else:
                session.add(cls(identifier=identifier, content=new_content))
            await session.commit()