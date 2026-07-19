# Project Title

**Strategy Tester - Bollinger Band EMA Trading Backtester**

A Python-based backtesting engine that evaluates Bollinger Band
(9-period) trend-following trades, simulates long/short positions,
applies trailing stop-loss logic, and generates detailed trade
performance statistics. The main backtesting for loop iterates 
sequentially one by one on the CPU (not parallely)

Built on - July 2024

## Table of Contents

-   [About The Project](#about-the-project)
-   [Built With](#built-with)
-   [Key Features](#key-features)
-   [Getting Started](#getting-started)
-   [Technologies Used
    (Prerequisites)](#technologies-used-prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [How It Works](#how-it-works)
-   [Main Python Functions](#main-python-functions)
-   [Disclaimer](#disclaimer)
-   [License Description](#license-description)

## About The Project

This project is a prototype trading strategy backtester focused on
Bollinger Band breakout behaviour. It calculates 9-period Bollinger
Bands, evaluates long and short entry/exit opportunities, simulates
trailing stop-loss exits, records every completed trade, and prints
profitability statistics. The current version also contains
placeholder/sample price data and commented-out live market data
integration using TradingView.

### Built With

-   Python 3
-   pandas
-   pandas-ta
-   yfinance
-   tvDatafeed
-   re
-   time

### Key Features

-   9-period Bollinger Band calculation
-   Long and short trade simulation
-   Dynamic trailing stop-loss
-   Trade logging
-   Profit/Loss calculation
-   Gross and net performance summary
-   TradingView data integration scaffold

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   pip
-   Internet connection (for live data)
-   TradingView account (optional)
-   Required libraries:
    -   pandas
    -   pandas-ta
    -   yfinance
    -   tvDatafeed

### Installation

``` bash
git clone https://github.com/pandiyan07/BTC-EMA-Bollinger-band-strategy-tester.git
cd BTC-EMA-Bollinger-band-strategy-tester
pip install pandas pandas-ta yfinance tvDatafeed
python Strategy_tester_BB_9EMA_130.py
```

## Usage

The script calculates Bollinger Bands, evaluates every candle, opens and
closes simulated positions, applies trailing stop-loss rules, and prints
detailed performance statistics.

## Project Structure

``` text
Strategy_tester_BB_9EMA_130.py
│
├── Imports
├── RSI_BOLLINGER_BAND_CALCULATOR()
│   ├── Creates indicator values
│   └── Sends processed data to trader
├── TRADER()
│   ├── Long entry logic
│   ├── Short entry logic
│   ├── Normal exits
│   ├── Trailing stop exits
│   └── Performance statistics
└── TradingView connection (prototype)
```

## How It Works

1.  Load historical/sample prices.
2.  Calculate 9-period Bollinger Bands.
3.  Iterate candle-by-candle.
4.  Check long entry conditions.
5.  Check short entry conditions.
6.  Monitor active positions.
7.  Apply normal exit conditions.
8.  Apply trailing stop-loss exits.
9.  Record every trade.
10. Display trade reports and profitability statistics.

## Main Python Functions

  --------------------------------------------------------------------------
  Function                            Description
  ----------------------------------- --------------------------------------
  `RSI_BOLLINGER_BAND_CALCULATOR()`   Creates Bollinger Band indicator
                                      dataset and prepares data for strategy
                                      execution.

  `TRADER()`                          Core backtesting engine handling
                                      entries, exits, stop-loss management,
                                      trade logging and statistics.
  --------------------------------------------------------------------------

## Disclaimer

This project is intended for educational, research, and strategy-testing
purposes only. It does not provide financial advice and should not be
used directly for live trading without extensive testing and risk
management.

## License Description

You may release this project under the MIT License, allowing
modification, distribution, commercial use, and private use while
preserving the copyright notice.
