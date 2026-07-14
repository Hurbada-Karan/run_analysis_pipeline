import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# App Page Configuration
st.set_page_config(
    page_title="Karan's Crypto Sentiment & Trader Performance Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Karan's Crypto Sentiment vs. Trader Performance Dashboard")
st.markdown("""
This interactive dashboard explores the relationship between **Hyperliquid Trader Performance (Closed PnL)** and **Bitcoin Market Sentiment (Fear & Greed Index)**.
*Built as a proof-of-concept pipeline for Web3 Trading Analytics.*
""")

# Sidebar settings
st.sidebar.header("📊 Upload & Configure")
uploaded_trader = st.sidebar.file_uploader("Upload Historical Trader CSV", type=["csv"])
uploaded_sentiment = st.sidebar.file_uploader("Upload Fear & Greed Index CSV", type=["csv"])

# Load default data if user hasn't uploaded their own files yet
@st.cache_data
def load_and_merge_data(trader_path, sentiment_path):
    try:
        fg_df = pd.read_csv(sentiment_path)
        hd_df = pd.read_csv(trader_path)
        
        # Datetime processing
        fg_df['date'] = pd.to_datetime(fg_df['date'])
        hd_df['Date'] = pd.to_datetime(hd_df['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
        hd_df['Date_Only'] = pd.to_datetime(hd_df['Date'].dt.date)
        
        # Merge
        merged = pd.merge(hd_df, fg_df, left_on='Date_Only', right_on='date', how='inner')
        merged = merged.drop(columns=['Date_Only', 'date'])
        
        # Direction clean-up
        def simplify_direction(dir_str):
            if pd.isna(dir_str): return 'Other'
            d = dir_str.lower()
            if 'long' in d or d == 'buy': return 'Long'
            elif 'short' in d or d == 'sell': return 'Short'
            return 'Other'
        
        merged['Direction_Group'] = merged['Direction'].apply(simplify_direction)
        return merged
    except Exception as e:
        st.error(f"Error processing files: {e}")
        return None

# Check if data is available (either uploaded or local fallback)
trader_file = uploaded_trader if uploaded_trader else 'historical_data.csv'
sentiment_file = uploaded_sentiment if uploaded_sentiment else 'fear_greed_index.csv'

try:
    df = load_and_merge_data(trader_file, sentiment_file)
except FileNotFoundError:
    df = None
    st.warning("Please upload both CSV files in the sidebar to populate the charts!")

if df is not None:
    # --- METRICS ROW ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades Analyzed", f"{len(df):,}")
    with col2:
        st.metric("Total Generated PnL", f"${df['Closed PnL'].sum():,.2f}")
    with col3:
        # Win rate of actual closed positions (PnL != 0)
        closed_trades = df[df['Closed PnL'] != 0]
        win_rate = (closed_trades['Closed PnL'] > 0).mean() * 100 if len(closed_trades) > 0 else 0
        st.metric("Core Position Win Rate", f"{win_rate:.1f}%")
    with col4:
        st.metric("Traded Tokens", f"{df['Coin'].nunique()}")

    st.markdown("---")

    # --- VISUALIZATION SECTION ---
    st.subheader("🎯 Average Closed PnL by Sentiment & Trade Direction")
    
    sentiment_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    plot_df = df[df['Direction_Group'].isin(['Long', 'Short'])].copy()
    plot_df['classification'] = pd.Categorical(plot_df['classification'], categories=sentiment_order, ordered=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=plot_df, 
        x='classification', 
        y='Closed PnL', 
        hue='Direction_Group', 
        estimator=np.mean, 
        errorbar=None, 
        palette='viridis',
        ax=ax
    )
    ax.set_ylabel('Average Closed PnL ($)')
    ax.set_xlabel('Bitcoin Fear & Greed Sentiment')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

    # --- STRATEGY SUMMARY ---
    st.info("""
    💡 **Alpha Insight:** Notice how Short positions dramatically outperform Longs in **Extreme Greed** (average short makes ~$106.45 vs. ~$23.89 for longs). 
    This indicates that top traders successfully exploit overextended market euphoria!
    """)