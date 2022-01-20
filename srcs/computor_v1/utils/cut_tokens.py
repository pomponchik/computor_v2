def get_subs(source_list, splitter):
    result = []
    for element in source_list:
        for sub_element in element.split(splitter):
            result.append(sub_element)
    return result

def cut_tokens(string, need_split=True):
    if need_split:
        string = string.split('=')
    string = get_subs(splitted, '-')
    string = get_subs(splitted, '+')
    return string
