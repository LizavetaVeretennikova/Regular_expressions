from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
def split_full_name(list_name):
    #Разделение ФИО
    full_name = ["", "", ""]
    start = 0
    for name in list_name:
        if name:
            name = name.split()
            stop = len(name)
            full_name[start: start + stop] = name
            start += stop
    return full_name

def delete_identical_full_name(contacts_list):
    #удаление одинаковых ФИО
    del_identical_name_dict = {}
    for row in contacts_list:
        key = row[0], row[1]
        data_dict = {
            "surname": row[2],
            "organization": row[3],
            "position": row[4],
            "phone": row[5],
            "email": row[6]
        }
        if del_identical_name_dict.get(key):
            for value in del_identical_name_dict.get(key):
                if row[2] in value.get("surname"):
                    value.update(
                    {key: data_dict.get(key) for key in value if not value.get(key)}
                    )
                else:
                    del_identical_name_dict.get(key).append(data_dict)
        else:
            del_identical_name_dict[key] = [data_dict]
    return del_identical_name_dict

def organization_number(phone):
    #организация номера телефона
    pattern = r"\+?([7|8])\s?\(?(\d{3})\)?[\s-]?(\d{3,})\-?(\d{2,})\-?(\d{2,})\s?\(?(\w{3})?\.?\s?(\d{4})?\)?"
    sub_pattern = r"+7(\2)\3-\4-\5 \6.\7"
    result_org_number = re.sub(pattern, sub_pattern, phone)
    return result_org_number
def extract_full_name(contacts_list):
    #Извлечение ФИО
    for row in contacts_list:
            row[:3] = split_full_name(row[:3])
            row[5] = organization_number(row[5])
    return contacts_list

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
def write_new_csv_file(del_identical_name_dict, fieldnames):
    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
        datawriter.writeheader()
        for key, value_contacts_list in del_identical_name_dict.items():
            for value in value_contacts_list:
                datawriter.writerow(
                    {
                        "lastname": key[0],
                        "firstname": key[1],
                        "surname": value.get("surname"),
                        "organization": value.get("organization"),
                        "position": value.get("position"),
                        "phone": value.get("phone"),
                        "email": value.get("email")
                    }
                )

#    with open('phonebook.csv', newline='') as f:
#        reader = csv.DictReader(f)
#        for row in reader:
#            print(row['lastname'],
#                  row['firstname'],
#                  row['surname'],
#                  row['organization'],
#                  row['position'],
#                  row['phone'],
#                  row['email'],
#                  )


if __name__ == "__main__":
    extract_full_name(contacts_list[1:])
    delete_identical_name_dict = delete_identical_full_name(contacts_list[1:])
    fieldnames = contacts_list[0]
    write_new_csv_file(delete_identical_name_dict, fieldnames)