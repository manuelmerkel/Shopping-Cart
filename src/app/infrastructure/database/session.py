from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_sqlite_session_maker(database_url: str) -> sessionmaker:
    engine = create_engine(
        database_url,
        echo=True,
        connect_args={
            "timeout": 5
        },
    )
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
