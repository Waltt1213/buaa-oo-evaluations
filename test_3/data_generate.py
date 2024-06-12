import random

# n = random.randint(1, 100)
n = 100
line_num = 4998
special_flag = True
tag_flag = True

personId = ''
personName = ''
personAge = ''

print(f'load_network {n}')

for i in range(n):
    personId += str(i + 1) + ' '
    personName += 'PRE_ROB-' + str(i + 1) + ' '
    personAge += str(random.randint(1, 90)) + ' '
print(personId)
print(personName)
print(personAge)

for i in range(n - 1):
    value = ''
    for j in range(i + 1):
        value += str(1) + ' '
    print(value)

if special_flag:
    print('ap 1 1 1')
    print('ap 2 2 2')
    print('ar 1 2 100')

    for i in range(line_num):
        print(f'sei {i}')

    for j in range(line_num):
        print(f'aem {j} {j} 0 1 2')

    print(f'dce 1')


if tag_flag:
    for i in range(100):
        print(f'at ' + str(i) + ' 1')

    edge = 0
    for i in range(100):
        for j in range(100):
            if edge <= line_num / 3:
                edge += 1
                print(f'att ' + str(j + 1) + ' ' + str(i + 1) + ' 1')
            else:
                break
            if edge % 50 == 0:
                print("qtvs " + str(i + 1) + ' 1')
    edge = 0
    for i in range(100):
        for j in range(100):
            if edge <= line_num / 3:
                edge += 1
                print(f'dft ' + str(j + 1) + ' ' + str(i + 1) + ' 1')
            else:
                break
            if edge % 50 == 0:
                print("qtvs " + str(i + 1) + ' 1')

for i in range(n):
    for j in range(i + 1, n):
        if line_num < 10000:
            flag = random.random() + (10000 - line_num) / 20000
            if flag < 0.3:
                line_num += 1
                print('qbs')
            elif 0.3 < flag < 0.4:
                line_num += 1
                print('qts')
            elif 0.6 < flag < 0.7:
                line_num += 1
                if random.random() < 0.4:
                    print('qci ' + str(i + 1) + ' ' + str(random.randint(1, 80)))
                else:
                    print('qci ' + str(i + 1) + ' ' + str(j + 1))
            elif flag > 0.8:
                line_num += 1
                print('mr ' + str(i + 1) + ' ' + str(j + 1) + ' ' + '-2')
            elif 0.7 < flag < 0.8:
                line_num += 1
                if random.random() < 0.4:
                    print('qv ' + str(i + 1) + ' ' + str(random.randint(1, 80)))
                else:
                    print('qv ' + str(i + 1) + ' ' + str(j + 1))