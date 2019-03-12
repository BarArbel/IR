def is_main_connector(statement, index):
    opens = statement[0:index].count('(')-1
    closes = statement[0:index].count(')')
    if opens == closes:
        return True
    return False

statements = []

def find_connectors(s):
    connectors_list = ["|" , "&"]
    connectors_indecies = []
    i = 0
    while i < len(s):
        if s[i] in connectors_list:
            if i+1 < len(s) and s[i+1] == s[i]:
                connectors_indecies.append(i)
                i += 1
        i += 1
    return connectors_indecies

def is_statement(s):
    found_connectors = find_connectors(s)
    if len(s) == 0:
        return False
    if len(found_connectors) == 0 and s.isalnum() :
        return True
    if s[0] == '!' and s[1] == '!':
        return is_statement(s[2])
    for connector in found_connectors:
        if is_main_connector(s,connector):
            #print "connector =", s[connector]
            return is_statement(s[1:connector]) and is_statement(s[connector+2:-1])
    return False




