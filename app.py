from flask import Flask, render_template
from models import db

app=Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'IR',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

"""class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self,username,email):
        self.username = username
        self.email = email
    
    def __repr__(self):
        return 'User %r>' % self.username"""

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()