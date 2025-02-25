import yfinance as yf
import requests
from datetime import datetime
from logger_config import logger

def coletar_dados_acoes(assets):
    """
    Coleta dados das ações.
    Collects stock data.

    Args:
        assets (dict): Dicionário de ativos.
                       Dictionary of assets.

    Returns:
        list: Lista de dicionários com os dados das ações.
              List of dictionaries with stock data.
    """
    dados_acoes = []
    for symbol, empresa in assets.items():
        try:
            stock = yf.Ticker(symbol)
            historico = stock.history(period="2d")
            
            # Verificar se há dados disponíveis | Check if data is available
            if historico.empty or len(historico) < 2:
                logger.warning(f"Nenhum dado disponível para a ação {symbol} | No data available for stock {symbol}")
                continue

            preco_atual = historico["Close"].iloc[-1]
            preco_anterior = historico["Close"].iloc[-2]
            variacao_percentual = ((preco_atual - preco_anterior) / preco_anterior) * 100
            tendencia = "Subindo | Up" if variacao_percentual > 0 else "Caindo | Down"
            horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            link = f"https://finance.yahoo.com/quote/{symbol}"
            dados_acoes.append({
                "EMPRESA": empresa,
                "AÇÃO": symbol,
                "COTAÇÃO": preco_atual,
                "VARIAÇÃO PERCENTUAL": variacao_percentual,
                "HORÁRIO": horario,
                "TENDÊNCIA": tendencia,
                "LINK": link
            })
            logger.info(f"EMPRESA: {empresa} | AÇÃO: {symbol} | COTAÇÃO: {preco_atual} | VARIAÇÃO: {variacao_percentual:.2f}% | HORÁRIO: {horario} | TENDÊNCIA: {tendencia} | LINK: {link}")
        except Exception as e:
            logger.error(f"Erro ao obter dados da ação {symbol}: {e} | Error getting data for stock {symbol}: {e}")
    return dados_acoes

def obter_cotacoes_moedas(moedas):
    """
    Obtém as cotações do Real (BRL) em relação a outras moedas.
    Gets the exchange rates of BRL against other currencies.

    Args:
        moedas (dict): Dicionário de moedas.
                       Dictionary of currencies.

    Returns:
        list: Lista de dicionários com as cotações das moedas.
              List of dictionaries with currency exchange rates.
    """
    cotacoes = []
    for moeda, nome in moedas.items():
        try:
            response = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL")
            response.raise_for_status()
            dados = response.json()[f"{moeda}BRL"]
            cotacao_atual = float(dados["bid"])
            cotacao_anterior = float(dados["ask"])
            variacao = ((cotacao_atual - cotacao_anterior) / cotacao_anterior) * 100
            tendencia = "Subindo | Up" if variacao > 0 else "Caindo | Down"
            horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cotacoes.append({
                "NOME": nome,
                "MOEDA": moeda,
                "COTAÇÃO": cotacao_atual,
                "VARIAÇÃO PERCENTUAL": variacao,
                "TENDÊNCIA": tendencia,
                "DATA E HORÁRIO": horario
            })
            logger.info(f"MOEDA: {nome} | COTAÇÃO: {cotacao_atual} | VARIAÇÃO: {variacao:.2f}% | TENDÊNCIA: {tendencia} | HORÁRIO: {horario}")
        except Exception as e:
            logger.error(f"Erro ao obter dados da moeda {moeda}: {e} | Error getting data for currency {moeda}: {e}")
    return cotacoes