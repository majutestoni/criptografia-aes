from Algoritmo import Algoritmo
from Bloco import dividir_em_blocos, remover_padding_pkcs7
from Chave import expandir_chave
import numpy as np


class Decifrar(Algoritmo):

    def decifrar(self, msg, chave: bytes):
        key_schedule = expandir_chave(chave)
        blocos = dividir_em_blocos(msg)
        
        msg_decifrada = b''

        for bloco in blocos:
            bloco_decifrado = self.decifrar_bloco(bloco, key_schedule)
            msg_decifrada += self.matriz_para_bytes(bloco_decifrado)

        msg_decifrada = remover_padding_pkcs7(msg_decifrada)
        return msg_decifrada

    def decifrar_bloco(self, bloco, key_schedule):
        matriz_estado = self.obter_matriz_estado(bloco)

        matriz_estado = self.add_round_key(matriz_estado, key_schedule[10])

        for i in range(9, 0, -1):
            matriz_estado = self.inv_shift_rows(matriz_estado)
            matriz_estado = self.inv_sub_bytes(matriz_estado)
            matriz_estado = self.add_round_key(matriz_estado, key_schedule[i])
            matriz_estado = self.inv_mix_columns(matriz_estado)

        matriz_estado = self.inv_shift_rows(matriz_estado)
        matriz_estado = self.inv_sub_bytes(matriz_estado)
        matriz_estado = self.add_round_key(matriz_estado, key_schedule[0])

        return matriz_estado