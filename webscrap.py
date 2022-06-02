from bs4 import BeautifulSoup
import requests
import zipfile

arquivosParaZip = []

html = requests.get("https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude").content
soup = BeautifulSoup(html, 'html.parser')
#Arquivos estão na tag <p> com o nome da classe "callout"
links = soup.find_all("p", {'class':'callout'})

for link in links:
    if link.text.startswith("Anexo"):
        #Pega a url que está no elemento <a>
        urlDoArquivo = link.a.get('href')
        nome_e_formato_arquivo = link.text+'.'+link.a.get('href').split('.')[-1]
        arquivo = requests.get(urlDoArquivo)

        try:
            with open(nome_e_formato_arquivo, 'wb') as f:
                print("Baixando o arquivo: " +nome_e_formato_arquivo)
                f.write(arquivo.content)
                arquivosParaZip.append(nome_e_formato_arquivo)
        except:
            print("Falha ao processar "+nome_e_formato_arquivo)

#Compacta os arquivos baixados
if (len(arquivosParaZip) != 0):
    print("Compactando arquivos baixados...")
    with zipfile.ZipFile("Anexos.zip", mode="w") as zip:
        for arquivo in arquivosParaZip:
            zip.write(arquivo)

print("Concluído")
