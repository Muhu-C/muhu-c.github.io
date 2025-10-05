import os
import datetime
import re
import yaml

def get_multiple_inputs(prompt):
    """获取多项输入"""
    print(prompt)
    items = []
    while True:
        item = input(f"第 {len(items)+1} 项: ").strip()
        if not item:
            break
        items.append(item)
    return items

def format_brevity_content(content):
    """格式化即刻essay_type内容：转换换行和加粗"""
    # 将 **text** 转换为 <b>text</b>
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
    # 将换行符转换为 <br />
    content = content.replace('\n', '<br />')
    return content

def update_front_matter(content, updates):
    """更新 Front-matter 内容"""
    lines = content.split('\n')
    in_front_matter = False
    front_matter_end = 0
    
    # 查找 Front-matter 的结束位置
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if in_front_matter:
                front_matter_end = i
                break
            else:
                in_front_matter = True
    
    if front_matter_end == 0:
        return content
    
    # 提取 Front-matter 内容
    front_matter_lines = lines[1:front_matter_end]
    front_matter_content = '\n'.join(front_matter_lines)
    
    # 更新各个字段
    for key, value in updates.items():
        print(key, value)
        if value:
            if key in ['tags', 'categories']:
                # 处理列表类型的字段
                yaml_value = f'{key}:\n' + '\n'.join([f'  - {item}' for item in value]) + '\n'
                if f'{key}:' in front_matter_content:
                    front_matter_content = re.sub(f'{key}:.*\n(  - .*\n)*', yaml_value, front_matter_content)
                else:
                    # 在适当位置插入新字段
                    if key == 'tags' and 'categories:' in front_matter_content:
                        front_matter_content = front_matter_content.replace('categories:', yaml_value + 'categories:')
                    else:
                        front_matter_content = re.sub(r'(date: .*\n)', r'\1' + yaml_value, front_matter_content)
            else:
                # 处理字符串类型的字段
                if key == 'cover':
                    front_matter_content = front_matter_content.replace("\ncover:", f"\ncover: {value}")
                elif f'{key}:' in front_matter_content:
                    front_matter_content = re.sub(f'{key}:.*\n', f'{key}: {value}\n', front_matter_content)
    
    # 重新构建内容
    updated_content = '---\n' + front_matter_content + '\n---' + '\n'.join(lines[front_matter_end+1:])
    return updated_content

