import os

def append_genshin_data():
    """
    交互式收集原神攒球数据，并追加写入到指定的MD文件中
    """
    # 定义目标文件路径
    file_path = os.path.join(os.getcwd(), "source/_posts/gs-accumulate.md")
    
    # 确保文件所在目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        # 1. 交互式获取用户输入，并进行类型验证
        while True:
            try:
                days = int(input("请输入天数："))
                if days <= 0:
                    print("天数必须是正整数，请重新输入！")
                    continue
                break
            except ValueError:
                print("输入无效，请输入数字格式的天数！")

        while True:
            try:
                new_fate = int(input("请输入新垫的纠缠之缘数："))
                if new_fate < 0:
                    print("纠缠之缘数不能为负数，请重新输入！")
                    continue
                break
            except ValueError:
                print("输入无效，请输入数字格式的纠缠之缘数！")

        while True:
            try:
                saved_fate = int(input("请输入攒的纠缠之缘数："))
                if saved_fate < 0:
                    print("纠缠之缘数不能为负数，请重新输入！")
                    continue
                break
            except ValueError:
                print("输入无效，请输入数字格式的纠缠之缘数！")

        while True:
            try:
                primogems = int(input("请输入原石数："))
                if primogems < 0:
                    print("原石数不能为负数，请重新输入！")
                    continue
                break
            except ValueError:
                print("输入无效，请输入数字格式的原石数！")

        # 2. 计算平均攒球速度（保留1位小数）
        avg_speed = round((new_fate + saved_fate) / days, 1)

        # 3. 构造MD格式文本（严格保留空格和格式）
        md_content = f"""#### 第 {days} 天  
总情况：大 39 + {new_fate} + {saved_fate}, {primogems}  
平均攒球速度：{avg_speed} 粉球/天  

"""  # 末尾加空行是为了和下一次追加的内容分隔，更美观

        # 4. 追加写入文件（使用UTF-8编码避免中文乱码）
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"\n✅ 数据已成功追加到文件：{file_path}")
        print(f"写入的内容：\n{md_content}")

    except Exception as e:
        print(f"❌ 发生错误：{e}")

if __name__ == "__main__":
    append_genshin_data()