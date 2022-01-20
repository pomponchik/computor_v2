def is_number(string):
    if string == '':
        return False
    if string[0] == '-':
        string = string[1:]
    if string.isdigit():
        return True
    splitted_string = string.split('.')
    if '' in splitted_string or len(splitted_string) != 2:
        return False
    return True
