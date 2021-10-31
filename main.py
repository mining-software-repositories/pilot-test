import utils
import dao
import os
import datetime
import specials

os.system('clear')

my_commit = '969531a113530eb87d5ea350aa005abc946a5152'
repositorio_git_cassandra = '/Users/armandosoaressousa/git/msr/cassandra'
#repositorio_git_cassandra = 'https://github.com/apache/cassandra.git'
tag1 = 'cassandra-3.0.0'
tag2 = 'cassandra-3.1'
tag3 = 'cassandra-3.2'
tag4 = 'cassandra-3.3'

t1 = datetime.datetime.now()
print(f'Analise do Cassandra: {t1} \n')

#lista_tags_cassandra = utils.load_tags_from_repository()
#print(len(lista_tags_cassandra) )

#lista_commits_cassandra = utils.list_commits_hash_from_repository(repositorio_git_cassandra)
#print(f'No repositório {repositorio_git_cassandra} existe um total de {len(lista_commits_cassandra)} commits.')

lista_commits_entre_tags = utils.list_commits_between_tags(from_tag=tag1, to_tag=tag2, my_repository=repositorio_git_cassandra) 

print(f'Para as tags: {tag1} e {tag2} é feita uma análise dos {len(lista_commits_entre_tags)} commits \
e para cada commit é guardada uma lista de arquivos modificados nesse commit.')

print('Aguarde...')

dicionario_commits_com_arquivos_java_modificados = utils.generate_dictionary_commits_and_modifield_java_files(lista_commits_entre_tags, repositorio_git_cassandra)

print('1. Dicionario de commits com seus arquivos modificados gerado com sucesso!\n')

print('')
print('2. Criando o arquivo para salvar os commits analisados.')
utils.create_file_from_dictionary('analise-commits-cassandra-3-0-ao-3-1.txt', dicionario_commits_com_arquivos_java_modificados)

print('')
print(f'Configura e carrega o banco {dao.data_base}...')
db_session = dao.create_session()
dao.drop_tables()
dao.create_tables()
print(f'Banco {dao.data_base} carregado com sucesso! \n')

commitsCollection = dao.CommitsCollection(session=db_session)
filesCollections = dao.FilesCollection(session=db_session)

utils.save_commits_and_modifield_files_in_db(dicionario_commits_com_arquivos_java_modificados, commitsCollection, filesCollections)

lista_de_arquivos_e_commits = filesCollections.query_all_files()
dicionario_files_com_commits = utils.generate_modifield_files_with_commits(lista_de_arquivos_e_commits)

file_name = 'arquivos-e-seus-commmits-v3-0-a-v3-1.txt'
print(f'3. Criando o arquivo {file_name} ...')

utils.create_file_from_dictionary(file_name, dicionario_files_com_commits)

# Conjunto dos hash commnis das tags analisadas
lista_commits_teste = []
# Conjunto de todos os arquivos (nomes) que foram modificados nas tags
lista_arquivos_teste = []

for k, v in dicionario_commits_com_arquivos_java_modificados.items():
    lista_commits_teste.append(k)

for k, v in dicionario_files_com_commits.items():
  lista_arquivos_teste.append(k)

print('')
print(f'Total de commits analisados: {len(lista_commits_teste)}')

print('')
print(f'Total de arquivos analisados: {len(lista_arquivos_teste)}')

#print(utils.raw_generate_list_of_groups(lista_commits_teste, dicionario_files_com_commits) )

arquivos_mais_modificados = specials.counterWithFrequencyOfFile2(dicionario_commits_com_arquivos_java_modificados)
arquivos_mais_modificados = arquivos_mais_modificados.most_common()

pega_10_arquivos_mais_modificados = utils.get_n_most_modifield_files(10, arquivos_mais_modificados)

print('')
print('4. Mostra os 10 arquivos mais modificados')
print('')
print(pega_10_arquivos_mais_modificados)
print('')

lista_temp = utils.get_names_from_n_most_modifield_files(pega_10_arquivos_mais_modificados)
lista_subconjuntos = utils.gera_subconjuntos_ate_3_elementos(lista_temp)

print(f'Para o conjunto de {len(lista_temp)} elementos foi gerado um total {len(lista_subconjuntos)} subconjuntos de até 3 elementos.')
print('')

lista_grupos = utils.generate_list_of_groups_from_commits(lista_subconjuntos, dicionario_commits_com_arquivos_java_modificados)

print('5. Mostra os grupos de arquivos mais modificados ao longo do tempo')
utils.show_groups_of_most_modifield_files(lista_grupos)

print('')
t2 = datetime.datetime.now()
print(f'Hora: {t2}')

delta = t2 - t1
print(f'Tempo de análise final: {delta}')

