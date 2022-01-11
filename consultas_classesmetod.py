from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import json
import pandas as pd


class ConfigDriver:
    def driver_config(downloaddir, user_data_dir=None, page_load=False):
        """
        Criação e configuração padrão do webdriver do selenium para Chrome
        Possível passar os parâmetros da configuração rcb acessando como dict
        :param downloaddir: Caminho de download do diretório
        :param driver_path: Caminho do chromedriver.exe
        :return: web_driver
        """
        chromedriver_autoinstaller.install()

        appState = {"recentDestinations": [
            {"id": "Save as PDF", "origin": "local"}], "selectedDestinationId": "Save as PDF", "version": 2}
        options = Options()
        options.add_experimental_option("prefs", {
            "plugins.always_open_pdf_externally": True,
            "download.default_directory": downloaddir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "printing.print_preview_sticky_settings.appState": json.dumps(appState)
        })
        options.add_argument('--kiosk-printing')
        options.add_argument('--no-sandbox')
        options.add_argument('--zoom=70')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")

        if user_data_dir:
            options.add_argument(f'user-data-dir={user_data_dir}')
        if page_load:
            options.page_load_strategy = 'none'

        web_driver = webdriver.Chrome(
            options=options)
        web_driver.implicitly_wait(3)

        return web_driver


class ConfigPdXlsx():
    def __init__(self, consulta, resultado):
        self.tabela_consulta: str = consulta
        self.tabela_resultado: str = resultado
        self.df_consulta: object = None
        self.df_resultado: object = None
        self.lista_consultados:list = []
        self.lista_consultar:list = []

    def ler_xlsx_consulta(self):
        try:
            self.df_consulta = pd.read_excel(self.tabela_consulta)
            return self.df_consulta
        except Exception as e:
            return e

    def listar_processos_consulta(self):
        try:
            for processo in self.df_consulta['Processos'].iteritems():
                if processo not in self.lista_consultados:
                    self.lista_consultar.append(processo[1])
            return self.lista_consultar
        except Exception as e:
            return e

    def ler_xlsx_resultado(self):
        try:
            self.df_resultado = pd.read_excel(self.tabela_resultado)
            return self.df_resultado
        except Exception as e:
            self.df_resultado = pd.DataFrame({'Processo': [], 'UF': [], 'Movimentação': [], 'Data da Movimentação': [], 'Feedback': [], 'URL Consulta': []})
            self.df_resultado.to_excel(self.tabela_resultado, index=False)
            return self.df_resultado

    def ler_processos_consultados(self):
        try:
            for processo in self.df_resultado['Processo'].iteritems():
                if processo not in self.lista_consultados:
                    self.lista_consultados.append(processo[1])
            return self.lista_consultados
        except Exception as e:
            return e

    def anotar_consulta(self, lista_dados):
        try:
            self.df_resultado.loc[len(self.df_resultado.index)] = lista_dados
            self.df_resultado.to_excel(self.tabela_resultado, index=False)
        except Exception as e:
            print(e)
            return e

