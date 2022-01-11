import time
import os
import pygetwindow
import pyautogui
from consultas_funcoes import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BotsPje():
    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.dados_uf = None
        self.uf: str = None
        self.url_final: str = ''

    def reseta_variaveis(self):
        self.dados_uf = None
        self.uf: str = None
        self.url_final = None

    def aguardar_carregamento(self):
        while True:
            try:
                time.sleep(1)
                carregamento = self.web_driver.find_element(By.ID, '_viewRoot:status.start').get_attribute('style')
                if carregamento == 'display: none;':
                    break
            except:
                continue

    def dados_por_uf(self, codigo_cpj):
        dicionario_dados_uf = {
            '8.05': {
                'url': 'https://consultapublicapje.tjba.jus.br/pje/ConsultaPublica/listView.seam',
                'uf': 'BA'
            },
            '8.07': {
                'url': 'https://pje.tjdft.jus.br/consultapublica/ConsultaPublica/listView.seam',
                'uf': 'DF'
            },
            '8.08': {
                'url': 'https://sistemas.tjes.jus.br/pje/ConsultaPublica/listView.seam',
                'seletor_consulta': 'a[onclick*="/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]',
                'uf': 'ES',
                'url_parcial': 'https://sistemas.tjes.jus.br'
            },
            '8.10': {
                'url': 'https://pje.tjma.jus.br/pje/ConsultaPublica/listView.seam',
                'uf': 'MA',
                'seletor_consulta': 'a[onclick*="/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]',
                'url_parcial': 'https://pje.tjma.jus.br/pje/ConsultaPublica/listView.seam'
            },
            '8.13': {
                'url': 'https://pje-consulta-publica.tjmg.jus.br/',
                'uf': 'MG'
            },
            '8.11': {
                'url': 'https://pje.tjmt.jus.br/pje/ConsultaPublica/listView.seam',
                'uf': 'MT'
            },
            '8.15': {
                'url': 'https://pje.tjpb.jus.br/pje/ConsultaPublica/listView.seam',
                'uf': 'PB',
                'seletor_consulta': 'a[onclick*="/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]',
                'url_parcial': 'https://pje.tjpb.jus.br'
            },
            '8.17': {
                'url': 'https://pje.app.tjpe.jus.br/1g/ConsultaPublica/listView.seam',
                'uf': 'PE'
            },
            '8.18': {
                'url': 'https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam',
                'uf': 'PI'
            },
            '8.20': {
                'url': 'https://pje1g.tjrn.jus.br/pje/ConsultaPublica/listView.seam',
                'uf': 'RN'
            },
            '8.22': {
                'url': 'https://pjepg.tjro.jus.br/consulta/ConsultaPublica/listView.seam',
                'uf': 'RO',
                'seletor_consulta': 'a[onclick*="/consulta/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]',
                'url_parcial': 'https://pjepg.tjro.jus.br'
            }
        }
        try:
            return dicionario_dados_uf[codigo_cpj]
        except:
            return codigo_cpj

    def iniciar_consulta_publica(self, codigo_cpj):
        self.dados_uf = self.dados_por_uf(codigo_cpj)
        try:
            self.web_driver.get(self.dados_uf['url'])
        except:
            return False

    def consultar_processo(self, num_proc):
        evitar_encontrado = self.web_driver.find_elements(By.CLASS_NAME, 'text-muted')[-1].text
        input_processo = self.web_driver.find_element(By.ID, 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso')
        espere_ate(input_processo.send_keys(num_proc + Keys.ENTER))
        resultado_busca = self.verificar_processo(evitar_encontrado)
        return resultado_busca

    def verificar_processo(self, evitar_encontrado):
        # VERIFICAÇÃO SE ENCONTRA PROCESSO (0-1 PROCESSOS ENCONTRADOS)
        while True:
            try:
                processo_encontrado = self.web_driver.find_elements(By.CLASS_NAME, 'text-muted')[-1].text
                if processo_encontrado != evitar_encontrado:
                    break
            except:
                continue

        if '0' in processo_encontrado:
            return 0
        elif '1' in processo_encontrado:
            url_consulta = self.web_driver.find_element(By.CSS_SELECTOR, 'a[onclick*="/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca="]').get_attribute('onclick').split(',')[1].replace("'", '').replace(')', '')
            self.url_final = self.dados_uf['url_parcial']+url_consulta
            return 1

    def abrir_processo(self):
        self.web_driver.find_element(By.CLASS_NAME, "fa-external-link").click()
        while True:
            try:
                tabs = self.web_driver.window_handles
                if len(tabs) >= 2:
                    self.web_driver.switch_to.window(tabs[1])
                    break
            except:
                try:
                    time.sleep(0.3)
                    self.web_driver.switch_to.alert().accept()
                except:
                    continue
        espere_ate(self.web_driver.find_element(By.ID, 'pesquisar_lbl'))

    def fechar_processo(self):
        tabs = self.web_driver.window_handles
        self.web_driver.close()
        self.web_driver.switch_to.window(tabs[0])

    def coletar_movimentacoes(self, pandas, processo):
        try:
            movimentacoes = self.web_driver.find_elements(By.CSS_SELECTOR, 'span[id*=":processoEvento:"]')
            for index, movimentacao in enumerate(movimentacoes):
                movimentacao_div = movimentacao.text.split(' - ')
                if index == 0:
                    lista_dados = [processo, self.dados_uf['uf'], movimentacao_div[1], movimentacao_div[0], 'Consulta Realizada', 'URL']
                else:
                    lista_dados = [processo, self.dados_uf['uf'], movimentacao_div[1], movimentacao_div[0], '', '']
                pandas.anotar_consulta(lista_dados)
        except Exception as e:
            return e
