import psycopg2

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

# show or hide the file    
def hideshow_file(file_name, file_author):
    con = None
    cur = None
    try:
        con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
        cur = con.cursor()
        cur.execute("SELECT * FROM retrieval.files WHERE f_name='"+file_name+"' AND f_author='"+file_author+"'")
        if cur.fetchone()[4]:
            cur.execute("UPDATE retrieval.files SET hidden = false WHERE f_name='"+file_name+"' AND f_author='"+file_author+"'")
        else:
            cur.execute("UPDATE retrieval.files SET hidden = true WHERE f_name='"+file_name+"' AND f_author='"+file_author+"'")
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()    

# return if file is hidden or shown
def file_status(file_name, file_author):
    con = None
    cur = None
    result = ''
    try:
        con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
        cur = con.cursor()
        cur.execute("SELECT * FROM retrieval.files WHERE f_name='"+file_name+"' AND f_author='"+file_author+"'")
        print(hideshow_file(file_name, file_author))
        # Check if hidden option is available 
        # hidden false = possible to delete.
        # hidden true = possible to add back.
        result = cur.fetchone()[4]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()    
            
    return result