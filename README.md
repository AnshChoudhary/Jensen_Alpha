# Stock Performance Analysis Web App

This repository contains a **Streamlit web application** for analyzing the performance of any stock by calculating **Jensen's Alpha**, **Beta**, and providing insights into its sensitivity and performance relative to the market index.

## Features

- Upload stock price and market index data (CSV format).
- Automatically calculate monthly returns for the stock and market index.
- Estimate **Jensen's Alpha** and **Beta** using regression analysis.
- Visualize the stock's performance compared to the market index.
- Generate detailed insights based on the results.
- User-friendly interface powered by **Streamlit**.

## Installation

To run the web app locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/stock-performance-app.git
   cd stock-performance-app
   ```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

Open the app in your browser at http://localhost:8501.
