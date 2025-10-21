def aplicar_padding_pkcs7(msg) -> bytes:
    tamanho_bloco = 16
    valor_padding = tamanho_bloco - (len(msg) % tamanho_bloco)
    padding = bytes([valor_padding] * valor_padding)
    return msg + padding

def dividir_em_blocos(msg):
    tamanho_bloco = 16
    blocos = []
    for i in range(0, len(msg), tamanho_bloco):
        block = list(msg[i:i + tamanho_bloco])
        blocos.append(block)
    return blocos