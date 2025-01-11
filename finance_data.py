import yfinance as yf


def get_company_details(ticker):
    """Retrieves details about a company using its stock ticker via yfinance."""
    try:
        stock = yf.Ticker(ticker)
        company_info = stock.info

        # Check if the ticker corresponds to a valid company
        if 'longName' not in company_info:
            return f"'{ticker}' does not appear to be a valid stock ticker."

        # Retrieve company information
        company_name = company_info.get('longName', 'Unknown')
        sector = company_info.get('sector', 'Unknown')
        industry = company_info.get('industry', 'Unknown')
        total_revenue = company_info.get('totalRevenue', None)

        # Build response
        details = f"Company: {company_name} ({ticker})\n"
        details += f"Sector: {sector}\n"
        details += f"Industry: {industry}\n"

        if total_revenue:
            revenue_in_billions = total_revenue / 1e9  # Convert to billions
            details += f"Revenue: Approximately ${revenue_in_billions:.2f} billion\n"
        else:
            details += "Revenue data not found.\n"

        return details.strip()
    except KeyError:
        return f"Invalid data format received for {ticker}."
    except Exception as error:
        return f"An unexpected error occurred: {str(error)}"


def get_financial_data(ticker):
    """Retrieves key financial metrics for a company using its stock ticker."""
    try:
        stock = yf.Ticker(ticker)
        company_info = stock.info

        # Extract financial metrics
        pe_ratio = company_info.get('trailingPE', None)
        peg_ratio = company_info.get('pegRatio', None)
        beta_value = company_info.get('beta', None)
        company_name = company_info.get('longName', ticker)

        # Build response
        metrics = f"**Financial Metrics for {company_name} ({ticker}):**\n"

        if pe_ratio is not None:
            metrics += f"• P/E Ratio: {pe_ratio:.2f}\n"
            if pe_ratio < 15:
                metrics += "  ➡️ Indicates the stock might be undervalued.\n"
            elif pe_ratio > 25:
                metrics += "  ⚠️ Indicates the stock might be overvalued.\n"
            else:
                metrics += "  ✅ Indicates a fair valuation.\n"
        else:
            metrics += "• P/E Ratio: Not available\n"

        if peg_ratio is not None:
            metrics += f"• PEG Ratio: {peg_ratio:.2f}\n"
            if peg_ratio < 1:
                metrics += "  ➡️ Indicates the stock may have strong growth potential relative to its price.\n"
            else:
                metrics += "  ⚠️ Indicates the stock may be expensive for its growth.\n"
        else:
            metrics += "• PEG Ratio: Not available\n"

        if beta_value is not None:
            metrics += f"• Beta: {beta_value:.2f}\n"
            if beta_value < 1:
                metrics += "  ✅ Indicates lower volatility than the market (safer).\n"
            elif beta_value > 1.5:
                metrics += "  ⚠️ Indicates higher volatility than the market (riskier).\n"
            else:
                metrics += "  ➡️ Indicates moderate market volatility.\n"
        else:
            metrics += "• Beta: Not available\n"

        return metrics
    except KeyError:
        return f"Invalid data format received for {ticker}."
    except Exception as error:
        return f"An unexpected error occurred: {str(error)}"


def get_52_week_high_low(ticker):
    """Retrieves the 52-week high and low prices for a stock."""
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1y")

        high_52_week = stock_data['High'].max()
        low_52_week = stock_data['Low'].min()

        data = f"**52-Week High and Low for {ticker}:**\n"
        data += f"• 52-Week High: ${high_52_week:.2f}\n"
        data += f"• 52-Week Low: ${low_52_week:.2f}\n"

        return data
    except Exception as error:
        return f"An unexpected error occurred: {str(error)}"


def get_stock_recommendations(ticker):
    """Retrieves stock recommendations (counts of ratings for each period)."""
    try:
        stock = yf.Ticker(ticker)
        recommendations = stock.recommendations

        # If no recommendation data is available, return a message
        if recommendations.empty:
            return f"No stock recommendations found for {ticker}."

        # Get the most recent recommendation period (last row)
        latest_recommendation = recommendations.iloc[-1]
        period = latest_recommendation['period']

        # Build the recommendation summary text
        recommendation_text = f"**Stock Recommendations for {ticker} (Period: {period}):**\n"
        recommendation_text += f"• Strong Buy: {latest_recommendation['strongBuy']}\n"
        recommendation_text += f"• Buy: {latest_recommendation['buy']}\n"
        recommendation_text += f"• Hold: {latest_recommendation['hold']}\n"
        recommendation_text += f"• Sell: {latest_recommendation['sell']}\n"
        recommendation_text += f"• Strong Sell: {latest_recommendation['strongSell']}\n"

        return recommendation_text
    except Exception as error:
        return f"An unexpected error occurred: {str(error)}"
