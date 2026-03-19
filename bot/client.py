import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_binance_client() -> Client:
    """
    Initializes and returns an authenticated Binance Client.
    Strictly connects to the Futures Testnet URL provided in the requirements.
    """
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        logger.critical("API Key or Secret missing from environment variables.")
        raise ValueError("Missing Binance API credentials. Please check your .env file.")

    try:
        client = Client(api_key, api_secret, testnet=True)
        
        client.FUTURES_URL = base_url
        
        client.futures_ping()
        logger.info("Successfully connected to Binance Futures Testnet.")
        
        return client
        
    except BinanceAPIException as e:
        logger.error(f"Binance API connection failed: {e.message} (Code: {e.code})")
        raise
    except Exception as e:
        logger.error(f"Unexpected network or initialization error: {e}")
        raise

def get_account_info(client, symbol):
    """Fetches USDT balance and current position for a specific symbol."""
    try:
        balances = client.futures_account_balance()
        usdt_balance = next((item['balance'] for item in balances if item['asset'] == 'USDT'), "0.00")

        positions = client.futures_position_information(symbol=symbol)
        symbol_pos = next((item['positionAmt'] for item in positions if item['symbol'] == symbol), "0.00")

        return {
            "usdt_balance": float(usdt_balance),
            "symbol_position": float(symbol_pos)
        }
    except Exception as e:
        logger.error(f"Error fetching account info: {e}")
        raise e