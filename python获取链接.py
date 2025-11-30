import requests
# 仓库信息（替换成你的）
owner = "qyxay"
repo = "m4a"
branch = "main"
# GitHub API获取文件列表
url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
response = requests.get(url, verify=False)
data = response.json()
# 筛选.m4a文件并生成播放链接
m4a_links = []
for item in data["tree"]:
    if item["path"].endswith(".m4a"):
        raw_url = f"https://github.com/{owner}/{repo}/raw/{branch}/{item['path']}"
        m4a_links.append(raw_url)
# 保存到文件
with open("m4a_播放链接.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(m4a_links))
# 打印结果
print(f"✅ 成功生成 {len(m4a_links)} 个音频文件的播放链接")
print(f"📁 链接已保存到：C:\\Users\\未来可期\\Desktop\\音频\\m4a_播放链接.txt")