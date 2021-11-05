from pydriller import Repository
import entities
import dao
import itertools
import json
import threading
import multiprocessing
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Analyze single commit
def commit_detailed_from_repository(my_commit, my_repository):
    single_commit = Repository(my_repository, single=my_commit).traverse_commits()
    return single_commit

# Dado um repositorio 
# retorna uma lista dos hashs dos commits
def list_commits_hash_from_repository(my_repository):
    list_temp = []
    for commit in Repository(my_repository).traverse_commits():
        list_temp.append(commit.hash)
    return list_temp

def list_commits_from_repository(my_repository):
    list_temp = []
    for commit in Repository(my_repository).traverse_commits():
        list_temp.append(commit)
    return list_temp

# Dado um repositorio, tag de origem e tag destino
# retorna a lista de commits hash entre as tags
def list_commits_hash_between_tags(from_tag, to_tag, my_repository):
    list_temp = []
    for commit in Repository(my_repository, from_tag=from_tag, to_tag=to_tag).traverse_commits():
        list_temp.append(commit.hash)
    return list_temp

def list_commits_between_tags(from_tag, to_tag, my_repository):
    list_temp = []
    for commit in Repository(my_repository, from_tag=from_tag, to_tag=to_tag).traverse_commits():
        list_temp.append(commit)
    return list_temp

