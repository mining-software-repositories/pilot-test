import utils
import dao
import os
import datetime
from threading import Thread
import config
import specials
import pandas as pd

CREATE_DATA_BASE = False
SHOW_LIST_OF_ANALYSED_COMMIT = True

t1 = datetime.datetime.now()

os.system('clear')

print(f'Analise do Repositório de Código do Cassandra: intervalo de {config.tag1} até {config.tag2} - Data: {t1}\n')

if SHOW_LIST_OF_ANALYSED_COMMIT:
    lista_commits_entre_tags = utils.list_commits_between_tags(from_tag=config.tag1, to_tag=config.tag2, my_repository=config.repositorio_git_cassandra) 
    print(f'Para as tags: {config.tag1} e {config.tag2} é feita uma análise dos {len(lista_commits_entre_tags)} commits \
e para cada commit é guardada uma lista de arquivos modificados nesse commit.')
file_name = config.path_arquivos_modificados + '/' + f'lista_commits_entre_tags_{config.tag1}_{config.tag2}.txt'
utils.create_file_by_list_of_commits(file_name, lista_commits_entre_tags)

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

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo de carregamento do Banco: {delta}')
print('Aguarde...')

t1 = datetime.datetime.now()
# Carrega um dicionario contendo os commits e seus arquivos modificados
dicionario_commits_com_arquivos_java_modificados = {}
all_commits_analysed = commitsCompleteCollection.query_commits_from_list(lista_commits_entre_tags)

my_commits = []
my_data_commit = []
my_files_commit = []
for commit in all_commits_analysed:
    dicionario_commits_com_arquivos_java_modificados[commit.hash] = commit.modified_files
    my_commits.append(commit.hash)
    my_data_commit.append(commit.author_date)
    my_files_commit.append(commit.modified_files)

# Cria um dataframe de commit ordenado por data ascendente
df_commits = pd.DataFrame.from_dict({'commit':my_commits, 'date':my_data_commit, 'files':my_files_commit})
df_commits = df_commits.sort_values(['date'], ascending=True)

# Carrega um dicionario contendo os arquivos e os commits onde eles apareceram
dicionario_files_com_commits = {}
lista_de_arquivos_e_commits = filesCompleteCollection.query_files_from_list_of_commits(lista_commits_entre_tags)
dicionario_files_com_commits = utils.generate_modifield_files_with_commits(lista_de_arquivos_e_commits)

# Carrega uma lista contendo os arquivos dessa versão analisada
lista_de_arquivos = []
for k, v in dicionario_files_com_commits.items():
    lista_de_arquivos.append(k)

# Carrega em uma lista os arquivos mais modificados dentro da faixa de commits analisados
arquivos_mais_modificados = specials.counterWithFrequencyOfFile3(dicionario_commits_com_arquivos_java_modificados)
arquivos_mais_modificados = arquivos_mais_modificados.most_common()
pega_100_arquivos_mais_modificados = utils.get_n_most_modifield_files(100, arquivos_mais_modificados)

file_name =  config.path_arquivos_modificados + '/' + 'pega_100_arquivos_mais_modificados.txt'
utils.create_file_by_list(file_name, utils.get_names_and_counts_from_n_most_modifield_files(pega_100_arquivos_mais_modificados))
print('')

pega_20_arquivos_mais_modificados = utils.get_n_most_modifield_files(20, arquivos_mais_modificados)
pega_nome_20_arquivos_mais_modificados = utils.get_names_from_n_most_modifield_files(pega_20_arquivos_mais_modificados)

dicionario_df_files_commits = {}
lista_linha_file = []

for each in pega_nome_20_arquivos_mais_modificados:
    if ".java" in each:
        for index, row in df_commits.iterrows():
            if each in row['files']:
                elemento = (row['commit'], 1)
            else: 
                elemento = (row['commit'], 0)
            lista_linha_file.append(elemento)
        dicionario_df_files_commits[each] = lista_linha_file
        lista_linha_file = []

t2 = datetime.datetime.now()
print(f'Hora: {t2}')
delta = t2 - t1
print(f'Tempo de análise dos 100 arquivos mais modificados e geração do dicionário de arquivos e seus commits: {delta} para as tags {config.tag1}  e {config.tag2}')

# Gera uma lista que contem os dados de uma linha
# (file1, [commit1, commit2, ..., commitn], [0,0, ..., 1])
lista_relacao_commits = []
lista_linha_arquivo_commits = []
lista_auxiliar = []
for k, v in dicionario_df_files_commits.items():
    # v é uma lista [(commit1, 0), (commit2, 1), (commit3, 0), ... (commitn, 0)]
    for elemento in v:
        # Guarda apenas o elemento[1]
        lista_relacao_commits.append(elemento[0])
        lista_auxiliar.append(elemento[1])
    lista_auxiliar = []
    lista_relacao_commits = []
    linha  = (k, lista_relacao_commits, lista_auxiliar)
    lista_linha_arquivo_commits.append(linha)

# Monta o cabecalho do arquivo df_files_commits
# file, commit1, commit2, ... commitN
lista_cabecalho_arquivo_commits = []
lista_cabecalho_arquivo_commits.append('file')

i = 0
for each in lista_linha_arquivo_commits:
    if i < 1:
        filename = each[0]
        lista_hash_commits = each[1]
        lista_01_commits = each[2]
        lista_cabecalho_arquivo_commits = lista_cabecalho_arquivo_commits + lista_hash_commits
        i += 1
    else:
        break

def create_file_by_list_file_commits(file_name, lista_cabecalho, lista_linha_arquivo_commits):
    try:
        linha = ''
        cabecalho = utils.convert_list_to_str(lista_cabecalho)
        with open(file_name, mode='w+', encoding='utf8') as f:
            f.write(cabecalho)
            f.write('\n')
            for each in lista_linha_arquivo_commits:
                filename = each[0]
                lista_de_commits = each[1]
                lista_01_commits = each[2]
                linha = filename + ',' + utils.convert_list_to_str(lista_01_commits)
                f.write(linha)
                f.write('\n')
                linha = ''
        print(f'File: {file_name} created successfully')
    except Exception as e:
        print(f'Error during creation of file {e}')

create_file_by_list_file_commits('df_files_commits.csv', lista_cabecalho_arquivo_commits, lista_linha_arquivo_commits)