import csv
from datetime import datetime


lst = [
    
    [52232480, 'все работает вот ссылка', True,],
    [52233119, 'все не работает', False,],
    [52233721,'ОК вот ссылка', True,],
    ]
        


def write_to_database(list_vc: list) -> None:
    with open('datebase.csv', 'w+') as csv_file: 
        writer = csv.writer(csv_file)
        for line in list_vc:
            date_write = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            line.append(date_write)
            writer.writerow(line)


def read_from_datebase():  # ToDo annotation
    result = []
    with open('datebase.csv', 'r') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in spamreader:
            result.append(row)
    return result

write_to_database(lst)