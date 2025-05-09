import pymysql
from dbutils.pooled_db import PooledDB  # 需要先安装：pip install dbutils
filename = '变量设置.txt'
iddizhi = 'ip'
useryonghuzhi = 'useryonghuzhi'
database = 'database'
port = 端口号
charset = 'utf8mb4'
connect_timeout = 10
# 打开并读取文件内容
with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        # 去除每行的空白字符（包括换行符）
        line = line.strip()

        # 如果行中有赋值操作（=），就解析变量名和值
        if '=' in line:
            var_name, var_value = line.split('=', 1)
            var_name = var_name.strip()  # 去除变量名两端的空白字符
            var_value = var_value.strip()  # 去除值两端的空白字符

            # 判断值的类型，如果是数字或字符串，转换相应类型
            if var_value.isdigit():  # 如果是数字，转换为整数
                var_value = int(var_value)
            elif var_value.replace('.', '', 1).isdigit() and var_value.count('.') < 2:  # 判断是否是浮点数
                var_value = float(var_value)
            elif var_value.startswith("'") and var_value.endswith("'") or var_value.startswith('"') and var_value.endswith('"'):
                var_value = var_value[1:-1]  # 去掉字符串的引号

            # 使用 exec() 将变量和值动态赋给 Python 变量
            exec(f"{var_name} = {repr(var_value)}")
# 全局数据库配置常量（保持不变）
DB_CONFIG = {
    'host': iddizhi,
    'user': useryonghuzhi,
    'password': 'Linxiruo~20040201',
    'database': database,
    'port': port,
    'charset': charset,
    'connect_timeout': connect_timeout
}
print(DB_CONFIG)

# 创建连接池（在模块加载时初始化）
connection_pool = PooledDB(
    creator=pymysql,
    maxconnections=6,  # 根据业务需求调整
    **DB_CONFIG
)
def connect_db():
    """从连接池获取数据库连接"""
    try:
        return connection_pool.connection()
    except Exception as e:
        print(f"从连接池获取连接失败: {e}")
        return None
def view_data_by_id(record_id):
    """根据字符ID查询（显示新字段）"""
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM new_table WHERE id = %s;", (record_id,))
                result = cursor.fetchone()
                if result:
                    print(f"查询结果 - ID: {result[0]}, Cishuo: {result[1]}, Keyongcishuo: {result[2]}, Zhuangtai: {result[3]}, 备注: {result[4]}")  # 新增输出
                else:
                    print("未找到该ID的数据")
                return result if result else None
        except pymysql.MySQLError as e:
            print(f"查询失败: {e}")
        finally:
            connection.close()
# 数据库连接函
# 数据操作函数
def get_all_status_with_id():
    """获取所有设备的ID和状态（流量优化版）"""
    status_list = []
    connection = connect_db()
    if not connection:
        return status_list  # 保持返回类型一致性

    try:
        with connection.cursor() as cursor:
            # 仅查询状态字段，ID通过循环自增生成
            cursor.execute("SELECT zhuangtai FROM new_table;")
            current_id = 1  # 初始化自增ID
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                # 用自增ID和数据库状态组成元组
                status_list.append((current_id, row[0]))
                current_id += 1  # ID递增
            return status_list
    finally:
        connection.close()  # 确保连接关闭
def get_all_status():
    """获取所有设备状态（流量优化版）"""
    status_list = []
    connection = connect_db()
    if not connection:
        return status_list  # 返回空列表而不是None

    try:
        with connection.cursor() as cursor:
            # 只查询需要的字段，减少数据传输量
            cursor.execute("SELECT zhuangtai FROM new_table;")
            # 流式获取结果（适合大数据量场景）
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                status_list.append(row[0])
            return status_list

    except pymysql.MySQLError as e:
        print(f"查询状态失败: {e}")
        return []  # 发生错误返回空列表
    finally:
        connection.close()
