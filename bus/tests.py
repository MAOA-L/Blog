import pymssql

server = '192.168.0.141'  # 数据库服务器名称或IP
user = 'sa'  # 用户名
password = '13486059134Chen'  # 密码
database = 'new_con'  # 数据库名称
charset = 'utf8'
conn = pymssql.connect(server, user, password, database, charset)

cursor = conn.cursor()
cursor.execute('SELECT * FROM group_tb')

for row in cursor:
    print([i.encode("latin-1").decode("gbk") for i in row if isinstance(i, str)])
    # for j in row:
    #     if isinstance(j, str):
    #         print(j.encode("latin-1").decode("gbk"), type(j), end='')
    # print()

conn.close()
