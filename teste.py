import utils
import dao
import os
import datetime
from threading import Thread
import config

CREATE_DATA_BASE = True

os.system('clear')

t1 = datetime.datetime.now()
print(f'Analise do Cassandra: {t1} \n')

lista_commits_entre_tags = utils.list_commits_between_tags(from_tag=config.tag1, to_tag=config.tag2, my_repository=config.repositorio_git_cassandra) 

print(f'Para as tags: {config.tag1} e {config.tag2} é feita uma análise dos {len(lista_commits_entre_tags)} commits \
e para cada commit é guardada uma lista de arquivos modificados nesse commit.')

print(f'Configura e carrega o banco {dao.data_base}...')
if CREATE_DATA_BASE:
    # Recria o banco e insere todos os commits analisados
    try:
        dao.drop_tables()
        dao.create_tables()
        db_session = dao.create_session()
        commitsCompleteCollection = dao.CommitsCompleteCollection(session=db_session)
        filesCompleteCollection = dao.FilesCompleteCollection(session = db_session)
        print('Aguarde...')
        utils.save_complete_commits_and_modifield_files_in_db(lista_commits_entre_tags, commitsCompleteCollection, filesCompleteCollection)
        utils.display('save_complete_commits_and_modifield_files_in_db(')
        print('Commits e arquivos salvos com sucesso no banco!')
    except Exception as e:
        print(f'Erro: {e}')

# Carrega o banco já criado
db_session = dao.create_session()
commitsCompleteCollection = dao.CommitsCompleteCollection(session=db_session)
filesCompleteCollection = dao.FilesCompleteCollection(session = db_session)
print(f'Banco {dao.data_base} carregado com sucesso! \n')

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo de carregamento do banco para análise dos commmits: {delta}')

t1 = datetime.datetime.now()
dicionario_commits_com_arquivos_java_modificados = {}
all_commits_analysed = commitsCompleteCollection.query_all_commits()
for commit in all_commits_analysed:
    dicionario_commits_com_arquivos_java_modificados[commit.hash] = commit.modified_files

dicionario_files_com_commits = {}
lista_de_arquivos_e_commits = filesCompleteCollection.query_all_files()
dicionario_files_com_commits = utils.generate_modifield_files_with_commits(lista_de_arquivos_e_commits)

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo2 de análise dos commmits: {delta}')