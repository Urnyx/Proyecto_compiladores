import ply.lex as lex

reservedWords = {
    'siempreque':'IF',
    'cuandosi': 'ELIF',
    'cuandono': 'ELSE',
    'anota': 'PRINT',
    'duranteque': 'WHILE',
    'desde':'FOR',
    '^':'AND',
    'devuelve':'RETURN',
    'funta':'DEF',
    '~':'OR',
    'hasta':'IN',
    'inter':'RANGE',
    'cortar':'BREAK'
}

# List of token names.   
# This is always required
tokens = [ 
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'DOBPUNTO',
    'PARDER',
    'IGUAL',
    'IGUALQUE',
    'NIGUALQUE',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MENQUE',
    'MAYQUE',
    'MAYIGUAL',
    'MENIGUAL',
    'DECIMAL',
    'ENTERO',
    'ID',         
    'STRING',
    'CONCAT',
    'PTCOMA',
    'COMA',
] + list(reservedWords.values())

# Regular expression rules for simple tokens
t_LLAVIZQ = r'\{'
t_LLAVDER = r'\}'
t_PARIZQ = r'\('
t_DOBPUNTO = r'\[:'
t_PARDER = r'\)'
t_COMA = r'\,'
t_IGUAL = r'¬:'
t_IGUALQUE = r':¬¬:'
t_NIGUALQUE = r'!¬:'
t_MAS = r'\+'
t_MENOS = r'- '
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MENQUE = r'<'
t_MAYQUE = r'>'
t_MAYIGUAL = r'>¬:'
t_MENIGUAL = r'<¬:'
t_PRINT = r'anota'
t_IF = r'siempreque'
t_WHILE = r'duranteque'
t_AND = r'\^'
t_OR = r'~'
t_ELIF = r'cuandosi'
t_ELSE = r'cuandono'
t_RANGE = r'inter'
t_IN = r'hasta'
t_BREAK = r'cortar'
t_RETURN = r'devuelve'
t_DEF = r'funta'
t_FOR = r'desde'
t_PTCOMA = r'\[;'
t_CONCAT = r'&'

t_ignore  = "\t"

def t_STRING(t):
    r'\°.*?\°'
    t.value=t.value[1:-1]
    return t

#Salto de linea
def t_newline(t):
    r'\s+'
    t.lexer.lineno += len(t.value)

#Comentarios
def t_COMMENT(t):
    r'\|\|.*\n'
    t.lexer.linero += 1

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservedWords.get(t.value.lower(),'ID')
    return t

#detecta cuando es decimal
def t_DECIMAL(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d",t.value)
        t.value = 0
    return t

# detecta cuando es entero
def t_ENTERO(t):
    r'(-\d+|\d+)'
    try :
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d",t.value)
        t.value = 0
    return t

    
# Error handling rule
def t_error(t):
    print("Caracter Invalido '%s'" % t.value[0])
    t.lexer.skip(1)
    return t


# Build the lexer
analizador = lex.lex()