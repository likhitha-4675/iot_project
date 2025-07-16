from . import db 

class User(db.Model):
    id=db.Column(db.Integer,Primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    otp=db.Column(db.String(6),nullable=False)
    verified=db.Column(db.Boolean,default=False)
    data_used=db.column(db.Integer,default=0)
    paid_data=db.column(db.Integer,default=500)
