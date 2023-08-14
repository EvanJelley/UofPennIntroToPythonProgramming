def open_read_file(file):
    f = open(file, 'r')
    print(type(f))

    cnt = 0

    line = f.readline()
    while line:
        print(line, end = '')
        line = f.readline()

        cnt += 1


    print('')
    print('there are', cnt, 'lines in the file')

    f.close()

def open_read_append_new_file(file1, file2):
    with open(file1) as f1:

        lst = f1.readlines()

        lst.reverse()

        f2 = open(file2, 'a')

        f2.writelines(lst)

        f2.close()

def open_read_append_same_file(file):
    f = open(file, 'r+')

    lst = f.readlines()

    lst.insert(0, '\n')
    lst.insert(0, 'HERE IS THE ARTICLE AGAIN :)')
    lst.insert(0, '\n')

    f.writelines(lst)

    f.close()

def open_read_write_new_file(file1, file2):
    with open(file1) as f1:

        text = f1.read()

        f2 = open(file2, 'w')

        f2.write(text)

        f2.close()

def import_and_create_dictionary(filename):
    expenses = {}

    f = open(filename, 'r')
    lines = f.readlines()

    for line in lines:
        lst = line.strip().split(',')

        if len(lst)<= 1:
            continue

        key = lst[0].strip()
        value = lst[1].strip()

        try:
            value = float(value)

            expenses[key] = expenses.get(key, 0) + value

        except:
            continue

    f.close()

    return expenses


def main():
    expenses = import_and_create_dictionary('expenses.txt')
    print(expenses)


if __name__ == '__main__':
    main()