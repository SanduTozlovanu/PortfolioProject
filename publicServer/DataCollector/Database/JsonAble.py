from datetime import datetime


class JsonAble:
    def as_dict(self):
        dict_to_return = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return dict_to_return


class FinancialStatementJsonAble(JsonAble):
    def as_dict(self):
        dict_to_return = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dict_to_return["date"] = dict_to_return["date"].strftime("%Y-%m-%d")
        return dict_to_return
