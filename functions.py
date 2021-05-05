import re


def create_formated_list(unformated_list, flag):
    for item in unformated_list:
        list_of_cats = [i for i in item.get_text().split('\n') if i != '']
    tup = (1, len(list_of_cats) - 2, 2) if flag else (0, len(list_of_cats) - 1)

    formated_list = []
    for category in range(*tup):
        link_part = formatting(list_of_cats[category])
        formated_list.append(link_part)
    return formated_list


def formatting(string):
    return re.sub(r'[?!.,]', '', string.lower()).replace(' ', '-')
