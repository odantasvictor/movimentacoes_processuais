import os
from base.util import *
from base.portais import Portais
from base.planilhas import PandasXlsx
from base.database import Database
from base.automacao import SeleniumWebdriver
from base.config import Configuracoes
from bot_pje import BotPje

config = Configuracoes()
portais = Portais().portais
web_driver = SeleniumWebdriver().inicializar_selenium_webdriver()
bot = BotPje(web_driver)

if config.getboolean('Bot', 'planilha'):
    fonte_processos = PandasXlsx(config.getstring('Bot', 'caminho_padrao'))
    lista_processos = fonte_processos.listar_processos_consulta()
elif config.getboolean('Bot', 'database'):
    fonte_processos = Database()
    lista_processos = fonte_processos.listar_processos_atualizar()

for indice, processo in enumerate(lista_processos):
    try:
        numero_processo = formata_numproc(numero_processo=processo)
        codigo_cpj_processo = numero_processo[16:20]
        bot.iniciar_consulta_publica(portais[codigo_cpj_processo].get('url'))
        bot.realizar_consulta_processo(numero_processo)
        resultado_consulta = bot.verificar_resultado_consulta()
        if resultado_consulta:
            bot.abrir_processo()
            bot.confirmar_abertura_processo()
            lista_movimentacoes = bot.coletar_movimentacoes()
            fonte_processos.lancar_movimentacoes(processo, portais[codigo_cpj_processo].get('uf'), lista_movimentacoes)
            bot.fechar_processo()
    except Exception as e:
        print(f'Ocorreu um erro na coleta de movimentacoes do processo {processo}. Erro: {e}')
        if len(web_driver.window_handles) > 1:
            web_driver.switch_to.window(web_driver.window_handles[1])
            web_driver.close()
            web_driver.switch_to.window(web_driver.window_handles[0])
