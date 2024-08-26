from sqlmodel import create_engine, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def get_session():
    with Session(engine) as session:
        yield session


# This replaces the Base = declarative_base()
# All your models will inherit from SQLModel instead of Base
