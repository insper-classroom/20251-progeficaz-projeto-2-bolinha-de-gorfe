from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.env')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'defaultdb'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}


# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None



@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()
    sql = "SELECT * from imoveis.imoveis"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8],
            }
            imoveis.append(imovel_dict)

        resp = {"imovel": imoveis}
        return resp, 200
    

@app.route("/imoveis/cidade/<string:cidade>", methods=["GET"])
def listar_imoveis_por_cidade(cidade):
    """Retorna uma lista de imóveis filtrados por cidade."""
    imoveis = imoveis.query.filter_by(cidade=cidade).all()
    
    if not imoveis:
        resp = {"erro": "Nenhum imóvel encontrado nessa cidade."}
        return resp, 404

    resultado = [
        {"id": imovel.id, "titulo": imovel.titulo, "preco": imovel.preco, "cidade": imovel.cidade}
        for imovel in imoveis
    ]

    resp = {'imoveis': resultado}
    
    return resp, 200




@app.route('/imoveis/delete/<int:id>', methods=['DELETE'])
def excluir_imovel(id):
        
  conn = connect_db

  if conn is None:
      resp = {'erro': 'Erro ao conectar ao banco de dados'}
      return resp, 500 

  cursor = conn.cursor()

  cursor.execute("DELETE FROM imoveis.imoveis WHERE id = %s", (id)) 
  conn.commit()

  if conn.is_connected(): 
    cursor.close()
    conn.close()

    resp = { "mensagem": "Imóvel removido com sucesso."}

    return resp, 200
   
@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def listar_por_cidade(cidade):
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM imoveis.imoveis WHERE cidade = %s"

    cursor.execute(sql,(cidade,))
    results = cursor.fetchall()
    
    if not results:
        resp = {"erro": "Nenhum imovel encontrado nessa cidade"}
        return resp, 404
    
    imoveis = []
    for imovel in results:
        imovel_dict = {
            "id": imovel[0],
            "logradouro": imovel[1],
            "tipo_logradouro": imovel[2],
            "bairro": imovel[3],
            "cidade": imovel[4],
            "cep": imovel[5],
            "tipo": imovel[6],
            "valor": imovel[7],
            "data_aquisicao": imovel[8],
        }
        imoveis.append(imovel_dict)

    resp = {"imovel": imoveis}
    return resp, 200


    
@app.route('/imoveis/<int:id>', methods=['GET'])
def get_imovel_by_id(id):
    conn = connect_db()
    cursor = conn.cursor()


    sql = ("SELECT * FROM imoveis.imoveis WHERE id =%s")  
    cursor.execute(sql,(id,))
    imovel = cursor.fetchone()

    return jsonify({"id": imovel[0], "logradouro": imovel[1], "tipo_logradouro": imovel[2], "bairro": imovel[3],"cidade": imovel[4], "cep": imovel[5], "tipo": imovel[6], "valor": imovel[7], "data_aquisicao": imovel[8]}),200

@app.route('/imoveis', methods=['POST'])
def post_imovel():
    
    conn = connect_db()
    cursor = conn.cursor()

    dados = request.json
    sql = "INSERT INTO imoveis.imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    valores = dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"], dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"]

    cursor.execute(sql, valores)
    

    conn.commit()
    return jsonify({"mensagem": "imovel criado com sucesso"}), 200

@app.route('/imoveis/<int:id>', methods=['PUT'])
def update_imovel(id):
    
    conn = connect_db()
    cursor = conn.cursor()

    dados = request.json
    sql = "UPDATE imoveis.imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s"

    valores = dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"], dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"], id
    cursor.execute(sql, valores)
    conn.commit()
    return jsonify({"mensagem": "imovel atualizade com sucesso"}), 201


if __name__ == '__main__':
    app.run(debug=True)