import json

# 读取txt文件中的URL
with open('30url.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# 读取json文件
with open('30_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 确保txt文件中的URL数量与json文件中的重构数量匹配
assert len(urls) == len(data), "URL数量与重构数量不匹配"

# 将URL添加到每个重构信息中
for i, block in enumerate(data):
    block['URL'] = urls[i]

# 将更新后的数据写回json文件
with open('30_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("URL已成功添加到每个重构信息中")
