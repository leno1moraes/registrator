from flask import Flask, request, jsonify, send_file, abort, redirect, url_for, render_template
import os
import psycopg2

app = Flask(__name__)


DATABASE_URL = "postgresql://postgres:mypassword@database:5432/mydatabase"


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrator (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(15) NOT NULL,
            campus VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Rota para pagina inicial
@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

# Rota para criar um novo registro
@app.route('/add', methods=['POST'])
def create_registrator():
    data = request.get_json()
    ip = data['ip']
    campus = data['campus']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO registrator (ip, campus) VALUES (%s, %s)", (ip, campus))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro criado com sucesso'}), 201

# Rota para obter todos os registros
@app.route('/registrator', methods=['GET'])
def get_all_registrators():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrator")
    rows = cur.fetchall()
    conn.close()
    registrators = [{'id': row[0], 'ip': row[1], 'campus': row[2]} for row in rows]
    return jsonify(registrators), 200

# Rota para atualizar um registro existente
# @app.route('/registrator/<int:id>', methods=['PUT'])
# def update_registrator(id):
#     data = request.get_json()
#     ip = data['ip']
#     campus = data['campus']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("UPDATE registrator SET ip = %s, campus = %s WHERE id = %s", (ip, campus, id))
#     conn.commit()
#     conn.close()
#     return jsonify({'message': 'Registro atualizado com sucesso'}), 200

# Rota para excluir um registro existente
@app.route('/registrator/<int:id>', methods=['DELETE'])
def delete_registrator(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM registrator WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro excluído com sucesso'}), 200

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=8000)
