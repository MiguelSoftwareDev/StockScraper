from data_collector import coletar_dados_acoes, obter_cotacoes_moedas
from file_handler import salvar_parquet, salvar_excel_formatado, abrir_excel
from database_manager import conectar_banco_dados, criar_tabelas, inserir_dados
from config import ASSETS, MOEDAS
from logger_config import logger
import time
from datetime import datetime, timedelta

def main():
    # Verifica se o usuário tem um banco de dados MySQL aberto | Check if the user has a MySQL database open
    print("O MySQL já está rodando? (Sim/Não) | Is MySQL already running? (Yes/No)")
    resposta = input().strip().lower()
    tem_banco = resposta in ["s", "sim", "y", "yes"]

    if tem_banco:
        DB_HOST = "localhost"
        DB_USER = input("Usuário do banco (padrão: root): | Database user (default: root): ") or "root"
        DB_PASSWORD = input("Senha do banco: | Database password: ") or ""
        DB_NAME = "CoinAI"

        try:
            # Conectar ao MySQL e garantir que o banco de dados existe | Connect to MySQL and ensure the database exists
            conn, cursor = conectar_banco_dados(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
            criar_tabelas(cursor)

            # Pergunta o tempo de execução e intervalo de coleta | Ask for execution time and collection interval
            tempo_execucao = int(input("Tempo de execução (minutos): | Execution time (minutes): "))
            intervalo = int(input("Intervalo entre coletas (segundos): | Interval between collections (seconds): "))
            tempo_final = datetime.now() + timedelta(minutes=tempo_execucao)

            while datetime.now() < tempo_final:
                # Captura os dados do mercado | Fetch market data
                dados_acoes = coletar_dados_acoes(ASSETS)
                dados_moedas = obter_cotacoes_moedas(MOEDAS)

                # Salva os dados em arquivos Parquet | Save data in Parquet files
                nome_arquivo_acoes = f"dados_acoes_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet"
                nome_arquivo_moedas = f"dados_moedas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet"
                salvar_parquet(dados_acoes, nome_arquivo_acoes)
                salvar_parquet(dados_moedas, nome_arquivo_moedas)

                # Insere os dados no banco de dados | Insert data into the database
                inserir_dados(cursor, "acoes", dados_acoes)
                inserir_dados(cursor, "moedas", dados_moedas)
                conn.commit()

                logger.info(f"Próxima coleta em {intervalo} segundos. | Next collection in {intervalo} seconds.")
                time.sleep(intervalo)

            # Fecha a conexão com o banco de dados | Close the database connection
            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(f"Erro ao interagir com o banco de dados: {e} | Error interacting with the database: {e}")
    else:
        # Caso não tenha banco, apenas salva os dados em Excel | If no database, save data in Excel only
        dados_acoes = coletar_dados_acoes(ASSETS)
        dados_moedas = obter_cotacoes_moedas(MOEDAS)

        # Gera um arquivo Excel com os dados | Generate an Excel file with the data
        nome_arquivo = f"dados_bolsa_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        caminho_excel = salvar_excel_formatado(dados_acoes, dados_moedas, nome_arquivo)

        if caminho_excel:
            # Abre o arquivo Excel gerado | Open the generated Excel file
            abrir_excel(caminho_excel)

if __name__ == "__main__":
    main()
