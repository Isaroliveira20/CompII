#!-*- conding: utf8 -*-
from Lexico import Lexico
from Sintatico import Sintatico

def main():
    #pass
    lex = Lexico("correto2.lalg.txt")
    lista = lex.catchAllTokens()
    sint = Sintatico(lista)
      
   # if lista:
   #    for isa in lista:
   #       print(isa.termo, isa.tipo.name) 

    sint.programa()


if __name__=="__main__":
    main()
    #f = open("exemplo.lalg.txt")
    #print(f.read())
    