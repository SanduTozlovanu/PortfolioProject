from plotly import graph_objs as go
from plotly.graph_objs import Figure

from privateServer.DTOs.PieChartDto import PieChartDto
from privateServer.PortfolioAnalyser import PortfolioAnalyser
from privateServer.app.models import Portfolio, Transaction, User, Stock


class ChartController:
    @staticmethod
    def get_portfolio_performance_chart(email, portfolio_analyser: PortfolioAnalyser) -> Figure:
        portfolio = Portfolio.get_portfolio(email)
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.asc()).all()
        user: User = User.query.filter(User.email == email).first()
        df = portfolio_analyser.portfolio_value_tracking_algorithm(transactions, user.created_on, portfolio.initial_money)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], name="Stock Value"))
        fig.layout.update(xaxis_rangeslider_visible=True, showlegend=False)
        return fig

    @staticmethod
    def get_portfolio_pieChart(portfolio: Portfolio) -> list[PieChartDto]:
        stocks: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        chart_data = [PieChartDto("CASH", portfolio.money)]
        for stock in stocks:
            chart_data.append(PieChartDto(stock.ticker, stock.quantity * stock.medium_buy_price))
        return chart_data
