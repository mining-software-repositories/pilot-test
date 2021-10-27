from pydriller import Repository

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
