import threading
import multiprocessing
import logging
from threading import Thread
import time
import datetime
from pydriller import Repository
from collections import Counter

def display(msg):
    threadname = threading.current_thread().name
    processname = multiprocessing.current_process().name
    logging.info(f'{processname}\{threadname}: {msg}')

# List all Commits with Author
# return a dictionary like this: hash, author, date, list of files in commit
# dictionary = {'hash': ['author', 'date of commit', [file1, file2, ...]]}
def dictionaryWithAllCommmits(client, repository):
    dictionaryAux = {}
    display(f'Gera um dicionário com todos os commits do repositório {repository}')
    t1 = datetime.datetime.now()
    try: 
        for commit in Repository(repository).traverse_commits():
            commitAuthorNameFormatted = '{}'.format(commit.author.name)
            commitAuthorDateFormatted = '{}'.format(commit.author_date)
            listFilesModifiedInCommit = []
            for modification in commit.modified_files:
                itemMofied = '{}'.format(modification.filename)
                listFilesModifiedInCommit.append(itemMofied)
            dictionaryAux[commit.hash] = [commitAuthorNameFormatted, commitAuthorDateFormatted, listFilesModifiedInCommit] 
    except Exception as e:
        display(f'Error during processing dictionaryWithAllCommmits in {repository} error: {e}')
        dictionaryAux = None
    t2 = datetime.datetime.now()
    delta = t2 - t1
    display(f'Dicionário gerado com sucesso em {delta} s')
    return dictionaryAux

# Return a Counter with frequency of each file analysed
# The Counter like this:
# Counter({file1: frequency of file1, file2: frequence of file2, ...})
def counterWithFrequencyOfFile2(dictionaryCommits):
  listFull = []
  for key, value in dictionaryCommits.items():
    listAxu = []
    listAxu = value
    for eachItem in listAxu:
      listFull.append(eachItem)
  return Counter(listFull)

# Return a Counter with frequency of each file analysed
# The Counter like this:
# Counter({file1: frequency of file1, file2: frequence of file2, ...})
def counterWithFrequencyOfFile3(dictionaryCommits):
  listFull = []
  for key, value in dictionaryCommits.items():
    listAxu = []
    listAxu = value.split(',')
    for eachItem in listAxu:
      listFull.append(eachItem)
  return Counter(listFull)
