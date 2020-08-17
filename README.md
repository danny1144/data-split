virtualenv excel
source excel/bin/activate #linux

excel/Scripts/activate.bat # win

pip install -r requirements.txt

pip freeze >requirements.txt

## 拆分csv
1、文件超过10M就拆
2、每个csv最多30000条
## 拆分Excel
1、文件超过10M就拆
2、每个excel最多10000条


##数据库迁移
从oracle批量获取数据批量更新pgsql