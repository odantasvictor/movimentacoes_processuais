import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SeleniumWebdriver(metaclass=Singleton):

    def __init__(self, head: bool = True) -> None:
        self.head = head
        self.definir_options_webdriver()

    def definir_options_webdriver(self) -> Options:
        """
        Criação e configuração padrão do webdriver do selenium para Chrome
        :param downloaddir: Caminho de download do diretório
        :param user_data_dir: Caminho no qual serão salvos as extensões e demais caches p/ reutilização
        :param page_load: Valor booleano, trata do aguardo de carregamento da página
        :param head: Valor booleano, trata da exibição ou não o Chrome durante a execução
        :return: web_driver
        """

        appState = {"recentDestinations": [
            {"id": "Save as PDF", "origin": "local"}], "selectedDestinationId": "Save as PDF", "version": 2}
        self.options = Options()
        self.options.add_experimental_option("prefs", {
            "plugins.always_open_pdf_externally": True,
            #"download.default_directory": f'C:/',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "printing.print_preview_sticky_settings.appState": json.dumps(appState)
        })
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--kiosk-printing')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--zoom=70')
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--log-level=3")  # fatal
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if not self.head:
            self.options.add_argument('--headless')
        return self.options

    def inicializar_selenium_webdriver(self):
        self.web_driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=self.options
        )
        return self.web_driver
