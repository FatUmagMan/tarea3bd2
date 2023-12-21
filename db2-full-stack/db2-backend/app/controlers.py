from advanced_alchemy.exceptions import ConflictError
from advanced_alchemy.filters import CollectionFilter, SearchFilter
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.repository import NotFoundError

from app import dtos
from app.models import Author, Book, BookCopy, Category, Client, Loan
from app.repositories import (
    AuthorRepository,
    BookCopyRepository,
    BookRepository,
    CategoryRepository,
    ClientRepository,
    LoanRepository,
    provide_authors_repo,
    provide_book_copies_repo,
    provide_books_repo,
    provide_categories_repo,
    provide_clients_repo,
    provide_loans_repo,
)

class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = dtos.AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @get("/{author_id:int}", return_dto=dtos.AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
            return authors_repo.get(author_id)
        except NotFoundError as e:
            raise HTTPException(detail="Author not found", status_code=404) from e

    @post(dto=dtos.AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @patch("/{author_id:int}", dto=dtos.AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
    ) -> Author:
        try:
            author, updated = authors_repo.get_and_update(
                id=author_id, **data.as_builtins(), match_fields=["id"]
            )
            return author
        except NotFoundError as e:
            raise HTTPException(detail="Author not found", status_code=404) from e


class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = dtos.BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(
        self, books_repo: BookRepository, available_copies: bool = None, categories: tuple = (), order_by: str = "id"
    ) -> list[Book]:
        # Filtra y ordena los libros según los parámetros
        filters = []
        if available_copies is not None:
            filters.append(BookCopy.is_available == available_copies)
        if categories:
            filters.append(Category.name.in_(categories))

        return books_repo.list(*filters, order_by=order_by)

    @post(
        dto=dtos.BookWriteDTO,
        return_dto=dtos.BookReadFullDTO,
        dependencies={
            "categories_repo": Provide(provide_categories_repo),
            "book_copies_repo": Provide(provide_book_copies_repo),
        },
    )
    async def create_book(
        self,
        data: Book,
        books_repo: BookRepository,
        categories_repo: CategoryRepository,
        book_copies_repo: BookCopyRepository,
    ) -> Book:
        try:
            category_ids = [c.id for c in data.categories]
            data.categories = categories_repo.list(CollectionFilter("id", category_ids))
            book = books_repo.add(data)

            # Agrega las copias disponibles
            for serial_number in data.copies_serial_numbers:
                book_copy = BookCopy(serial_number=serial_number, book_id=book.id, is_available=True)
                book_copies_repo.add(book_copy)

            return book
        except ConflictError as e:
            raise HTTPException(
                detail=f"Error creating book. Error: {e.__cause__}",
                status_code=400,
            ) from e

    @patch(
        "/{book_id:int}",
        dto=dtos.BookUpdateDTO,
        dependencies={"categories_repo": Provide(provide_categories_repo)},
    )
    async def update_book(
        self,
        book_id: int,
        data: DTOData[Book],
        books_repo: BookRepository,
        categories_repo: CategoryRepository,
    ) -> Book:
        try:
            data_dict = data.as_builtins()
            category_ids = [c.id for c in data_dict["categories"]]
            data_dict["categories"] = categories_repo.list(CollectionFilter("id", category_ids))
            book, updated = books_repo.get_and_update(
                id=book_id, **data_dict, match_fields=["id"]
            )
            return book
        except NotFoundError as e:
            raise HTTPException(detail="Book not found", status_code=404) from e


class BookCopyController(Controller):
    path = "/book_copies"
    tags = ["book-copies"]
    return_dto = dtos.BookCopyReadDTO
    dependencies = {"book_copies_repo": Provide(provide_book_copies_repo)}

    @get()
    async def list_book_copies(self, book_copies_repo: BookCopyRepository) -> list[BookCopy]:
        return book_copies_repo.list()

    @get("/{book_copy_id:int}", return_dto=dtos.BookCopyReadFullDTO)
    async def get_book_copy(
        self, book_copy_id: int, book_copies_repo: BookCopyRepository
    ) -> BookCopy:
        try:
            return book_copies_repo.get(book_copy_id)
        except NotFoundError as e:
            raise HTTPException(detail="Book copy not found", status_code=404) from e

    @post(dto=dtos.BookCopyWriteDTO)
    async def create_book_copy(
        self, data: BookCopy, book_copies_repo: BookCopyRepository
    ) -> BookCopy:
        try:
            return book_copies_repo.add(data)
        except ConflictError as e:
            raise HTTPException(
                detail=f"Error creating book copy. Error: {e.__cause__}", status_code=400
            ) from e

    @patch("/{book_copy_id:int}")
    async def update_book_copy(
        self, book_copy_id: int, data: DTOData[BookCopy], book_copies_repo: BookCopyRepository
    ) -> BookCopy:
        try:
            book_copy, updated = book_copies_repo.get_and_update(
                id=book_copy_id, **data.as_builtins(), match_fields=["id"]
            )
            return book_copy
        except NotFoundError as e:
            raise HTTPException(detail="Book copy not found", status_code=404) from e


class CategoryController(Controller):
    path = "/categories"
    tags = ["categories"]
    return_dto = dtos.CategoryReadDTO
    dependencies = {"categories_repo": Provide(provide_categories_repo)}

    @get()
    async def list_categories(self, categories_repo: CategoryRepository) -> list[Category]:
        return categories_repo.list()

    @post(dto=dtos.CategoryWriteDTO)
    async def create_category(
        self, data: Category, categories_repo: CategoryRepository
    ) -> Category:
        try:
            return categories_repo.add(data)
        except ConflictError as e:
            raise HTTPException(
                detail=f"Error creating category. Error: {e.__cause__}", status_code=400
            ) from e


class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = dtos.ClientReadDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()

    @get("/{client_id:int}")
    async def get_client(self, client_id: int, clients_repo: ClientRepository) -> Client:
        try:
            return clients_repo.get(client_id)
        except NotFoundError as e:
            raise HTTPException(detail="Client not found", status_code=404) from e

    @post(dto=dtos.ClientWriteDTO)
    async def create_client(self, data: Client, clients_repo: ClientRepository) -> Client:
        return clients_repo.add(data)

    @patch("/{client_id:int}", dto=dtos.ClientUpdateDTO)
    async def update_client(
        self, client_id: int, data: DTOData[Client], clients_repo: ClientRepository
    ) -> Client:
        try:
            client, updated = clients_repo.get_and_update(
                id=client_id, **data.as_builtins(), match_fields=["id"]
            )
            return client
        except NotFoundError as e:
            raise HTTPException(detail="Client not found", status_code=404) from e


class LoanController(Controller):
    path = "/loans"
    tags = ["loans"]
    return_dto = dtos.LoanReadDTO
    dependencies = {"loans_repo": Provide(provide_loans_repo)}

    @get()
    async def list_loans(self, loans_repo: LoanRepository) -> list[Loan]:
        return loans_repo.list()

    @get("/{loan_id:int}", return_dto=dtos.LoanReadWithBookDTO)
    async def get_loan(self, loan_id: int, loans_repo: LoanRepository) -> Loan:
        try:
            return loans_repo.get(loan_id)
        except NotFoundError as e:
            raise HTTPException(detail="Loan not found", status_code=404) from e

    @post(
        "/borrow",
        dto=dtos.LoanBorrowDTO,
        dependencies={
            "book_copies_repo": Provide(provide_book_copies_repo),
            "clients_repo": Provide(provide_clients_repo),
        },
    )
    async def borrow_book(
        self,
        data: Loan,
        loans_repo: LoanRepository,
        book_copies_repo: BookCopyRepository,
        clients_repo: ClientRepository,
    ) -> Loan:
        try:
            # Configura la cantidad de días del préstamo (por defecto 7 días)
            loan_days = int(self.request.query_params.get("loan_days", 7))

            # Realiza el préstamo con la cantidad de días configurada
            return loans_repo.borrow_book(data, book_copies_repo, clients_repo, loan_days)
        except ConflictError as e:
            raise HTTPException(
                detail=f"Error borrowing book. Error: {e.__cause__}", status_code=400
            ) from e
        except Exception as e:
            raise HTTPException(
                detail=f"Error borrowing book. Error: {str(e)}", status_code=400
            ) from e

    @post(
        "/{loan_id:int}/return",
        dto=dtos.LoanReturnDTO,
        dependencies={"book_copies_repo": Provide(provide_book_copies_repo)},
    )
    async def return_book(
        self,
        loan_id: int,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
        book_copies_repo: BookCopyRepository,
    ) -> Loan:
        try:
            # Obtiene la información necesaria para el cálculo de la multa
            loan = loans_repo.get(loan_id)
            return_date = data.get("return_date")
            penalty_fee_paid = data.get("penalty_fee_paid")

            # Realiza la devolución del libro y calcula la multa
            return loans_repo.return_book(
                loan_id=loan_id,
                return_date=return_date,
                penalty_fee_paid=penalty_fee_paid,
                book_copies_repo=book_copies_repo,
            )
        except NotFoundError as e:
            raise HTTPException(detail="Loan not found", status_code=404) from e