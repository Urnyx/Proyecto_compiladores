import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *

    
def procesar_imprimir(instr, ts) :
    result = ''
    # print('> ',resolver_cadena(instr.cad, ts))
    result=(resolver_cadena(instr.cad, ts))
    return result
    
def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

def procesar_asignacion(instr, ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, val)
    ts.actualizar(simbolo)

def procesar_mientras(instr, ts) :
    while resolver_expreision_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_for(instr, ts) :
    cont = 0
    while resolver_expreision_logica(instr.expLogica, ts): 
        # print(instr.instrucciones)
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        if cont == 0:
            procesar_asignacion(instr.asignacion1,ts_local)
            cont+=1
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_funcion(instr,ts):
    simbolo = TS.Simbolo(instr.nombreF, TS.TIPO_DATO.FUNCION, instr.instrucciones)
    ts.agregar(simbolo)
    
def procesar_funcionCall(instr,ts):
    ts_local = TS.TablaDeSimbolos(ts.simbolos)
    print(ts_local.obtener())
     

def procesar_if(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if_else(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionConcatenar) :
        exp1 = resolver_cadena(expCad.exp1, ts)
        exp2 = resolver_cadena(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionDobleComilla) :
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico) :
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    else :
        print('Error: Expresión cadena no válida')


def resolver_expreision_logica(expLog, ts) :
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MAYOR_IGUAL : return exp1 >= exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_IGUAL : return exp1 <= exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2

def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if expNum.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor


def procesar_instrucciones(instrucciones, ts) :
    res =[]
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : res.append(procesar_imprimir(instr, ts))
        elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
        elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        elif isinstance(instr, For) : procesar_for(instr, ts)
        elif isinstance(instr, Funcion) : procesar_for(instr, ts)
        elif isinstance(instr, FuncionCall) : procesar_for(instr, ts)
        else : print('Error: instrucción no válida')
    return res

f = open("entrada.txt", "r")
input = f.read()

def run(input):
    instrucciones = g.parse(input)
    ts_global = TS.TablaDeSimbolos()
    return procesar_instrucciones(instrucciones, ts_global)
    
def mostrar(input):
    try:
        return run(input)
    except:
        return 'error'

data='''
anota(2)[;

anota(4)[;
'''


# print(mostrar(data))