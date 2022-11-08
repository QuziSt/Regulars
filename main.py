import re
import csv
from pprint import pprint


def get_file_data():
    with open('phonebook_raw.csv', 'r', encoding='utf-8') as pb:
        data = csv.reader(pb, delimiter=',')
        persons = list(data)
        change_names(persons)


def change_names(persons):
    for person in persons:
        full_name = []
        for piece in person[:3]:
            full_name += piece.split()
        if len(full_name) == 3:
            person[:3] = full_name
        else:
            full_name.append('')
            person[:3] = full_name
    change_numbers(persons)


def change_numbers(persons):
    for person in persons:
        pattern = re.compile("(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?")
        person[5] = pattern.sub(r'+7(\2)\3-\4-\5 \6\7', person[5]).strip()
    delete_duplicates(persons)



def merge(data1, data2):
    result = []
    for value1, value2 in zip(data1, data2):
        result += [value1] if value1 else [value2]
    return result


def delete_duplicates(persons):
    contacts = {}
    for person in persons:
        name = (person[0], person[1])
        duplicate = contacts.get((person[0], person[1]))
        if duplicate:
            contacts[name] = merge(person, duplicate)
        else:
            contacts[name] = person
    new_contacts = [value for value in contacts.values()]
    write(new_contacts)


def write(contacts):
    with open('phonebook.csv', 'w') as new:
        datawriter = csv.writer(new, delimiter=',')
        datawriter.writerows(contacts)




if __name__ == '__main__':
    get_file_data()
