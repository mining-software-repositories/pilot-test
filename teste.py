import utils
import dao
import os
import datetime

os.system('clear')

my_commit = '969531a113530eb87d5ea350aa005abc946a5152'
repositorio_git_cassandra = '/Users/armandosoaressousa/git/msr/cassandra'
#repositorio_git_cassandra = 'https://github.com/apache/cassandra.git'
tag1 = 'cassandra-3.0.0'
tag2 = 'cassandra-3.1'

t1 = datetime.datetime.now()
print(f'Analise do Cassandra: {t1} \n')

lista_commits_entre_tags = utils.list_commits_between_tags(from_tag=tag1, to_tag=tag2, my_repository=repositorio_git_cassandra) 

print(f'Para as tags: {tag1} e {tag2} é feita uma análise dos {len(lista_commits_entre_tags)} commits \
e para cada commit é guardada uma lista de arquivos modificados nesse commit.')

print(f'Configura e carrega o banco {dao.data_base}...')
db_session = dao.create_session()
dao.drop_tables()
dao.create_tables()
print(f'Banco {dao.data_base} carregado com sucesso! \n')

commitsCompleteCollection = dao.CommitsCompleteCollection(session=db_session)
filesCompleteCollection = dao.FilesCompleteCollection(session = db_session)

print('Aguarde...')

try: 
    utils.save_complete_commits_and_modifield_files_in_db(lista_commits_entre_tags, commitsCompleteCollection, filesCompleteCollection)
    print('Commits e arquivos salvos com sucesso no banco!')
except Exception as e:
    print(f'Erro: {e}')

print('')
t2 = datetime.datetime.now()
print(f'Hora: {t2}')

delta = t2 - t1
print(f'Tempo de análise final: {delta}')

