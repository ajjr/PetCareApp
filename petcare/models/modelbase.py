# import sqlalchemy.ext.declarative as dec
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelBase:

    def __repr__(self):
        return "<{} {}>".format(self.__class__, self.id)
