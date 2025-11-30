import re
import os

# 1. 定义文件路径（链接文件和 README 路径）
links_file_path = r"C:\Users\未来可期\Desktop\音频\m4a_播放链接.txt"  # 音频链接文件路径（r前缀处理反斜杠）
readme_path = r"C:\Users\未来可期\Desktop\音频\README.md"  # 要生成的 README 路径


# 2. 从文本文件中读取所有音频链接
audio_links = []
try:
    with open(links_file_path, "r", encoding="utf-8") as f:
        # 读取每行，去除空行和换行符
        for line in f.readlines():
            line = line.strip()  # 去除前后空格和换行符
            if line:  # 跳过空行
                audio_links.append(line)
    print(f"成功读取 {len(audio_links)} 个音频链接")
except FileNotFoundError:
    print(f"错误：未找到文件 {links_file_path}，请检查路径是否正确")
    exit()


# 3. 解析每个链接，提取集数、标题（复用之前的逻辑，适配链接格式）
audio_list = []
for link in audio_links:
    # 从链接中提取文件名（如 "002.阴阳行者篇 第1集 ... .m4a"）
    filename = link.split("/")[-1]  # 分割链接，取最后一段（文件名）
    
    # 提取集数（匹配 "第X集" 中的数字，如 "第1集" → 1）
    episode_match = re.search(r"第(\d+)集", filename)
    episode = episode_match.group(1) if episode_match else "未知"  # 无集数标记则显示"未知"
    
    # 提取标题（清洗文件名：去掉序号、扩展名、括号内的冗余信息）
    title = re.sub(r"^\d+\.", "", filename)  # 去掉开头的序号（如 "002."）
    title = re.sub(r"\.m4a$", "", title)     # 去掉结尾的 .m4a 扩展名
    title = re.sub(r"\（.*?\）", "", title)  # 去掉中文括号内的内容（如 "（新专辑上线...）"）
    title = re.sub(r"\(.*?\)", "", title)    # 去掉英文括号内的内容（如果有的话）
    title = title.strip()  # 去除首尾空格
    
    audio_list.append({
        "episode": episode,
        "title": title,
        "link": link
    })


# 4. 按集数排序（确保顺序正确，"未知"集数放最后）
# 先按集数数字排序，无法转数字的（如"未知"）放后面
audio_list.sort(key=lambda x: int(x["episode"]) if x["episode"].isdigit() else float("inf"))


# 5. 生成 Markdown 表格内容
md_table = "\n## 阴阳行者篇 音频列表\n\n"
md_table += "| 集数 | 标题 | 播放链接 |\n"
md_table += "|------|------|----------|\n"
for audio in audio_list:
    md_table += f"| {audio['episode']} | {audio['title']} | [点击播放]({audio['link']}) |\n"


# 6. 写入或更新 README.md
# 读取现有 README 内容（如果存在）
existing_content = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        existing_content = f.read()

# 检查是否已有相同表格，有则替换，无则追加
if "## 阴阳行者篇 音频列表" in existing_content:
    # 用正则替换旧表格（匹配从标题到下一个标题或文件结束的内容）
    new_content = re.sub(
        pattern=r"## 阴阳行者篇 音频列表.*?(?=\n## |$)",  # 匹配表格内容
        repl=md_table.strip(),
        string=existing_content,
        flags=re.DOTALL  # 让 .*? 匹配换行符
    )
else:
    # 追加到现有内容末尾
    new_content = existing_content + md_table

# 写入更新后的内容
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"已成功将 {len(audio_list)} 条音频链接写入 {readme_path}")