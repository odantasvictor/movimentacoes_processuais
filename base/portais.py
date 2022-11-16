import xml.etree.ElementTree as xml


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Portais(metaclass=Singleton):

    def __init__(self):
        self.portais = {}
        self.carregar_xlsx_portais()

    def carregar_xlsx_portais(self):
        tree = xml.parse('./data/portais.xml')
        root = tree.getroot()
        for sistema in root:
            for portal in sistema.iter('portal'):
                dados_portal = {
                    'sistema': sistema.attrib.get('nome'),
                    'uf': portal.get('uf'),
                    'codigo_cpj': portal.get('codigo_cpf'),
                    'url': portal.get('url'),
                    'seletor': portal.get('seletor', ''),
                    'parcial': portal.get('parcial', ''),
                    'sitekey': portal.get('sitekey', ''),
                }
                self.portais[portal.get('codigo_cpj')] = dados_portal