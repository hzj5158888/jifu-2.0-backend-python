from application_initializer import db

"""
为model类实体添加数据转为json字典的方法
"""


def model_to_dict(cls):
    def to_dict(self):

        def _filter(key: str, value):
            if key.startswith('_'):
                return False
            if isinstance(value, db.Model):
                return False
            return True

        def _mapper(value):
            import datetime
            if isinstance(value, datetime.datetime):
                return value.timestamp()
            return value

        d = vars(self)
        d = {k: v for k, v in d.items() if _filter(k, v)}
        d = {k: _mapper(v) for k, v in d.items()}
        return d

    cls.to_dict = to_dict
    return cls
