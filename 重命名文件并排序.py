import os

def replace_class_ids(input_dir, output_dir, old_to_new):
    """
    批量替换YOLO标注文件的类别索引，并删除字典中没有对应映射的行
    :param input_dir: 原始标注文件目录
    :param output_dir: 新标注文件目录（可与input_dir相同）
    :param old_to_new: 旧索引到新索引的映射字典，格式如 {6: 6, 9: 5}
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 遍历所有txt文件
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
            for line in f_in:
                parts = line.strip().split()

                if not parts:
                    continue  # 跳过空行
                # 解析旧索引
                old_id = int(parts[0])
                # 判断是否在映射字典中
                if old_id in old_to_new:
                    new_id = old_to_new[old_id]  # 获取新索引
                    if new_id != old_id:  # 只有在新索引与旧索引不相同的情况下才替换
                        new_line = f"{new_id} {' '.join(parts[1:])}\n"
                        f_out.write(new_line)
                # 如果该数字没有映射关系，则跳过该行

if __name__ == "__main__":
    # ========== 使用示例 ==========
    # 定义需要替换的映射关系（旧索引 : 新索引）
    replacement_map ={0: 0, 1: 5, 2: 6, 3: 7, 4: 8, 5: 9}
    # 设置路径（建议先备份原文件）
    input_folder = r"C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\datasets\icon\labels\daixiug"
    output_folder = r"C:\Users\67167\Desktop\YOLU\YOLOXUNLIAN\ultralytics-8.3.55\datasets\icon\labels\xin"  # 可与input_folder相同

    # 执行替换
    replace_class_ids(input_folder, output_folder, replacement_map)