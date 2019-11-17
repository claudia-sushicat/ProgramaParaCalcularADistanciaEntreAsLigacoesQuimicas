# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:16:48 2019

@author: CASA
"""

import sqlite3
import json
import math

conexao = sqlite3.connect('elementos.db')
leitor = conexao.cursor() #le e executar codigo

def cadastra_elemento(nome, sigla, categoria, raio, configuracao_eletronica):
    leitor.execute("INSERT INTO elementos (nome, sigla, categoria, raio, configuracao_eletronica) VALUES(?,?,?,?,?)", (nome, sigla, categoria, raio, configuracao_eletronica))

def cria_tabela():
    tabela_periodica = json.load(open("PeriodicTableJSON.json"))["elements"] 
    for elemento in tabela_periodica:
        print(elemento["name"])
        cadastra_elemento(elemento["name"], elemento["symbol"], elemento["category"], 0, elemento["electron_configuration"])
        conexao.commit()
        
def consulta_elemento(sigla):
    return leitor.execute("SELECT * FROM elementos where upper(sigla) = '"+ sigla.upper() + "'").fetchall()[0]

def consulta_nox(sigla):
    return leitor.execute("SELECT nox FROM tabela_de_nox where upper(sigla) = '"+ sigla.upper() + "' ORDER by nox ").fetchall()

print('Esse programa consiste em calcular a distancia entre as ligações do atomo central de uma molécula aos adjacentes')

def comparar_elementos(elemento1, elemento2):   
    #elemento1 = consulta_elemento(input('Digite um elemento: ').upper())
    #elemento2 = consulta_elemento(input('Digite outro elemento: ').upper())
    if (elemento1[5] == "ametal" and elemento2[5] == "metal") or (elemento2[5] == "ametal" and elemento1[5] == "metal"):
        print('ligação ionica') 
        return {'tipo_ligacao': "ionica", 'n_eletrons1': conta_eletrons_ultima_camada(elemento1[4].split(" ")), 'n_eletrons2': conta_eletrons_ultima_camada(elemento2[4].split(" "))}
    elif (elemento1[5] == "gas nobre" or elemento2[5] == "gas nobre"): 
        print('Inválido. Gases nobres já são estaveis por isso nao se associam com outros elementos')
        return comparar_elementos()
    elif (elemento1[5] == "ametal" and elemento2[5] =="ametal"):
        print('ligação covalente')
        return {'tipo_ligacao': "covalente", 'n_eletrons1': conta_eletrons_ultima_camada(elemento1[4].split(" ")), 'n_eletrons2': conta_eletrons_ultima_camada(elemento2[4].split(" "))}
    elif (elemento1[5] == "lantanideos" or elemento2[5] == "lantanideos"):
        print('Inválido. Lantanideos não possuem raios atomicos constatados, isso se deve a natureza artificial dos mesmos. São instaveis. Existem por frações de segundos')
        return comparar_elementos()
    elif (elemento1[5] == "actinideos" or elemento2[5] == "actinideos"):
        print('Inválido. Actinideos não possuem raios atomicos constatados, isso se deve a natureza artificial dos mesmos. São instaveis. Existem por frações de segundos')
        return comparar_elementos()
    
def conta_eletrons_ultima_camada(distribuicao):
    if(distribuicao[0] == "1s1"): 
        return 1
    n_ultima_camada = distribuicao[len(distribuicao) - 1][0]
    soma = 0
    for camada in range(len(distribuicao) - 1, 0, -1):
        if(distribuicao[camada][0] == n_ultima_camada):
            soma += int(distribuicao[camada][2])
    return soma  

elemento1 = consulta_elemento(input('Digite um elemento: '))
elemento2 = consulta_elemento(input('Digite outro elemento: '))

resultado = comparar_elementos(elemento1, elemento2)
print(resultado) #valores = ["tipo_ligacao","n_eletrons1", "n_eletrons2"]


#comentei tudo oq eu fui fazendo pq se não eu mesma não ia entender oq eu tava fazendo

def determinar_formula(elemento1, elemento2):
    nox1 = []
    consulta_nox1 = consulta_nox(elemento1[2])
    
    for i in range(0,len(consulta_nox1)):
        nox1.append(consulta_nox1[i][0])

    print("Nox do(a)", elemento1[2], ":", nox1)

    nox2 = []
    consulta_nox2 = consulta_nox(elemento2[2])
    
    for i in range(0,len(consulta_nox2)):
        nox2.append(consulta_nox2[i][0])

    print("Nox do(a)", elemento2[2], ":", nox2)
    
    #dai ce vai ter q mudar tudo DKNASKDNASDKL pq tem mais de um nox boa parte dos elementos
    
    soma_nox = nox1[0] + nox2[0] #somo os nox dos elementos
    n_elemento1 = 1 #número de vezes que o elemento 1 se repete
    n_elemento2 = 1 #número de vezes que o elemento 2 se repete

    while(soma_nox != 0): #enquanto a soma do nox não for 0
        if(math.fabs(nox1[0]) < math.fabs(nox2[0])): #se módulo do nox 1 é menor que o módulo do nox 2
            n_elemento1 = n_elemento1 + 1 #somo 1 na quantidade de vezes que o elemento 1 se repete
            soma_nox = soma_nox + nox1[0] #calculo nova soma do nox
 
        else: #se módulo do nox 2 for menor que o módulo do nox 1
            n_elemento2 = n_elemento2 + 1 #somo mais um na quantidade de vezes que o elemento 2 se repete
            soma_nox = soma_nox + nox2[0] #calculo nova soma do nox

    if(nox2[0] < 0): #se o nox do elemento2 for negativo
        mais_el = elemento2[2]
        n_mais_el = str(n_elemento2)

        menos_el = elemento1[2]
        n_menos_el = str(n_elemento1)

    else: #se o nox do elemento 1 for negativo
        mais_el = elemento1[2]
        n_mais_el = str(n_elemento1)

        menos_el = elemento2[2]
        n_menos_el = str(n_elemento2)

    print(menos_el, n_menos_el, mais_el, n_mais_el)

    formula = menos_el + n_menos_el + mais_el + n_mais_el

    for i in range(0, len(formula)):
        if(formula[i] == "1"):
            formula = formula.replace(formula[i], "")
            break
        
    if nox1 > nox2:
        print(elemento1[2] + ', é um cation e ' + elemento2[2] +' é um anion')
    else:
        print(elemento1[2] + ', é um anion e ' + elemento2[2] + 'é um cation')
    

    return formula



    
    
def calcular_distancia(elemento1, elemento2):
    return (elemento1[3] + elemento2[3]) /2 


print("Fórmula:", determinar_formula(elemento1, elemento2))
print("Distância:", calcular_distancia(elemento1, elemento2), "pm")





