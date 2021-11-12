# Relação de scripts e notebooks

## Resultados das análises entre as versões 3.0.0 e 3.11.11 do Apache Cassandra

[identifica_smells_e_grupos_de_arquivos.ipynb](https://github.com/mining-software-repositories/pilot-test/blob/master/identifica_smells_e_grupos_de_arquivos.ipynb)

### Scripts de apoio

[main.py](https://github.com/mining-software-repositories/pilot-test/blob/master/main.py) - Cria a estrutura inicial da análise da versão 3.1.0

[teste.py](https://github.com/mining-software-repositories/pilot-test/blob/master/teste.py) - Faz a análise do repositório dentro de uma faixa de commits das tags definidas no config.py

[teste_clustering.py](https://github.com/mining-software-repositories/pilot-test/blob/master/teste_clustering.py) - Faz as análises e testes de K-means Clustering para encontrar os grupos de arquivos que são modificados no mesmo commit dentro da faixa de commits das tags definidas.

### Notebooks de apoio

[analisar_repositorio_cassandra.ipynb](https://github.com/mining-software-repositories/pilot-test/blob/master/analisar_repositorio_cassandra.ipynb) - Faz uma análise geral do repositório

[extract_data_from_designite.ipynb](https://github.com/mining-software-repositories/pilot-test/blob/master/extract_data_from_designite.ipynb) - Extrai Architectural Smells e Design Smells baseados nos dados gerados pelo DesigniteJava

[Cluster_de_Arquivos_e_Commits.ipynb](https://github.com/mining-software-repositories/pilot-test/blob/master/Cluster_de_Arquivos_e_Commits.ipynb) - Faz a análise dos commits e arquivos da versão 3.1 e testes com o K-means clustering para encontrar o grupo de arquivos que aparecem juntos em mais de um commit.
