from litestar import Litestar
from litestar.config.cors import CORSConfig

from app.controlers import (
    AuthorController,
    BookController,
    BookCopyController,
    CategoryController,
    ClientController,
    LoanController,
)
from app.database import sqlalchemy_config

cors_config = CORSConfig(allow_origins=["http://localhost:5173"])

app = Litestar(
    [
        AuthorController,
        BookController,
        BookCopyController,
        CategoryController,
        ClientController,
        LoanController,
    ],
    debug=True,
    plugins=[sqlalchemy_config],
    cors_config=cors_config,
)
