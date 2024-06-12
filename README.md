# buaa-oo-evaluations

buaa oo2024第二三单元测评机，自建

## 项目说明

本仓库保存了本人在buaa2024oo中Unit2和Unit3中使用的测评机，均为自建，用于评测作业代码正确性。此库建立是为申请oo助教所用。

## 文件说明

目录test_2下放置着第二单元测评机，支持第二单元**hw6**作业的测试(由于迭代开发不再适用hw5的输入格式)

* data_generator.py为数据生成器。
* main_auto,py为正确性检验代码，当前支持11份代码同时测评（使用多线程），该数字可调。
* main.py为自建娱乐玩法，可以自定义测评次数n，每次测评同时测评11份代码（同main_auto.py可调），输出电梯运行时间，并按照时间进行排名，从而可以估计自己代码的性能（纯娱乐，**需要保证代码不会TLE**）

目录test_3下放置着第三单元测评机

## 使用说明

### test_2

* main.py和main_auto.py下的`code_num`设置了同时测评的代码份数，当前设置为10，注意运行时需要设置为相同数字。
* data_generator.py中`testdata_line`为输入数据行数，当数据量超过40时几乎一定包含6次RESET，当前设置上限为70。`special_flag`不要修改，请保持`False`（若为`True`，则会生成hw7压力测试数据，但本人并未搭建hw7测评机，因此不能与main.py一起使用）。
* 请将待测代码的jar包命名为`code{i}.jar`(i = 1、2……code_num)并与测评机代码放置在一个目录下，同时需要官方输入程序`datainput_student_win64.exe`帮助输入（也放置在同一目录下）。
* 命令行或pycharm运行main_auto.py后会自动测试一次；运行main.py后可以自选测试次数，实现自动化测评，当出现`wrong answer`时结束测评，输出当前错误信息，保存当前测试的输入数据至`stdin.txt`，每份代码的输出保存在`out{i}.txt`下。

### test_3

