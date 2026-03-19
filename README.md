# 📈 Binance Futures Pro Trading Terminal
**Production-Ready Trading Suite for USDT-M Testnet**

A robust, high-performance Python application designed for the **Binance Futures Testnet**. This project demonstrates a modular API architecture, a polished Command Line Interface (CLI), and a modern Native Desktop GUI with real-time account tracking.

---

## ✨ Key Features
* **🖥️ Dual-Interface Support:**
    * **Pro CLI:** Interactive terminal experience powered by `Typer` and `Rich` for color-coded data visualization.
    * **Desktop App:** A sleek, dark-mode GUI (`CustomTkinter`) featuring a "one-click" execution workflow.
* **💰 Live Portfolio Stats:** Real-time fetching of **USDT Balance** and **Symbol Position** directly on the dashboard.
* **🛡️ Smart Error Translation:** Technical API errors (e.g., `-2019`, `-4005`) are automatically translated into friendly, actionable advice.
* **⚡ Advanced Order Logic:** Native support for `MARKET`, `LIMIT`, and `STOP_MARKET` order types.
* **📑 Enterprise Logging:** Automated, daily-rotating logs (`/logs`) capture every request and network event for full auditability.

---

## 📁 Project Architecture
The codebase follows strict **SOLID** principles, ensuring the trading logic is fully decoupled from the presentation layer.

```text
trading_bot/
├── bot/
│   ├── client.py          # API connection & Data fetching
│   ├── logging_config.py  # Centralized logging setup
│   ├── orders.py          # Trade execution logic
│   └── validators.py      # Input sanitization & business rules
├── logs/                  # Auto-generated execution proof
├── cli.py                 # Premium CLI Entry point
├── gui.py                 # Desktop Application source
├── requirements.txt       # Dependency list
└── README.md              # Documentation
```

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### 2. Configuration
Create a .env file in the root directory:

```bash
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BINANCE_BASE_URL=[https://testnet.binancefuture.com](https://testnet.binancefuture.com)
```

### 3. Usage
Launch Desktop GUI:

python gui.py
Execute via CLI:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

## 🧠 Development Assumptions

Asset Focus: Validated exclusively for USDT-Margined Futures pairs.

UI Responsiveness: Utilizes Python threading to keep API calls off the main UI loop, preventing interface lag.

Security: Implements .env variable loading to ensure API credentials remain out of the source code.

# Developed by Aarush | Python Developer & AI Agent Specialist