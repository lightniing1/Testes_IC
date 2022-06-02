import os
import tabula
import pandas as pd
import csv
import zipfile


diretorio = os.listdir()
tabela_pdf = ""
tabela_csv = "anexo1.csv"
palavra_abreviada = {"OD": "Seg. Odontologica", "AMB":"Seg. Ambulatoria"}

#Procura no diretorio do script se existe o Anexo I em formato pdf
for arquivo in diretorio:
    if (arquivo.startswith("Anexo I ") and (arquivo.split(".")[-1] == "pdf")): 
        tabela_pdf = arquivo

if (tabela_pdf != ""):
    #Deve retornar uma lista de dataframes do pandas
    print("Extraindo tabelas do pdf...")
    df = tabula.read_pdf(tabela_pdf, encoding='utf-8', pages='all')

    #Substitue as palavras nos dataframes de acordo o dicionario
    print("Substituindo abreviacoes...")
    for palavra in palavra_abreviada.keys():
        for i in range(len(df)):
            df[i].replace(to_replace = palavra, value = palavra_abreviada[palavra], inplace = True)

    #Unifica os dataframes e salva em .csv
    df = pd.concat(df)
    df.to_csv(tabela_csv, encoding='utf-8', index=False)

    print("Compactando arquivo...")
    with zipfile.ZipFile("Teste_DanielOliveira.zip", mode="w") as zip:
        zip.write(tabela_csv)
    
    print("Concluído")

else:
    print("Não foi possível achar o arquivo Anexo I em pdf")