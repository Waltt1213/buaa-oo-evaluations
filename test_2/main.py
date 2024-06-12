import subprocess

code_num = 10  # 注意与main_auto同步


def run_evaluation(n):
    scores = {i: 0.0 for i in range(1, code_num + 1)}  # 初始化每个code.jar的评分为0
    time_sum = {i: 0 for i in range(1, code_num + 1)}
    for j in range(n):
        times = {}  # 用于存储每个code.jar的运行时间
        print("------------------Round {j}------------------".format(j=j))
        process = subprocess.Popen(['python', 'main_auto.py'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, stderr_output = process.communicate()
        print(stderr_output)
        output_lines = output.decode(encoding='gbk').splitlines()

        for line in output_lines:
            # 处理每一行输出
            output_str = line.strip()  # 将字节串解码为字符串并去除两端空白字符
            code_id = int(output_str.split()[1])
            action = output_str.split()[2]
            if action == 'Error':
                print(line)
                times[code_id] = 220
                continue
            time_str = output_str.split()[-1]  # 分割字符串并获取最后一个部分，即时间部分
            time = float(time_str[:-1])  # 将时间部分转换为浮点数，去除末尾的's'字符
            times[code_id] = time
            time_sum[code_id] += time
            print(f"Code {code_id} Elevator behavior check complete. Using {time}s")
        print("--------------------------------------------------")
        print("Scores:")
        # 按照运行时间对code.jar进行排序，并根据排序结果给出评分
        sorted_times = sorted(times.items(), key=lambda x: x[1])
        for i, (code_id, _) in enumerate(sorted_times):
            if i < 3:
                scores[code_id] += 5
                print(f"Code {code_id}: add 5 points")
            elif 3 <= i < 7:
                scores[code_id] += 3
                print(f"Code {code_id}: add 3 points")
            elif 7 <= i < 11:
                scores[code_id] += 2
                print(f"Code {code_id}: add 2 points")
            else:
                scores[code_id] += 1
                print(f"Code {code_id}: add 1 points")
        print("--------------------------------------------------")
        print("Now Scores:")
        for code_id, score in scores.items():
            print(f"Code {code_id}: {score} points")
        print("------------------Round {j} OVER------------------".format(j=j))

    print("-------------------------------------------------------------------------------")
    sorted_time = sorted(time_sum.items(), key=lambda x: x[1])
    print("AvgTime:")
    for code_id, time in sorted_time:
        print(f"Code {code_id}: {time / n: .4f} points")
    for i, (code_id, _) in enumerate(sorted_time):
        scores[code_id] = scores[code_id] * 0.4 + 0.6 * (13 - i)
    # 根据得分排序输出
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("Final Scores:")
    for code_id, score in sorted_scores:
        print(f"Code {code_id}: {score: .4f} points")


if __name__ == "__main__":
    m = int(input("请输入评测次数："))
    run_evaluation(m)
