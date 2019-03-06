import psycopg2
from os import listdir
from os.path import isfile, join, exists
from shutil import copyfile
import re


# add files to the DB and index them
def add_files():
    # collects the names of all the files from the designated folder to add to the system.
    files_list = [f for f in listdir("files/files_to_add") if isfile(join("files/files_to_add", f))]

    # checks if the files where already indexed by searching for them by name in the designated folder were the
    # processed files are saved.
    # the new files that require indexing are kept in the to_add list.
    to_add = []
    for file in files_list:
        if exists("files/files_indexed/"+file) is False:
            copyfile("files/files_to_add/"+file, "files/files_indexed/"+file)
            to_add.append(file)
        else:
            print(file+" already indexed")

    # indexing and DB management
    for file in to_add:
        # a dictionary is created for each file. the keys are the words in the file and the values are the number of
        # occurrences for the word
        filePtr = open("files/files_indexed/"+file, "r")
        fileDict = {}
        for line in filePtr:
            for word in re.split("[ .,;:\"\n!?()]+", line):
                word = word.lower()
                word = word.replace("'", "_")  # ' is replaced with _ because it doesn't work with the syntax rules
                if word in fileDict:
                    fileDict[word] = fileDict[word] + 1
                else:
                    if word is not "":
                        fileDict[word] = 1
        # the indexing process
        con = None
        cur = None
        try:
            con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
            cur = con.cursor()
            cur.execute("INSERT INTO retrieval.files(f_name, hidden) VALUES('"+file+"', FALSE) RETURNING f_id;")
            fileID = cur.fetchone()[0]
            con.commit()
            for word in fileDict:
                cur.execute("SELECT * FROM retrieval.inverted_index WHERE word='"+word+"'")
                row = cur.fetchone()
                if row is not None:
                    cur.execute("UPDATE retrieval.inverted_index SET docs_num="+str(row[1] + 1)+" WHERE word='"+word+"'")
                    con.commit()
                    cur.execute("INSERT INTO retrieval."+row[2]+"(f_id, hits_num) VALUES("+str(fileID)+", "
                                +str(fileDict[word])+");")
                    con.commit()
                else:
                    cur.execute("INSERT INTO retrieval.inverted_index(word, docs_num, files_table_name) VALUES('"
                                +word+"', "+str(1)+", '"+word+"_table');")
                    con.commit()
                    cur.execute("CREATE TABLE retrieval."+word+"_table(f_id BIGINT PRIMARY KEY NOT NULL, "
                                "hits_num BIGINT NOT NULL);")
                    con.commit()
                    cur.execute("INSERT INTO retrieval."+word+"_table(f_id, hits_num) VALUES("+str(fileID)+", "
                                +str(fileDict[word])+");")
                    con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        filePtr.close()
