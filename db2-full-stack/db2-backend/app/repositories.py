from datetime import date, timedelta
from typing import Optional

from litestar.contrib.sqlalchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import Author, Book, BookCopy, Category, Client, Loan


class AuthorRepository(SQLAlchemySyncRepository[Author]):
    model_type = Author


async def provide_authors_repo(db_session: Session):
    return AuthorRepository(session=db_session, auto_commit=True)


class BookRepository(SQLAlchemySyncRepository[Book]):
    model_type = Book


async def provide_books_repo(db_session: Session):
    return BookRepository(session=db_session, auto_commit=True)


class BookCopyRepository(SQLAlchemySyncRepository[BookCopy]):
    model_type = BookCopy


async def provide_book_copies_repo(db_session: Session):
    return BookCopyRepository(session=db_session, auto_commit=True)


class CategoryRepository(SQLAlchemySyncRepository[Category]):
    model_type = Category


async def provide_categories_repo(db_session: Session):
    return CategoryRepository(session=db_session, auto_commit=True)


class ClientRepository(SQLAlchemySyncRepository[Client]):
    model_type = Client


async def provide_clients_repo(db_session: Session):
    return ClientRepository(session=db_session, auto_commit=True)


class LoanRepository(SQLAlchemySyncRepository[Loan]):
    model_type = Loan

    def borrow_book(
        self, loan: Loan, book_copies_repo: BookCopyRepository, client_repo: ClientRepository
    ) -> Loan:
        book_copy = book_copies_repo.get(loan.book_copy_id)
        client = client_repo.get(loan.client_id)
        # check if book copy is available and client can borrow
        if not book_copy.is_available:
            raise Exception("Book copy already borrowed")
        if client.borrowed_books > 2:
            raise Exception("Client already borrowed 2 books")

        # save loan and update book copy
        self.add(loan)
        book_copy.is_available = False
        book_copies_repo.update(book_copy)

        return loan

    def return_book(
        self,
        loan_id: int,
        return_date: Optional[date],
        penalty_fee_paid: Optional[bool],
        book_copies_repo: BookCopyRepository,
    ) -> Loan:
        loan = self.get(loan_id)
        book_copy = book_copies_repo.get(loan.book_copy_id)

        # set defaults
        if return_date is None:
            return_date = date.today()
        if penalty_fee_paid is None:
            penalty_fee_paid = False

        # update loan details
        loan.return_date = return_date
        if return_date > loan.loan_date + timedelta(days=7):
            loan.penalty_fee = ((return_date - loan.loan_date).days - 7) * 200
            loan.penalty_fee_paid = penalty_fee_paid
        else:
            loan.penalty_fee = 0
        self.update(loan)

        # update book copy
        book_copy.is_available = True
        book_copies_repo.update(book_copy)

        return loan


async def provide_loans_repo(db_session: Session):
    return LoanRepository(session=db_session, auto_commit=True)
