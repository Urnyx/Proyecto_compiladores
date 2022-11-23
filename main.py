from functionalities import funtions as F
from functionalities import ejecutar
from flask import Flask, render_template,request
import jyserver.Flask as jsf

app = Flask(__name__,template_folder='templates')

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/',methods = ['GET','POST'])
def check():    
    result= ''
    if request.method == 'POST':
        text = request.form["syntax"]
        try:
            state = request.form["lexer"]
            if state == 'lexer':
                syntax = F(text)
                syntax.saveTokens()
                tokens = syntax.getTokens()
                result = tokens
            return render_template('index.html',result=result,text=text)   
        except:
            result=''
            result = ejecutarCodigo(text)
            print(result)
            return render_template('index.html',result=result,text=text)
    
    return render_template('index.html',result=result,text=text)
    
        
def ejecutarCodigo(text):    
    syntax = ejecutar(text)
        
    return syntax

if __name__ == "__main__":
    app.run(debug=True)