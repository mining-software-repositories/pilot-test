import pandas as pd

PATH_DESIGNITE = '/Users/armandosoaressousa/git/msr/pilot-test/analises/designite'
PATH_ARQUIVOS_MODIFICADOS = '/Users/armandosoaressousa/git/msr/pilot-test/analises/modificados'
PATH_DESIGNITE_RESULTS_V_3_1_0 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/designite/v-3-1-0/resultados'
PATH_ARQUIVOS_MODIFICADOS_V_3_1_0 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/modificados/v-3-1-0'
PATH_DESIGNITE_RESULTS_V_3_2_0 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/designite/v-3-2-0/resultados'
PATH_ARQUIVOS_MODIFICADOS_V_3_2_0 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/modificados/v-3-2-0'
PATH_DESIGNITE_RESULTS_V_3_11_11 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/designite/v-3-11-11/resultados'
PATH_ARQUIVOS_MODIFICADOS_V_3_11_11 = '/Users/armandosoaressousa/git/msr/pilot-test/analises/modificados/v-3-11-11'

# Compara os resultados da analise do designite e dos arquivos modificados
#####  Analise da versao 3.1.0
## Arquivos e Pacotes analisados via Designite na versao 3.1.0

dictionary_log_analise_v_3_1_0 = {}
dictionary_log_analise_v_3_11_11 = {}

dictionary_analysis_summxary_v_3_1_0 = {'Total LOC analyzed':152143, 'Number of packages':75, 'Number of classes':2103, 'Number of methods':20349}

dictionary_architecture_smell_v_3_1_0 = {
 	'Cyclic dependency': 190, 'God component': 24, 'Ambiguous interface': 0 , 'Feature concentration': 59,
	'Unstable dependency': 39, 'Scattered functionality': 3, 'Dense structure': 1
}

dictionary_design_smell_v_3_1_0 = {
	'Imperative abstraction': 3 ,'Multifaceted abstraction': 8, 
	'Unnecessary abstraction': 18,	'Unutilized abstraction': 1431,
	'Feature envy': 0,	'Deficient encapsulation': 596,
	'Unexploited encapsulation': 0,	'Broken modularization': 4,
	'Cyclically-dependent modularization': 61,	'Hub-like modularization': 4,
	'Insufficient modularization': 186,	'Broken hierarchy': 27,
	'Cyclic hierarchy': 2,	'Deep hierarchy': 0,
	'Missing hierarchy': 0,	'Multipath hierarchy': 0,
	'Rebellious hierarchy':2,	'Wide hierarchy': 0
}

dictionary_implementation_smell_v_3_1_0 = {
	'Abstract function call from constructor': 4,	'Complex conditional': 209,
	'Complex method': 332,	'Empty catch clause': 23,
	'Long identifier': 123,	'Long method': 12,
	'Long parameter list': 511,	'Long statement': 3687,
	'Magic number': 2415,	'Missing default': 75,
    }

dictionary_analysis_summary_v_3_11_11 = {'Total LOC analyzed': 199133, 'Number of packages': 93,
	'Number of classes': 2645, 'Number of methods': 26183}

dictionary_architecture_smell_v_3_11_11 = {'Cyclic dependency': 229, 'God component': 32, 
	'Ambiguous interface': 0, 'Feature concentration': 74, 
	'Unstable dependency': 47, 'Scattered functionality': 4, 
	'Dense structure': 1}

dictionary_design_smell_v_3_11_11 = {'Imperative abstraction': 6, 'Multifaceted abstraction': 14, 
	'Unnecessary abstraction': 22, 'Unutilized abstraction': 1803, 
	'Feature envy': 0, 'Deficient encapsulation': 684, 
	'Unexploited encapsulation': 0, 'Broken modularization': 4, 
	'Cyclically-dependent modularization': 65, 	'Hub-like modularization': 7, 
	'Insufficient modularization': 227, 'Broken hierarchy': 27,
	'Cyclic hierarchy': 3, 	'Deep hierarchy': 0,
	'Missing hierarchy': 0,	'Multipath hierarchy': 0,
	'Rebellious hierarchy': 2,	'Wide hierarchy': 0}

dictionary_analysis_summary_v_3_11_11 = {'Total LOC analyzed': 199133, 'Number of packages': 93,
	'Number of classes': 2645, 'Number of methods': 26183}

dictionary_architecture_smell_v_3_11_11 = {'Cyclic dependency': 229, 'God component': 32, 
	'Ambiguous interface': 0, 'Feature concentration': 74, 
	'Unstable dependency': 47, 'Scattered functionality': 4, 
	'Dense structure': 1}

