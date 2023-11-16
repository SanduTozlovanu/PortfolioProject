from datetime import datetime, timedelta
from random import randint

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
import JWTHelper
from exceptions import UnauthorizedException, ForbiddenException, BadRequestException, ConflictException, \
    NotFoundException
from privateServer import mailSender
from privateServer.app import db
from privateServer.app.models import User, Portfolio, Transaction, Stock


class UserController:
    @staticmethod
    def login(user_email: str, user_password: str, jwt_helper: JWTHelper) -> dict:
        user = User.query.filter(and_(User.email == user_email, User.password == user_password)).first()
        if user is None:
            raise UnauthorizedException()
        user: User
        if not user.status:
            raise ForbiddenException("The account hasn't been confirmed yet")
        return {"token": jwt_helper.create_jwt_token(user_email),  "name": user.name}

    @staticmethod
    def register(user_email: str, user_password: str, user_name: str, money, confirmations=None) -> User:
        try:
            created_on = datetime.now()
            if created_on.weekday() >= 5:
                created_on -= timedelta(days=2)
            else:
                created_on -= timedelta(days=1)
            new_user = User(email=user_email, password=user_password, name=user_name, type="user", status=True,
                            created_on=created_on)
            ''' Email confirmation functionality disabled 
            new_user = User(email=user_email, password=user_password, name=user_name, type="user", status=False,
                            created_on=created_on)
            random_number = randint(10000, 99999)
            confirmations.insert_one({'code': random_number, "email": user_email})
            mailSender.send_mail(user_email, random_number)
        except:
            raise BadRequestException("Wrong Data")
        try:
            '''
            db.session.add(new_user)
            db.session.commit()
            inserted_user = User.query.filter(User.email == new_user.email).first()
            new_portfolio = Portfolio(user_id=inserted_user.id, money=money, initial_money=money)
            db.session.add(new_portfolio)
            db.session.commit()
            return new_user
        except SQLAlchemyError:
            raise ConflictException("This user already exists")

    @staticmethod
    def reset(email):
        user: User = User.query.filter(User.email == email).first()
        created_on = datetime.now()
        if created_on.weekday() >= 5:
            created_on -= timedelta(days=2)
        else:
            created_on -= timedelta(days=1)
        user.created_on = created_on
        portfolio = Portfolio.get_portfolio(email)
        portfolio.money = portfolio.initial_money
        transaction_list: list[Transaction] = Transaction.query.filter(Transaction.portfolio_id == portfolio.id).all()
        for transaction in transaction_list:
            db.session.delete(transaction)

        stock_list: list[Stock] = Stock.query.filter(Stock.portfolio_id == portfolio.id).all()
        for stock in stock_list:
            db.session.delete(stock)
        db.session.commit()

    @staticmethod
    def confirm_resend(user_email, confirmations=None):
        random_number = randint(10000, 99999)
        confirmations.insert_one({'code': random_number, "email": user_email})
        mailSender.send_mail(user_email, random_number)

    @staticmethod
    def confirm(user_email: str, user_code: int, confirmations=None):
        found_code = False
        found_email = False
        for confirmation in confirmations.find({'email': user_email}):
            found_email = True
            if confirmation['email'] == user_email:
                if confirmation['code'] == user_code:
                    user = User.query.filter(User.email == user_email).first()
                    if user is None:
                        raise UnauthorizedException()
                    user: User
                    if user.status:
                        raise BadRequestException("User email is already confirmed!")
                    user.status = True
                    db.session.commit()
                    return
        if not found_email:
            raise NotFoundException("Email not found!")
        if not found_code:
            raise BadRequestException("Invalid Code")