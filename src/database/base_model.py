from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect

from main.extensions import db
from utils.utils import Utils


class BaseModel(db.Model):
    """Base table class. It includes convenience methods for creating,
    querying, saving, updating and deleting models.
    """
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    __repr_props__ = ()
    """Set to customize automatic string representation.

    For example::

        class User(database.Model):
            __repr_props__ = ('id', 'email')

            email = Column(String)

        user = User(id=1, email='foo@bar.com')
        print(user)  # prints <User id=1 email="foo@bar.com">
    """
    
    @declared_attr
    def __plural__(self):
        return Utils.pluralize(self.__name__)

    @declared_attr
    def __label__(self):
        return Utils.title_case(self.__name__)

    @declared_attr
    def __plural_label__(self):
        return Utils.pluralize(self.__label__)

    @classmethod
    def all(cls):
        """Get all models."""
        return cls.query.all()

    @classmethod
    def get(cls, id):
        """Get one model by ID.

        :param id: The model ID to get.
        """
        return cls.query.get(int(id))

    @classmethod
    def get_by(cls, **kwargs):
        """Get one model by keyword arguments.

        :param kwargs: The model attribute values to filter by.
        """
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_create(cls, commit=False, **kwargs):
        """Get or create model by keyword arguments.

        :param bool commit: Whether or not to immediately commit the DB session (if create).
        :param kwargs: The model attributes to get or create by.
        """
        instance = cls.get_by(**kwargs)
        if not instance:
            instance = cls.create(**kwargs, commit=commit)
        return instance

    @classmethod
    def join(cls, *props, **kwargs):
        return cls.query.join(*props, **kwargs)

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.query.filter(*args, **kwargs)

    @classmethod
    def filter_by(cls, **kwargs):
        """Find models by keyword arguments.

        :param kwargs: The model attribute values to filter by.
        """
        return cls.query.filter_by(**kwargs)

    @classmethod
    def create(cls, commit=False, **kwargs):
        """Create a new model and add it to the database session.

        :param bool commit: Whether or not to immediately commit the DB session.
        :param kwargs: The model attribute values to create the model with.
        """
        instance = cls(**kwargs)
        return instance.save(commit)

    def update(self, commit=False, **kwargs):
        """Update fields on the model.

        :param bool commit: Whether or not to immediately commit the DB session.
        :param kwargs: The model attribute values to update the model with.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save(commit)

    def save(self, commit=False):
        """Save the model.

        :param bool commit: Whether or not to immediately commit the DB session.
        """
        try:
            db.session.add(self)
            if commit:
                self.commit()
            return self
        except Exception as e:
            self.rollback()
            raise e

    def delete(self, commit=False):
        """Delete the model.

        :param bool commit: Whether or not to immediately commit the DB session.
        """
        db.session.delete(self)
        return commit and db.session.commit()

    def commit(self):
        db.session.commit()
        
    def rollback(self):
        db.session.rollback()
        
    def to_dict(self, columns=None):
        data = {}
        mapper = inspect(self)

        if columns is None:  # Return all columns if no argument provided
            for column in mapper.mapper.column_attrs:
                data[column.key] = getattr(self, column.key)
        else:  # Include only specified columns
            for column in columns:
                if hasattr(self, column):  # Check if column exists
                    data[column] = getattr(self, column)
                else:
                    print(f"Warning: Column '{column}' not found in {self.__class__.__name__} model.")

        return data
    
    def __repr__(self):
        properties = [f'{prop}={getattr(self, prop)!r}'
                      for prop in self.__repr_props__ if hasattr(self, prop)]
        return f"<{self.__class__.__name__} {' '.join(properties)}>"