dictionary_design_smell_v_3_11_11 = {'Imperative abstraction': 6, 'Multifaceted abstraction': 14, 
	'Unnecessary abstraction': 22, 'Unutilized abstraction': 1803, 
	'Feature envy': 0, 'Deficient encapsulation': 684, 
	'Unexploited encapsulation': 0, 'Broken modularization': 4, 
	'Cyclically-dependent modularization': 65, 	'Hub-like modularization': 7, 
	'Insufficient modularization': 227, 'Broken hierarchy': 27,
	'Cyclic hierarchy': 3, 	'Deep hierarchy': 0,
	'Missing hierarchy': 0,	'Multipath hierarchy': 0,
	'Rebellious hierarchy': 2,	'Wide hierarchy': 0}

dictionary_log_analise_v_3_1_0['analysis summxary'] = dictionary_analysis_summxary_v_3_1_0
dictionary_log_analise_v_3_1_0['architecture smell'] = dictionary_architecture_smell_v_3_1_0
dictionary_log_analise_v_3_1_0['design smell'] = dictionary_design_smell_v_3_1_0
dictionary_log_analise_v_3_1_0['implementation_smell'] = dictionary_implementation_smell_v_3_1_0

dictionary_log_analise_v_3_11_11['analysis summary'] = dictionary_analysis_summary_v_3_11_11
dictionary_log_analise_v_3_11_11['architecture smell'] = dictionary_architecture_smell_v_3_11_11
dictionary_log_analise_v_3_11_11['design smell'] = dictionary_design_smell_v_3_11_11

## Architectural Smells
texto_padrao_Cyclic_Dependency = "The tool detected the smell in this component because this component participates in a cyclic dependency. The participating components in the cycle are:"
texto_padrao_God_Component = "The tool detected the smell in this component because the component contains high number of classes. Number of classes in the component are:"
texto_padrao_Feature_Concentration = "The tool detected the smell in this component because the component realizes more than one architectural concern/feature. Independent sets of related classes within this component are:"
texto_padrao_Unstable_Dependency = "The tool detected the smell in this component because this component depends on other components that are less stable than itself. This component depends on following less stable component(s):"
texto_padrao_Scattered_functionality = "The tool detected the smell in this component because a set of two or more components realizes the same high-level architectural concern. Following components realize the same concern:"
texto_padrao_Dense_structure = "The tool detected the smell because all the analyzed components exhibit excessive and dense dependencies among themselves."

## Design Smells
texto_padrao_Broken_modularization = "The tool detected the smell in this class because it contains only data members without any method implementation."
texto_padrao_Cyclically_dependent_Modularization = "The tool detected the smell in this class because this class participates in a cyclic dependency."
texto_padrao_Insufficient_Modularization = "The tool detected the smell in this class becuase the class has bloated interface (large number of public methods)."
texto_padrao_Hub_like_Modularization = "The tool detected the smell in this class because this class has high number of incoming as well as outgoing dependencies."

def init_df_architecture_smell_analysis(versao, path=None):
    df_architecture_smells = None
    
    if versao == '3.1.0':
        if path is None:
          path = PATH_DESIGNITE_RESULTS_V_3_1_0
        df_architecture_smells = pd.read_csv(filepath_or_buffer=path + '/' + 'ArchitectureSmells.csv', sep=',', encoding='utf-8')
    
    if versao == '3.11.11':
        if path is None:
          path = PATH_DESIGNITE_RESULTS_V_3_11_11
        df_architecture_smells = pd.read_csv(filepath_or_buffer=path + '/' + 'ArchitectureSmells.csv', sep=',', encoding='utf-8')
        
    return df_architecture_smells

def init_df_design_smell_analysis(versao, path=None):
    df_design_smells = None

    if versao == '3.1.0':
        if path is None:
          path = PATH_DESIGNITE_RESULTS_V_3_1_0
        df_design_smells = pd.read_csv(filepath_or_buffer=path + '/' + 'DesignSmells.csv', sep=',', encoding='utf-8')
    
    if versao == '3.11.11':
        if path is None:
          path = PATH_DESIGNITE_RESULTS_V_3_11_11
        df_design_smells = pd.read_csv(filepath_or_buffer=path + '/' + 'DesignSmells.csv', sep=',', encoding='utf-8')
    
    return df_design_smells

