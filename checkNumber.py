
def check():
    with open('log.txt','r') as f:
        allLines = f.readlines()

    count = 0
    for line in allLines:
        if 'successfully' in line:
            count += 1

    print(f'Form successfully submitted {count} times!! fuck VFS :)')


if __name__ == '__main__':
    check()
