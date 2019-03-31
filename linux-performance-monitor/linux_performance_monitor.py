#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 持续监控linux系统中指定进程占用系统CPU和内存情况
# 跟据需要，可将监控结果保存到excel表格中，或MySQL数据库中

# @Author : leeyoshinari

import paramiko
import pymysql
import time
import matplotlib.pyplot as plt
import xlwt
import argparse
from six.moves import xrange


class PerMon(object):
    def __init__(self, PID, total_time, interval, linux_ip, linux_name, linux_password,
                 mysql_ip, mysql_username, mysql_password, database_name, is_mysql, is_save):

        self.counter = 0    # 执行linux命令失败计数，默认5次
        self.linux_flag = False 	# 程序执行过程中是否连接linux标志
        self.linux_link_counter = 0		# 程序执行过程中重复连接linux计数，默认3次
        self.pid = PID
        self.client = None
        self.ssh = None
        self.db = None
        self.cursor = None
        self.is_mysql = is_mysql
        self.is_save = is_save
        self.total_time = total_time + 300
        self.interval = interval

        self.x_label = []
        self.cpu = []
        self.mem = []

        self.linux_ip = linux_ip
        self.linux_username = linux_name
        self.linux_password = linux_password
        self.mysql_ip = mysql_ip
        self.mysql_username = mysql_username
        self.mysql_password = mysql_password
        self.database_name = database_name

        self.connect_linux()

        if self.is_mysql:
            self.connect_mysql()

        self.start_time = time.time()

    def connect_linux(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.linux_ip, username=self.linux_username, password=self.linux_password)

    def connect_mysql(self):
        self.db = pymysql.connect(self.mysql_ip, self.mysql_username, self.mysql_password, self.database_name)
        self.cursor = self.db.cursor()

        sql = 'CREATE TABLE IF NOT EXISTS performance (' \
              'id INT NOT NULL PRIMARY KEY auto_increment,' \
              'pid INT,' \
              'time CHAR(25), ' \
              'cpu FLOAT,' \
              'mem FLOAT);'

        self.cursor.execute(sql)
        self.db.commit()

    def get_data(self):
        start_search_time = time.time()

        while True:
            if time.time() - self.start_time < self.total_time:
                if self.counter == 5:   # 如果执行命令失败次数等于5次，则重新连接linux
                    self.linux_flag = True		# 连接linux
                    self.counter = 0		# 重新计数

                if self.linux_flag:
                    self.connect_linux()    # 连接linux
                    self.linux_link_counter += 1    # linux连接次数
                    self.linux_flag = False  # 重置是否连接linux标志

                if self.linux_link_counter == 3:    # 如果连续3次连接linux，仍然执行命令失败，则跳出循环
                    break

                get_data_time = time.time()
                if get_data_time - start_search_time > self.interval:
                    self.ssh = self.client.get_transport().open_session()
                    if self.ssh.active:
                        self.ssh.exec_command('top -n 1 -b |grep -P {} |tr -s " "'.format(self.pid))
                        res = self.ssh.recv(1024).decode().split('java')[0].strip().split(' ')
                    else:
                        continue

                    if res:
                        try:
                            search_time = time.strftime('%Y-%m-%d %H:%M:%S')
                            cpu = float(res[-3])
                            mem = float(res[-2])
                            if self.is_save:
                                self.x_label.append(search_time)
                                self.cpu.append(cpu)
                                self.mem.append(mem)

                            if self.is_mysql:
                                self.write_in_sql(search_time, cpu, mem)

                            # 如果命令执行成功，所有计数和标志重置
                            self.counter = 0
                            self.linux_flag = False
                            self.linux_link_counter = 0
                        except Exception as e:
                            print('The PID {} is not exist. Error maybe {}.'.format(self.pid, e))
                            self.counter += 1
                            continue

                    else:
                        self.counter += 1
                        continue

                    print('{} CPU: {}, MEM: {}'.format(search_time, cpu, mem))

                    start_search_time = get_data_time

            else:
                break

    def write_in_sql(self, search_time, cpu, mem):
        if self.db is None:     # If MySQL connection is broken, reconnect.
            self.db = pymysql.connect(self.mysql_ip, self.mysql_username, self.mysql_password, self.database_name)
            self.cursor = self.db.cursor()

        sql = "INSERT INTO performance(id, pid, time, cpu, mem) " \
              "VALUES (default, {}, '{}', {}, {});".format(self.pid, search_time, cpu, mem)

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def write_file(self, file):
        excel = xlwt.Workbook(encoding='utf-8')
        sheet = excel.add_sheet('PerfMon')
        sheet.write(0, 0, 'time')
        sheet.write(0, 1, 'cpu %')
        sheet.write(0, 2, 'mem %')
        for i in xrange(len(self.cpu)):
            sheet.write(i+1, 0, self.x_label[i])
            sheet.write(i+1, 1, self.cpu[i])
            sheet.write(i+1, 2, self.mem[i])

        excel.save(file)

    def draw_graph(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(self.x_label, self.cpu, 'b-', label='cpu')
        ax2 = ax1.twinx()
        ax2.plot(self.x_label, self.mem, 'r--', label='mem')
        ax1.grid()
        ax1.set_ylabel('cpu %')
        ax2.set_ylabel('mem %')
        ax1.legend()
        ax2.legend()

    def run(self, file, is_save, is_plot):
        self.get_data()

        if is_save:
            self.write_file(file)

        if is_plot:
            self.draw_graph()
            plt.show()

        self.client.close()
        self.db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--PID', default=66666, type=int, help='The PID that is monitored.')
    parser.add_argument('--total_time', default=7200, type=int, help='The total time(/s) of monitoring.')
    parser.add_argument('--interval', default=2, type=int, help='The interval(/s) of getting data from server.')

    parser.add_argument('--linux_ip', default='xxx.xxx.xxx.xxx', type=str, help='The server ip that the PID is in it.')
    parser.add_argument('--linux_username', default='root', type=str, help='The username of the server.')
    parser.add_argument('--linux_password', default='password', type=str, help='The password of the server.')

    parser.add_argument('--mysql_ip', default='xxx.xxx.xxx.xxx', type=str, help='The MySQL ip.')
    parser.add_argument('--mysql_username', default='root', type=str, help='The username of the MySQL.')
    parser.add_argument('--mysql_password', default='password', type=str, help='The password of the MySQL.')
    parser.add_argument('--database', default='performance_monitor', type=str, help='The name of the database '
                                                                                    'of the MySQL.')

    parser.add_argument('--savefile', default='perform.xls', type=str, help='The saved path of file that the '
                                                                            'perform data. It must be excel(.xls).')

    parser.add_argument('--is_save', default=False, type=bool, help='Whether the data is saved to excel(.xls)')
    parser.add_argument('--is_mysql', default=True, type=bool, help='Whether the data is written to MySQL.')
    parser.add_argument('--is_plot', default=False, type=bool, help='Whether draw graph of CPU and MEM when the end.')

    args = parser.parse_args()

    if args.is_save:
        if args.savefile.split('.')[-1] != 'xls':
            raise Exception('The file must be excel(.xls).')

    perfmon = PerMon(args.PID, args.total_time, args.interval, args.linux_ip, args.linux_username,
                     args.linux_password, args.mysql_ip, args.mysql_username, args.mysql_password,
                     args.database, args.is_mysql, args.is_save)

    perfmon.run(args.savefile, args.is_save, args.is_plot)


if __name__ == '__main__':
    main()