def init_df_100_arquivos_mais_modificados(versao, path=None):
    df_arquivos_modificados = None

    if versao == '3.1.0':
      if path is None:
        path = PATH_ARQUIVOS_MODIFICADOS_V_3_1_0
      df_arquivos_modificados = pd.read_csv(filepath_or_buffer=path + '/' + 'df_100_arquivos_mais_modificados.csv', sep=',', encoding='utf-8')
    
    if versao == '3.11.11':
      if path is None:
        path = PATH_ARQUIVOS_MODIFICADOS_V_3_11_11
      df_arquivos_modificados = pd.read_csv(filepath_or_buffer=path + '/' + 'df_100_arquivos_mais_modificados.csv', sep=',', encoding='utf-8')

    return df_arquivos_modificados

def extract_list_of_architecture_smells(df_architecture_smells, texto_padrao):
    list_temp = []
    for index, row in df_architecture_smells.iterrows():
        if texto_padrao in row['Cause of the Smell']:
            texto_temp = row['Cause of the Smell']
            texto_temp = texto_temp.replace(texto_padrao, '')
            elemento = (row['Package Name'], row['Architecture Smell'], texto_temp)
            list_temp.append(elemento)
    return list_temp

def extract_list_of_design_smells(df_design_smells, design_smell):
    list_temp = []
    for index, row in df_design_smells.iterrows():
        if design_smell == row['Design Smell']:
            elemento = (row['Package Name'], row['Type Name'], row['Design Smell'], row['Cause of the Smell'])
            list_temp.append(elemento)
    return list_temp

def generate_dictionary_filename_modifications(df_arquivos_modificados):
    lista_filename = df_arquivos_modificados['name']
    conjunto_filename = list(set(lista_filename.tolist()) )
    conjunto_filename.sort()

    dictionary_filename_modifications = {}
    for each in conjunto_filename:
        #print(f'Escaneia modificações de {each}')
        lista_aux = []
        for index, row in df_arquivos_modificados.iterrows():
            if each == row['name']:
                elemento = (row['hash'], row['date'], row['modifications'], row['nloc'], row['complexity'])
                lista_aux.append(elemento)
        dictionary_filename_modifications[each] = lista_aux
    return dictionary_filename_modifications


def generate_df_file_tempo_modifications(file, dictionary_filename_modifications):
    lista_commits = []
    lista_tempo = []
    lista_modifications = []
    lista_loc = []
    lista_complexidade = []

    for k, values in dictionary_filename_modifications.items():
        if k == file:
            for v in values: 
                lista_commits.append(v[0])
                lista_tempo.append(v[1])
                lista_modifications.append(v[2])
                lista_loc.append(v[3])
                lista_complexidade.append(v[4])

    df_x_tempo_modifications = pd.DataFrame({'tempo':lista_tempo, 'modifications':lista_modifications})

    return df_x_tempo_modifications

def generate_df_file_tempo_loc(file, dictionary_filename_modifications):
    lista_commits = []
    lista_tempo = []
    lista_modifications = []
    lista_loc = []
    lista_complexidade = []

    for k, values in dictionary_filename_modifications.items():
        if k == file:
            for v in values: 
                lista_commits.append(v[0])
                lista_tempo.append(v[1])
                lista_modifications.append(v[2])
                lista_loc.append(v[3])
                lista_complexidade.append(v[4])

    df_x_tempo_loc = pd.DataFrame({'tempo':lista_tempo, 'loc':lista_loc})

    return df_x_tempo_loc

def generate_df_file_tempo_complexidade(file, dictionary_filename_modifications):
    lista_commits = []
    lista_tempo = []
    lista_modifications = []
    lista_loc = []
    lista_complexidade = []

    for k, values in dictionary_filename_modifications.items():
        if k == file:
            for v in values: 
                lista_commits.append(v[0])
                lista_tempo.append(v[1])
                lista_modifications.append(v[2])
                lista_loc.append(v[3])
                lista_complexidade.append(v[4])

    df_x_tempo_complexidade = pd.DataFrame({'tempo':lista_tempo, 'complexidade':lista_complexidade})

    return df_x_tempo_complexidade

def extract_list_of_arquivos_modifiados(df_arquivos_modificados):
    list_temp = []
    for index, row in df_arquivos_modificados.iterrows():
        if row['old_path'] == row['new_path']:
            path = row['new_path']
            path = path.replace('src/java/', '')
            path = path.replace('/', '.')
            path = path.replace('.' + row['name'], '')
        else:
            path = None
        elemento = (row['index'], row['name'], row['hash'], row['modifications'], row['change_type'], row['nloc'], row['complexity'], path)
        list_temp.append(elemento)
    return list_temp
