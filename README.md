# Consulta Google Analytics

Projeto foi desenvolvido visando atender a necessidade de extração dos dados do analytics.
Nesse projeto foi utilizada a linguagem Python com auxilio do framework Panda.

---------------------
## Passos para instalação do ambiente:

- No site do mongo: https://www.mongodb.com baixar o mongodb e o mongo database-tools.

- Após instalação do mongodb, executar o comando de importação abaixo:
  mongoimport --db dados-google-analytics --collection analytics --file fileName.json
    * fileName.json o caminho bla bla
 
- Instalar o python 3.8.
- Instalar o pip.
- Executar a instalação do pacote pymongo.
  * via comando: pip install pymongo
- Executar a instalação do pacote pandas.
  * via comando: pip install pandas

---------------------
## Execução do programa:

- Baixar os fontes via git:
  git clone 'path'
- Executar o comando:
  python main.py
---------------------
## Informações adicionais:

Neste repositório também é possível encontrar o MER (modelo entidade relacionamento) do Google Analytics