# Dado um commit de origem e outro commit de destino
# retorna a lista de commits entre eles
def list_commits_between_commits(from_commit, to_commit, my_repository):
    list_temp = []
    for commit in Repository(my_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits():
        list_temp.append(commit)
    return list_temp

# Dado um commit e um repositorio
# retorna a lista de arquivos modificados
def list_modified_files_from_commit(my_commit, my_repository):
    single_commit = commit_detailed_from_repository(my_commit, my_repository)
    list_temp = []
    for commit in single_commit:
        for m in commit.modified_files:
            list_temp.append(m)
    return list_temp

def load_tags_from_repository(path_file='dados/tags-cassandra.txt'):
    list_aux = []
    with open(path_file, mode='r+', encoding='utf-8') as file:
        for line in file:
            list_aux.append(line.rstrip())
    return list_aux

def generate_dictionary_commits_and_modifield_java_files(list_commits_from_tags, git_repository):
    dictionary = {}
    lista_aux = []
    for commit in list_commits_from_tags:
        for m in list_modified_files_from_commit(commit.hash, git_repository):
            mf = entities.MyModifiedFile(m)
            name = mf.get_filename()
            if '.java' in name:
                lista_aux.append(name)
        dictionary[commit.hash] = lista_aux
        lista_aux = []
    return dictionary

def create_file_from_dictionary(file_name, dictionary):
    try:
        linha = ''
        with open(file_name, mode='w+', encoding='utf8') as f:
            for key, value in dictionary.items():
                linha = key + ':' + ','.join(value)
                f.write(linha)
                f.write('\n')
                linha = ''
        print(f'File: {file_name} created successfully')
    except Exception as e:
        print(f'Error during creation of file {e}')

def save_commits_and_modifield_files_in_db(dictionary_commits, commitsCollection, filesCollections):
    try:
        for key, value in dictionary_commits.items():
            commit = dao.Commit(name=key)
            commitsCollection.insert_commit(commit)
            for each in value:
                my_file = dao.File(name=each, hash=key, commit_id=commit.id)
                filesCollections.insert_file(my_file)
        print(f'Commits and Files saved successfully!')
    except Exception as e:
        print(f'Error during save files in DB: {e}')

def generate_modifield_files_with_commits(lista_de_arquivos_e_commits):
    dicionario_files_com_commits = {}
    lista_conjunto_arquivos = []

    for each in lista_de_arquivos_e_commits:
        lista_conjunto_arquivos.append(each.name)

    conjunto_arquivos = set(lista_conjunto_arquivos)

    lista_temp = list(conjunto_arquivos)
    lista_temp = sorted(lista_temp)

    lista_files_modificados = lista_temp

    for each in lista_files_modificados:
        lista_aux = []
        for item in lista_de_arquivos_e_commits:
            if each == item.name:
                lista_aux.append(item.hash)
        dicionario_files_com_commits[each] = lista_aux

    return dicionario_files_com_commits

def get_size_group_of_commits(dicionario_files_com_commits):
    lista_tamanho_grupo_commits = []

    for key, value in dicionario_files_com_commits.items():
        value_to_str = ','.join(value)

        if len(value) > 0:
            lista_tamanho_grupo_commits.append(len(value))
    return lista_tamanho_grupo_commits

def findsubsets(s, n):
    return list(itertools.combinations(s,n) )

# Dada uma lista de n elementos
# gera seus respectivos subconjuntos variando de 2 a n-2 agrupamentos
def gera_subconjuntos(lista):
  conjunto = set(lista)
  n =  len(conjunto)
  lista_de_subconjuntos = []
  lista_de_subconjuntos_temp = []

  print(f'Para o conjunto {conjunto} de {n} elementos. ')
  print(f' Serão gerados os seguintes subconjuntos: ')

  for i in range(1, (n-2) + 1):
    print(f'Subconjunto{i} com {i+1} elementos')
    lista_de_subconjuntos_temp = findsubsets(conjunto, i+1)
    lista_de_subconjuntos = lista_de_subconjuntos + lista_de_subconjuntos_temp

  print('')
  print('Lista de subconjuntos final')
  return lista_de_subconjuntos

# Por questões de performance e análise combinatória 
#criei uma função que gera subconjunto de até 3 elementos agrupados
def gera_subconjuntos_ate_3_elementos(lista):
  conjunto = set(lista)
  n = len(conjunto)
  lista_de_subconjuntos = []
  lista_de_subconjuntos_temp = []

  for i in range(1, 3):
      lista_de_subconjuntos_temp = findsubsets(conjunto, i+1)
      lista_de_subconjuntos = lista_de_subconjuntos + lista_de_subconjuntos_temp
    
  return lista_de_subconjuntos

def raw_generate_list_of_groups(lista_commits_teste, dicionario_files_com_commits):
    lista_grupos = []
    lista_grupo = []
    i = 0
    for each_commit in lista_commits_teste:
        for chave, valor in dicionario_files_com_commits.items():
            if each_commit in valor:
                # o commit apareceu no arquivo
                grupo = 'grupo' + str(i) + ',' + each_commit
                elemento = (grupo, chave)
                lista_grupo.append(elemento)
    i += 1 
    lista_grupos.append(lista_grupo)
    # limpa o lista_grupo
    lista_grupo = []

    return lista_grupos

# Pega os n arquivos mais modificados:
def get_n_most_modifield_files(n, arquivos_mais_modificados):
    i = 0
    pega_n_arquivos_mais_modificados = []
    for each in arquivos_mais_modificados:
        if i < n:
            pega_n_arquivos_mais_modificados.append(each)
            i += 1
        else:
            break
    return pega_n_arquivos_mais_modificados

def get_names_from_n_most_modifield_files(most_modifield_files):
    lista_temp = []

    for each in most_modifield_files:
        lista_temp.append(each[0])
    return lista_temp 

def generate_list_of_groups_from_commits(lista_subconjuntos, dictionary_commits):
    lista_grupos = []
    lista_grupo = []
    i = 0
    for tupla_arquivo in lista_subconjuntos:
        for commit, lista_arquivos_do_commit in dictionary_commits.items():
            if len(lista_arquivos_do_commit) < 10:
                lista_subconjunto_arquivos_do_commit = gera_subconjuntos_ate_3_elementos(lista_arquivos_do_commit)
            if tupla_arquivo in lista_subconjunto_arquivos_do_commit:
                grupo = 'grupo' + str(i) + f':{tupla_arquivo}'
                elemento = (grupo, commit)
                lista_grupo.append(elemento)
        i += 1
        lista_grupos.append(lista_grupo)
        # limpa o lista_grupo
        lista_grupo = []
    return lista_grupos

def show_groups_of_most_modifield_files(lista_grupos):
    lista_de_commits_por_grupo = []
    for item in lista_grupos:
        if len(item) > 0:
            for elemento in item:
                grupo = elemento[0]
                commit = elemento[1]
                lista_de_commits_por_grupo.append(commit)
            print(f'Lista de Commis do grupo {grupo} : {len(lista_de_commits_por_grupo)} : {lista_de_commits_por_grupo}')
            lista_de_commits_por_grupo = []

def convert_list_to_str(lista):
    temp = ''
    if len(lista) > 0:
        temp = ','.join( str(v) for v in lista)
    return temp

def convert_modifield_list_to_str(lista):
    list_aux = []
    for each in lista:
        list_aux.append(each.filename)
    str = convert_list_to_str(list_aux)
    return str

def convert_method_list_to_str(lista):
    list_aux = []
    for each in lista:
        list_aux.append(each)
    str = convert_list_to_str(list_aux)
    return str

def convert_dictionary_to_str(dictionary):
    temp = ''
    if len(dictionary) > 0:
        temp = str(json.dumps(dictionary))
    return temp

def concat_str(str1, str2):
    temp = str1 + ',' + str2
    return temp

def save_complete_commits_and_modifield_files_in_db(lista_commits_entre_tags, commitCompleteCollection, fileCompleteCollection):
  for commit in lista_commits_entre_tags:
    c = dao.CommitComplete(name = commit.hash, 
        hash = commit.hash, 
        msg = commit.msg,
        author = concat_str(commit.author.name,commit.author.email), 
        committer = concat_str(commit.committer.name,commit.committer.email), 
        author_date = commit.author_date,
        author_timezone = commit.author_timezone,
        committer_date = commit.committer_date,
        committer_timezone = commit.committer_timezone,
        branches = convert_list_to_str(commit.branches),
        in_main_branch = commit.in_main_branch,
        merge = commit.merge,
        modified_files = convert_modifield_list_to_str(commit.modified_files),
        parents = convert_list_to_str(commit.parents),
        project_name = commit.project_name,
        project_path = commit.project_path,
        deletions = commit.deletions,
        insertions = commit.insertions,
        lines = commit.lines,
        files = commit.files,
        dmm_unit_size = commit.dmm_unit_size,
        dmm_unit_complexity = commit.dmm_unit_complexity,
        dmm_unit_interfacing = commit.dmm_unit_interfacing)
    # salva o commit corrente
    commitCompleteCollection.insert_commit(c)
    display(f'Save commit {c.hash}')
    for m in commit.modified_files:
        if m is not None and  m.filename is not None:
            mf = dao.FileComplete(
                name = m.filename,
                hash = commit.hash,
                old_path = m.old_path,
                new_path = m.new_path,
                filename = m.filename,
                change_type = m.change_type.name,
                diff = str(m.diff),
                diff_parsed = convert_dictionary_to_str(m.diff_parsed),
                added_lines = m.added_lines,
                deleted_lines = m.deleted_lines,
                source_code = str(m.source_code),
                source_code_before = str(m.source_code_before),
                methods = convert_list_to_str(m.methods),
                methods_before = convert_list_to_str(m.methods_before),
                changed_methods = convert_list_to_str(m.changed_methods),
                nloc = m.nloc,
                complexity = m.complexity,
                token_count = m.token_count, 
                commit_id = commitCompleteCollection.query_commit_hash(commit.hash)
            )
            name = mf.filename

            if '.java' in name:
            # salva o arquivo correte
              fileCompleteCollection.insert_file(mf)
              display(f'Save file {mf.name}')

def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info(f'{processname}\{threadname}: {msg}')

def gera_dicionario_lista_arquivos_mais_modificados(lista_elementos_arquivos, commitsCompleteCollection):
    dicionario_lista_arquivos_mais_modificados = {}

    i = 0
    lista_aux_index = []
    lista_aux_name = []
    lista_aux_hash = []
    lista_aux_date_commit = []
    lista_aux_added_lines = []
    lista_aux_deleted_lines = []
    lista_aux_modifications = []
    lista_aux_old_path = []
    lista_aux_new_path = []
    lista_aux_change_type = []
    lista_aux_nloc = []
    lista_aux_complexity = []

    for each in lista_elementos_arquivos:
        lista_aux_index.append(i)
        lista_aux_name.append(each.name)
        lista_aux_hash.append(each.hash)
        date_commit = commitsCompleteCollection.query_date_from_commit_by_hash(each.hash)
        lista_aux_date_commit.append(date_commit)
        lista_aux_old_path.append(each.old_path)
        lista_aux_new_path.append(each.new_path)
        lista_aux_change_type.append(each.change_type)
        lista_aux_nloc.append(each.nloc)
        lista_aux_complexity.append(each.complexity)
        lista_aux_added_lines.append(each.added_lines)
        lista_aux_deleted_lines.append(each.deleted_lines)
        modifications = each.added_lines + each.deleted_lines
        lista_aux_modifications.append(modifications)
        i += 1

    dicionario_lista_arquivos_mais_modificados = {'index': lista_aux_index,'name':lista_aux_name, 
    'hash':lista_aux_hash, 'date': lista_aux_date_commit, 'added_lines':lista_aux_added_lines, 
        'deleted_lines':lista_aux_deleted_lines, 'modifications':lista_aux_modifications, 
        'old_path': lista_aux_old_path, 'new_path': lista_aux_new_path, 
        'change_type': lista_aux_change_type,  'nloc': lista_aux_nloc, 'complexity': lista_aux_complexity}

    return dicionario_lista_arquivos_mais_modificados

def get_names_and_counts_from_n_most_modifield_files(most_modifield_files):
    lista_temp = []

    for each in most_modifield_files:
        elemento = ( str(each[0]), str(each[1]) )
        elemento = ','.join(elemento)
        lista_temp.append( elemento ) 
    return lista_temp 

def create_file_by_list(file_name, lista):
    try:
        linha = ''
        with open(file_name, mode='w+', encoding='utf8') as f:
            for each in lista:
                linha = each
                f.write(linha)
                f.write('\n')
                linha = ''
        print(f'File: {file_name} created successfully')
    except Exception as e:
        print(f'Error during creation of file {e}')

def create_file_by_list_of_commits(file_name, lista):
    try:
        linha = ''
        with open(file_name, mode='w+', encoding='utf8') as f:
            for each in lista:
                linha = str(each.hash)
                f.write(linha)
                f.write('\n')
                linha = ''
        print(f'File: {file_name} created successfully')
    except Exception as e:
        print(f'Error during creation of file {e}')