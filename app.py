from flask import Flask, render_template, request
import os, psycopg2
app = Flask(__name__)


app.config['DEBUG'] = False

def init_schema(cur):

    cur.execute("CREATE SCHEMA IF NOT EXISTS retrieval;")
    cur.execute("CREATE TABLE IF NOT EXISTS retrieval.files(" \
                	"f_id BIGSERIAL PRIMARY KEY NOT NULL, " \
                	"f_name TEXT NOT NULL, " \
                	"f_author TEXT NOT NULL, " \
                	"f_type TEXT NOT NULL, " \
                	"hidden BOOLEAN NOT NULL " \
                "); " )
    
    cur.execute("CREATE TABLE IF NOT EXISTS retrieval.inverted_index( " \
                	"word TEXT PRIMARY KEY NOT NULL, " \
                	"docs_num BIGINT NOT NULL " \
                "); " )
    cur.execute("CREATE TABLE IF NOT EXISTS retrieval.posting_file( " \
                	"word TEXT NOT NULL, " \
                	"f_id BIGINT NOT NULL, " \
                	"hits_num BIGINT NOT NULL, " \
                	"PRIMARY KEY(word, f_id) " \
                "); " )
    
    cur.execute("CREATE TABLE IF NOT EXISTS retrieval.stop_words( " \
                	"word TEXT PRIMARY KEY NOT NULL " \
                "); " )
    
    try:
        cur.execute("INSERT INTO retrieval.stop_words(word) VALUES " \
                    	"('a'), ('all'), ('and'), ('any'), ('at'), " \
                    	"('be'), ('do'), ('for'), ('her'), ('how'), " \
                    	"('if'), ('is'), ('many'), ('not'), ('see'), " \
                    	"('the'), ('their'), ('when'), ('why');")
    except:
        pass

    
@app.route('/')
def index():
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
            
            #Check if directory is empty
            for filename in os.listdir("files/files_indexed/"):
                if filename.endswith(".txt"): 
                    file = open("files/files_indexed/"+filename, "r") 
                    file_content = file.read() 
                    author = file_content.split(',', 1)[0]
                    html_content+= ('<a class="result toDelete"><h2>&#128686 &#8998 Delete '+filename.split('.txt', 1)[0]+'/'+author+'</h2></a>')
                    continue
                else:
                    continue
            html_content += "</section>"
            print(html_content)
            return render_template("adminZone.html", literaturegohere=html_content)

if __name__ == '__main__':
    
    #Initialize connection, update schema if needed and add process files
    con = psycopg2.connect(
            host="localhost",
            database="IR",
            user="postgres",
            password="1234")
    
    cur = con.cursor()
    init_schema(cur)
    os.system('add.py')
    con.commit()
    
    app.run()
    con.close()