class Normalizator:
    def __init__(self, string):
        self.string = string

    def get_norm_version(self):
        string = self.deleting_extra_spaces(self.string)
        string = self.add_need_spaces(string)
        return string

    @staticmethod
    def deleting_extra_spaces(string):
        string = string.strip()
        while True:
            new_string = string.replace('  ', ' ')
            new_string = new_string.replace('^ ', '^')
            new_string = new_string.replace(' ^', '^')
            new_string = new_string.replace('. ', '.')
            new_string = new_string.replace(' .', '.')
            if new_string == string:
                break
            string = new_string
        return new_string

    @staticmethod
    def add_need_spaces(string):
        elements = list(string)
        new_elements = []
        for index, element in enumerate(elements):
            prev_elem = '' if index == 0 else elements[index - 1]
            next_elem = '' if index == (len(elements) - 1) else elements[index + 1]
            if element in ('+', '*', '='):
                if next_elem and next_elem != ' ':
                    element += ' '
                if prev_elem and prev_elem != ' ':
                    element = ' ' + element
            elif element == '-':
                if next_elem and next_elem != ' ' and not next_elem.isdigit():
                    element += ' '
                if prev_elem and prev_elem != ' ' and not prev_elem.isdigit():
                    element = ' ' + element
            new_elements.append(element)
        return ''.join(new_elements)
