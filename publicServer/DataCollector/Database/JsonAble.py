class JsonAble:
    def as_dict(self):
        dict_to_return = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return dict_to_return