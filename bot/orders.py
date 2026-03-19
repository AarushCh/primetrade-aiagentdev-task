import logging
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger("trading_bot.orders")

def execute_trade(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Executes a trade on Binance Futures Testnet.
    Handles MARKET, LIMIT, and STOP_MARKET orders.
    """
    
    order_params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        order_params["price"] = price
        order_params["timeInForce"] = "GTC" 
    elif order_type == "STOP_MARKET":
        order_params["stopPrice"] = price 
    
    logger.info(f"Attempting to place {side} {order_type} order for {quantity} {symbol}...")
    logger.debug(f"Order Parameters: {order_params}")

    try:
        response = client.futures_create_order(**order_params)
        
        logger.info(f"Order placed successfully! Order ID: {response.get('orderId')}")
        logger.debug(f"Full API Response: {response}")
        
        return response

    except BinanceAPIException as e:
        error_msg = f"Binance API Error: {e.message} (Code: {e.code})"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected Error during order execution: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)