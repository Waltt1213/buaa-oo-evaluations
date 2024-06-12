import os
import sys
import threading
import re

code_num = 10  # # 注意与main同步


def evaluate_code(i):
    input_file = "datainput_student_win64.exe"
    jar_file = f"code{i}.jar"
    output_file = f"out{i}.txt"

    cmd = f"{input_file} | java -jar {jar_file} > {output_file}"
    os.system(cmd)
    # 使用示例
    # lock.acquire()
    # print(f"Code {i} is testing")
    check_elevator_behavior('stdin.txt', 'out{i}.txt'.format(i=i), i)
    # print(f"Code {i} evaluated.")
    # lock.release()


def check_elevator_behavior(stdin_file, out_file, code_id):
    # 读取stdin.txt中的用户需求
    with open(stdin_file, 'r') as f:
        requests = f.readlines()

    # 读取out.txt中的电梯行为
    with open(out_file, 'r') as f:
        elevator_actions = f.readlines()

    # 初始化状态变量
    elevators = {}  # 用于跟踪每个电梯的状态
    elevators_reset_list = [0] * 7  # 记录电梯reset状态
    elevator_reset_time = {}  # accept, begin, end
    elevators_standard = {}
    elevators_passengers = {}
    passenger_elevator = {}
    passengers = {}

    for eid in range(1, 7):
        elevators[eid] = [1, 'CLOSE', 0, 1.0, 0, 0]  # 电梯楼层， 电梯状态， 电梯内人数, 时间戳, 分配标记, 重置标记
        elevators_standard[eid] = [1.0, 6, 400]  # 时间戳，满载人数， 移动时间
        elevators_passengers[eid] = []  # 分配给电梯的乘客序列

    for request in requests:
        match = re.search(r'\[(.*?)]', request)
        if match:
            timestamp_passenger = match.group(1)
            request = request.replace(match.group(0), '')
        else:
            continue
        parts = request.split('-')
        first_element = parts[0]
        # reset请求
        if first_element == 'RESET':
            elevator_id = int(parts[2])
            max_num = int(parts[3])
            move_time = float(parts[4])
            elevators_standard[elevator_id] = [700, max_num, int(move_time * 1000)]
            continue

        passenger_id = int(parts[0])
        from_floor = int(parts[2])
        goal_floor = int(parts[4])
        passengers[passenger_id] = [0, from_floor, goal_floor, 0]  # 记录乘客上电梯情况，出发楼层，目标楼层,结束位
    final_time = 1.0
    # 解析电梯行为并进行错误检查
    for action in elevator_actions:
        # 使用正则表达式提取时间戳
        match = re.search(r'\[(.*?)]', action)
        if match:
            timestamp = match.group(1)
            # 剔除时间戳部分，保留行为信息
            action = action.replace(match.group(0), '')
        else:
            # 如果没有时间戳，则直接跳过该行
            continue
        final_time = timestamp
        parts = action.split('-')
        action_type = parts[0]

        # 为乘客分配电梯
        if action_type == 'RECEIVE':
            passenger_id = int(parts[1])
            elevator_id = int(parts[2])
            passenger_elevator[passenger_id] = elevator_id
            # 电梯重置期间不接受请求
            if elevators_reset_list[elevator_id] == 1:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} could not be received when resetting at {timestamp}")
                return
            elif elevator_id < 1 or elevator_id > 6:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} was not a correct elevator id ({elevator_id} at {timestamp}")
                return
            # 乘客已经被分配或已经上电梯
            elif passengers[passenger_id][0] == 1 or passengers[passenger_id][0] == 2:
                print(f"Code {code_id} Error: Passenger {passenger_id} was on the elevator already at {timestamp}")
                return
            passengers[passenger_id][0] = 2  # 已分配但未上电梯
            elevators[elevator_id][4] += 1  # 电梯分配
            elevators_passengers[elevator_id].append(passenger_id)

        # 检查乘客状态
        if action_type == 'IN' or action_type == 'OUT':
            passenger_id = int(parts[1])
            floor = int(parts[2])
            elevator_id = int(parts[3])
            # 检查电梯到达楼层是否在1~11范围内
            if floor < 1 or floor > 11:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} arrived at an invalid floor ({floor}) at {timestamp}")
                return
            # 检查电梯id是否在1~6范围内
            if elevator_id < 1 or elevator_id > 6:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} was not a correct elevator id ({elevator_id} at {timestamp}")
                return
            # 检查电梯是否处于重置状态
            if elevators_reset_list[elevator_id] == 1:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} could not be get on when resetting at {timestamp}")
                return
            if passengers[passenger_id][0] == 0:
                print(
                    f"Code {code_id} Error: Passenger {passenger_id} was not assigned at {timestamp}")
                return

            # 跟踪乘客的当前位置
            # 检查乘客是否有上电梯
            if action_type == 'IN':
                # 乘客不在请求列表中
                if passenger_id not in passengers.keys():
                    print(f"Code {code_id} Error: Passenger {passenger_id} was not in passengers list at {timestamp}")
                    return
                    # print(f"Error: Passenger {passenger_id} did not board the elevator at {timestamp}.")
                # 乘客上电梯楼层不对
                elif passengers[passenger_id][1] != floor:
                    print(f"Code {code_id} Error: Passenger {passenger_id} was not in floor {floor} when he/she wanted "
                          f"to get on the elevator {elevator_id} at {timestamp}")
                    return
                # 乘客没有登上被分配的电梯
                elif passenger_elevator[passenger_id] != elevator_id:
                    print(
                        f"Code {code_id} Error: Passenger {passenger_id} did not board the correct elevator {elevator_id} at {timestamp}")
                    return
                # 是否满员后仍上人
                if elevators[elevator_id][5] == 0:
                    if elevators[elevator_id][2] == 6:
                        print(f"Code {code_id} Error: Elevator {elevator_id} was full at {timestamp}")
                        return
                else:
                    if elevators[elevator_id][2] == elevators_standard[elevator_id][1]:
                        print(f"Code {code_id} Error: Elevator {elevator_id} was full at {timestamp}")
                        return
                passengers[passenger_id][0] = 1  # 上电梯
                passengers[passenger_id][3] = 2  # 上过电梯
                elevators[elevator_id][2] = elevators[elevator_id][2] + 1

            elif action_type == 'OUT':
                if passenger_id not in passengers.keys():
                    print(f"Code {code_id} Error: Passenger {passenger_id} was not in passengers list")
                    return
                # 乘客没有离开被分配的电梯
                elif passenger_elevator[passenger_id] != elevator_id:
                    print(
                        f"Code {code_id} Error: Passenger {passenger_id} did not get off the correct elevator {elevator_id} at {timestamp}")
                    return
                if passengers[passenger_id][2] == floor:
                    # 乘客到目标楼层
                    passengers[passenger_id][3] = 1  # 结束
                passengers[passenger_id][0] = 0  # 下电梯
                passengers[passenger_id][1] = floor
                elevators[elevator_id][2] = elevators[elevator_id][2] - 1
                elevators[elevator_id][4] = elevators[elevator_id][4] - 1
                elevators_passengers[elevator_id].remove(passenger_id)

        # 检查电梯行为是否符合逻辑
        elif action_type == 'ARRIVE' or action_type == 'OPEN' or action_type == 'CLOSE':
            floor = int(parts[1])
            elevator_id = int(parts[2])
            # 检查电梯到达楼层是否在1~11范围内
            if floor < 1 or floor > 11:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} arrived at an invalid floor ({floor}) at {timestamp}")
                return
            # 检查电梯id是否在1~6范围内
            if elevator_id < 1 or elevator_id > 6:
                print(f"Code {code_id} Error: Elevator {elevator_id} was not a correct elevator id ({elevator_id}")
                return
            # 检查电梯是否处于重置状态
            if elevators_reset_list[elevator_id] == 1:
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} could not do anything when resetting at {timestamp}")
                return

            if action_type == 'ARRIVE':
                if elevators[elevator_id][2] == 0 and elevators[elevator_id][4] == 0:
                    print(
                        f"Code {code_id} Error: The movement of Elevator {elevator_id} was not allowed at {timestamp}")
                    return
                if elevators_reset_list[elevator_id] >= 4:
                    print(f"Code {code_id} Error: Elevator {elevator_id} could not move more than twice when waiting "
                          f"to reset at {timestamp}")
                    return
                if elevators[elevator_id][0] - floor != 1 and elevators[elevator_id][0] - floor != -1:
                    print(
                        f"Code {code_id} Error: The movement of Elevator {elevator_id} was not allowed at {timestamp}")
                    return
                if elevators[elevator_id][1] == 'OPEN':
                    print(f"Code {code_id} Error: Elevator {elevator_id} was not allowed to move because it was not "
                          f"close at {timestamp}")
                    return
                # 移动速度
                elif elevators[elevator_id][1] == 'ARRIVE':
                    move_speed = float(timestamp) - float(elevators[elevator_id][3])
                    move_standard_speed = 0.4
                    if elevators[elevator_id][5] == 1:
                        move_standard_speed = float(elevators_standard[elevator_id][2]) / 1000
                    if move_standard_speed - move_speed >= 0.12:
                        print(f"Code {code_id} Error: Elevator {elevator_id} moved so fast at {timestamp}")
                        return
                # 更新电梯状态
                elevators[elevator_id][0] = floor
                elevators[elevator_id][1] = action_type
                if elevators_reset_list[elevator_id] >= 2:
                    elevators_reset_list[elevator_id] += 1

            elif action_type == 'OPEN':
                if elevators[elevator_id][0] != floor:
                    print(
                        f"Code {code_id} Error: Elevator {elevator_id} could not open when it was not in floor {elevators[elevator_id]} at {timestamp}")
                    return
                # 更新电梯状态
                elevators[elevator_id][0] = floor
                elevators[elevator_id][1] = action_type

            elif action_type == 'CLOSE':
                if elevators[elevator_id][1] != 'OPEN':
                    print(
                        f"Code {code_id} Error: Elevator {elevator_id} did not need to close because it was not opened "
                        f"at {timestamp}")
                    return
                if elevators[elevator_id][0] != floor:
                    print(
                        f"Code {code_id} Error: Elevator {elevator_id} could not closed when it was not in floor {elevators[elevator_id]} at {timestamp}")
                    return
                # 更新电梯状态
                elevators[elevator_id][0] = floor
                elevators[elevator_id][1] = action_type
            elevators[elevator_id][3] = timestamp

        elif action_type == 'RESET_ACCEPT':
            elevator_id = int(parts[1])
            elevators_reset_list[elevator_id] = 2
            elevator_reset_time[elevator_id] = [timestamp, 0, 0]
            # elevators[elevator_id][1] = action_type
        elif action_type == 'RESET_BEGIN':
            elevator_id = int(parts[1])
            if elevators[elevator_id][1] != 'CLOSE' and elevators[elevator_id][1] != 'ARRIVE':
                print(
                    f"Code {code_id} Error: Elevator {elevator_id} did not close its door when resetting at {timestamp}.")
                return
            if elevators[elevator_id][2] != 0:
                print(f"Code {code_id} Error: Passengers did not get off the elevator when resetting at {timestamp}.")
                return
            elevators_reset_list[elevator_id] = 1
            elevators[elevator_id][1] = action_type
            elevator_reset_time[elevator_id][1] = timestamp
            elevators[elevator_id][4] = 0
            for passenger in elevators_passengers[elevator_id]:
                passengers[passenger][0] = 0
        elif action_type == 'RESET_END':
            elevator_id = int(parts[1])
            if float(timestamp) - float(elevator_reset_time[elevator_id][1]) >= 1.3 or float(timestamp) - float(
                    elevator_reset_time[elevator_id][0]) >= 5.1:
                print(f"Code {code_id} Error: Elevator {elevator_id} reset too slow at {timestamp}")
                return
            elevator_reset_time[elevator_id][2] = timestamp
            elevators_reset_list[elevator_id] = 0
            elevators[elevator_id][1] = action_type
            elevators[elevator_id][5] = 1

    # 检查电梯运行结束后是否有关门
    for elevator_id in elevators.keys():
        if elevators[elevator_id][1] != 'CLOSE' and elevators[elevator_id][1] != 'RESET_END':
            print(f"Code {code_id} Error: Elevator {elevator_id} did not close its door at the end.")
            return
    # 检查是否有乘客没上电梯
    for passenger in passengers.keys():
        if passengers[passenger][3] == 0:
            print(f"Code {code_id} Error: Passenger {passenger} did not get on the elevator.")
            return
    # 检查是否有乘客没下电梯
    for passenger in passengers.keys():
        if passengers[passenger][0] == 1:
            print(f"Code {code_id} Error: Passenger {passenger} did not get off the elevator.")
            return
    # 检查是否有乘客没到目标楼层
    for passenger in passengers.keys():
        if passengers[passenger][3] == 2:
            print(
                f"Code {code_id} Error: Passenger {passenger} did not arrive at correct floor {passengers[passenger][1]}(Wrong: {passengers[passenger][0]})")
            return
    # 输出检查结果
    print(f"Code {code_id} Elevator behavior check complete. Using {final_time}s")


# 创建一个线程列表
threads = []
# print("生成数据中")
os.system("python data_generator.py > stdin.txt")
# print("生成完成，准备测评")
# 创建并启动评测线程
for i in range(1, code_num + 1):
    lock = threading.Lock()
    t = threading.Thread(target=evaluate_code, args=(i,))
    threads.append(t)
    t.start()

# 等待所有评测线程完成
for t in threads:
    t.join(timeout=220)

for t in threads:
    if t.is_alive():
        print(f"TLE: Thread is still alive")

# print("所有代码评测完成。")
sys.exit()
