📈 MT5 Trading Bot (Python)

A high-performance automated trading bot built with MetaTrader5 and Python for real-time market analysis, strategy execution, and efficient trade management.


## 🧠 Strategy Logic:
  The bot uses a simple breakout-based trading strategy:

  * **Buy Signal**: Triggered when the current candle closes above the previous candle’s high (bullish breakout)
  * **Sell Signal**: Triggered when the current candle closes below the previous candle’s low (bearish breakout)

  ### Position Management:
    * Only one position is open at a time
    * Opposite signals will close the current position and open a new one
    * Stop Loss and Take Profit are dynamically calculated based on entry price


## ⚙️ System Design

  * MT5 Terminal handles market data and execution
  * Python script connects using MetaTrader5 API
  * Real-time ticks are fetched every seconds
  * OHLC data is used to generate trading signals with candels showing (open, high, low, close)
  * Orders are sent using `order_send()` function

    The system runs in a continuous loop, simulating a live trading environment.


## ⚠️ Limitations

  * Strategy is simplistic and not optimized for all market conditions
  * No backtesting module implemented yet
  * No advanced risk management (fixed SL/TP only)
  * Performance may vary based on broker latency



## 🚀 Future Improvements

  * Add backtesting engine
  * Improve strategy using indicators (RSI, FVG, MSS)
  * Build a web dashboard for monitoring trades
  * Deploy bot on VPS for 24/7 execution
  * Add logging and analytics for performance tracking



## Setup :

1. Install dependencies:
 ```
  pip install MetaTrader5 pandas python-dotenv
  ```

2. Create a `.env` file:
  ```
  LOGIN=your_login
  PASSWORD=your_password
  SERVER=your_server
  ```

3. Run the bot:
  ```
  python test.py
  ```


##  Disclaimer

  This bot is for educational purposes only. Trading involves risk. COOL ?
