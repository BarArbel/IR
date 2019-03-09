from flask import Flask, render_template, request
import os

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'IR',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
"""app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

class User(db.Model):
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
    os.system('add.py')
    return render_template('index.html')

@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/get_file_page", methods=['GET'])
def get_file_page():
    if request.method == 'GET':
        fileName = request.args.getlist('param1')
        
        # Get file and print it
        file = open("files/files_indexed/"+fileName[0]+".txt", "r") 
        file_content = file.read() 
        author = file_content.split(',', 1)[0]
        text = file_content.split("\n",1)[1].replace("\n", "<br>")
        html_content = "<main> <h1>Literature Search</h1> <h2>"+fileName[0]+" / "+author+"</h2> "+text+" </main>"
       
    return render_template("file.html",literaturegohere=html_content)


@app.route("/adminZone", methods=['POST'])
def adminZone():
    if request.method == 'POST':
        password = request.form['Enter']
        if password == "1234":
            html_content = "<section>"
            for filename in os.listdir("files/files_indexed/"):
                if filename.endswith(".txt"): 
                     # print(os.path.join(directory, filename))
                    continue
                else:
                    continue
            html_content += "</section>"
            return render_template("adminZone.html", literaturegohere=html_content)

if __name__ == '__main__':
    app.run()