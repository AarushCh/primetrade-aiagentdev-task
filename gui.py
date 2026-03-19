import tkinter as tk
import customtkinter as ctk
import threading
from bot.client import get_binance_client, get_account_info
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import execute_trade

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TradingBotUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Binance Testnet Bot - Pro Edition")
        self.geometry("450x650")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self._copy_command)
        self.context_menu.add_command(label="Paste", command=self._paste_command)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self._select_all_command)
        self._current_widget = None

        self.label_title = ctk.CTkLabel(self.frame, text="🤖 Trading Terminal", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=10)

        self.stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.stats_frame.pack(pady=5, padx=20, fill="x")

        self.balance_label = ctk.CTkLabel(self.stats_frame, text="USDT Balance: $---", font=("Roboto", 12, "italic"))
        self.balance_label.pack(side="left", padx=10)

        self.pos_label = ctk.CTkLabel(self.stats_frame, text="Position: ---", font=("Roboto", 12, "italic"))
        self.pos_label.pack(side="right", padx=10)

        self.refresh_btn = ctk.CTkButton(self.frame, text="🔄 Refresh Stats", height=24, fg_color="gray25", command=self.update_account_stats)
        self.refresh_btn.pack(pady=5)

        self.symbol_input = ctk.CTkEntry(self.frame, placeholder_text="Symbol (e.g., BTCUSDT)", justify="center")
        self.symbol_input.insert(0, "BTCUSDT")
        self.symbol_input.pack(pady=10, padx=20, fill="x")
        self.symbol_input.bind("<Button-3>", self._show_context_menu)

        self.side_var = ctk.StringVar(value="BUY")
        self.side_segment = ctk.CTkSegmentedButton(self.frame, variable=self.side_var, values=["BUY", "SELL"])
        self.side_segment.pack(pady=10, padx=20, fill="x")

        self.type_var = ctk.StringVar(value="MARKET")
        self.type_segment = ctk.CTkSegmentedButton(self.frame, variable=self.type_var, values=["MARKET", "LIMIT", "STOP_MARKET"])
        self.type_segment.pack(pady=10, padx=20, fill="x")

        self.qty_input = ctk.CTkEntry(self.frame, placeholder_text="Quantity (e.g., 0.01)", justify="center")
        self.qty_input.insert(0, "0.01")
        self.qty_input.pack(pady=10, padx=20, fill="x")
        self.qty_input.bind("<Button-3>", self._show_context_menu)

        self.price_input = ctk.CTkEntry(self.frame, placeholder_text="Price (Leave blank for Market)", justify="center")
        self.price_input.pack(pady=10, padx=20, fill="x")
        self.price_input.bind("<Button-3>", self._show_context_menu)

        self.submit_btn = ctk.CTkButton(self.frame, text="Execute Trade 🚀", command=self.start_trade_thread, font=("Roboto", 14, "bold"))
        self.submit_btn.pack(pady=20, padx=20, fill="x")

        self.console = ctk.CTkTextbox(self.frame, height=120, state="normal", wrap="word")
        self.console.pack(pady=10, padx=20, fill="both", expand=True)
        self.console.bind("<Button-3>", self._show_context_menu)

        self.after(200, lambda: self.symbol_input.focus_set())
        self.after(500, self.update_account_stats)

    def _show_context_menu(self, event):
        self._current_widget = event.widget
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _copy_command(self):
        if self._current_widget:
            try:
                self._current_widget.event_generate("<<Copy>>")
            except Exception:
                pass

    def _paste_command(self):
        if self._current_widget:
            try:
                self._current_widget.event_generate("<<Paste>>")
            except Exception:
                pass

    def _select_all_command(self):
        if self._current_widget:
            try:
                if hasattr(self._current_widget, "select_range"):
                    self._current_widget.select_range(0, "end")
                    self._current_widget.icursor("end")
                elif hasattr(self._current_widget, "tag_add"):
                    self._current_widget.tag_add("sel", "1.0", "end")
            except Exception:
                pass

    def log_to_console(self, text):
        self.console.insert("end", text + "\n")
        self.console.see("end")

    def translate_error(self, error_msg):
        msg = str(error_msg).lower()
        if "invalid symbol" in msg and "''" in msg:
            return "Oops! You forgot to enter a coin. Try typing 'BTCUSDT' up top."
        elif "invalid symbol" in msg:
            return "We don't recognize that coin. Make sure it ends in 'USDT'."
        elif "quantity must be a number" in msg:
            return "Please enter a valid number for your trade amount."
        elif "greater than 0" in msg:
            return "You can't trade zero or negative amounts!"
        elif "positive price" in msg:
            return "For this order type, you need to tell us exactly what price you want."
        elif "-4005" in msg or "max quantity" in msg:
            return "Whoa there, whale! 🐋 That amount is too high for one trade."
        elif "-2019" in msg or "insufficient" in msg:
            return "It looks like your testnet account doesn't have enough fake funds."
        else:
            return f"Trade failed: {error_msg}"

    def update_account_stats(self):
        def fetch():
            try:
                symbol = self.symbol_input.get().upper()
                client = get_binance_client()
                data = get_account_info(client, symbol)
                self.balance_label.configure(text=f"USDT Balance: ${data['usdt_balance']:.2f}")
                self.pos_label.configure(text=f"{symbol} Pos: {data['symbol_position']}")
            except Exception:
                self.balance_label.configure(text="USDT Balance: Error")
        threading.Thread(target=fetch, daemon=True).start()

    def start_trade_thread(self):
        self.console.delete("1.0", "end")
        self.log_to_console("⏳ Sending order to Binance...")
        self.submit_btn.configure(state="disabled")
        threading.Thread(target=self.execute_trade_gui, daemon=True).start()

    def execute_trade_gui(self):
        try:
            symbol = self.symbol_input.get()
            side = self.side_var.get()
            order_type = self.type_var.get()
            quantity = float(self.qty_input.get())
            raw_price = self.price_input.get()
            price = float(raw_price) if raw_price.strip() else None

            clean_symbol = validate_symbol(symbol)
            clean_side = validate_side(side)
            clean_type = validate_order_type(order_type)
            clean_qty = validate_quantity(quantity)
            clean_price = validate_price(clean_type, price)

            client = get_binance_client() 
            response = execute_trade(client, clean_symbol, clean_side, clean_type, clean_qty, clean_price)

            self.log_to_console("✅ TRADE SUCCESSFUL!")
            self.log_to_console(f"Receipt ID: {response.get('orderId', 'N/A')}")
            self.update_account_stats()

        except Exception as e:
            friendly_msg = self.translate_error(e)
            self.log_to_console(f"❌ {friendly_msg}")
        finally:
            self.submit_btn.configure(state="normal")

if __name__ == "__main__":
    app = TradingBotUI()
    app.mainloop()