import string
import random
import psycopg2


# creates a random string of 5 characters
def key_gen():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(5))


# finds couples of parentheses in the boolean expression and processes them
def find_parentheses(qry_str, par_dict):
    while qry_str.find("(") is not -1:  # looks for the starting (
        i = qry_str.find("(")
        open_count = 1
        close_count = 0
        j = i  # j holds the index of the first (
        while open_count != close_count:  # counts the parentheses until the number of closers equals the openers
            i += 1
            if qry_str[i] == '(':
                open_count += 1
            else:
                if qry_str[i] == ')':
                    close_count += 1
        key = key_gen()  # generates a random string to replace the parentheses section
        par_dict[key] = qry_str[j+1:i]  # saves the original parentheses section with the generated key
        qry_str = qry_str.replace(qry_str[j:i+1], key, 1)
        par_dict[key] = find_parentheses(par_dict[key], par_dict)  # recursive call to check for nested parentheses
        par_dict[key] = par_dict[key].split()  # splits the final section into the different parts
    return qry_str  # returns the processed boolean expression


# executes an SQL query to find the files based on the word and the notFlag
def find_file(word, notFlag):
    con = None
    cur = None
    try:
        con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
        cur = con.cursor()
        if notFlag is True:  # if the flag is on, look for all the files that don't contain the word
            cur.execute("SELECT * FROM retrieval.posting_file NATURAL JOIN retrieval.files WHERE files.f_id NOT IN "
                        "(SELECT files.f_id FROM retrieval.posting_file NATURAL JOIN retrieval.files WHERE "
                        "word='"+word+"')"
                        "GROUP BY f_id ORDER BY hits_num DESC")
        else:  # else, look for all the files that contain the word
            cur.execute("SELECT * FROM retrieval.posting_file NATURAL JOIN retrieval.files WHERE word='"+word+"' "
                        "ORDER BY hits_num DESC")
        res = cur.fetchall()
        if res is not None:
            return res
        else:
            return []
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()


# checks if the word should be ignored if part of the stop list, or start the SQL query process
def start_search(word, notFlag):
    if word.startswith('"') and word.endswith('"'):  # if the word is between " ", we need to look for it regardless of the stop list
        return find_file(word, notFlag)
    else:  # if not, we need only to look for words that are not on the stop list
        con = None
        cur = None
        try:
            con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
            cur = con.cursor()
            cur.execute("SELECT * FROM retrieval.stop_words WHERE word='"+word+"'")
            if cur.fetchone() is None:  # if the word is not on the list, move on
                return find_file(word, notFlag)
            else:  # if it is, return an empty set (there is no reason to search the DB for it)
                return []
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()


# fills searchArr with the results of SQL queries for the single words in the expression
def extract_words(strArr, parD, srchArr):
    op = ["!!", "&&", "||"]  # operands: !! - NOT, && - AND, || - OR
    notFlag = False  # indicates if a not has been found, and therefor how the next word should be handled in the SQL query
    for word in strArr:  # for each word in the string
        if word is "!!":  # if the word is !!, turn on the flag for the next word and continue
            notFlag = True
        else:
            if word not in op: # if the word is an actual word and not an OP move on
                if word in parD.keys():  # if the word is a key in the () dictionary start a recursive call to handle that section
                    extract_words(parD[word], parD, srchArr)
                else:  # else execute an SQL query for the word
                    srchArr[word] = start_search(word, notFlag)
            notFlag = False


# combines the different queries and returns the final result
def final_set(strArr, parD, srchArr):



# translates the boolean expression to SQL queries and searches the DB
def search_words(bool_exp):
    lowerExp = bool_exp.lower()  # lower all the characters to match the index
    searchArr = []  # will hold the results of the SQL queries
    parDict = {}  # will hold the parentheses sections
    lowerExp = find_parentheses(lowerExp, parDict)  # finds couples of parentheses in the boolean expression and processes them
    stringArr = lowerExp.split()  # creates an array from the string
    extract_words(stringArr, parDict, searchArr)  # fills searchArr with the results of SQL queries for the single words in the expression
    final_set(stringArr, parDict, searchArr)  # combines the different queries and returns the final result


par_dict1 = {}
str1 = find_parentheses("A       && (B || (!! C &&     D)) && (E && F)", par_dict1)
print(par_dict1)
print(str1)
