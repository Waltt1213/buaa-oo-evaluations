import random


def generate_ln(ln):
    print(f'ln {ln}')
    personId = ''
    personName = ''
    personAge = ''

    for j in range(ln):
        personId += str(j + 1) + ' '
        personName += 'PRE_ROB-' + str(j + 1) + ' '
        personAge += str(random.randint(1, 90)) + ' '
    print(personId)
    print(personName)
    print(personAge)

    for j in range(ln - 1):
        value = ''
        for j in range(j + 1):
            flag_ln = random.random()
            if flag_ln < 0.6:
                value += str(0) + ' '
            else:
                value += str(random.randint(0, 30)) + ' '
        print(value)


def generate_mr(num):
    mr_flag = random.random()
    first_id = random.randint(1, num)
    second_id_has = random.randint(1, num)
    second_id_not_has = random.randint(num, 300)
    mr_value = random.randint(-40, 40)
    if mr_flag < 0.7:
        print(f'mr {first_id} {second_id_has} {mr_value}')
    else:
        print(f'mr {first_id} {second_id_not_has} {mr_value}')


def generate_qs():
    qs_flag = random.random()
    if qs_flag < 0.5:
        print(f'qbs')
    else:
        print(f'qts')


def generate_qcv():
    qcv_flag = random.random()
    first_id = random.randint(1, ln_num + 30)
    second_id_has = random.randint(1, ln_num + 30)
    if qcv_flag < 0.5:
        print(f'qv {first_id} {second_id_has}')
    else:
        print(f'qci {first_id} {second_id_has}')


def generate_ap(ap_num) -> int:
    ad_flag = random.random()
    if ad_flag < 0.5 and ap_num < 300:
        print(f'ap {ap_num + 1} PRE_ROB-{ap_num + 1} {99}')
        return 1
    else:
        ar_id_1 = random.randint(1, ap_num)
        ar_id_2 = random.randint(1, ap_num)
        print(f'ar {ar_id_1} {ar_id_2} {99}')
        return 0


if __name__ == '__main__':
    n = random.randint(2000, 3000)
    ln_num = random.randint(80, 100)
    generate_ln(ln_num)
    for i in range(1, n):
        flag = random.random()
        if 0.2 < flag < 0.6:
            generate_mr(ln_num)
        elif 0.6 < flag < 0.8:
            generate_qs()
        elif flag < 0.2:
            ln_num += generate_ap(ln_num)
        else:
            generate_qcv()
