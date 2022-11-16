"""
Arquivo de funções genéricas
Cada função possui suas próprias instruções de uso
"""
### RECOMENDO ADICIONAR CAMINHO NAS PASTAS ESPECÍFICAS ATRAVÉS DO SYS.PATH.INSERT()
from typing import Any


def formata_numproc(numero_processo: str) -> str:
    """
    Atribui . e - ao número do processo
    """
    np = numero_processo.replace('.', '').replace('-', '')
    if len(np) == 20 and np.isnumeric():
        processo_formatado = f'{np[0:7]}-{np[7:9]}.{np[9:13]}.{np[13]}.{np[14:16]}.{np[16:]}'
        return processo_formatado
    else:
        return numero_processo

def espere_ate(condicao: Any) -> Any:
    """
    Espera até determinado evento/condição acontecer e então encerra
    """
    while True:
        try:
            retorno_condicao = condicao
            return retorno_condicao
        except:
            continue

def formata_data_pje(data: str) -> str:
    """Formata data para o formato americano YYYY-mm-dd H:M:S, aceitando como atuais formatos de formatação (dd/mm/YYYY c/c +)\n
    Aceita estrutura datetime 'data tempo'\n
    :param data: str -> Data a ser formatada\n
    Retorna a data e hora na estrutura str YYYY-mm-dd H:M:S"""
    if ' ' in data: # TRATAMENTO DE POSSÍVEL FORMATO DATA TIME
        hora = data.split(' ')[1]
        data = data.split(' ')[0]
    if '/' in data and len(data.split('/')[-1]) == 4:
        data = '-'.join(data.split('/')[::-1])
        return f'{data} {hora}'
    raise KeyError('Dado informado inválido')