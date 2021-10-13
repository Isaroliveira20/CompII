from TokenIsa import Token,TokenType


# class NumberType(Enum):
#     num_inteiro = 1
#     num_real = 2

class Sintatico():

    def __init__(self,lista):
        self.listaTokens = lista
        self.ponteiro = 0
        self.tabelaSimbolos = {}
        self.tabelaSimbolosPosicao = {}
        self.tipoAtual = None
        self.instrucoes = []

    def pegaTokenAtual(self):
        return self.listaTokens[self.ponteiro] 

    def verificaTipo(self,tipo):
        return self.listaTokens[self.ponteiro] != None and self.listaTokens[self.ponteiro].tipo == tipo


    def verificaSimbolo(self, termo):
        return self.listaTokens[self.ponteiro] != None and self.listaTokens[self.ponteiro].termo == termo

    def verificaSimboloException(self,termo):
        if self.verificaSimbolo(termo):
            return True
        else:
            raise Exception("Esperando "+ termo + "Obtido " +self.listaTokens[self.ponteiro].termo)

    def verificaTipoException(self,tipo):
        if self.verificaTipo(tipo):
            return True
        else:
            raise Exception("Esperando "+ tipo + "Obtido " +self.listaTokens[self.ponteiro].tipo)

    guardaPos = 0

    def programa(self):
        if self.verificaSimboloException("program"):
            self.instrucoes.append("INPP")
            self.ponteiro += 1
        
            if self.verificaTipoException(TokenType.identificador):
                self.ponteiro += 1
                self.corpo()
                 
                if self.verificaSimboloException("."):
                    self.ponteiro += 1
                    self.instrucoes.append("PARA")
                    if len(self.listaTokens) == self.ponteiro:
                        print("Programa compilado! :)")

                     

    def corpo(self):
        self.dc()
        self.tipoAtual = None 
        if self.verificaSimboloException("begin"):
            self.ponteiro += 1
            self.comandos()   

            if self.verificaSimboloException("end"):
                self.ponteiro += 1

    #<dc> -> <dc_v> <mais_dc>  | λ
    def dc(self):
        if self.verificaSimbolo("real") or self.verificaSimbolo("integer"):
            self.dc_v()
            self.mais_dc()
        else:
            return 

    def mais_dc(self):
        if self.verificaSimbolo(";"):
            self.ponteiro += 1
            self.dc()
        else:
            return 

    def dc_v(self):
        self.tipo_var()
        if self.verificaSimboloException(":"):
            self.ponteiro +=1
            self.variaveis()
    
    def tipo_var(self):
        if self.verificaSimbolo("real") or self.verificaSimbolo("integer"):
            if self.verificaSimbolo("real"):
                self.tipoAtual = "real"
            else:
                self.tipoAtual = "integer"
            self.ponteiro +=1
        else:
            raise Exception("Esperando real ou inteiro, Recebido " + self.listaTokens[self.ponteiro].tipo )


    def variaveis(self):
        if self.verificaTipoException(TokenType.identificador):
            if self.pegaTokenAtual().termo in self.tabelaSimbolos:
                raise Exception ("Variavel já foi declarada")
            else:
                self.tabelaSimbolos[self.pegaTokenAtual().termo] = self.tipoAtual
                self.tabelaSimbolosPosicao[self.pegaTokenAtual().termo] = len(self.tabelaSimbolosPosicao)
                #print("ALME 1")
                self.instrucoes.append("ALME 1")
            self.ponteiro +=1
            self.mais_var()
    
    
    def mais_var(self):
        if self.verificaSimbolo(","):
            self.ponteiro += 1
            self.variaveis()
        else:
            return

    def comandos(self):
        self.comando()
        self.mais_comandos()


    def mais_comandos(self):
        if self.verificaSimbolo(";"):
            self.ponteiro += 1
            self.comandos()
        else:
            return 
        

    def comando(self):
        if self.verificaSimbolo('read'):
            self.ponteiro += 1
            if self.verificaSimboloException("("):
                self.ponteiro += 1
                if self.verificaTipoException(TokenType.identificador):
                    if self.pegaTokenAtual().termo not in self.tabelaSimbolos:
                        raise Exception ("Variavel não foi declarada")
                    #print("LEIT ") 
                    self.instrucoes.append("LEIT")
                    #print("ARMZ " + str(self.tabelaSimbolosPosicao[self.pegaTokenAtual().termo]))
                    self.instrucoes.append("ARMZ " + str(self.tabelaSimbolosPosicao[self.pegaTokenAtual().termo]))
                    self.ponteiro +=1
                    if self.verificaSimboloException(")"):
                        self.ponteiro += 1
                        return
        elif self.verificaSimbolo("write"):
            self.ponteiro += 1
            if self.verificaSimboloException("("):
                self.ponteiro += 1
                if self.verificaTipoException(TokenType.identificador):
                    if self.pegaTokenAtual().termo not in self.tabelaSimbolos:
                        raise Exception ("Variavel não foi declarada")
                    #print("CRVL " + str(self.tabelaSimbolosPosicao[self.pegaTokenAtual().termo]))
                    self.instrucoes.append("CRVL"+ str(self.tabelaSimbolosPosicao[self.pegaTokenAtual().termo]))
                    #print("IMPR ")
                    self.instrucoes.append("IMPR")
                    self.ponteiro += 1
                    if self.verificaSimboloException(")"):
                        self.ponteiro +=1
                        
                        return

        elif self.verificaSimbolo("if"):
            self.ponteiro +=1
            self.condicao()
            posCondicao = len(self.instrucoes)-1
            if self.verificaSimboloException("then"):
                self.ponteiro += 1
                self.comandos()
                self.instrucoes[posCondicao] = "DSVF " + str(len(self.instrucoes))
                self.pfalsa()
                if self.verificaSimboloException("$"):
                    self.ponteiro += 1
                    return
        elif self.verificaSimbolo("while"):
            self.ponteiro +=1
            guardaCondicao = len(self.instrucoes)-1
            self.condicao()
            guardaInstrucao = len(self.instrucoes)-1
            self.verificaSimboloException("do")
            self.ponteiro +=1
            self.comandos()
            self.instrucoes.append("DSVI " + str(guardaCondicao))
            self.instrucoes[guardaInstrucao]= "DSVF " + str(len(self.instrucoes)-1)
            self.verificaSimboloException("$")
            self.ponteiro +=1

        elif self.verificaTipoException(TokenType.identificador):
            if self.pegaTokenAtual().termo not in self.tabelaSimbolos:
                raise Exception ("Variavel não foi declarada: " + self.pegaTokenAtual().termo)
            self.tipoAtual = self.tabelaSimbolos[self.pegaTokenAtual().termo] #le a variavel e atribui o valor para o tipo dela
            self.ponteiro +=1
            if self.verificaSimboloException(":="):
                self.ponteiro += 1
                self.expressao()
                self.tipoAtual = None 
                #print("ARMZ " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro -3].termo]))
                self.instrucoes.append("ARMZ " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro -3].termo]))
                return


    def condicao(self):
        self.expressao()
        self.relacao()
        instrucaoTipo = self.instrucoes[-1]
        self.instrucoes = self.instrucoes[:-1] 
        self.expressao()
        self.tipoAtual = None 
        self.instrucoes.append(instrucaoTipo)
        self.instrucoes.append("DSVF")


    def relacao(self):
        if self.verificaSimbolo("="):
            self.ponteiro += 1
            self.instrucoes.append("CPIG")
            return
        elif self.verificaSimbolo("<>"):
            self.ponteiro +=1
            self.instrucoes.append("CDES")
            return
        elif self.verificaSimbolo('>='):
            self.ponteiro +=1
            self.instrucoes.append("CMAI")
            return
        elif self.verificaSimbolo("<="):
            self.ponteiro +=1
            self.instrucoes.append("CPMI")
            return
        elif self.verificaSimbolo(">"):
            self.ponteiro +=1
            self.instrucoes.append("CPMA")
            return
        elif self.verificaSimboloException("<"):
            self.ponteiro +=1
            self.instrucoes.append("CPME")
            return
    
    def expressao(self):
        self.termo()
        self.outros_termos()

    
    def termo(self):   
        self.op_un()
        self.fator()
        self.mais_fatores()
       
    def op_un(self): 
        if self.verificaSimbolo("-"):
            self.ponteiro +=1
        else:
            return          
      
    def fator(self):
        if self.verificaTipo(TokenType.identificador):
            if self.pegaTokenAtual().termo not in self.tabelaSimbolos:
                raise Exception ("Variavel não foi declarada")
            if self.tipoAtual == None:
                self.tipoAtual = self.tabelaSimbolos[self.pegaTokenAtual().termo] 

            if self.tabelaSimbolos[self.pegaTokenAtual().termo] != self.tipoAtual:
                raise Exception ("Tipos de variaveis diferentes")
            #print("CRVL " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro].termo]))
            self.instrucoes.append("CRVL " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro].termo]))
            self.ponteiro +=1
        elif self.verificaTipo(TokenType.num_inteiro):
            if self.tipoAtual == None:
                self.tipoAtual = "integer"
            if "integer" != self.tipoAtual:
                raise Exception ("Tipos de variaveis diferentes")
            #print("CRCT " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro].termo]))
            self.instrucoes.append("CRCT " + str(self.listaTokens[self.ponteiro].termo))
            self.ponteiro +=1
        elif self.verificaTipo(TokenType.num_real):
            if self.tipoAtual == None:
                self.tipoAtual = "real"
            if "real" != self.tipoAtual:
                raise Exception ("Tipos de variaveis diferentes")
            #print("CRCT " + str(self.tabelaSimbolosPosicao[self.listaTokens[self.ponteiro].termo]))
            self.instrucoes.append("CRCT " + str(self.listaTokens[self.ponteiro].termo))
            self.ponteiro +=1
        elif self.verificaSimboloException("("):
            self.ponteiro +=1
            self.expressao()

            if self.verificaSimboloException(")"):
                self.ponteiro +=1
                return 

    def outros_termos(self):
        if self.verificaSimbolo("+") or self.verificaSimbolo("-"):
            self.op_ad()
            self.termo()
            self.outros_termos()
            
            return
        else:
            return

    def op_ad(self):
        if self.verificaSimbolo("+") or self.verificaSimbolo('-'):
            if self.verificaSimbolo("+"):
                #print ("SOMA")
                self.instrucoes.append("SOMA")
            elif self.verificaSimbolo("-"):
                #print("SUBT")
                self.instrucoes.append("SUBT")
            self.ponteiro +=1
        else:
            raise Exception("Erro não é + nem -")

    def mais_fatores(self):
        if self.verificaSimbolo("*") or self.verificaSimbolo("/"):
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            return

    def op_mul(self):
        if self.verificaSimbolo("*") or self.verificaSimbolo("/"):
            self.ponteiro += 1
        else:
            raise Exception("Erro não é * nem /")


    def pfalsa(self):
        if self.verificaSimbolo("else"):
            tamanhoInstrucao = len(self.instrucoes)-1
            self.instrucoes.append("DSVI")
            self.ponteiro +=1
            self.comandos()
            self.instrucoes[tamanhoInstrucao+1] = "DSVI " + str(len(self.instrucoes)) 
        else:
            return 