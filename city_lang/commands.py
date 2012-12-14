# # -*- encoding: utf-8 -*-
# from flask import current_app
# from flask.ext.script import Command

# from werkzeug.local import LocalProxy

# __all__ = ['ImportVisitors']

# mongo = LocalProxy(lambda: current_app.extensions['mongoset'])
# db = LocalProxy(lambda: current_app.extensions['sqlalchemy'].db)


# class ImportVisitors(Command):

#     def get_visitor_class(self):
#         class Visitor(db.Model):
#             __tablename__ = 'member'
#             id = db.Column(db.Integer, primary_key=True)
#             name = db.Column(db.Unicode(255), nullable=False)
#             company = db.Column(db.Unicode(255), nullable=False)
#             position = db.Column(db.Unicode(255), nullable=False)
#             email = db.Column(db.Unicode(255), unique=True)
#             confirmation = db.Column(db.Enum('approved', 'unapproved'),
#                                      default='unapproved')
#             approved = db.Column(db.Boolean, default=False)

#             def __repr__(self):
#                 return u"<Visitor: {0.email}>".format(self)

#         return Visitor

#     def import_data(self):
#         from city_lang.pages.models import Visitor as MVisitor
#         SQLVisitor = self.get_visitor_class()
#         for visitor in SQLVisitor.query.all():
#             if MVisitor.query.find({'email': visitor.email}).count() == 0:
#                 MVisitor.create(name=visitor.name,
#                                 email=visitor.email,
#                                 position=visitor.position,
#                                 company=visitor.company)

#     def run(self):
#         self.import_data()
