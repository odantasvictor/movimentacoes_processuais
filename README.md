# Automação - Captura de movimentações processuais - PJE

## Sumário
- [Sobre](#sobre) 
- [Orientações de uso](#orientacoes)
- [Arquitetura e Funcionalidade](#funcionalidade)
- [Demonstração](#demonstracao)
- [Versões](#versoes)

<div id="sobre"/>

## Sobre
Trata-se de automação (bot) construída em Python 3x, que realiza consultas processuais, através da consulta pública, e realiza a captura das últimas movimentações (data, hora e movimentação), preenchendo os dados em uma planilha do tipo excel (.xlsx) ou em banco de dados MySQL.

<div id="orientacoes"/>

## Orientações de uso -> OBRIGATÓRIO
### Bibliotecas:
* Python 3x+, devendo atentar-se ao suporte das libs (consulta disponível no pyreadiness.org)
* A automação utiliza a biblioteca Selenium, tendo suporte para todas as versões 3.141.0 ou as mais atuais 4+, dentre outras.
* O chromedriver é instalado dinamicamente, para tanto é necessário a instalação da lib webdriver-manager (anteriormente utilizada a lib chromedriver-autoinstaller)
* Para gestão da planilha é utilizada a biblioteca pandas, em qualquer versão da lib.
* Para gestão da utilização do SQL (a partir da versão 3.0) é utilizada a biblioteca mysql
* As outras bibliotecas já instaladas já são padrões do Python, entre elas: json; os; datetime

### Utilização:
* A automação possui suporte para duas formas de funcionamento, via planilha XLSX e via SQL (a partir da versão 3.0)
* Para utilização via XLSX: consome uma planilha que deve ser nomeada com a data do dia, em formato dd-mm-aaaa, como por exemplo: 07-11-2021.xlsx, devendo a referida planilha deve estar dentro da pasta C:/movimentacoes_processuais (a partir da versão 3.0, antes disso C:/consulta_pje)
* A partir da versão 3.0 o caminho padrão da pasta da planilha pode ser livremente alterado em /config/config.ini
* A partir da versão 3.0 há possibilidade de utilização via SQL, devendo ser configurado no arquivo /config/config.ini e com modelo de estrutura de tabelas em /data/database.sql
* Para utilização via XLSX: Os números dos processos devem estar preenchidos na primeira coluna, em linhas separadas, podendo estar em formato apenas numérico ou com seus devidos caracteres especiais (ex.: 08020154020208150251 ou 0802015-40.2020.8.15.0251)
* Para utilização via XLSX: A primeira linha da planilha deve conter o nome Processos
* Para utilização via SQL: Deve existir obrigatoriamente a estrutura SQL contida em /data/database.sql
* Para utilização via SQL: Cada processo é atualizado 1x ao dia, havendo ainda tratamento para evitar duplicidade no lançamento da movimentação ao banco
* Os processos devem pertencer, obrigatoriamente, a qualquer UF que utilize o sistema PJE - CNJ.

<div id="funcionalidade"/>

## Arquitetura e Funcionalidade
### Arquitetura
A automação foi desenvolvida em uma estrutura a evitar falhas/pausas(parciais ou totais) da automação, tendo diversas características essenciais:
* Adaptação a instabilidade do sistema (caso o sistema esteja mais lento ou mais rápido, a adaptação irá se adaptar ao surgimento dos elementos e interagir com eles assim que possível for);
* Verificação de duplicidade (caso seja necessário pausar a automação e retomá-la posteriormente, ela não realizará a consulta no mesmo processo, mantendo a planilha de resultados enxuta);

### Desempenho:
<b>São realizadas, em média, entre 15-20 consultas por minuto, ou seja, entre 900-1200 consultas por hora</b> (estes números podem variar para mais ou para menos, de acordo com a velocidade do sistema).

### Resultado:
Os resultados da consulta serão cadastrados em uma planilha (versão padrão de uso XLSX) nomeada com a data padrão dd-mm-aaaa_resultados.xlsx ou em banco SQL

<div id="versoes"/>

## Versões
* v1.0 - A versão 1 utilizava a biblioteca openpyxl para tratamento dos arquivos XLSX (leitura e anotações);
* v2.0 - A versão 2 utiliza a biblioteca pandas para tratamento dos arquivos XLSX (leitura e anotações), permitindo grande avanço na OO e limpeza do código.
* v3.0 - A versão 3 recebeu grande atualização na estrutura do repositório, tanto de repositório quanto de funcionalidades. O modo de utilização anterior (via XLSX) permanece por padrão, mas também há suporte para utilização via banco de dados, devendo ser configurado no arquivo .ini e com modelo de SQL na pasta /data. A opção entre o tipo de execução (planilha XLSX ou SQL) deve ser atribuída como true no arquivo .ini, devendo a outra ser atribuída como false  (caso contrário executará via planilha por padrão).

<div id="demonstracao"/>

## Demonstração
Funcionamento via SQL
![sql](https://user-images.githubusercontent.com/87952070/202148344-0a2b9fa6-9f5c-4aca-8300-4758103a7cc3.png)

Vídeo (versão 1.0)
[![Vídeo de desempenho disponível](https://user-images.githubusercontent.com/87952070/140660877-507cefee-2009-49cf-9c16-7ca47f257876.png)
](https://youtu.be/bO7ZXjKHlY4)
