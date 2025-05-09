def 输入颜色和形状查找序号(data, yanshe=None, xingzhuang=None,chaoxiang=None):
    # matching_ids = []
    for entry_id, entry in data.items():
        # 检查颜色条件
        color_match = (yanshe is None) or (entry['yanshe'] == yanshe)
        # 检查形状条件
        shape_match = (xingzhuang is None) or (entry['xingzhuang'] == xingzhuang)
        # 检查朝向条件（如果参数为None则忽略该条件）
        chaoxiang_match = (chaoxiang is None) or (entry.get('chaoxiang') == chaoxiang)
        if color_match and shape_match and chaoxiang_match:
            return entry_id
    #
    # # 按数值大小排序（将字符串转换为整数比较）
    # matching_ids.sort(key=lambda x: int(x))
    # return matching_ids
def 输入形状查找颜色(data, xingzhuang):
    # 提取所有匹配形状的条目，并转换为 (整数ID, 颜色) 的列表
    matches = [
        (int(entry_id), entry["yanshe"])
        for entry_id, entry in data.items()
        if entry["xingzhuang"] == xingzhuang
    ]

    if not matches:
        return None  # 无匹配时返回空

    # 按 ID 的数值从小到大排序
    matches.sort()

    # 返回第一个匹配的颜色
    return matches[0][1]
def 输入形状查找朝向(data, xingzhuang):
    # 提取所有匹配形状的条目，并转换为 (整数ID, 颜色) 的列表
    matches = [
        (int(entry_id), entry["chaoxiang"])
        for entry_id, entry in data.items()
        if entry["xingzhuang"] == xingzhuang
    ]

    if not matches:
        return None  # 无匹配时返回空

    # 按 ID 的数值从小到大排序
    matches.sort()

    # 返回第一个匹配的颜色
    return matches[0][1]
def 查找所有的数字对应的_id(your_dict):
    matches = [
        entry_id
        for entry_id, entry in your_dict.items()
        if len(entry["xingzhuang"]) == 1
           and entry["xingzhuang"] in '0123456789'
    ]
    matches.sort(key=lambda x: int(x))
    return matches
def 查找所有的字母对应的_id(your_dict):
    """
    查找字典中所有xingzhuang为单个英文字母的条目ID
    （包含大小写 A-Z, a-z）
    """
    target_letters = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    }

    matches = [
        entry_id
        for entry_id, entry in your_dict.items()
        if len(entry["xingzhuang"]) == 1
           and entry["xingzhuang"] in target_letters
    ]
    matches.sort(key=lambda x: int(x))
    return matches
    # 调用示例
def 获取中心点(字典, 序号):
    x1, y1, x2, y2 = 字典[序号]['zuobiao']
    return ((x1 + x2)//2, (y1 + y2)//2)
def 获取左上角坐标(字典, 序号):
    x1, y1, x2, y2 = 字典[序号]['zuobiao']
    return ((x1 + x2)//2, (y1 + y2)//2)
def 根据列表id找到形状(数据字典, 序号列表):
    """根据输入的序号列表返回对应的形状列表"""
    return [数据字典.get(序号, {}).get("xingzhuang", None) for 序号 in 序号列表]

# 调用方式不变

if __name__ == '__main__':
    # 你的字典数据
    your_dict ={
  "1": {
    "zuobiao": [
      125,
      60,
      153,
      94
    ],
    "yanshe": "红色",
    "xingzhuang": "e",
    "chaoxiang": "正向"
  },
  "2": {
    "zuobiao": [
      131,
      21,
      157,
      51
    ],
    "yanshe": "紫色",
    "xingzhuang": "e",
    "chaoxiang": "正向"
  },
  "3": {
    "zuobiao": [
      197,
      1,
      248,
      50
    ],
    "yanshe": "紫色",
    "xingzhuang": "矩形",
    "chaoxiang": "正向"
  },
  "4": {
    "zuobiao": [
      48,
      55,
      83,
      101
    ],
    "yanshe": "黑色",
    "xingzhuang": "6",
    "chaoxiang": "右侧向"
  },
  "5": {
    "zuobiao": [
      272,
      98,
      307,
      147
    ],
    "yanshe": "黄色",
    "xingzhuang": "4",
    "chaoxiang": "右侧向"
  },
  "6": {
    "zuobiao": [
      276,
      8,
      309,
      53
    ],
    "yanshe": "红色",
    "xingzhuang": "E",
    "chaoxiang": "正向"
  },
  "7": {
    "zuobiao": [
      202,
      62,
      237,
      101
    ],
    "yanshe": "红色",
    "xingzhuang": "e",
    "chaoxiang": "正向"
  },
  "8": {
    "zuobiao": [
      309,
      0,
      336,
      26
    ],
    "yanshe": "橙色",
    "xingzhuang": "刷新",
    "chaoxiang": "正向"
  }
}
    # 示例调用：
    # 1. 只找颜色为"蓝色"的条目
    print(输入颜色和形状查找序号(your_dict, yanshe='蓝色'))  # 输出：['4', '6', '10']
    # 2. 只找形状为"圆柱"的条目
    print(输入颜色和形状查找序号(your_dict, xingzhuang='圆柱'))  # 输出：['2', '8']
    print(输入颜色和形状查找序号(your_dict, chaoxiang='右侧向'))  # 输出：['2', '8']
    # 3. 同时找颜色为"蓝色"且形状为"h"的条目
    print(输入颜色和形状查找序号(your_dict, yanshe='红', xingzhuang='矩形'))  # 输出：['6', '10']
    print('_' * 100)
    print(输入形状查找颜色(your_dict, "h"))  # 输出：黑色
    print(输入形状查找颜色(your_dict, "圆柱"))  # 输出：红色
    print(输入形状查找颜色(your_dict, "H"))  # 输出：蓝色
    print(输入形状查找颜色(your_dict, "未知"))  # 输出：None
    print(输入形状查找朝向(your_dict, "球"))  # 输出：None
    print('_' * 100)
    print(查找所有的数字对应的_id(your_dict))
    print(查找所有的字母对应的_id(your_dict))
    XUHAIID=输入颜色和形状查找序号(your_dict, yanshe='黑色', xingzhuang='矩形')  # 输出：['6', '10']
    print(XUHAIID)
    if XUHAIID:
        print(获取中心点(your_dict, XUHAIID))