def view_all_data1():
    """查看全部数据（包含备注），并以列表形式返回"""
    id_list = []  # 用于存储所有ID的列表
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM new_table;")
                for row in cursor.fetchall():
                    id_list.append(row[0])  # 将ID添加到列表中
        except pymysql.MySQLError as e:
            print(f"查询数据失败: {e}")
        finally:
            print(f'关闭数据库')
            connection.close()
    return id_list
def view_all_data():
    """查看全部数据（包含备注）"""
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM new_table;")
                for row in cursor.fetchall():
                    print(f"ID: {row[0]}, 使用次数: {row[1]}, 剩余次数: {row[2]}, 状态: {row[3]}, 备注: {row[4]}")
        except pymysql.MySQLError as e:
            print(f"查询数据失败: {e}")
        finally:
            connection.close()
def get_by_id(record_id):
    """根据ID查询完整数据"""
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, cishuo, keyongcishuo, zhuangtai, remark FROM new_table WHERE id = %s",
                    (record_id,)
                )
                result = cursor.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "cishuo": result[1],
                        "keyongcishuo": result[2],
                        "zhuangtai": result[3],
                        "remark": result[4]
                    }
                return None
        except pymysql.MySQLError as e:
            print(f"查询失败: {e}")
            return None
        finally:
            connection.close()
    return None
def add_data(record_id, cishuo, keyongcishuo, zhuangtai, remark):
    """添加新数据（包含备注）"""
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO new_table
                             (id, cishuo, keyongcishuo, zhuangtai, remark)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (record_id, cishuo, keyongcishuo, zhuangtai, remark))
                connection.commit()
                print("数据添加成功！")
        except pymysql.MySQLError as e:
            print(f"添加失败: {e}")
        finally:
            connection.close()
def update_data(record_id, new_cishuo, new_keyongcishuo, new_zhuangtai, new_remark):
    """更新数据（包含备注）"""
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE new_table \
                         SET cishuo       = %s, \
                             keyongcishuo = %s, \
                             zhuangtai    = %s, \
                             remark       = %s
                         WHERE id = %s"""
                affected = cursor.execute(sql, (new_cishuo, new_keyongcishuo, new_zhuangtai, new_remark, record_id))
                connection.commit()
                print(f"更新成功，影响{affected}行" if affected else "未找到该ID数据")
        except pymysql.MySQLError as e:
            print(f"更新失败: {e}")
        finally:
            connection.close()
# 主界面
def main():
    """交互式主界面"""
    while True:
        print("\n=== 设备管理系统 ===")
        print("1. 显示所有数据")
        print("2. ID查询设备")
        print("3. 添加新设备")
        print("4. 更新设备数据")
        print("5. 退出系统")

        choice = input("请输入操作编号: ")

        if choice == '1':
            view_all_data()

        elif choice == '2':
            data = get_by_id(input("请输入设备ID: "))
            if data:
                print("\n=== 设备详细信息 ===")
                print(f"设备ID: {data['id']}")
                print(f"累计使用次数: {data['cishuo']}")
                print(f"剩余可用次数: {data['keyongcishuo']}")
                print(f"当前状态: {data['zhuangtai']}")
                print(f"设备备注: {data['remark']}")
            else:
                print("未找到该设备记录")

        elif choice == '3':
            print("\n=== 添加新设备 ===")
            add_data(
                input("设备ID: "),
                int(input("初始使用次数: ")),
                int(input("初始剩余次数: ")),
                int(input("初始状态(0/1): ")),
                input("设备备注: ")
            )

        elif choice == '4':
            print("\n=== 更新设备数据 ===")
            update_data(
                input("要修改的设备ID: "),
                int(input("新的使用次数: ")),
                int(input("新的剩余次数: ")),
                int(input("新的状态(0/1): ")),
                input("新的备注信息: ")
            )

        elif choice == '5':
            print("系统已退出")
            break

        else:
            print("无效输入，请重新选择")


if __name__ == "__main__":
    # 先执行数据库表结构变更（只需要执行一次）
    # ALTER TABLE new_table ADD COLUMN remark VARCHAR(255);
    main()