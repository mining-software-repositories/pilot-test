import utils
import dao
import os
import datetime
from threading import Thread
import config
import specials
import pandas as pd

CREATE_DATA_BASE = False
SHOW_LIST_OF_ANALYSED_COMMIT = False

t1 = datetime.datetime.now()

os.system('clear')

print(f'Analise do Repositório de Código do Cassandra: intervalo de {config.tag1} até {config.tag2} - Data: {t1}\n')

if SHOW_LIST_OF_ANALYSED_COMMIT:
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
else: 
    # Carrega o banco já criado
    db_session = dao.create_session()
    commitsCompleteCollection = dao.CommitsCompleteCollection(session=db_session)
    filesCompleteCollection = dao.FilesCompleteCollection(session = db_session)
    print(f'Banco {dao.data_base} carregado com sucesso! \n')

print('Aguarde...')
t1 = datetime.datetime.now()
# Carrega um dicionario contendo os commits e seus arquivos modificados
dicionario_commits_com_arquivos_java_modificados = {}
all_commits_analysed = commitsCompleteCollection.query_all_commits()

for commit in all_commits_analysed:
    dicionario_commits_com_arquivos_java_modificados[commit.hash] = commit.modified_files

# Carrega um dicionario contendo os arquivos e os commits onde eles apareceram
dicionario_files_com_commits = {}
lista_de_arquivos_e_commits = filesCompleteCollection.query_all_files()
dicionario_files_com_commits = utils.generate_modifield_files_with_commits(lista_de_arquivos_e_commits)

# Carrega em uma lista os arquivos mais modificados dentro da faixa de commits analisados
arquivos_mais_modificados = specials.counterWithFrequencyOfFile3(dicionario_commits_com_arquivos_java_modificados)
arquivos_mais_modificados = arquivos_mais_modificados.most_common()
pega_100_arquivos_mais_modificados = utils.get_n_most_modifield_files(100, arquivos_mais_modificados)

print('')
print(f'Mostra os 100 arquivos mais modificados entre as tags: {config.tag1} e {config.tag2}')
print('')
print(utils.get_names_from_n_most_modifield_files(pega_100_arquivos_mais_modificados))
print('')

file_name =  config.path_arquivos_modificados + '/' + 'pega_100_arquivos_mais_modificados.txt'
utils.create_file_by_list(file_name, utils.get_names_and_counts_from_n_most_modifield_files(pega_100_arquivos_mais_modificados))
print('')

lista_elementos_arquivos = []
for each in pega_100_arquivos_mais_modificados:
    lista_registros_pelo_nome = filesCompleteCollection.query_files_by_name(each[0])
    lista_elementos_arquivos = lista_elementos_arquivos + lista_registros_pelo_nome

# Cria um dictionary para representar os detalhes (nome, commits, quantidade de modificações em LOC) mais importantes dos 100 arquivos mais modificados
dicionario_lista_100_arquivos_mais_modificados = utils.gera_dicionario_lista_arquivos_mais_modificados(lista_elementos_arquivos)

# Cria um dataframe dos 100 arquivos mais modificados
pd.set_option('display.max_rows', None)
df_100_arquivos_mais_modificados = pd.DataFrame.from_dict(dicionario_lista_100_arquivos_mais_modificados)
print(f'Mostra as 10 primeiras linhas do dataframe df_100_arquivos_mais_modificados')
print(df_100_arquivos_mais_modificados[['name', 'hash', 'nloc', 'complexity', 'modifications']].sort_values(by=['hash'], ascending=True).head(10))
print('')

try:
    file_name = config.path_arquivos_modificados + '/' + 'df_100_arquivos_mais_modificados.csv'
    df_100_arquivos_mais_modificados.to_csv(file_name, sep=',', encoding='utf-8')
    print(f'Arquivo {file_name} exportado com sucesso!')
except Exception as e:
    print('Erro ao tentar exportar arquivo {file_name}: {e}')

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo de análise dos 100 arquivos mais modificados: {delta} para as tags {config.tag1}  e {config.tag2}')