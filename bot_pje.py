import time
from base.util import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BotPje:

    def __init__(self, web_driver: webdriver) -> None:
        self._web_driver = web_driver
        self.dados_uf = None
        self.uf: str = None
        self.url_final: str = ''

    def reseta_variaveis(self):
        self.dados_uf = None
        self.uf: str = None
        self.url_final = None

    def aguardar_carregamento(self) -> None:
        while True:
            try:
                time.sleep(1)
                carregamento = self._web_driver.find_element(By.ID, '_viewRoot:status.start').get_attribute('style')
                if carregamento == 'display: none;':
                    return
            except:
                continue

    def iniciar_consulta_publica(self, url_consulta: str) -> None:
        self._web_driver.get(url_consulta)
        while True:
            try:
                self._web_driver.find_element(By.ID, 'barraSuperiorPrincipal')
                return
            except:
                continue

    def realizar_consulta_processo(self, numero_processo: str) -> None:
        while True:
            try:
                input_processo = self._web_driver.find_element(By.ID, 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso')
                input_processo.clear()
                input_processo.send_keys(numero_processo + Keys.ENTER)
                return
            except:
                continue

    def verificar_resultado_consulta(self) -> bool:
        sleep_time = 0
        while True:
            try:
                if sleep_time == 20:
                    return False
                verificacao_processo = self._web_driver.find_elements(By.CLASS_NAME, 'text-muted')[-1].text.split(' ')[0]
                if verificacao_processo.isnumeric():
                    if verificacao_processo == '1':
                        return True
                    elif verificacao_processo == '0':
                        return False
                time.sleep(1)
                sleep_time += 1
            except Exception as e:
                continue

    def abrir_processo(self) -> None:
        self._web_driver.find_element(By.CLASS_NAME, "fa-external-link").click()
        while True:
            try:
                tabs = self._web_driver.window_handles
                if len(tabs) >= 2:
                    self._web_driver.switch_to.window(tabs[1])
                    return
            except:
                try:
                    time.sleep(0.3)
                    self._web_driver.switch_to.alert().accept()
                except:
                    continue

    def confirmar_abertura_processo(self) -> None:
        while True:
            try:
                self._web_driver.find_element(By.ID, 'pesquisar_lbl')
                return
            except:
                continue

    def fechar_processo(self):
        tabs = self._web_driver.window_handles
        self._web_driver.close()
        self._web_driver.switch_to.window(tabs[0])

    def coletar_movimentacoes(self):
        lista_movimentacoes = []
        try:
            movimentacoes = self._web_driver.find_elements(By.CSS_SELECTOR, 'span[id*=":processoEvento:"]')
            for index, movimentacao in enumerate(movimentacoes):
                movimentacao_div = movimentacao.text.split(' - ')
                if index == 0:
                    lista_dados = [movimentacao_div[1], movimentacao_div[0], 'Consulta Realizada', 'URL']
                else:
                    lista_dados = [movimentacao_div[1], movimentacao_div[0], '', '']
                lista_movimentacoes.append(lista_dados)
            return lista_movimentacoes
        except Exception as e:
            return e
