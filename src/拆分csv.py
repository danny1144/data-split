# ecoding=utf-8
import os
import time
import shutil


def mkdir(path):
    # 判断目录是否存在
    # 存在：True
    # 不存在：False
    folder = os.path.exists(path)

    # 判断结果
    if not folder:
        # 如果不存在，则创建新目录
        os.makedirs(path)
        print('-----创建成功-----')

    else:
        # 如果目录已存在，则不创建，提示目录已存在
        print(path + '目录已存在')


# path = 'd:\\xxoo\\test'
# mkdir(path)


def moveFile(dir=None):
    # dir = "D:\\importdir\\sensors\\List4 201804~201806\\"
    # dir = "D:\\importdir\\sensors\\List4 201807~201809\\"
    # dir = "D:\\importdir\\sensors\\List4 201810-201812\\"
    sensors = os.listdir(dir)
    for sensor in sensors:
        if sensor.endswith('csv'):
            dirname = sensor.split('.')[1].split('_')[0]
            mkdir(os.path.join(dir) + '\\' + dirname)
            shutil.move(
                os.path.join(dir) + '\\' + sensor,
                os.path.join(dir) + '\\' + dirname)


# moveFile()


# 2020/04/21 将大的csv文件拆分多个小的csv文件
def mkSubFile(lines, head, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, encoding="utf-8")
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()


if __name__ == '__main__':
    begin = time.time()
    # 解压完第一步：创建每天的目录，并移动数据到每天的文件夹
    # globalDir = 'D:\\importdir\\sensors\\'
    globalDir = input("please enter the csv home path: ")
    print(globalDir)
    globalSensorDir = os.listdir(globalDir)
    for outerDir in globalSensorDir:
        if os.path.isdir(os.path.join(globalDir + '\\' + outerDir)):
            # 季度文件夹
            dir = os.path.join(globalDir + outerDir)
            # 依次对每天的数据进行裁剪至30000条一个文件
            # dir = "D:\\importdir\\sensors\\List4 201804~201806\\"
            moveFile(dir)
            sensors = os.listdir(dir)
            for day in sensors:
                if os.path.isdir(os.path.join(dir + '\\' + day)):
                    needSplit = os.listdir(os.path.join(dir + '\\' + day))
                    first = needSplit[0]
                    if needSplit.__len__() > 1:
                        continue
                    if first.endswith('csv'):
                        # 超过10M就裁剪
                        if os.path.getsize(
                                os.path.join(dir + '\\' + day + '\\' +
                                             first)) > 10485760:
                            splitByLineCount(
                                os.path.join(dir) + '\\' + day + '\\' + first,
                                30000)  # 每个小的csv文件存放30000条
                            os.remove(
                                os.path.join(dir) + '\\' + day + '\\' + first)
                        else:
                            print("文件{0}大小不超过10M不需要裁剪".format(first))
    end = time.time()
    print('time is %d seconds ' % (end - begin))
