import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

# Configuracoes do banco de dados 
data_base = 'testecassandra.db'
my_data_base = 'sqlite:///' + data_base

# Cria o engine de acesso ao banco
engine = create_engine(my_data_base, echo=False)
Base = declarative_base()

class Commit(Base):
    __tablename__ = 'commits'
    id = Column(Integer, Sequence('commit_id_seq'), primary_key=True)
    name = Column(String)

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hash = Column(String)
    commit_id = Column(Integer, ForeignKey('commits.id'))
    commit = relationship('Commit')

class CommitsCollection():
    def __init__(self, session):
        self.session = session
    
    def insert_commit(self, commit):
        self.session.add(commit)
        self.session.commit()
    
    def query_commit_id(self, id):
        return self.session.query(Commit).filter(Commit.id==id).first()

    def query_commit_name(self, name):
        return self.session.query(Commit).filter(Commit.name==name).first()

class FilesCollection():
    def __init__(self, session):
        self.session = session

    def insert_file(self, file):
        self.session.add(file)
        self.session.commit()

    def query_file_id(self, id):
        return self.session.query(File).filter(File.id==id).first()

    def query_file_name(self, name):
        return self.session.query(File).filter(File.name==name).first()

    def query_files_by_commit_id(self, commit_id):
        return self.session.query(File).filter(File.commit_id==commit_id).all()
    
    def query_files_by_commit_name(self, commit_name):
        my_commit = self.session.query(Commit).filter(Commit.name==commit_name).first()
        return self.session.query(File).filter(File.commit_id==my_commit.id).all()

    def query_commits_from_file_name(self, name):
        files = self.session.query(File).filter(File.name==name).all()
        return files

    def query_all_files(self):
        files = self.session.query(File).all()
        return files

# Cria a sessao com o banco 
def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Limpa o banco e recria as tabelas 
def drop_tables():
    Base.metadata.drop_all(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)


