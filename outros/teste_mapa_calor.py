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

os.system('clear')

t1 = datetime.datetime.now()
print(f'Analise do Cassandra: {t1} do intervalo de {config.tag1} até {config.tag2} \n')

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
dicionario_commits_com_arquivos_java_modificados = {}
all_commits_analysed = commitsCompleteCollection.query_all_commits()
for commit in all_commits_analysed:
    dicionario_commits_com_arquivos_java_modificados[commit.hash] = commit.modified_files

dicionario_files_com_commits = {}
lista_de_arquivos_e_commits = filesCompleteCollection.query_all_files()
dicionario_files_com_commits = utils.generate_modifield_files_with_commits(lista_de_arquivos_e_commits)

print(f'{t1}')
arquivos_mais_modificados = specials.counterWithFrequencyOfFile3(dicionario_commits_com_arquivos_java_modificados)
arquivos_mais_modificados = arquivos_mais_modificados.most_common()
pega_100_arquivos_mais_modificados = utils.get_n_most_modifield_files(100, arquivos_mais_modificados)

print('')
print('Mostra os 100 arquivos mais modificados')
print('')
print(utils.get_names_from_n_most_modifield_files(pega_100_arquivos_mais_modificados))
print('')

lista_elementos_arquivos = []
for each in pega_100_arquivos_mais_modificados:
    print(each)
    lista_registros_pelo_nome = filesCompleteCollection.query_files_by_name(each[0])
    lista_elementos_arquivos = lista_elementos_arquivos + lista_registros_pelo_nome

# Cria um dictionary para representar os detalhes mais importantes dos 100 arquivos mais modificados
dicionario_lista_10_arquivos_mais_modificados = {}

i = 0
lista_aux_index = []
lista_aux_name = []
lista_aux_hash = []
lista_aux_added_lines = []
lista_aux_deleted_lines = []
lista_aux_modifications = []

for each in lista_elementos_arquivos:
    lista_aux_index.append(i)
    lista_aux_name.append(each.name)
    lista_aux_hash.append(each.hash)
    lista_aux_added_lines.append(each.added_lines)
    lista_aux_deleted_lines.append(each.deleted_lines)
    modifications = each.added_lines + each.deleted_lines
    lista_aux_modifications.append(modifications)
    i += 1

dicionario_lista_10_arquivos_mais_modificados = {'index': lista_aux_index,'name':lista_aux_name, 
'hash':lista_aux_hash, 'added_lines':lista_aux_added_lines, 
    'deleted_lines':lista_aux_deleted_lines, 'modifications':lista_aux_modifications}

lista_de_commits = dicionario_lista_10_arquivos_mais_modificados['hash']
lista_de_commits = list(set(lista_de_commits))
#print(f'lista_de_commits: {len(lista_de_commits)}, {lista_de_commits} ')

lista_de_arquivos_java = dicionario_lista_10_arquivos_mais_modificados['name']
lista_de_arquivos_java = list(set(lista_de_arquivos_java))
#print(f'lista_de_arquivos_java: {len(lista_de_arquivos_java)}, {lista_de_arquivos_java}')

lista_aux = []
for commit in lista_de_commits:
    for file in lista_de_arquivos_java:
        temp = filesCompleteCollection.query_files_by_name(file)
        find = False
        for item in temp:
            if commit == item.hash:
                elemento = (commit, file, item.added_lines, item.deleted_lines)
                find = True
        if find == False: 
            elemento = (commit, file, 0, 0)
        lista_aux.append(elemento)

dicionario_lista_10_arquivos_mais_modificados = {}

i = 0
lista_aux_index = []
lista_aux_name = []
lista_aux_hash = []
lista_aux_added_lines = []
lista_aux_deleted_lines = []
lista_aux_modifications = []

for each in lista_aux:
    lista_aux_index.append(i)
    lista_aux_hash.append(each[0])
    lista_aux_name.append(each[1])
    lista_aux_added_lines.append(each[2])
    lista_aux_deleted_lines.append(each[3])
    modifications = each[2] + each[3]
    lista_aux_modifications.append(modifications)
    i += 1

dicionario_lista_10_arquivos_mais_modificados = {'index': lista_aux_index,'name':lista_aux_name, 
'hash':lista_aux_hash, 'added_lines':lista_aux_added_lines, 
    'deleted_lines':lista_aux_deleted_lines, 'modifications':lista_aux_modifications}

pd.set_option('display.max_rows', None)
df_arquivos_mais_modificados = pd.DataFrame.from_dict(dicionario_lista_10_arquivos_mais_modificados)

print(df_arquivos_mais_modificados.sort_values(by=['hash'], ascending=True))
## select name, hash, added_lines, deleted_lines , (added_lines + deleted_lines) as modfications from filescomplete where name='UserType.java' or  name='LeveledManifest.java' order by name, hash

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo3 de análise dos arquivos mais modificados: {delta}')

import seaborn as sns
import matplotlib.pyplot as plt
##df_flights = pd.read_csv('flights.csv')
##flights = df_flights.pivot("month", "year", "passengers")
##sns.heatmap(flights)
##plt.show()

df_commits = df_arquivos_mais_modificados.pivot('name', 'hash', 'modifications')
sns.heatmap(df_commits)
plt.show()