def create_markdown_post():
    """创建 Markdown 文章"""
    print("\n新建文章")
    
    # 获取可用的文章类型
    mdtypes = []
    for filename in os.listdir("scaffolds"):
        if filename.endswith(".md"):
            mdtypes.append(filename.split(".md")[0])
    
    # 移除不需要的类型
    mdtypes = [t for t in mdtypes if t not in ['page']]
    
    if not mdtypes:
        print("错误: 未找到任何文章模板")
        return None
    
    # 显示文章类型选项
    for ind, mdtype in enumerate(mdtypes):
        display_name = {
            'draft': '草稿',
            'post': '文章'
        }.get(mdtype, mdtype)
        print(f"{ind+1}. {display_name}")
    
    try:
        sel_mdtype = int(input("请输入文章类型: ")) - 1
        if sel_mdtype < 0 or sel_mdtype >= len(mdtypes):
            print("无效的文章类型！")
            return None
    except ValueError:
        print("请输入有效的数字！")
        return None
    
    selected_type = mdtypes[sel_mdtype]
    
    # 获取文章信息
    file_title = input("请输入文件名: ").strip()
    if not file_title:
        print("文件名不能为空！")
        return None
    
    article_title = input("请输入文章标题: ").strip()
    if not article_title:
        article_title = file_title
    
    # 获取标签和分类
    print("\n=== 输入标签 ===")
    tags = get_multiple_inputs("请输入标签（每行一个标签，直接回车结束）：")
    
    print("\n=== 输入分类 ===")
    categories = get_multiple_inputs("请输入分类（每行一个分类，直接回车结束）：")

    cover = input("\n请输入封面图片链接（直接回车跳过）: ").strip()
    if cover.startswith("[") or cover.startswith("!") or not cover.endswith(".png") or not cover.endswith(".png") or not cover.endswith(".avif") or not cover.endswith(".webp"):
        cover = re.findall("(https://(.*?)(.jpg|.png|.avif|.webp))", cover)[0][0]

    # 使用 hexo 命令创建文章
    print(f"正在创建 {selected_type} 类型的文章: {file_title}")
    result = os.system(f'hexo new {selected_type} "{file_title}"')
    
    if result != 0:
        print("创建文章失败，请检查 Hexo 环境是否正确配置")
        return None
    
    # 根据文章类型确定目录
    target_dir = "source\\_drafts" if selected_type == "draft" else "source\\_posts"
    
    # 确保目录存在
    if not os.path.exists(target_dir):
        print(f"错误: 目录 {target_dir} 不存在")
        return None
    
    # 查找并更新生成的 markdown 文件
    for filename in os.listdir(target_dir):
        if file_title in filename and filename.endswith(".md"):
            filepath = os.path.join(target_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 准备更新内容
                updates = {
                    'title': article_title,
                    'tags': tags,
                    'categories': categories,
                    'cover': cover if cover else None
                }
                
                # 更新 Front-matter
                updated_content = update_front_matter(content, updates)
                
                # 写入更新后的内容
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"文章已创建并更新：{filepath}")
                return filepath
                
            except Exception as e:
                print(f"处理文件时出错: {e}")
                return None
    
    print(f"在 {target_dir} 目录中未找到包含 '{file_title}' 的 Markdown 文件")
    return None

def create_brevity_post():
    """创建即刻essay_type"""
    essay_type = ""
    essay_show = True
    essay_type_input = input("新建即刻说说类型\n  1. 即刻短文\n  2. 即刻公告\n请输入类型（默认为公告）: ")
    if essay_type_input == "1":
        essay_type = "短文"
        essay_show = False
    else:
        if essay_type_input != "2": 
            print("未知的即刻说说类型，将默认以公告配置")
        essay_type = "公告"
        essay_show = True

    print(f"\n新建即刻{essay_type}")
    
    # 获取essay_type内容
    print(f"请输入{essay_type}内容（可包含**加粗**、*斜体*等 Markdown 符号）:")
    content_lines = []
    while True:
        line = input().strip()
        if not line:
            break
        content_lines.append(line)
    
    if not content_lines:
        print(f"{essay_type}内容不能为空！")
        return None
    
    content = '\n'.join(content_lines)
    
    # 格式化内容：转换换行和加粗
    formatted_content = format_brevity_content(content)
    
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 构建essay_type数据结构
    brevity_entry = {
        "content": formatted_content,
        "date": current_time,
        "show_in_home": essay_show
    }
    
    # 询问其他可选字段
    print("\n可选媒体类型（可多选，用逗号分隔）：")
    print("1. 图片")
    print("2. 音乐")
    print("3. B 站视频")
    print("4. 外链视频")
    print("5. 链接")
    print("6. 地点")
    
    media_selections = input("请选择媒体类型（例如: 1,3,6，直接回车跳过）: ").strip()
    
    if media_selections:
        selected_types = [s.strip() for s in media_selections.split(',') if s.strip()]
        
        for media_type in selected_types:
            if media_type == "1":  # 图片
                images = []
                has_alt = input("是否添加图片描述？(y/N): ").lower() == 'y'
                
                while True:
                    img_url = input("请输入图片链接（直接回车结束添加）: ").strip()
                    if not img_url:
                        break
                    
                    if has_alt:
                        alt_text = input("请输入图片描述: ").strip()
                        images.append({"url": img_url, "alt": alt_text})
                    else:
                        images.append(img_url)
                
                if images:
                    brevity_entry["image"] = images
                    
            elif media_type == "2":  # 音乐
                server = input("音乐服务商 (netease/qq/xiami/kugou/baidu): ").strip()
                music_id = input("单曲 ID: ").strip()
                if server and music_id:
                    brevity_entry["aplayer"] = {"server": server, "id": music_id}
                    
            elif media_type == "3":  # B站视频
                bvid = input("请输入 B 站视频 BV 号: ").strip()
                if bvid:
                    if "video" not in brevity_entry:
                        brevity_entry["video"] = {}
                    brevity_entry["video"]["bilibili"] = bvid
                    
            elif media_type == "4":  # 外链视频
                video_url = input("请输入视频直链: ").strip()
                if video_url:
                    if "video" not in brevity_entry:
                        brevity_entry["video"] = {}
                    brevity_entry["video"]["player"] = video_url
                    
            elif media_type == "5":  # 链接
                link_url = input("请输入链接: ").strip()
                if link_url:
                    brevity_entry["link"] = link_url
                    
            elif media_type == "6":  # 地点
                location = input("请输入发布地点: ").strip()
                if location:
                    brevity_entry["location"] = location
                    
            else:
                print(f"未知的媒体类型: {media_type}")
    
    # 更新 brevity.yml 文件
    brevity_file = "source\\_data\\brevity.yml"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(brevity_file), exist_ok=True)
    
    # 读取现有内容
    existing_data = []
    if os.path.exists(brevity_file):
        try:
            with open(brevity_file, 'r', encoding='utf-8') as f:
                existing_data = yaml.safe_load(f) or []
        except Exception as e:
            print(f"读取现有 brevity 数据时出错: {e}")
            existing_data = []
    
    # 添加新条目
    existing_data.append(brevity_entry)
    
    # 写入文件
    try:
        with open(brevity_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_data, f, allow_unicode=True, default_flow_style=False, indent=2)
        print(f"即刻{essay_type}已添加到 brevity.yml！")
        return brevity_file
    except Exception as e:
        print(f"写入 brevity 文件时出错: {e}")
        return None

