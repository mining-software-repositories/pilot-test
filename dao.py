import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import datetime

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

class CommitComplete(Base):
    __tablename__ = 'commitscomplete'
    id = Column(Integer, Sequence('commitscomplete_id_seq'), primary_key=True)
    name = Column(String)
    hash = Column(String, nullable=True)
    msg = Column(String, nullable=True)
    author = Column(String, nullable=True)
    committer = Column(String, nullable=True)
    author_date = Column(DateTime, nullable=True)
    author_timezone = Column(Integer, nullable=True)
    committer_date = Column(DateTime, nullable=True)
    committer_timezone = Column(Integer, nullable=True)
    branches = Column(String, nullable=True)
    in_main_branch = Column(Boolean, nullable=True)
    merge = Column(Boolean, nullable=True)
    modified_files = Column(String, nullable=True)
    parents = Column(String, nullable=True)
    project_name = Column(String, nullable=True)
    project_path = Column(String, nullable=True)
    deletions = Column(Integer, nullable=True)
    insertions = Column(Integer, nullable=True)
    lines = Column(Integer, nullable=True)
    files = Column(Integer, nullable=True)
    dmm_unit_size = Column(Float, nullable=True)
    dmm_unit_complexity = Column(Float, nullable=True)
    dmm_unit_interfacing = Column(Float, nullable=True)

class FileComplete(Base):
    __tablename__ = 'filescomplete'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hash = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now())
    old_path = Column(String, nullable=True)
    new_path = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    change_type = Column(String, nullable=True)
    diff = Column(String, nullable=True)
    diff_parsed = Column(String, nullable=True)
    added_lines = Column(Integer, nullable=True)
    deleted_lines = Column(Integer, nullable=True)
    source_code = Column(String, nullable=True)
    source_code_before = Column(String, nullable=True)
    methods = Column(String, nullable=True)
    methods_before = Column(String, nullable=True)
    changed_methods = Column(String, nullable=True)
    nloc = Column(Integer, nullable=True)
    complexity = Column(Integer, nullable=True)
    token_count= Column(Integer, nullable=True)
    commit_id = Column(Integer, ForeignKey('commitscomplete.id'))
    commit = relationship('CommitComplete')

class CommitsCollection():
    def __init__(self, session):
        self.session = session
    
    def insert_commit(self, commit):
        try:
            self.session.add(commit)
            self.session.commit()
        except Exception as e:
            print('Erro during insert commit: {e}')
            self.session.rollback()
    
    def query_commit_id(self, id):
        return self.session.query(Commit).filter(Commit.id==id).first()

    def query_commit_name(self, name):
        return self.session.query(Commit).filter(Commit.name==name).first()

class FilesCollection():
    def __init__(self, session):
        self.session = session

    def insert_file(self, file):
        try:
            self.session.add(file)
            self.session.commit()
        except Exception as e:
            print('Erro during insert file: {e}')
            self.session.rollback()
    
    def query_file_id(self, id):
        return self.session.query(File).filter(File.id==id).first()

    def query_file_name(self, name):
        return self.session.query(File).filter(File.name==name).first()

    def query_files_by_name(self, name):
        return self.session.query(File).filter(File.name==name).all()

    def query_files_by_commit_id(self, commit_id):
        return self.session.query(File).filter(File.commit_id==commit_id).all()
    
    def query_files_by_commit_name(self, commit_name):
        my_commit = self.session.query(Commit).filter(Commit.name==commit_name).first()
        return self.session.query(File).filter(File.commit_id==my_commit.id).all()

    def query_commits_from_file_name(self, name):
        files = self.session.query(File).filter(File.name==name).all()
        list_of_commits = []
        for each in files:
            list_of_commits.append(each.hash)
        return list_of_commits

    def query_all_files(self):
        files = self.session.query(File).all()
        return files

class CommitsCompleteCollection():
    def __init__(self, session):
        self.session = session
    
    def insert_commit(self, commitcomplete):
        try:
            self.session.add(commitcomplete)
            self.session.commit()
        except Exception as e:
            print('Erro during insert commit: {e}')
            self.session.rollback()
    
    def query_commit_id(self, id):
        return self.session.query(CommitComplete).filter(CommitComplete.id==id).first()

    def query_commit_name(self, name):
        return self.session.query(CommitComplete).filter(CommitComplete.name==name).first()

    def query_commit_hash(self, hash):
        return self.session.query(CommitComplete).filter(CommitComplete.hash==hash).first().id

    def query_all_commits(self):
        commits = self.session.query(CommitComplete).all()
        return commits

class FilesCompleteCollection():
    def __init__(self, session):
        self.session = session

    def insert_file(self, filecomplete):
        try:
            self.session.add(filecomplete)
            self.session.commit()
        except Exception as e:
            print('Erro during insert file: {e}')
            self.session.rollback()
    
    def query_file_id(self, id):
        return self.session.query(FileComplete).filter(FileComplete.id==id).first()

    def query_file_name(self, name):
        return self.session.query(FileComplete).filter(FileComplete.name==name).first()

    def query_files_by_commit_id(self, commit_id):
        return self.session.query(FileComplete).filter(FileComplete.commit_id==commit_id).all()
    
    def query_files_by_commit_name(self, commit_name):
        my_commit = self.session.query(CommitComplete).filter(CommitComplete.name==commit_name).first()
        return self.session.query(FileComplete).filter(FileComplete.commit_id==my_commit.id).all()

    def query_commits_from_file_name(self, name):
        files = self.session.query(FileComplete).filter(FileComplete.name==name).all()
        list_of_commits = []
        for each in files:
            list_of_commits.append(each.hash)
        return list_of_commits

    def query_all_files(self):
        files = self.session.query(FileComplete).all()
        return files

    def query_files_by_name(self, name):
        return self.session.query(FileComplete).filter(FileComplete.name==name).all()


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