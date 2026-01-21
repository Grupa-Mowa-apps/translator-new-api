from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, String, Integer, Text, ForeignKey, UniqueConstraint

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    books = relationship("BookDB", back_populates="owner")
    files = relationship("FileDB", back_populates="owner")

class BookDB(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    quotation_marks = Column(String, nullable=False)

    file_id = Column(String, ForeignKey("files.id", ondelete="SET NULL"), nullable=True)

    status = Column(String, nullable=False, default="uploaded")
    version = Column(Integer, nullable=False, default=1)

    owner = relationship("UserDB", back_populates="books", passive_deletes=True)
    chapters = relationship("ChapterDB", back_populates="book", cascade="all, delete-orphan")
    annotation_sets = relationship(
        "AnnotationSetDB", 
        back_populates="book", 
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    translation_task = relationship("TranslationTaskDB", back_populates="book", uselist=False)
    file = relationship(
        "FileDB", 
        foreign_keys=[file_id],
        uselist=False,
        post_update=True
    )
    files = relationship(
        "FileDB",
        back_populates="book",
        foreign_keys="FileDB.book_id",
        passive_deletes=True,
    )

class ChapterDB(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_id = Column(String, ForeignKey("chapters.id", ondelete="SET NULL"), index=True, nullable=True)

    chapter_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    content = Column(Text, nullable=True)

    book = relationship("BookDB", back_populates="chapters")
    parent = relationship(
        "ChapterDB", 
        remote_side=[id], 
        backref=backref("children", passive_deletes=True),
    )

    __table_args__ = (
        UniqueConstraint("book_id", "chapter_number", name="uq_chapters_book_chapter_number"),
    )


class AnnotationSetDB(Base):
    __tablename__ = "annotation_sets"

    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False)

    file_path = Column(String, nullable=False, unique=True, index=True)

    status = Column(String, nullable=False, default="extracted_from_md_to_xlsx")
    version = Column(Integer, nullable=False, default=1)

    book = relationship("BookDB", back_populates="annotation_sets")
    failed_applications = relationship(
        "FailedAnnotationApplicationDB", 
        back_populates="annotation_set", 
        cascade="all, delete-orphan"
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

class FileDB(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    kind = Column(String, nullable=False)
    path = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    book_id = Column(String, ForeignKey("books.id", ondelete="SET NULL"), index=True, nullable=True)
    version = Column(Integer, nullable=False, default=1)

    owner = relationship("UserDB", back_populates="files", uselist=False)
    book = relationship(
        "BookDB",
        back_populates="files",
        foreign_keys=[book_id],
        uselist=False,
    )

class FailedAnnotationApplicationDB(Base):
    __tablename__ = "failed_annotation_applications"

    id = Column(String, primary_key=True)
    annotation_set_id = Column(String, ForeignKey("annotation_sets.id", ondelete="CASCADE"), index=True, nullable=False)
    
    type = Column(String, nullable=False)
    original_text = Column(Text, nullable=False)
    translation = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
    
    annotation_set = relationship("AnnotationSetDB", back_populates="failed_applications")