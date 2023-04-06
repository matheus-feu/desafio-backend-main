from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from app.models.analise_git_model import Base


def get_db_session():
    """Cria conexão com o banco de dados"""
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
