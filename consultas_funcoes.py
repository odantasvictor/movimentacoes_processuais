"""
Arquivo de funções genéricas
Cada função possui suas próprias instruções de uso
"""
### RECOMENDO ADICIONAR CAMINHO NAS PASTAS ESPECÍFICAS ATRAVÉS DO SYS.PATH.INSERT()
# Imports ################################
import os
import time
from unicodedata import normalize
from capmonster_python import *
#from PIL import Image

def formata_numproc(num_proc):
    """
    Atribui . e - ao número do processo
    """
    processo_formatado = ''
    num_proc = num_proc.replace('.', '').replace('-', '')
    if len(num_proc) == 20 and num_proc.isnumeric():
        for index, dig in enumerate(num_proc):
            if index == 7:
                processo_formatado += '-'
                processo_formatado += dig
            elif index == 9 or index == 13 or index == 14 or index == 16:
                processo_formatado += '.'
                processo_formatado += dig
            else:
                processo_formatado += dig
        return {
            'sucesso': 1,
            'valido': 'Número do processo formatado',
            'num_proc': processo_formatado
        }
    else:
        return {
            'sucesso': 0,
            'valido': 'Número do processo inválido',
            'num_proc': num_proc
        }

def espere_ate(condicao):
    """
    Espera até determinado evento/condição acontecer e então encerra
    """
    while True:
        try:
            condicao
            return condicao
        except:
            continue

def pje_aguardar_carregamento(web_driver):
    """
    Recebe como parâmetro o webdriver
    Aguarda animação de carregamento do PJE
    """
    while True:
        try:
            carregamento = web_driver.find_element_by_id('_viewRoot:status.start').get_attribute('style')
            if carregamento == 'display: none;':
                break
        except:
            continue

"""
def fullpage_screenshot(driver, file, specific=''):
    
    Tira um print completo da tela
    Recebe como parâmetro o webdriver
    File = caminho+nome do arquivo final
    Specific é opcional, mas recomendado caso estejam sendo executadas -
    várias automações em simultaneo
    
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            rectangles.append((ii, i, top_width,top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = f"{specific}part_{part}.png"
        
        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    stitched_image.save(file)
    return True
"""

if __name__ == '__main__':
    proc = '08041603520218150251'
    teste_formatacao = formata_numproc(proc)
    print(teste_formatacao)