from TokenIsa import Token,TokenType


class Lexico():

    def __init__(self,nome_arq):
        with open(nome_arq,"r",encoding="utf-8") as arq: #enquanto este arquivo estiver aberto leio ele como arq uuhuu
            self.listachar = arq.read() #lista de caractere
            self.pos = 0 #colocando a posicao inicial da listagem :)
    
    def catchAllTokens(self): #pegando todos os tokens de uma vez
        self.guardaToken = [] #lista sem nada
        
        estado = 0 
        token = None
        nomeToken = ""



        while True:

            c = self.proxcaracter() #ler o proximo caracter
            if c == 0:
                return self.guardaToken
            print(c)

            if estado == 0:
                if self.isEspaco(c):
                    estado = 0
                elif self.isDigito(c):
                    estado = 1
                    nomeToken += c
                elif self.isLetra(c):
                    estado = 2
                    nomeToken += c
                elif c == ">" or c==":":
                    estado = 3
                    nomeToken += c 

                elif c == "<" :
                    estado = 5
                    nomeToken += c 

                elif c == "{" :
                    estado = 69

                elif c == "/" and self.espia() == "*":
                    estado = 6969

                elif self.isSimbolo(c):
                    estado = 0
                    nomeToken += c
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.simbolo
                    self.guardaToken.append(token)
                    token = None
                    estado = 0 

                else:
                    print("Erro")
                    return False
            
            elif estado == 1:
                if self.isDigito(c):
                    estado = 1
                    nomeToken += c
                elif c == '.':
                    estado = 4
                    nomeToken += c 
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.num_inteiro
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0

            elif estado == 2:
                if self.isLetra(c) or self.isDigito(c):
                    estado = 2
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.identificador
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0
                
            elif estado == 3:
                if c == ">" or c ==":":
                    estado = 3
                    nomeToken += c
                elif c == "=":
                    estado = 6
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.simbolo
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0                             

            elif estado == 4:
                if self.isDigito(c):
                    estado = 4
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.num_real
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0 

            elif estado == 5:
                if c == "<" :
                    estado = 5
                    nomeToken += c
                elif c == "=" or c == ">":
                    estado = 7
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.simbolo
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0    
            elif estado == 6:
                if c == "=" :
                    estado = 6
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.simbolo
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0   
            elif estado == 7:
                if c == "=" or c == ">" :
                    estado = 7
                    nomeToken += c
                else:
                    token = Token()
                    token.termo = nomeToken
                    nomeToken = ""
                    token.tipo = TokenType.simbolo
                    self.guardaToken.append(token)
                    self.back()
                    token = None
                    estado = 0  
            elif estado == 69:
                if c == "}":
                    estado = 0
                else:
                    estado = 69

            elif estado == 6969:
                if c == "*" and self.espia() == "/":
                    estado = 0
                    self.proxcaracter()
                else:
                    estado = 6969
            
        return self.guardaToken


    def espia(self):
        if self.pos > len(self.listachar):
            return 0
        return self.listachar[self.pos] 

    def proxcaracter(self):
        if self.isEOF():
            return 0

        posicao = self.pos
        self.pos += 1
        return self.listachar[posicao] #pegando a lista de caracter e retornando o caracter posição
        
    def isEOF(self):
        return self.pos >= len(self.listachar) #identificando fim do arquivo
    
    def isEspaco(self,caractere):
        if caractere == " " or caractere == "\n" or caractere == "\t" :
            return True

        else: 
            return False

    def isDigito(self,caractere):
        if caractere >= "0" and caractere <= "9":
            return True

        else: 
            return False


    def isSimbolo(self,caractere):
        listaSimbolos = "*/-.,=;$+()"
        if caractere in listaSimbolos:
     
            return True

        else: 
            return False

    def isLetra(self,caractere):
        if (caractere >= "a" and caractere <= "z") or (caractere >= "A" and caractere <= "Z"):
            return True

        else:
            return False

    def back(self):
        if not self.isEOF():
            self.pos -=1  
