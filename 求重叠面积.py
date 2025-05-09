import json


def calculate_overlap(rect1, rect2):
    """计算两个矩形区域的相交面积"""
    x1 = max(rect1[0], rect2[0])
    y1 = max(rect1[1], rect2[1])
    x2 = min(rect1[2], rect2[2])
    y2 = min(rect1[3], rect2[3])
    return max(0, x2 - x1) * max(0, y2 - y1) if x2 > x1 and y2 > y1 else 0


def find_max_overlap(data, shape1, shape2):
    """
    增强版函数：支持传入单个形状或形状列表

    参数：
    data: 形状字典数据
    shape1: 单个形状字符串 或 形状列表
    shape2: 单个形状字符串 或 形状列表
    """
    # 统一转换为列表
    shapes1 = [shape1] if isinstance(shape1, str) else shape1
    shapes2 = [shape2] if isinstance(shape2, str) else shape2

    max_area = -1
    best_pair = (None, None)
    found_valid = False
    # 遍历所有形状组合
    for s1 in shapes1:
        for s2 in shapes2:
            # 筛选对象
            objs1 = {k: v for k, v in data.items() if v["xingzhuang"] == s1}
            objs2 = {k: v for k, v in data.items() if v["xingzhuang"] == s2}

            if not objs1 or not objs2:
                continue

            found_valid = True

            # 遍历对象组合
            for k1, v1 in objs1.items():
                for k2, v2 in objs2.items():
                    if k1 == k2:  # 跳过同对象比较
                        continue
                    area = calculate_overlap(v1["zuobiao"], v2["zuobiao"])
                    if area > max_area:
                        max_area = area
                        best_pair = (k1, k2)

    if not found_valid:
        missing = []
        if not any(v["xingzhuang"] in shapes1 for v in data.values()):
            missing.append(shapes1)
        if not any(v["xingzhuang"] in shapes2 for v in data.values()):
            missing.append(shapes2)
        print(f"未找到形状组合 {missing} 对应的有效对象")
        return None

    return best_pair, max_area
if __name__ == '__main__':
    input_data = {'1': {'zuobiao': [610, 90, 769, 217], 'yanshe': '橙色', 'xingzhuang': 'm'},
                  '2': {'zuobiao': [111, 38, 242, 197], 'yanshe': '红色', 'xingzhuang': '圆柱'},
                  '3': {'zuobiao': [879, 208, 1012, 396], 'yanshe': '黑色', 'xingzhuang': 'h'},
                  '4': {'zuobiao': [879, 20, 1036, 224], 'yanshe': '蓝色', 'xingzhuang': 'H'},
                  '5': {'zuobiao': [371, 377, 496, 540], 'yanshe': '紫色', 'xingzhuang': '4'},
                  '6': {'zuobiao': [610, 230, 733, 389], 'yanshe': '蓝色', 'xingzhuang': 'h'},
                  '7': {'zuobiao': [327, 20, 511, 206], 'yanshe': '黑色', 'xingzhuang': '矩形'},
                  '8': {'zuobiao': [71, 280, 275, 491], 'yanshe': '绿色', 'xingzhuang': '圆柱'},
                  '9': {'zuobiao': [1039, 10, 1143, 115], 'yanshe': '橙色', 'xingzhuang': '刷新'},
                  '10': {'zuobiao': [120, 218, 225, 364], 'yanshe': '蓝色', 'xingzhuang': 'h'}}
    # 用户输入
    shape_a = '圆柱'
    shape_b =['m', 'h', 'H', 'h', 'h']

    # 执行计算
    result = find_max_overlap(input_data, shape_a, shape_b)
    print(result)

    if result:
        (id1, id2), area = result
        if area > 0:
            print(f"最大重叠面积发生在 {shape_a}-{id1} 和 {shape_b}-{id2} 之间，面积为 {area}")
            print(f'点击{id2}')
        else:
            print(f"没有找到 {shape_a} 和 {shape_b} 之间的重叠区域")
    else:
        print("输入形状不存在有效组合")
# 示例数据（替换为你的实际输入）


# 示例测试：输入 p 和 圆锥
# 输出：最大重叠面积发生在 p-7 和 圆锥-8 之间，面积为 0（根据实际数据可能需要调整）