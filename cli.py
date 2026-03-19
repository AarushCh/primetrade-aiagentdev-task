import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from bot.logging_config import logger
from bot.client import get_binance_client
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)
from bot.orders import execute_trade

app = typer.Typer(help="Binance Futures Testnet Trading Bot (Overachiever Edition)")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair, e.g., BTCUSDT"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET, LIMIT, or STOP_MARKET"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Amount to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Required for LIMIT and STOP_MARKET orders")
):
    """
    Executes a trade on the Binance Futures Testnet with beautiful CLI output.
    """
    console.print(Panel.fit("[bold cyan] Initializing Trading Bot...[/bold cyan]", border_style="cyan"))

    try:
        clean_symbol = validate_symbol(symbol)
        clean_side = validate_side(side)
        clean_type = validate_order_type(order_type)
        clean_qty = validate_quantity(quantity)
        clean_price = validate_price(clean_type, price)

        summary_table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Parameter", style="dim")
        summary_table.add_column("Value", style="bold white")
        
        summary_table.add_row("Symbol", clean_symbol)
        summary_table.add_row("Side", f"[{'green' if clean_side == 'BUY' else 'red'}]{clean_side}[/]")
        summary_table.add_row("Type", clean_type)
        summary_table.add_row("Quantity", str(clean_qty))
        if clean_price:
            summary_table.add_row("Price", str(clean_price))

        console.print(summary_table)

        with console.status("[bold yellow]Connecting to Binance Testnet & Executing...[/bold yellow]", spinner="dots"):
            client = get_binance_client()
            response = execute_trade(
                client=client,
                symbol=clean_symbol,
                side=clean_side,
                order_type=clean_type,
                quantity=clean_qty,
                price=clean_price
            )

        console.print(Panel("[bold green]Trade Executed Successfully![/bold green]", border_style="green"))
        
        res_table = Table(show_header=True, header_style="bold green")
        res_table.add_column("Order ID")
        res_table.add_column("Status")
        res_table.add_column("Executed Qty")
        res_table.add_column("Avg Price")

        res_table.add_row(
            str(response.get("orderId", "N/A")),
            response.get("status", "N/A"),
            str(response.get("executedQty", "0")),
            str(response.get("avgPrice", "0"))
        )
        console.print(res_table)
        console.print("\n")

    except ValueError as ve:
        console.print(Panel(f"[bold red]Input Error:[/bold red] {ve}", border_style="red"))
        logger.warning(f"User input error: {ve}")
    except Exception as e:
        console.print(Panel(f"[bold red]Execution Error:[/bold red] {e}", border_style="red"))
        logger.error(f"Critical error during CLI execution: {e}")

if __name__ == "__main__":
    app()