from typing import Optional

def validate_symbol(symbol: str) -> str:
    """Ensures the symbol is uppercase and looks valid."""
    symbol = symbol.strip().upper()
    if not symbol.endswith("USDT"):
        raise ValueError(f"Invalid symbol '{symbol}'. Please use a USDT pair (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    """Ensures the side is strictly BUY or SELL."""
    side = side.strip().upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Ensures the order type is supported."""
    order_type = order_type.strip().upper()
    valid_types = ["MARKET", "LIMIT", "STOP_MARKET"]
    if order_type not in valid_types:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {', '.join(valid_types)}.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Ensures quantity is a positive number."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(order_type: str, price: Optional[float]) -> Optional[float]:
    """Ensures price is provided if the order type requires it."""
    if order_type in ["LIMIT", "STOP_MARKET"] and (price is None or price <= 0):
        raise ValueError(f"A positive price must be specified for a {order_type} order.")
    if order_type == "MARKET" and price is not None:
        pass
    return price