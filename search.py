import string
import random
import psycopg2


# creates a random string of 5 characters
def key_gen():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(5))


# finds couples of parentheses in the boolean expression and processes them
def find_parentheses(bool_str, par_dict):
    while bool_str.find("(") is not -1:  # looks for the starting (
        i = bool_str.find("(")
        open_count = 1
        close_count = 0
        j = i  # j holds the index of the first (
        while open_count != close_count:  # counts the parentheses until the number of closers equals the openers
            i += 1
            if bool_str[i] == '(':
                open_count += 1
            else:
                if bool_str[i] == ')':
                    close_count += 1
        key = key_gen()  # generates a random string to replace the parentheses section
        par_dict[key] = bool_str[j+1:i]  # saves the original parentheses section with the generated key
        bool_str = bool_str.replace(bool_str[j:i+1], key, 1)
        par_dict[key] = find_parentheses(par_dict[key], par_dict)  # recursive call to check for nested parentheses
        par_dict[key] = par_dict[key].split()  # splits the final section into the different parts
    return bool_str  # returns the processed boolean expression


# executes an SQL query to find the files based on the word and the notFlag
def find_file(word, not_flag):
    con = None
    cur = None
    try:
        con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
        cur = con.cursor()
        if not_flag is True:  # if the flag is on, look for all the files that don't contain the word
            cur.execute("SELECT * FROM retrieval.files WHERE f_id NOT IN "
                        "(SELECT f_id FROM retrieval.posting_file WHERE word='"+word.replace("'", "_")+"') "
                        "AND hidden=False GROUP BY files.f_id")
        else:  # else, look for all the files that contain the word
            cur.execute("SELECT * FROM retrieval.files WHERE f_id IN "
                        "(SELECT f_id FROM retrieval.posting_file WHERE word='"+word.replace("'", "_")+"') "
                        "AND hidden=False GROUP BY files.f_id")
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
def start_search(word, not_flag):
    if word.startswith('"') and word.endswith('"'):  # if the word is between " ", we need to look for it regardless of the stop list
        return find_file(word.strip('"'), not_flag)
    else:  # if not, we need only to look for words that are not on the stop list
        con = None
        cur = None
        try:
            con = psycopg2.connect(host="localhost", database="IR", user="postgres", password=1234, port=5432)
            cur = con.cursor()
            cur.execute("SELECT * FROM retrieval.stop_words WHERE word='"+word.replace("'", "_")+"'")
            if cur.fetchone() is None:  # if the word is not on the list, move on
                return find_file(word, not_flag)
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
def extract_words(str_l, par_d, sets_d):
    op = ["!!", "&&", "||"]  # operands: !! - NOT, && - AND, || - OR
    not_flag = False  # indicates if a not has been found, and therefor how the next word should be handled in the SQL query
    for word in str_l:  # for each word in the string
        if word == "!!":  # if the word is !!, turn on the flag for the next word and continue
            not_flag = True
        else:
            if word not in op: # if the word is an actual word and not an OP move on
                if word in par_d.keys():  # if the word is a key in the () dictionary start a recursive call to handle that section
                    extract_words(par_d[word], par_d, sets_d)
                else:  # else execute an SQL query for the word
                    if not_flag is True:
                        sets_d["!!"+word] = set(start_search(word, not_flag))
                    else:
                        sets_d[word] = set(start_search(word, not_flag))
                not_flag = False


# executes the correct set method - intersection\union - based on the operand
def operator(frst, scnd, op):
    if op == "&&":
        return frst.intersection(scnd)
    if op == "||":
        return frst.union(scnd)


# combines the different queries and returns the final result
def combine_sets(str_l, par_d, sets_d):
    answer = None
    first = str_l[0]  # holds the first word in the list
    str_l.pop(0)  # remove the word from the list
    if first == "!!":  # if it's a not operand - attach it to the word that comes next
        first = "!!" + str_l[0]
        str_l.pop(0)
    if first not in sets_d.keys():  # if the word is a () expression and wasn't handled yet, recursive call for that section
        sets_d[first] = combine_sets(par_d[first], par_d, sets_d)
    if len(str_l) == 0:  # if the word was the only word in the list than we can return its set
        return sets_d[first]
    while len(str_l) > 0:  # while there are other words in the list - continue
        op = str_l[0]  # holds the operand
        str_l.pop(0)
        second = str_l[0]  # holds the second word
        str_l.pop(0)
        if second == "!!":
            second = "!!" + str_l[0]
            str_l.pop(0)
        if second not in sets_d.keys(): # if the word is a () expression and wasn't handled yet, recursive call for that section
            sets_d[second] = combine_sets(par_d[second], par_d, sets_d)
        if answer is not None:  # the sets will be combined into answer until it will hold the final answer that corresponds to the entire expression
            answer = operator(answer, sets_d[second], op)
        else:
            answer = operator(sets_d[first], sets_d[second], op)
    return answer


# translates the boolean expression to SQL queries and searches the DB
def search_words(bool_exp):
    lower_exp = bool_exp.lower()  # lower all the characters to match the index
    sets_dict = {}  # will hold the results of the SQL queries
    par_dict = {}  # will hold the parentheses sections
    lower_exp = find_parentheses(lower_exp, par_dict)  # finds couples of parentheses in the boolean expression and processes them
    str_list = lower_exp.split()  # creates a list from the string
    extract_words(str_list, par_dict, sets_dict)  # fills searchArr with the results of SQL queries for the single words in the expression
    answer = combine_sets(str_list, par_dict, sets_dict)  # combines the different queries and returns the final result
    return answer