def publish_draft():
    """发布草稿"""
    drafts_dir = "source/_drafts"

    if not os.path.exists(drafts_dir):
        print("草稿目录不存在！")
        return None
    
    draft_files = [f for f in os.listdir(drafts_dir) if f.endswith('.md')]
    
    if not draft_files:
        print("没有找到草稿文件！")
        return None
    
    print("\n=== 草稿列表 ===")
    for i, draft in enumerate(draft_files, 1):
        print(f"{i}. {draft}")
    
    try:
        selection = int(input("\n请选择要发布的草稿编号: ")) - 1
        if selection < 0 or selection >= len(draft_files):
            print("无效的选择！")
            return None
        
        # 使用 hexo publish 命令发布草稿
        draft_name = draft_files[selection].split(".md")[0]
        result = os.system(f'hexo publish "{draft_name}"')
        
        if result == 0:
            print(f"草稿 '{draft_files[selection]}' 已成功发布！")
            return f"source/_posts/{draft_files[selection]}"
        else:
            print("发布失败，请检查 Hexo 环境")
            return None
            
    except ValueError:
        print("请输入有效的数字！")
        return None

def newcontent():
    """主函数：创建新内容"""
    global openFile
    
    print("Hexo 快捷文章工具")
    print("  1. Markdown 文章")
    print("  2. 即刻说说")
    print("  3. 发布草稿")
    
    try:
        newtype = int(input("请输入类型："))
    except ValueError:
        print("请输入有效的数字！")
        return
    
    if newtype == 1:
        openFile = create_markdown_post()
    elif newtype == 2:
        openFile = create_brevity_post()
    elif newtype == 3:
        openFile = publish_draft()
    else:
        print("无效的选择，请重新输入！")
        newcontent()


if __name__ == "__main__":
    openFile = "NONE"
    
    # 设置控制台编码为 UTF-8
    os.system("chcp 65001 > nul")
    os.system("cls")
    
    newcontent()
    
    _ = input("\n按 Enter 键结束...")
    if openFile and openFile != "NONE" and os.path.exists(openFile):
        os.system(openFile)