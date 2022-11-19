

def notification_on_off():
    with open('users_datebase.txt', 'r') as file:
        data = file.readlines()
        new_data = []
        try:
            for line in data:
                id, name, flag = line.split()
                if flag == "True":
                    new_data.append(f'{id} {name} Stop \n')
                elif flag == 'Stop':
                    new_data.append(f'{id} {name} True \n')
                else:
                    new_data.append(line)
            print(*new_data)
        except Exception as e:
            print(f'Error - notification_on_off : {e}')
    with open('users_datebase.txt', 'w') as file:
        file.writelines(new_data)


def main():
    notification_on_off()


if __name__ == '__main__':
    main()