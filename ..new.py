import os
import datetime
import re
import glob

openFile = "NONE"

os.system("chcp 65001 & cls")

def get_multiple_inputs(prompt):
    """获取多项输入，每行一项，空行结束"""
    print(prompt)
    items = []
    while True:
        item = input(f"第 {len(items)+1} 项（直接回车结束）: ").strip()
        if not item:
            break
        items.append(item)
    return items

def publish_draft():
    """发布草稿功能"""
    drafts_dir = "source/_drafts"
    
    if not os.path.exists(drafts_dir):
        print("草稿目录不存在！")
        return
    
    draft_files = [f for f in os.listdir(drafts_dir) if f.endswith('.md')]
    
    if not draft_files:
        print("没有找到草稿文件！")
        return
    
    print("\n=== 草稿列表 ===")
    for i, draft in enumerate(draft_files, 1):
        print(f"{i}. {draft}")
    
    try:
        selection = int(input("\n请选择要发布的草稿编号: ")) - 1
        if selection < 0 or selection >= len(draft_files):
            print("无效的选择！")
            return
        
        selected_draft = draft_files[selection]
        draft_path = os.path.join(drafts_dir, selected_draft)
        
        # 使用 hexo publish 命令发布草稿
        result = os.system(f'hexo publish "{selected_draft}"')
        
        if result == 0:
            print(f"草稿 '{selected_draft}' 已成功发布！")
        else:
            print("发布失败，请检查 Hexo 环境")
            
    except ValueError:
        print("请输入有效的数字！")

