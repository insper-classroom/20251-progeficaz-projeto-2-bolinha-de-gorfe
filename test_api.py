import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db  # Importamos a aplicação Flask e a função de conexão

@pytest.fixture
def imovel():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel

@patch("api.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_imoveis(mock_connect_db, imovel):
    """Testa a rota /imoveis sem acessar o banco de dados real."""
 
    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "Mariana Gomes", "Rua", "Itaim Bibi", "São Paulo", "04550004", "apartamento", "123425", "2017-07-29"),
        (2, "Lorenzo Flosi", "Avenida", "Vila Olimpia", "São Paulo", "04545004", "apartamento", "458609", "2024-04-10"),
    ]

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = imovel.get("/imoveis")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "Mariana Gomes", "tipo_logradouro": "Rua", "bairro": "Itaim Bibi", "cidade": "São Paulo", "cep": "04550004", "tipo": "apartamento", "valor": "123425", "data_aquisicao":"2017-07-29"},
            {"id": 2, "logradouro": "Lorenzo Flosi", "tipo_logradouro": "Avenida", "bairro": "Vila Olimpia", "cidade": "São Paulo", "cep": "04545004", "tipo": "apartamento", "valor": "458609", "data_aquisicao": "2024-04-10"},
        ]
    }
    
    assert response.get_json() == expected_response





@patch("api.connect_db")  
def test_listar_por_cidade(mock_connect_db, imovel):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [(1, "Mariana Gomes", "Rua", "Itaim Bibi", "São Paulo", "04550004", "apartamento", "123425", "2017-07-29"),
        (2, "Lorenzo Flosi", "Avenida", "Vila Olimpia", "São Paulo", "04545004", "apartamento", "458609", "2024-04-10"),], 200

    mock_connect_db.return_value = mock_conn

    response = imovel.get("/cidade")

    assert response.status_code == 200

    expected_response = {
        'imovel': [ 
        {1, "Mariana Gomes", "Rua", "Itaim Bibi", "São Paulo", "04550004", "apartamento", "123425", "2017-07-29"},
        {2, "Lorenzo Flosi", "Avenida", "Vila Olimpia", "São Paulo", "04545004", "apartamento", "458609", "2024-04-10"}
        ]
    }

    assert response.get_json() == expected_response   

@patch("api.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_excluir_imovel(mock_connect_db, imovel):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.return_value = None


    mock_cursor.fetchall.side_effect = [
        [
        (1, "Mariana Gomes", "Rua", "Itaim Bibi", "São Paulo", "04550004", "apartamento", "123425", "2017-07-29"),
        (2, "Lorenzo Flosi", "Avenida", "Vila Olimpia", "São Paulo", "04545004", "apartamento", "458609", "2024-04-10")
        ]
    ]

    mock_connect_db.return_value = mock_conn

    response = imovel.delete("/imoveis/delete/1")


    assert response.status_code == 200

    expected_message = {
        "mensagem": "Imóvel removido com sucesso." 
    }

    assert response.get_json() == expected_message




 