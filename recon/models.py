from datetime import datetime

from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, InvalidRequestError


db = SQLAlchemy()


class CRUDMixin(object):

    __table_args__ = {'extend_existing': True}  # type: Any

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def create(cls, commit=True, ignore_if_exists=False, **kwargs):
        instance = cls(**kwargs)

        if hasattr(instance, 'created_at') \
                and getattr(instance, 'created_at') is None:
            instance.created_at = datetime.now()

        try:
            return instance.save(commit=commit)
        except (IntegrityError, InvalidRequestError):
            if ignore_if_exists:
                db.session.rollback()
                return cls.find(**kwargs)
            else:
                raise

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_404 for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def find(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def exists(cls, **kwargs):
        row = cls.find(**kwargs)
        return row is not None

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def __iter__(self):
        for column in self.__table__.columns:
            yield column.name, str(getattr(self, column.name))


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M')
        elif isinstance(obj, CRUDMixin):
            return dict(obj)
        else:
            return super(JSONEncoder, self).default(obj)
