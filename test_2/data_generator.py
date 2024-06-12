import random

special_flag = False  # hw7生成压力测试开关，保持False
testdata_line = 70    # 上限70

ans = ''
n = random.randint(10, 40)
prev_timestamp = 1.0
timestamp = 1.0
passengers_idList = [0] * 71
passenger_num = 0
pre_start_floor = 1
pre_end_floor = 11
reset_num = 0
elevator_reset_time = [0] * 7
elevator_list2reset = [0] * 7

if special_flag:
    max_num = random.randint(3, 8)
    move_time = 0.1 * random.randint(2, 6)
    for j in range(1, 7):
        print(f"[{timestamp:.1f}]RESET-DCElevator-{j}-5-{max_num}-{move_time:.1f}")
for i in range(testdata_line - 6):
    if special_flag:
        # if i % 8 == 0:
        #     timestamp += 10
        passengers_id = random.randint(1, 70)
        while passengers_idList[passengers_id] == 1:
            passengers_id = random.randint(1, 70)
        passengers_idList[passengers_id] = 1
        data = f"[{49.9}]{passengers_id}-FROM-{11}-TO-{1}"
        print(data)
        continue
    do_while_flag = True
    while do_while_flag:
        flag = random.random()
        if flag < 0.5:
            timestamp = prev_timestamp + random.random() + 0.1
        elif flag > 0.9:
            timestamp = prev_timestamp + random.randint(3, 7)
        else:
            timestamp = prev_timestamp

        if timestamp > 35:
            do_while_flag = False
            timestamp = prev_timestamp
        prev_timestamp = timestamp
        break


    rest_flag = random.random()
    while rest_flag < 0.3 and reset_num < 20:
        elevator_id = random.randint(1, 6)
        flag = 0
        while elevator_list2reset[elevator_id] == 1:
            elevator_id = random.randint(1,6)
            flag = flag + 1
            if flag >= 6:
                break
        if flag == 6:
            break
        if flag < 6:
            elevator_list2reset[elevator_id] = 1
            max_num = random.randint(3, 8)
            move_time = 0.1 * random.randint(2, 6)
            reset_num = reset_num + 1
            rest_flag = random.random()
            data = f"[{timestamp:.1f}]RESET-Elevator-{elevator_id}-{max_num}-{move_time:.1f}"
            print(data)
    passengers_id = random.randint(1, 70)
    while passengers_idList[passengers_id] == 1:
        passengers_id = random.randint(1, 70)
    passengers_idList[passengers_id] = 1
    flag = random.random()
    if flag < 0.2:
        start_floors = pre_start_floor
        end_floors = pre_end_floor
    else:
        start_floors = random.randint(1, 11)
        end_floors = random.randint(1, 11)
        while end_floors == start_floors:
            end_floors = random.randint(1, 11)
    pre_start_floor = start_floors
    pre_end_floor = end_floors

    data = f"[{timestamp:.1f}]{passengers_id}-FROM-{start_floors}-TO-{end_floors}"
    #data = f"{passengers_id}-FROM-{start_floors}-TO-{end_floors}"
    print(data)
