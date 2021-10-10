from enum import Enum

class TokenType(Enum):
    identificador = 0
    num_inteiro = 1
    num_real = 2
    simbolo = 3

class Token():

    tipo: TokenType
    termo: str


    def toString(self):
        return "Token["+ self.tipo.name+","+ self.termo +"]"

