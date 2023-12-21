from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, and_, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, column_property, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class BookCopy(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(index=True, unique=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    is_available: Mapped[bool] = mapped_column(default=True)

    # relationships
    book: "Mapped[Book]" = relationship("Book", back_populates="copies")
    loans: "Mapped[list[Loan]]" = relationship(back_populates="book_copy")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(index=True, unique=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    year: Mapped[int]
    language: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    # computed
    copies_available: Mapped[int] = column_property(
        select(func.count(BookCopy.id))
        .where(and_(BookCopy.book_id == id, BookCopy.is_available))
        .scalar_subquery()
    )

    # relationships
    author: "Mapped[Author]" = relationship(back_populates="books")
    categories: "Mapped[list[Category]]" = relationship(
        back_populates="books", secondary="books_categories"
    )
    copies: "Mapped[list[BookCopy]]" = relationship(back_populates="book")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    biography: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[date]]

    # relationships
    books: "Mapped[list[Book]]" = relationship(back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    # relationships
    books: "Mapped[list[Book]]" = relationship(
        back_populates="categories", secondary="books_categories"
    )


class BookCategory(Base):
    __tablename__ = "books_categories"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    book_copy_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id"))
    loan_date: Mapped[date]
    return_date: Mapped[Optional[date]]
    penalty_fee: Mapped[Optional[int]]
    penalty_fee_paid: Mapped[Optional[bool]]

    # relationships
    client: "Mapped[Client]" = relationship(back_populates="loans")
    book_copy: "Mapped[BookCopy]" = relationship(back_populates="loans")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[Optional[str]]

    # computed
    penalty_debt: Mapped[int] = column_property(
        select(func.coalesce(func.sum(Loan.penalty_fee), 0))
        .where(and_(Loan.client_id == id, Loan.penalty_fee_paid.is_(False)))
        .scalar_subquery()
    )
    borrowed_books: Mapped[int] = column_property(
        select(func.count(Loan.id))
        .where(and_(Loan.client_id == id, Loan.return_date.is_(None)))
        .scalar_subquery()
    )

    # relationships
    loans: "Mapped[list[Loan]]" = relationship(back_populates="client")
