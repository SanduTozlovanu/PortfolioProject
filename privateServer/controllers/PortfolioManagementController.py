from datetime import datetime

from sqlalchemy import and_

from exceptions import BadRequestException, NotFoundException
from privateServer.app import db
from privateServer.app.models import Portfolio, Stock, Transaction


class PortfolioManagementController:
    @staticmethod
    def buy_stock(ticker: str, price: float, quantity: int, portfolio: Portfolio):
        if quantity < 1:
            raise BadRequestException("You can't but less than 1 share")
        if quantity * price > portfolio.money:
            raise BadRequestException("Not enough funds to buy stock")
        stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
        if stock is None:
            new_stock = Stock(ticker=ticker, portfolio_id=portfolio.id, medium_buy_price=price,
                              buy_date=datetime.now(), quantity=quantity)
            db.session.add(new_stock)
        else:
            stock.medium_buy_price = (stock.medium_buy_price * stock.quantity + price * quantity) / (
                    quantity + stock.quantity)
            stock.quantity += quantity
        portfolio.money -= (quantity * price)
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.now(),
                                      quantity=quantity, is_buy=True, cash_after_transaction=portfolio.money)
        db.session.add(new_transaction)
        db.session.commit()

    @staticmethod
    def buy_stock_batch(portfolio: Portfolio, stock_list):
        for stock in stock_list:
            quantity = stock["quantity"]
            price = stock["price"]
            ticker = stock["ticker"]
            if quantity < 1:
                raise BadRequestException("You can't but less than 1 share")
            if quantity * price > portfolio.money:
                raise BadRequestException("Not enough funds to buy stock")
            stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
            if stock is None:
                new_stock = Stock(ticker=ticker, portfolio_id=portfolio.id, medium_buy_price=price,
                                  buy_date=datetime.now(), quantity=quantity)
                db.session.add(new_stock)
            else:
                stock.medium_buy_price = (stock.medium_buy_price * stock.quantity + price * quantity) / (
                        quantity + stock.quantity)
                stock.quantity += quantity
            portfolio.money -= (quantity * price)
            new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                          date=datetime.now(),
                                          quantity=quantity, is_buy=True, cash_after_transaction=portfolio.money)
            db.session.add(new_transaction)
        db.session.commit()

    @staticmethod
    def sell_stock(ticker: str, price: float, quantity: int, portfolio: Portfolio):
        stock: Stock = Stock.query.filter(and_(Stock.ticker == ticker, Stock.portfolio_id == portfolio.id)).first()
        if stock is None:
            raise NotFoundException("You dont own this stock!")
        else:
            if stock.quantity < quantity:
                raise BadRequestException("You dont have enough of this stock!")
            stock.quantity -= quantity
            if stock.quantity == 0:
                db.session.delete(stock)
        portfolio.money += (quantity * price)
        new_transaction = Transaction(portfolio_id=portfolio.id, ticker=ticker, piece_price=price,
                                      date=datetime.now(),
                                      quantity=quantity, is_buy=False, cash_after_transaction=portfolio.money)
        db.session.add(new_transaction)
        db.session.commit()
