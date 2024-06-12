import os


def isEqual(file_id) -> bool:
    # if file_id == 3:
    #     return False
    f1 = open(f'stdout_{file_id}.txt', 'r')
    fa = open('ans.txt', 'r')
    lines1 = f1.readlines()
    lines_fa = fa.readlines()
    if len(lines1) != len(lines_fa):
        print('lines is not same!')
        return False
    for i in range(len(lines_fa)):
        if lines1[i] != lines_fa[i]:
            print(f'lines {i + 1} is not same!')
            return False
    return True


n = int(input("请输入评测次数："))
data_generate = "data_generate.py"
for i in range(n):
    print(f'Test{i + 1} is beginning')
    os.system(f"python {data_generate} > stdin.txt")
    os.system("java -jar ./code1.jar < stdin.txt > stdout_1.txt")
    os.system("java -jar ./code2.jar < stdin.txt > stdout_2.txt")
    os.system("java -jar ./code3.jar < stdin.txt > stdout_4.txt")
    os.system("java -jar ./code4.jar < stdin.txt > stdout_3.txt")
    os.system("java -jar ./code5.jar < stdin.txt > stdout_5.txt")
    os.system("java -jar ./code5.jar < stdin.txt > stdout_6.txt")
    os.system("java -jar ./code7.jar < stdin.txt > stdout_7.txt")
    os.system("java -jar ./standard.jar < stdin.txt > ans.txt")
    right_flag = True
    for j in range(1, 8):
        if isEqual(j):
            print(f'file_{j} is AC!')
        else:
            print(f'file_{j} is not AC!')
            right_flag = False
    print(f'Test{i + 1} is end')
    if not right_flag:
        print(f'STOP in test {i + 1}')
        break
    print('\n')
