from plotly.graph_objs import Figure

from exceptions import NotFoundException
from publicServer.DTOs.RevenueChartBarDto import RevenueChartBarDto
from publicServer.Database.Models.FinancialStatement import FinancialStatement
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.PricePrediction import PricePrediction
from publicServer.Database.session import db
import yfinance as yf
from plotly import graph_objs as go


class ChartController:
    @staticmethod
    def receive_company_price_chart(company_ticker) -> Figure:
        company = db.query(Company).filter(Company.ticker == company_ticker).first()
        if company is None:
            raise NotFoundException("Company not Found!")
        data = yf.download(company_ticker, period="max")
        data.reset_index(inplace=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(xaxis_rangeslider_visible=True, showlegend=False)
        return fig

    @staticmethod
    def receive_company_price_prediction(company_ticker) -> PricePrediction:
        prediction: PricePrediction = db.query(PricePrediction).filter(PricePrediction.ticker == company_ticker).first()
        if prediction is None:
            raise NotFoundException("Company not Found!")
        return prediction

    @staticmethod
    def receive_company_revenue_chart(company_ticker) -> list[RevenueChartBarDto]:
        returned_dtos = []
        statements_list: list[FinancialStatement] = db.query(FinancialStatement).filter(
            FinancialStatement.ticker == company_ticker).order_by(FinancialStatement.date.asc()).all()
        if len(statements_list) == 0:
            raise NotFoundException("No financial statement found for this company_ticker")
        for statement in statements_list:
            returned_dtos.append(RevenueChartBarDto(statement.date, statement.revenue))
        return returned_dtos
