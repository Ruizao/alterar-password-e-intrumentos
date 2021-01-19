from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-18-203-62-227.eu-west-1.compute.amazonaws.com'
    Database = 'd3eqst3e8tmiel'
    User = 'qgqaupfcddzefz'
    Password = '0b5195a4d9d975747a145d5e3a53543130a3e0cb46df154981992e325ca97227'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')


def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def gravar2(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS insto (instro text, tipo text)")
    db.execute("INSERT INTO insto VALUES (%s, %s)", (v1, v2))
    ficheiro.commit()
    ficheiro.close()

def gravar3(v1, v2, v3, v4):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS arti (design text, descri text, quanti text, preço text)")
    db.execute("INSERT INTO arti VALUES (%s, %s, %s, %s)", (v1, v2, v3, v4))
    ficheiro.commit()
    ficheiro.close()

def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor

def existe2(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM insto WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor

def existe3(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM arti WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor

def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, code(v2),))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def alterar(v1, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (code(v3), v1))
    ficheiro.commit()
    ficheiro.close()


def apaga(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()

def code(passe):
    import hashlib
    return hashlib.sha3_256(passe.encode()).hexdigest()

@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, code (v3))
    return render_template('registo.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            apaga(v1)
            erro = 'Conta Eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['opass']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            alterar(v1, v2)
    return render_template('newpasse.html', erro=erro)


@app.route('/instrumento', methods=['GET', 'POST'])
def instrumento():
    erro = None
    if request.method == 'POST':
        v1 = request.form['instro']
        v2 = request.form['tipo']
        if existe2(v1):
            erro = ' O instrumento já existe'
        else:
            gravar2(v1, v2)
    return render_template('instrumento.html', erro=erro)

@app.route('/artigos', methods=['GET', 'POST'])
def artigos():
    erro = None
    if request.method == 'POST':
        v1 = request.form['design']
        v2 = request.form['descri']
        v3 = request.form['quanti']
        v4 = request.form['preço']
        if existe3(v1):
            erro = ' O Artigo já existe'
        else:
            gravar3(v1, v2, v3, v4)
    return render_template('artigos.html', erro=erro)

if __name__ == '__main__':
    app.run(debug=True)
