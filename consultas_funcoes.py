"""
Arquivo de funções genéricas
Cada função possui suas próprias instruções de uso
"""
### RECOMENDO ADICIONAR CAMINHO NAS PASTAS ESPECÍFICAS ATRAVÉS DO SYS.PATH.INSERT()
# Imports ################################

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

if __name__ == '__main__':
    proc = '08041603520218150251'
    teste_formatacao = formata_numproc(proc)
    print(teste_formatacao)