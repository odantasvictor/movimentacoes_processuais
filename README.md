# Automação - Captura de movimentações processuais - PJE

## Sumário
- [Sobre](#sobre)
- [Orientações de uso](#orientacoes)
- [Arquitetura e Funcionalidade](#funcionalidade)
- [Demonstração](#demonstracao)
- [Versões](#versoes)

<div id="sobre"/>

## Sobre
Trata-se de automação (bot) construída em Python, que realiza consultas processuais, através da consulta pública, e realiza a captura das últimas movimentações (data, hora e movimentação), preenchendo os dados em uma planilha do tipo excel (.xlsx).

<div id="orientacoes"/>

## Orientações de uso -> OBRIGATÓRIO
### Bibliotecas:
* A  automação utiliza a biblioteca Selenium, tendo suporte para todas as versões 3.141.0 ou as mais atuais 4+, dentre outras.
* O chromedriver é instalado dinamicamente, para tanto é necessário a instalação da lib chromedriver-autoinstaller
* Para gestão da planilha é utilizado a biblioteca pandas, em qualquer versão da lib.
* As outras bibliotecas já instaladas já são padrões do Python, entre elas: json; os; datetime

### Utilização:
* A automação consome uma planilha que deve ser nomeada com a data do dia, em formato dd-mm-aaaa, como por exemplo: 07-11-2021.xlsx
* A referida planilha deve estar dentro da pasta C:/consulta_pje
* Os números dos processos devem estar preenchidos na primeira coluna, em linhas separadas, podendo estar em formato apenas numérico ou com seus devidos caracteres especiais (ex.: 08020154020208150251 ou 0802015-40.2020.8.15.0251)
* A primeira linha da planilha deve conter o nome Processos
* Os processos devem pertencer, obrigatoriamente, a qualquer UF que utilize o sistema PJE - CNJ.

<div id="funcionalidade"/>

## Arquitetura e Funcionalidade
### Arquitetura
A automação foi desenvolvida em uma estrutura a evitar falhas/pausas(parciais ou totais) da automação, tendo diversas características essenciais:
* Adaptação a instabilidade do sistema (caso o sistema esteja mais lento ou mais rápido, a adaptação irá se adaptar ao surgimento dos elementos e interagir com eles assim que possível for);
* Estrutura de repetição (caso aconteça algum erro durante a captura das movimentações, a automação realizará uma nova tentativa de captura no mesmo processo);
* Verificação de duplicidade (caso seja necessário pausar a automação e retomá-la posteriormente, ela não realizará a consulta no mesmo processo, mantendo a planilha de resultados enxuta);

### Desempenho:
<b>São realizadas, em média, entre 15-20 consultas por minuto, ou seja, entre 900-1200 consultas por hora</b> (estes números podem variar para mais ou para menos, de acordo com a velocidade do sistema).

### Resultado:
Os resultados da consulta serão cadastrados em uma planilha, nomeada com a data padrão dd-mm-aaaa-consultas.xlsx, ficando o arquivo disponível no caminho: C:/consulta_pjepb

<div id="versoes"/>

## Versões
* v1.0 - A versão 1 utilizava a biblioteca openpyxl para tratamento dos arquivos XLSX (leitura e anotações);
* v2.0 - A versão 2 utiliza a biblioteca pandas para tratamento dos arquivos XLSX (leitura e anotações), permitindo grande avanço na OO e limpeza do código.

<div id="demonstracao"/>

## Demonstração
[![Vídeo de desempenho disponível](https://user-images.githubusercontent.com/87952070/140660877-507cefee-2009-49cf-9c16-7ca47f257876.png)
](https://youtu.be/bO7ZXjKHlY4)
