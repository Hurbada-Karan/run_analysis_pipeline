# Crypto Sentiment vs. Trader Performance Dashboard

🚀 **Live Interactive Application:** [👉 Click Here to View the Live Dashboard 👈](https://karananalysis.streamlit.app/)

An interactive data science pipeline and web application designed to analyze the relationship between Web3 trader performance (Historical Hyperliquid execution data) and market sentiment (Bitcoin Fear & Greed Index).

---

## 📊 Project Overview
This project maps out and uncovers hidden alpha patterns from decentralized perpetual exchange (Hyperliquid) traders across different stages of the market cycle. 

### Key Insights Discovered
* **Contrarian Outperformance:** During periods of **Extreme Greed**, short positions significantly outpace long positions, averaging **$106.45** in Closed PnL compared to **$23.89** for longs. This demonstrates that top-tier traders effectively exploit overextended market euphoria by scale-shorting overbought momentum.
* **Sentiment Shifts:** As the market transitions into **Extreme Fear**, the profitable edge flips, favoring spot/long accumulations.
* **Execution Efficiency:** Isolating active closed positions reveals a high win rate (>75%) among historical accounts during peak volatility windows.

---

## 📁 Repository Structure
```text
├── app.py                         # Streamlit Interactive Web Application
├── run_analysis_pipeline.py       # Single-file CLI Analytics Pipeline script
├── requirements.txt               # Project dependencies
├── historical_data.csv            # Anonymized Hyperliquid trader execution logs
├── fear_greed_index.csv           # Historic Bitcoin Fear & Greed Index values
└── README.md                      # Project documentation
