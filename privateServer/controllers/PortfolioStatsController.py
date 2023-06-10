from privateServer.DTOs.PortfolioStatsDto import PortfolioStatsDto
from privateServer.PortfolioAnalyser import PortfolioAnalyser
from privateServer.app.models import Portfolio, Stock, Transaction, User


class PortfolioStatsController:
    @staticmethod
    def get_portfolio_stock_list(portfolio: Portfolio) -> list[Stock]:
        stock_list: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        return stock_list

    @staticmethod
    def get_portfolio_stats(email: str, portfolio_analyser: PortfolioAnalyser) -> PortfolioStatsDto:
        portfolio = Portfolio.get_portfolio(email)
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.asc()).all()
        user: User = User.query.filter(User.email == email).first()
        stocks: Stock = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        stats: PortfolioStatsDto = portfolio_analyser.get_portfolio_stats(len(stocks), transactions, user.created_on,
                                                                          portfolio.initial_money)
        return stats
    @staticmethod
    def get_transaction_list(portfolio: Portfolio):
        transactions: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).order_by(
            Transaction.date.desc()).all()
        return transactions