def newcontent():
    global openFile
    newtype = int(input("Hexo 快捷文章工具\n1. Markdown 文章\n2. 即刻说说\n3. 发布草稿\n请输入类型："))

    if newtype == 1:
        print("")

        mdtypes = []

        for filename in os.listdir("scaffolds"):
            mdtypes.append(filename.split(".md")[0])
        mdtypes.remove("page")
        print("新建 Markdown 文章")

        for ind, mdtype in enumerate(mdtypes):
            print(ind+1,". ",mdtype, sep="")
        sel_mdtype = int(input("请输入文章类型: ")) - 1
        
        if sel_mdtype < 0 or sel_mdtype >= len(mdtypes):
            print("无效的文章类型！")
            newcontent()
            return
        
        selected_type = mdtypes[sel_mdtype]
        
        # 获取文章信息
        file_title = input("请输入文件名: ")
        article_title = input("请输入文章标题: ")
        
        # 逐项输入标签
        print("\n=== 输入标签 ===")
        tags = get_multiple_inputs("请输入标签（每行一个标签，直接回车结束）：")
        
        # 逐项输入分类
        print("\n=== 输入分类 ===")
        categories = get_multiple_inputs("请输入分类（每行一个分类，直接回车结束）：")
        
        cover = input("\n请输入封面图片链接（可选）: ")
        
        # 使用 hexo 命令创建文章
        print(f"正在创建 {selected_type} 类型的文章: {file_title}")
        result = os.system(f'hexo new {selected_type} "{file_title}"')
        
        if result != 0:
            print("创建文章失败，请检查 Hexo 环境是否正确配置")
            return
        
        # 根据文章类型确定目录
        if selected_type == "draft":
            target_dir = "source\_drafts"
        else:
            target_dir = "source\_posts"
            
        # 确保目录存在
        if not os.path.exists(target_dir):
            print(f"错误: 目录 {target_dir} 不存在")
            return
        
        # 查找并更新生成的 markdown 文件
        found = False
        for filename in os.listdir(target_dir):
            # 检查文件名是否包含文件标题
            if file_title in filename and filename.endswith(".md"):
                filepath = os.path.join(target_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新 Front-matter
                # 更新 title
                content = re.sub(r'title:.*\n', f'title: {article_title}\n', content)
                
                # 更新 tags
                if tags:
                    tags_yaml = 'tags:\n' + '\n'.join([f'    - {tag}' for tag in tags]) + '\n'
                    if 'tags:' in content:
                        content = re.sub(r'tags:.*\n(    - .*\n)*', tags_yaml, content)
                    else:
                        # 在 categories 前插入 tags
                        content = re.sub(r'categories:', tags_yaml + 'categories:', content)
                
                # 更新 categories
                if categories:
                    categories_yaml = 'categories:\n' + '\n'.join([f'    - {cat}' for cat in categories]) + '\n'
                    if 'categories:' in content:
                        content = re.sub(r'categories:.*\n(    - .*\n)*', categories_yaml, content)
                    else:
                        # 在 date 后插入 categories
                        content = re.sub(r'(date: .*\n)', r'\1' + categories_yaml, content)
                
                # 更新 cover
                if cover:
                    if 'cover:' in content:
                        content = re.sub(r'cover:.*\n', f'cover: {cover}\n', content)
                    else:
                        # 在 categories 后插入 cover
                        if categories:
                            content = re.sub(r'(categories:.*\n(    - .*\n)*)', r'\1cover: ' + cover + '\n', content)
                        elif tags:
                            content = re.sub(r'(tags:.*\n(    - .*\n)*)', r'\1cover: ' + cover + '\n', content)
                        else:
                            content = re.sub(r'(date: .*\n)', r'\1cover: ' + cover + '\n', content)
                
                # 写入更新后的内容
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"文章已创建并更新：{filepath}")
                print(filepath)
                openFile = filepath
                found = True
                break
        
        if not found:
            print(f"在 {target_dir} 目录中未找到包含 '{file_title}' 的 Markdown 文件")
            print("请检查文件是否成功创建")
            
    elif newtype == 2:
        print("\n新建即刻说说")
        
        # 获取说说内容（允许包含 Markdown 符号）
        content = input("请输入说说内容（可包含**加粗**、*斜体*等 Markdown 符号）: ")
        
        # 获取当前时间（格式：yyyy-MM-dd HH:mm）
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 构建说说数据结构
        brevity_entry = {"content": content, "date": current_time}
        
        # 询问其他可选字段 - 多选
        print("\n可选媒体类型（可多选，用逗号分隔）：")
        print("1. 图片")
        print("2. 音乐")
        print("3. B 站视频")
        print("4. 外链视频")
        print("5. 链接")
        print("6. 地点")
        
        media_selections = input("请选择媒体类型（例如: 1,3,6）: ").strip()
        
        # 处理多选
        selected_types = [s.strip() for s in media_selections.split(',') if s.strip()]
        
        for media_type in selected_types:
            if media_type == "1":  # 图片
                images = []
                has_alt = input("是否添加图片描述？(y/N): ").lower() == 'y'
                
                while True:
                    img_url = input("请输入图片链接（直接回车结束添加）: ")
                    if not img_url:
                        break
                    
                    if has_alt:
                        alt_text = input("请输入图片描述: ")
                        if alt_text:
                            images.append({"url": img_url, "alt": alt_text})
                        else:
                            images.append(img_url)
                    else:
                        images.append(img_url)
                
                if images:
                    brevity_entry["image"] = images
                    
            elif media_type == "2":  # 音乐
                server = input("音乐服务商 (netease / qq / xiami / kugou / baidu): ")
                music_id = input("单曲 ID: ")
                brevity_entry["aplayer"] = {"server": server, "id": music_id}
                
            elif media_type == "3":  # B站视频
                bvid = input("请输入 B 站视频 BV 号: ")
                if "video" not in brevity_entry:
                    brevity_entry["video"] = {}
                brevity_entry["video"]["bilibili"] = bvid
                
            elif media_type == "4":  # 外链视频
                video_url = input("请输入视频直链: ")
                if "video" not in brevity_entry:
                    brevity_entry["video"] = {}
                brevity_entry["video"]["player"] = video_url
                
            elif media_type == "5":  # 链接
                link_url = input("请输入链接: ")
                brevity_entry["link"] = link_url
                
            elif media_type == "6":  # 地点
                location = input("请输入发布地点: ")
                brevity_entry["location"] = location
                
            else:
                print(f"未知的媒体类型: {media_type}")
        
        # 更新 brevity.yml 文件
        brevity_file = "source/_data/brevity.yml"
        
        # 确保目录存在
        os.makedirs(os.path.dirname(brevity_file), exist_ok=True)
        
        # 读取现有内容
        existing_content = []
        if os.path.exists(brevity_file):
            with open(brevity_file, 'r', encoding='utf-8') as f:
                existing_content = f.readlines()
        
        # 将新条目转换为 YAML 格式
        new_lines = ["- "]
        
        # 按特定顺序构建 YAML
        fields_order = ["content", "date", "video", "aplayer", "image", "link", "location"]
        
        for field in fields_order:
            if field in brevity_entry:
                value = brevity_entry[field]
                if field == "content":
                    new_lines.append(f"{field}: {value}\n")
                elif field == "date":
                    new_lines.append(f"  {field}: {value}\n")
                elif field == "video":
                    new_lines.append(f"  {field}:\n")
                    for sub_key, sub_value in value.items():
                        new_lines.append(f"    {sub_key}: {sub_value}\n")
                elif field == "aplayer":
                    new_lines.append(f"  {field}:\n")
                    for sub_key, sub_value in value.items():
                        new_lines.append(f"    {sub_key}: {sub_value}\n")
                elif field == "image":
                    new_lines.append(f"  {field}:\n")
                    for item in value:
                        if isinstance(item, dict):
                            new_lines.append("    - ")
                            first = True
                            for sub_key, sub_value in item.items():
                                if first:
                                    new_lines.append(f"{sub_key}: {sub_value}\n")
                                    first = False
                                else:
                                    new_lines.append("      " + f"{sub_key}: {sub_value}\n")
                        else:
                            new_lines.append(f"    - {item}\n")
                elif field in ["link", "location"]:
                    new_lines.append(f"  {field}: {value}\n")
        
        # 写入文件（追加模式）
        with open(brevity_file, 'a', encoding='utf-8') as f:
            # 如果文件不为空且最后一行不是空行，先添加一个空行
            if existing_content and not existing_content[-1].strip() == '':
                f.write('\n')
            f.writelines(new_lines)
        
        print("即刻说说已添加到 brevity.yml！")
        openFile = brevity_file
    
    elif newtype == 3:
        # 发布草稿
        publish_draft()
            
    else:
        print("无效的选择，请重新输入！")
        newcontent()

newcontent()

_ = input("\n按 Enter 键结束...")
os.system(openFile)