from consultas_funcoes import *
from consultas_classesmetod import *
import os
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Testes
line = '-------------------------------------------------------'

# Date Config
date_func = datetime.now()
date_today = date_func.strftime('%d-%m-%Y')

# Directorys Config
directory_path = f'C:\\consulta_pjepb'
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Configuração da Planilha
pc = ConfigXlsx
planilha_caminho = f'{directory_path}\\{date_today}-consultas.xlsx'
planilha_arquivo = pc.ler_criar_xlsx(planilha_caminho)
planilha_principal = pc.planilha_principal(planilha_arquivo)
lista_cabecalho = ['Número Processo', 'Prognóstico', 'Data Movimentação', 'Movimentação', 'URL']
pc.criar_cabecalho(lista_cabecalho, planilha_principal, planilha_arquivo, planilha_caminho)
linha_atual = pc.linha_planilha(planilha_principal)

#  WebDriver Constructor
driver = ConfigDriver
web_driver = driver.driver_config(directory_path)

# Leitura de planilha para consulta e verificação de duplicidade (já consultados)
leitura_caminho = f'{directory_path}\\{date_today}.xlsx'
leitura_arquivo = pc.ler_criar_xlsx(leitura_caminho)
leitura_principal = pc.planilha_principal(leitura_arquivo)

# MONTAGEM DE LISTA DOS PROCESSOS JÁ CONSULTADOS
ja_consultados = []
for linha in planilha_principal:
    if not linha[0].value in ja_consultados:
        ja_consultados.append(linha[0].value)

# MONTAGEM DE LISTA DOS PROCESSOS A CONSULTAR
a_consultar = []
a_consultar_contador = 0
for linha in leitura_principal:
    try:
        if len(linha[0].value) == 25 or len(linha[0].value) == 20 and linha[0].value.isnumeric():
            if not linha[0].value in ja_consultados:
                a_consultar.append(linha[0].value)
                a_consultar_contador += 1
    except:
        continue

# Iniciando PJE PB CONSULTA PUBLICA
print('Iniciando consultas processuais para UF - PB')
print(line)

# Início do Loop principal
consulta_refazer = False
contador_atual = 0
while True:
    try:
        if not consulta_refazer:

            web_driver.get('https://pje.tjpb.jus.br/pje/ConsultaPublica/listView.seam')

            # TRATAMENTO Nº DO PROCESSO
            num_proc = formata_numproc(a_consultar[contador_atual])
            if num_proc['sucesso'] == 1: 
                processo = num_proc['num_proc']
            else:
                dados_planilha = [processo, 'Número de processo inválido']
                pc.escrever_planilha(planilha_principal, planilha_arquivo, planilha_caminho, 2, linha_atual, dados_planilha)
                linha_atual += 1
                contador_atual += 1
                print(line)
                continue

        # BUSCA DO PROCESSO
        print(f'Processo: {processo}')
        evitar_encontrado = web_driver.find_elements(By.CLASS_NAME, 'text-muted')[-1].text
        input_processo = web_driver.find_element(By.ID, 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso')
        espere_ate(input_processo.send_keys(processo + Keys.ENTER))
        
        # VERIFICAÇÃO SE ENCONTRA PROCESSO (0-1 PROCESSOS ENCONTRADOS)
        while True:
            try:
                processo_encontrado = web_driver.find_elements(By.CLASS_NAME, 'text-muted')[-1].text
                if processo_encontrado != evitar_encontrado:
                    break
            except:
                continue

        # CAPTURA DE URL
        if '0' in processo_encontrado:
            print("Processo não encontrado.")
            dados_planilha = [processo, 'Número de processo não encontrado']
            pc.escrever_planilha(planilha_principal, planilha_arquivo, planilha_caminho, 2, linha_atual, dados_planilha)
            linha_atual += 1
            contador_atual += 1
            print(line)
            continue
        elif '1' in processo_encontrado:
            url = web_driver.find_element(By.CSS_SELECTOR, 'a[onclick*="/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]').get_attribute('onclick').split(',')[1].replace("'", '').replace(')', '')
            url_final = f'https://pje.tjpb.jus.br{url}'

        # PROCESSO ENCONTRADO, ABERTURA DA JANELA
        web_driver.find_element(By.CLASS_NAME, "fa-external-link").click()

        # TENTATIVA CLICAR EM BOTÃO ALERT OU VERIFICA SE ABRIU NOVA ABA
        while True:
            try:
                tabs = web_driver.window_handles
                if len(tabs) >= 2:
                    web_driver.switch_to.window(tabs[1])
                    break
            except:
                try:
                    time.sleep(0.3)
                    web_driver.switch_to.alert().accept()
                except:
                    continue

        # CAPTURA DO BLOCO DE MOVIMENTAÇÕES
        espere_ate(web_driver.find_element(By.ID, 'pesquisar_lbl'))
        movimentacoes = web_driver.find_elements(By.CSS_SELECTOR, 'span[id*=":processoEvento:"]')
        for num_mov, movimentacao in enumerate(movimentacoes):
            movimentacao = movimentacao.text.split(' - ')
            if num_mov == 0:
                dados_planilha = [processo, 'Consulta realizada', movimentacao[0], movimentacao[1], url_final]
                pc.escrever_planilha(planilha_principal, planilha_arquivo, planilha_caminho, 5, linha_atual, dados_planilha)
            else:
                dados_planilha = [processo, '', movimentacao[0], movimentacao[1]]
                pc.escrever_planilha(planilha_principal, planilha_arquivo, planilha_caminho, 4, linha_atual, dados_planilha)
            linha_atual += 1

        print('Movimentações registradas com sucesso.')
        # TRATAMENTO DE VARIÁVEIS
        contador_atual += 1
        consulta_realizada = True
        consulta_refazer = False

        # FECHA ABA DE CONSULTA E CONCLUSÃO
        web_driver.close()
        web_driver.switch_to.window(tabs[0])
        print(line)

    # FIM DA LISTA DE CONSULTA    
    except IndexError:
        if len(a_consultar) == 0:
            print('Não há processos a consultar. Verificar planilha de consultas.')
            break
        else:
            print('Consultas finalizadas.')
            break

    # SISTEMA DE NOVA TENTATIVA
    except Exception as e:
        tabs = web_driver.window_handles
        # CONSULTA NÃO REALIZADA, HABILITA NOVA CONSULTA (NÃO PUXA NOVOS DADOS)
        if not consulta_refazer and not consulta_realizada:
            consulta_refazer = True
            print('Ocorreu um erro nesse processo. Realizando nova tentativa.')
            if len(tabs) >= 2:
                web_driver.close()
                web_driver.switch_to_window(tabs[0])
            continue
        # APÓS NOVA TENTATIVA, REGISTRA ERRO NA PLANILHA E SEGUE PARA PRÓXIMO
        elif consulta_refazer and not consulta_realizada:
            dados_planilha = [processo, 'Erro em 2 tentativas']
            pc.escrever_planilha(planilha_principal, planilha_arquivo, planilha_caminho, 2, linha_atual, dados_planilha)
            linha_atual += 1
            contador_atual += 1
            if len(tabs) >= 2:
                web_driver.close()
                web_driver.switch_to_window(tabs[0])
            continue
        # ERRO FINAL, MAS JÁ APÓS REALIZADA A CONSULTA, SEGUE PARA O PRÓXIMO
        else:
            print('Erro. Consulta já realizada.')
            contador_atual += 1
            if len(tabs) >= 2:
                web_driver.close()
                web_driver.switch_to_window(tabs[0])
            continue
        
web_driver.quit()