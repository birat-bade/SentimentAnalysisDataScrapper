import pandas as pd

test_list = list()


def parse(row):
    if 'ConnectionError' in row['log']:
        if '.html' not in row['log']:
            temp = row['log'].split('/')
            test_list.append(temp[-3] + '/' + temp[-2] + '/' + temp[-1])
        if '.html' in row['log']:
            temp = row['log'].split('/')
            test_list.append(temp[-4] + '/' + temp[-3] + '/' + temp[-2])


df_input = pd.read_csv('C:\\Users\\DELL\\Desktop\\Kantipur Daily\\log.csv', dtype=object, error_bad_lines=False,
                       encoding='ISO-8859-1').fillna('')
df_input.apply(parse, 1)

test_list = list(set(test_list))
for data in test_list:
    print(data)
