from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, String, Integer, Text, ForeignKey, UniqueConstraint

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    books = relationship("BookDB", back_populates="owner")

class BookDB(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)

    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    quotation_marks = Column(String, nullable=False)

    file_path = Column(String, nullable=True)

    status = Column(String, nullable=False, default="uploaded")
    version = Column(Integer, nullable=False, default=1)

    owner = relationship("UserDB", back_populates="books")
    chapters = relationship("ChapterDB", back_populates="book", cascade="all, delete-orphan")
    annotation_set = relationship("AnnotationSetDB", back_populates="book", uselist=False)
    translation_task = relationship("TranslationTaskDB", back_populates="book", uselist=False)

class ChapterDB(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_id = Column(String, ForeignKey("chapters.id", ondelete="CASCADE"), index=True, nullable=True)

    content = Column(Text, nullable=True)

    book = relationship("BookDB", back_populates="chapters")
    parent = relationship("ChapterDB", remote_side="ChapterDB.id", backref=backref("children", passive_deletes=True, cascade="all, delete-orphan"))

class AnnotationSetDB(Base):
    __tablename__ = "annotation_sets"

    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="SET NULL"), index=True, nullable=True)

    file_path = Column(String, nullable=False)

    status = Column(String, nullable=False, default="extracted_from_md_to_xlsx")
    version = Column(Integer, nullable=False, default=1)

    book = relationship("BookDB", back_populates="annotation_set")

    __table_args__ = (
        UniqueConstraint("book_id", name="uq_annotation_set_book"),
    )

class TranslationTaskDB(Base):
    __tablename__ = "translation_tasks"

    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="SET NULL"), index=True, nullable=True)

    total_chapters = Column(Integer, nullable=True)
    message = Column(Text, nullable=True)

    status = Column(String, nullable=False, default="queued")
    progress = Column(Integer, nullable=False, default=0)
    translated_chapters = Column(Integer, nullable=False, default=0)

    book = relationship("BookDB", back_populates="translation_task")

    __table_args__ = (
        UniqueConstraint("book_id", name="uq_translation_task_book"),
    )