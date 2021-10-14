def start():
    arq = open("saida.txt",encoding = "utf-8")
    instrucoes = arq.read().split("\n")
    print(instrucoes)

    ponteiro = 0
    memoria = []
    pilha = []


    while True:
        instrucaoAtual = instrucoes[ponteiro].split(" ")
        if instrucaoAtual[0] == "INPP":
            if ponteiro != 0:
                raise Exception("INPP invalido!")
            
        elif instrucaoAtual[0] == "ALME":
            memoria.append(0)
            
        elif instrucaoAtual[0] == "CRVL":
            pilha.append(memoria[int(instrucaoAtual[1])])

        elif instrucaoAtual[0] == "ARMZ":
            valorAtual = pilha.pop()
            memoria[int(instrucaoAtual[1])] = valorAtual

        elif instrucaoAtual[0] == "SOMA":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()
            pilha.append(valorAtual1 + valorAtual2)            
            
        elif instrucaoAtual[0] == "SUBT":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()
            pilha.append(valorAtual1 - valorAtual2) 

        elif instrucaoAtual[0] == "DIVI":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()
            pilha.append(valorAtual1 / valorAtual2) 

        elif instrucaoAtual[0] == "MULT":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()
            pilha.append(valorAtual1 * valorAtual2) 

        elif instrucaoAtual[0] == "INVE":
            valorAtual1 = pilha.pop()
            pilha.append(valorAtual1 * (-1)) 

        elif instrucaoAtual[0] == "CRCT":
            var = int(instrucaoAtual[1])
            pilha.append(var)

        elif instrucaoAtual[0] == "CPME":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 < valorAtual2))


        elif instrucaoAtual[0] == "CPMA":
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 > valorAtual2))

        elif instrucaoAtual[0] == "CPIG":   
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 = valorAtual2))

        elif instrucaoAtual[0] == "CDES": 
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 != valorAtual2))

        elif instrucaoAtual[0] == "CPMI": 
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 <= valorAtual2))

        elif instrucaoAtual[0] == "CMAI": 
            valorAtual1 = pilha.pop()
            valorAtual2 = pilha.pop()      
            pilha.append(int(valorAtual1 >= valorAtual2))
        
        elif instrucaoAtual[0] == "DSVF":
            valorAtual = pilha.pop()
            if valorAtual == 0:
                ponteiro = int(instrucaoAtual[1])

        elif instrucaoAtual[0] == "DSVI":
            ponteiro = int(instrucaoAtual[1])
        
        elif instrucaoAtual[0] == "LEIT":
            pilha.append(int(input()))

        elif instrucaoAtual[0] == "IMPR":
            print(pilha.pop)

        elif instrucaoAtual[0] == "PARA":
            break


        ponteiro += 1
      
if __name__=="__main__":
    start()



