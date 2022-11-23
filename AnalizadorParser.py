from sys import stdin
from lexer import tokens,analizador

precedence = (
    ('right','IGUAL'),
    ('right','IGUALQUE'),
    ('left','MAYQUE','MENQUE'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','PARIZQ','PARDER'),
    ('left','LLAVIZQ','LLAVDER')
    )

nombres = {}

def p_init(t):
    'init : instrucciones'
    t[0] = t[1]

def p_instrucciones(p):
    """
    instrucciones : imprimir_instr instrucciones
                   | asignacion_instr instrucciones
                   | if_instr instrucciones
                   | elif_instr instrucciones
                   | else_instr instrucciones
                   | while_instr instrucciones    
                   | empty
                   | for_instr instrucciones
    """
    p[0] = p[1]
    
    
def p_if(t):
    '''if_instr : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER 
                | IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER elif_instr
    '''
    try:
        if t[3] == True:
            t[0] = t[6]
        else:
            t[0] = t[8]
    except:
        pass
           
def p_if_else(t):
    '''if_instr : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER else_instr'''
    try:
        if t[3] == True:
            t[0] = t[6]
        else:
            t[0] = t[8]
    except:
        pass
            
def p_elif(t):
    '''elif_instr : ELIF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER
                  | ELIF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER else_instr'''
    try:
        if t[3] == True:
            t[0] = t[6]
        else:
            t[0] = t[8]
    except:
        pass

def p_else(t):
    """else_instr : ELSE LLAVIZQ instrucciones LLAVDER"""
    t[0] = t[3]
    
def p_while(t):
    '''while_instr : WHILE PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'''
    while(t[3]):
        t[0] = t[6]
        
def p_asignacion(t):
    '''asignacion_instr : ID IGUAL expresion PTCOMA'''
    nombres[t[1]] = t[3] 
    
    
def p_asignacion_increment(t):
    '''asignacion_instr_increment : ID IGUAL ID MAS ENTERO PTCOMA
                                  | ID IGUAL ID MENOS ENTERO PTCOMA 
    '''
    if t[4]=='+':
        t[0] = t[1] + 1
    elif t[4] == '-':
        t[0] = t[1] - 1
    elif t[3] == '+':
        t[1] = t[1] + 1
    elif t[3] == '-':
        t[1] = t[1] - 1
        
def p_asignacion_tipo(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | STRING        
    '''
    t[0] = t[1]
    
def p_expresion_id(t):
    'expresion : ID'
    t[0] = nombres[t[1]]
    
def p_print(t):
    '''imprimir_instr : PRINT PARIZQ expresion PARDER PTCOMA
                      | PRINT PARIZQ expresion_logica PARDER PTCOMA
    '''
    t[0] = t[3]
    
def p_expresion_logica(t):
    '''expresion_logica : expresion MENQUE expresion
                        | expresion MAYQUE expresion
                        | expresion IGUALQUE expresion
                        | expresion NIGUALQUE expresion
                        | expresion MENIGUAL expresion
                        | expresion MAYIGUAL expresion
    '''
    if t[2] == '<':t[0] = t[1] < t[3]
    elif t[2] == '>':t[0] = t[1] > t[3]
    elif t[2] == ':¬¬:':t[0] = t[1] is t[3]
    elif t[2] == '!¬':t[0] = t[1] != t[3]
    elif t[2] == '<¬:':t[0] = t[1] <= t[3]
    elif t[2] == '>¬:':t[0] = t[1] >= t[3]
    
def p_expresion_logica_group(t):
    '''expresion_logica : PARIZQ expresion_logica PARDER'''
    t[0] = t[2]    

def p_expresion_logica_group(t):
    '''expresion_logica : PARIZQ expresion_logica PARDER MENQUE PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER MAYQUE PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER IGUALQUE PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER NIGUALQUE PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER MAYIGUAL PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER MENIGUAL PARIZQ expresion_logica PARDER
    '''
    if t[4] == '<':t[0] = t[2] < t[6]
    elif t[4] == '>': t[0] = t[2] > t[6]
    elif t[4] == ':¬¬:': t[0] = t[2] is t[6]
    elif t[4] == '!¬:': t[0] = t[2] != t[6]
    elif t[4] == '<¬:': t[0] = t[2] <= t[6]
    elif t[4] == '>¬:': t[0] = t[2] >= t[6]
    
def p_expresion_operador_logico(t):
    '''expresion_logica : PARIZQ expresion_logica PARDER AND PARIZQ expresion_logica PARDER
                        | PARIZQ expresion_logica PARDER OR PARIZQ expresion_logica PARDER
                        | expresion_logica AND expresion_logica
                        | expresion_logica OR expresion_logica
    '''
    if t[4] == '^': t[0] = t[2] and t[6]
    elif t[4] == '~': t[0] = t[2] or t[6]
    elif t[2] == '~': t[0] = t[1] or t[3]
    elif t[2] == '~': t[0] = t[1] or t[3]
    
def p_expresion_operaciones(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

def p_for(t):
    'for_instr : FOR PARIZQ ID IN expresion PARDER LLAVIZQ instrucciones LLAVDER'
    i = int(str(t[5]))
    x = 0
    print(t[8],'xd')
    while x < i:
        t[0] = t[8]
        print(t[8])
        x = x + 1
        
    t[0] = t[8]
    
def p_empty(t):
    """empty :"""
    pass
    
# def p_funcion_expr(t):
#     '''funcion_expr : expresion COMA expresion
#                     | expresion
#                     | expresion COMA expresion COMA expresion
#                     | expresion COMA expresion COMA expresion COMA expresion
#     '''
#     pass
    
# def p_funcion(t):
#     '''funcion_instr : DEF ID PARIZQ funcion_expr PARDER LLAVIZQ instrucciones LLAVDER
#                      | DEF ID PARIZQ PARDER LLAVIZQ instrucciones LLAVDER
#     '''
#     pass

def p_error(t):
    global resultadoGramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format(str(t.type),str(t.value))
    else:
        resultado = "Error sintactico {}".format(t)        
    
    resultadoGramatica.append(resultado)

import ply.yacc as yacc
parser = yacc.yacc()

resultadoGramatica = []

def prueba(data):
    resultadoGramatica.clear()
    for item in data.splitlines():
        if item:            
            gram = parser.parse(item)
            if gram:
                try:
                    resultadoGramatica.append(str(gram[0])) 
                except:
                    resultadoGramatica.append(str(gram))
    
    return resultadoGramatica            



text = '''
y¬:0[;

anota(y+2)[;


'''

try:
    for i in parser.parse(text):
        if i!=None:
            print(i)
        else:
            continue
except:
    print("Error sintactico")
    

print(parser.parse(text))

for i in prueba(text):
    print(i)

