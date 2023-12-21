from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Author, Book, BookCopy, Category, Client, Loan


class AuthorReadDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class AuthorReadFullDTO(SQLAlchemyDTO[Author]):
    pass


class AuthorWriteDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class AuthorUpdateDTO(SQLAlchemyDTO[Author]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"}, partial=True)


class BookReadDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(exclude={"copies"})


class BookReadFullDTO(SQLAlchemyDTO[Book]):
    pass


class BookWriteDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(
        include={
            "isbn",
            "title",
            "description",
            "year",
            "language",
            "author_id",
            "categories.0.id",
            "copies.0.serial_number",
        }
    )


class BookUpdateDTO(SQLAlchemyDTO[Book]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "author", "copies_available", "copies"}, partial=True
    )


class BookCopyReadDTO(SQLAlchemyDTO[BookCopy]):
    config = SQLAlchemyDTOConfig(exclude={"loans"})


class BookCopyReadFullDTO(SQLAlchemyDTO[BookCopy]):
    pass


class BookCopyWriteDTO(SQLAlchemyDTO[BookCopy]):
    config = SQLAlchemyDTOConfig(exclude={"id", "book", "loans"})


class CategoryReadDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"books"})


class CategoryWriteDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "books"})


class ClientReadDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"loans"})


class ClientWriteDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(exclude={"id", "loans", "penalty_debt", "borrowed_books"})


class ClientUpdateDTO(SQLAlchemyDTO[Client]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "loans", "penalty_debt", "borrowed_books"}, partial=True
    )


class LoanReadDTO(SQLAlchemyDTO[Loan]):
    pass


class LoanReadWithBookDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(exclude={"client.loans", "book_copy.loans"}, max_nested_depth=2)


class LoanBorrowDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(include={"client_id", "book_copy_id", "loan_date"})


class LoanReturnDTO(SQLAlchemyDTO[Loan]):
    config = SQLAlchemyDTOConfig(include={"return_date", "penalty_fee_paid"})
