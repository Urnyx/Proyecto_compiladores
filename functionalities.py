from principal import mostrar
from gramatica import lexer as analyzer

class funtions:
    def __init__(self,syntax):
        self.ListTokens = []
        analyzer.input(syntax)

    def saveTokens(self):
        while True:
            tok = analyzer.token()
            if not tok: 
                break
            self.ListTokens.append(tok)
    
    def getTokens(self):
        result = ''
        for i in self.ListTokens:
            result+=str(i)+'\n'
            
        return result
    

def ejecutar(sintax):    
    result = ""    
    result += mostrar(sintax)+"\n"
    
    return result
        
data = '''
dca x[;

x-:2[;

anota(x)[;

anota(8)[;

desde(i hasta 10){
    anota(i)[;
}
'''

print(ejecutar(data))
