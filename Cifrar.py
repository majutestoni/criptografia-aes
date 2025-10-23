from Bloco import aplicar_padding_pkcs7, dividir_em_blocos
from Chave import expandir_chave
from Algoritmo import Algoritmo 


class Cifrar(Algoritmo):

    def cifrar(self, msg, chave: bytes):
        key_schedule = expandir_chave(chave)
        msg = aplicar_padding_pkcs7(msg)
        blocos = dividir_em_blocos(msg)

        msg_cifrada = b''

        for bloco in blocos:
            bloco_cifrado = self.cifrar_bloco(bloco, key_schedule)
            msg_cifrada += self.matriz_para_bytes(bloco_cifrado)

        return msg_cifrada

    def cifrar_bloco(self, bloco, key_schedule):
        matriz_estado = self.obter_matriz_estado(bloco)

        matriz_estado = self.add_round_key(matriz_estado, key_schedule[0])

        for i in range(1, 10):
            matriz_estado = self.sub_bytes(matriz_estado)
            matriz_estado = self.shift_rows(matriz_estado)
            matriz_estado = self.mix_columns(matriz_estado)
            matriz_estado = self.add_round_key(matriz_estado, key_schedule[i])

        matriz_estado = self.sub_bytes(matriz_estado)
        matriz_estado = self.shift_rows(matriz_estado)
        matriz_estado = self.add_round_key(matriz_estado, key_schedule[10])

        return matriz_estado