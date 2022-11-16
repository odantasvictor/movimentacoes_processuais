import os
import configparser


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuracoes(metaclass=Singleton):

    def __init__(self):
        caminho_base = '/'.join(os.path.realpath(__file__).replace('\\', '/').split('/')[:-2])
        self.arquivo_ini = f"{caminho_base}/config/config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.arquivo_ini)

    def getstring(self, sessao, chave)  -> str:
        try:
            return self.config.get(sessao, chave)
        except:
            return ''

    def getboolean(self, sessao, chave) -> bool:
        try:
            return self.config.getboolean(sessao, chave)
        except:
            return False

    def getinteger(self, sessao, chave) -> int:
        try:
            return self.config.getint(sessao, chave)
        except:
            return 0

    def getfloat(self, sessao, chave) -> float:
        try:
            return self.config.getfloat(sessao, chave)
        except:
            return 0.0

    def reload(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.arquivo_ini)

