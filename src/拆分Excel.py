# -*- coding: utf-8 -*-
import os
import math
import xlrd
import xlwt


def get_file_list(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def split_xls(name, path):
    limit = 10000
    print(name)
    limit = int(limit)
    data = xlrd.open_workbook(path + name)
    # 获取sheet
    table = data.sheets()[0]
    # 行数
    nrows = table.nrows
    print('总行数{}'.format(nrows))
    # 列数
    sheets = math.ceil(nrows / limit)
    print('拆分文件数量:{}'.format(sheets))
    for i in range(int(sheets)):
        if i == 0:
            start_row = 0
        else:
            start_row = i * limit
        if i == sheets - 1:
            end_row = nrows
        else:
            end_row = (i + 1) * limit
        # print(start_row)
        # print(end_row)

        new_arr = []
        new_arr.append([
            "ALERTID", "PLANTID", "CREWID", "SYSTEMID", "MODELID", "MODELNAME",
            "SPECIALTY", "ALERTLEVEL", "SIECODE", "RELATEDSIECODE",
            "WARNINGNUM", "WARNINGPERIOD", "ALERTMSG", "CLOSESTATUSCODE",
            "CLOSESTATUSNAME", "ALARMID", "BGTIME", "ENDTIME", "LATESTTIME",
            "RECOVERTIME", "ALERTSTATUSCODE", "ALERTSTATUSNAME", "COMMENTS"
        ])
        for row in range(start_row, end_row):
            if i == 0 and row == 0:
                continue
            ALERTID = table.cell_value(row, 0)
            PLANTID = table.cell_value(row, 1)
            CREWID = table.cell_value(row, 2)
            SYSTEMID = table.cell_value(row, 3)
            MODELID = table.cell_value(row, 4)
            MODELNAME = table.cell_value(row, 5)
            SPECIALTY = table.cell_value(row, 6)
            ALERTLEVEL = table.cell_value(row, 7)
            SIECODE = table.cell_value(row, 8)
            RELATEDSIECODE = table.cell_value(row, 9)
            WARNINGNUM = table.cell_value(row, 10)
            WARNINGPERIOD = table.cell_value(row, 11)
            ALERTMSG = table.cell_value(row, 12)
            CLOSESTATUSCODE = table.cell_value(row, 13)
            CLOSESTATUSNAME = table.cell_value(row, 14)
            ALARMID = table.cell_value(row, 15)
            BGTIME = table.cell_value(row, 16)
            ENDTIME = table.cell_value(row, 17)
            LATESTTIME = table.cell_value(row, 18)
            RECOVERTIME = table.cell_value(row, 19)
            ALERTSTATUSCODE = table.cell_value(row, 20)
            ALERTSTATUSNAME = table.cell_value(row, 21)
            COMMENTS = table.cell_value(row, 22)
            new_arr.append([
                ALERTID, PLANTID, CREWID, SYSTEMID, MODELID, MODELNAME,
                SPECIALTY, ALERTLEVEL, SIECODE, RELATEDSIECODE, WARNINGNUM,
                WARNINGPERIOD, ALERTMSG, CLOSESTATUSCODE, CLOSESTATUSNAME,
                ALARMID, BGTIME, ENDTIME, LATESTTIME, RECOVERTIME,
                ALERTSTATUSCODE, ALERTSTATUSNAME, COMMENTS
            ])
        # print(new_arr)

        new_workbook = xlwt.Workbook()
        new_worksheet = new_workbook.add_sheet('Sheet1',
                                               cell_overwrite_ok=True)
        for new_row in range(0, len(new_arr)):
            new_worksheet.write(new_row, 0, new_arr[new_row][0])
            new_worksheet.write(new_row, 1, new_arr[new_row][1])
            new_worksheet.write(new_row, 2, new_arr[new_row][2])
            new_worksheet.write(new_row, 3, new_arr[new_row][3])
            new_worksheet.write(new_row, 4, new_arr[new_row][4])
            new_worksheet.write(new_row, 5, new_arr[new_row][5])
            new_worksheet.write(new_row, 6, new_arr[new_row][6])
            new_worksheet.write(new_row, 7, new_arr[new_row][7])
            new_worksheet.write(new_row, 8, new_arr[new_row][8])
            new_worksheet.write(new_row, 9, new_arr[new_row][9])
            new_worksheet.write(new_row, 10, new_arr[new_row][10])
            new_worksheet.write(new_row, 11, new_arr[new_row][11])
            new_worksheet.write(new_row, 12, new_arr[new_row][12])
            new_worksheet.write(new_row, 13, new_arr[new_row][13])
            new_worksheet.write(new_row, 14, new_arr[new_row][14])
            new_worksheet.write(new_row, 15, new_arr[new_row][15])
            new_worksheet.write(new_row, 16, new_arr[new_row][16])
            new_worksheet.write(new_row, 17, new_arr[new_row][17])
            new_worksheet.write(new_row, 18, new_arr[new_row][18])
            new_worksheet.write(new_row, 19, new_arr[new_row][19])
            new_worksheet.write(new_row, 20, new_arr[new_row][20])
            new_worksheet.write(new_row, 21, new_arr[new_row][21])
            new_worksheet.write(new_row, 22, new_arr[new_row][22])

        old_name = name.split('.')
        new_name = old_name[0] + '-' + str(i) + '.xlsx'
        new_workbook.save(path + '\\' + new_name)
    print('************************************')


if __name__ == '__main__':
    # globalPath = 'D:\\importdir\\test\\'
    globalPath = input("please enter the excel path: ")
    print(globalPath)
    file_list = get_file_list(globalPath)
    for name in file_list:
        if name.endswith('xlsx'):
            # 大于10M就拆分10*1024*1024
            if os.path.getsize(
                    os.path.join(globalPath + '\\' + name)) > 10485760:
                split_xls(name, globalPath)
                os.remove(os.path.join(globalPath) + '\\' + name)
            else:
                print("文件{0}大小不超过10M不需要拆分".format(name))
