from flask import Flask, request, render_template
import psycopg2, json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/item', methods=['POST'])
def post_item():
    data = request.get_json()
    sql = f"INSERT INTO todolist(item, status) VALUES('{data['item']}','{data['status']}') RETURNING \"_lineNumber\""
    lineNumber = banco(sql)
    data["_lineNumber"] = lineNumber
    return data

@app.route('/item', methods=['GET'])
def get_item():
    sql = "SELECT * FROM todolist"
    return banco(sql)

@app.route('/item/<int:lineNumber>', methods=['PATCH'])
def patch_item(lineNumber):
    data = request.get_json()
    sql = f"UPDATE todolist SET item = '{data['item']}', status = '{data['status']}' WHERE \"_lineNumber\" = {lineNumber}"
    banco(sql)
    return data

@app.route('/item/<int:lineNumber>', methods=['DELETE'])
def delete_item(lineNumber):
    sql = f"DELETE FROM todolist WHERE \"_lineNumber\" = {lineNumber}"
    banco(sql)
    return ""

def banco(sql):
    resultado = ""
    try:
        # Conexão com o banco de dados PostgreSQL
        conn = psycopg2.connect(
            host = "dpg-cuhulhlds78s73e3eabg-a.oregon-postgres.render.com",
            port = "5432",
            dbname = "senaidb_giju",
            user = "senaidb_giju_user",
            password = "oynUaoIszXotTDt9caTgB5x17bp0etxB"
        )
        cursor = conn.cursor() # cursor vai ser a variável para executar os comandos SQL.
        cursor.execute(sql) # executa o comando sql seja insert, select .. etc

        if sql[0:6] == "INSERT":
            resultado = cursor.fetchone()[0]
        elif sql[0:6] == "SELECT":
            resultado = cursor.fetchall() # vai guardar o resultado do select na var resultado
            colunas = [desc[0] for desc in cursor.description]
            resultado = json.dumps([dict(zip(colunas, row)) for row in resultado])
            resultado = json.loads(resultado)

        cursor.close() # finaliza o cursor
        conn.commit() # confirma o comando SQL 
        conn.close() # finaliza a conexão
    except psycopg2.Error as e:
        print("Erro na conexão do baaaaaaanco de dados")
    return resultado


if __name__ == '__main__':
    app.run(debug=True)

    
