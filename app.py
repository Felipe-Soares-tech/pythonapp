from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route('/')

def home():
    return 'Olá, Flask'

@app.route('/item', methods = ['POST'])

def post_item():
    data = request.get_json()
    sql = f"INSERT INTO todolist(item, status) VALUES('{data['item']}','{data['status']}') RETURNING \"_lineNumber\""
    banco(sql)
    lineNumber = banco(sql)
    data["_lineNumber"] = lineNumber
    return data

@app.route('/item', methods = ['GET'])
def get_item():
    sql = "SELECT * FROM todolist"
    return banco(sql)

def banco(sql):
    resultado = ""
    try:
        # Conexão com o banco de dados PostgreeSQL
        conn = psycopg2.connect(
            host = 'dpg-cuhul4bv2p9s73c22g80-a.oregon-postgres.render.com',
            port = '5432',
            dbname = 'senaidb_fhpm',
            user = 'senaidb_fhpm_user',
            password = 'F8kSUUFo7ZUgLut1vGGrqJTY9IhL4cCz'
        )
        cursor = conn.cursor() # cursor vai ser a variavel para executar os comandos SQL.
        cursor.execute(sql) # executa o comando sql seja insert, select .. etc
        if sql[0:6] == "INSERT":
            resultado = cursor.fetchone()[0]
        elif sql[0:6] == "SELECT":
            resultado = cursor.fetchall() # vai guardar o resultado do select na var resultado
        cursor.close() #finaliza o cursor
        conn.commit() # confirma o comando SQL
        conn.close() # finaliza a conexão
        return resultado

    except psycopg2.Error as e:
        print("Erro na conexão do banco de dados")


if __name__ == '__main__':
    app.run(debug=True)
