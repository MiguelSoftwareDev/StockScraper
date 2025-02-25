import pymysql
from logger_config import logger

def conectar_banco_dados(host, user, password, database=None):
    """
    Conecta ao banco de dados MySQL.
    Connects to the MySQL database.

    Args:
        host (str): Host do banco de dados.
                    Database host.
        user (str): Usuário do banco de dados.
                    Database user.
        password (str): Senha do banco de dados.
                        Database password.
        database (str, optional): Nome do banco de dados.
                                  Database name.

    Returns:
        tuple: Conexão e cursor.
               Connection and cursor.
    """
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        logger.info("Conectado ao banco de dados. | Connected to the database.")
        return conn, cursor
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1049:  # Erro de banco de dados desconhecido | Unknown database error
            logger.info(f"Banco de dados '{database}' não existe. Criando... | Database '{database}' does not exist. Creating...")
            conn = pymysql.connect(host=host, user=user, password=password)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {database}")
            conn.select_db(database)
            logger.info(f"Banco de dados '{database}' criado. | Database '{database}' created.")
            return conn, cursor
        else:
            logger.error(f"Erro ao conectar ao banco de dados: {e} | Error connecting to the database: {e}")
            raise
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e} | Error connecting to the database: {e}")
        raise

def criar_tabelas(cursor):
    """
    Cria as tabelas no banco de dados, se não existirem.
    Creates tables in the database if they don't exist.

    Args:
        cursor: Cursor do banco de dados.
                Database cursor.
    """
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS acoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            empresa VARCHAR(255) NOT NULL,
            acao VARCHAR(50) NOT NULL,
            cotacao FLOAT NOT NULL,
            variacao_percentual FLOAT NOT NULL,
            horario DATETIME NOT NULL,
            tendencia VARCHAR(50) NOT NULL,
            link TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS moedas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            moeda VARCHAR(50) NOT NULL,
            cotacao FLOAT NOT NULL,
            variacao_percentual FLOAT NOT NULL,
            tendencia VARCHAR(50) NOT NULL,
            data_horario DATETIME NOT NULL
        )
        """)
        logger.info("Tabelas prontas. | Tables ready.")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e} | Error creating tables: {e}")
        raise

def inserir_dados(cursor, tabela, dados):
    """
    Insere dados na tabela especificada.
    Inserts data into the specified table.

    Args:
        cursor: Cursor do banco de dados.
                Database cursor.
        tabela (str): Nome da tabela.
                      Table name.
        dados (list): Lista de dicionários com os dados.
                      List of dictionaries with data.
    """
    try:
        if tabela == "acoes":
            for item in dados:
                cursor.execute("""
                INSERT INTO acoes (empresa, acao, cotacao, variacao_percentual, horario, tendencia, link)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (item["EMPRESA"], item["AÇÃO"], item["COTAÇÃO"], item["VARIAÇÃO PERCENTUAL"], item["HORÁRIO"], item["TENDÊNCIA"], item["LINK"]))
        elif tabela == "moedas":
            for item in dados:
                cursor.execute("""
                INSERT INTO moedas (nome, moeda, cotacao, variacao_percentual, tendencia, data_horario)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (item["NOME"], item["MOEDA"], item["COTAÇÃO"], item["VARIAÇÃO PERCENTUAL"], item["TENDÊNCIA"], item["DATA E HORÁRIO"]))
        logger.info(f"Dados inseridos na tabela {tabela}. | Data inserted into table {tabela}.")
    except Exception as e:
        logger.error(f"Erro ao inserir dados na tabela {tabela}: {e} | Error inserting data into table {tabela}: {e}")
        raise