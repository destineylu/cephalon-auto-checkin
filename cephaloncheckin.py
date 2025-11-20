import requests
import json

# 1. ✅ 更简单的接口地址 (今日签到)
url = "https://prod.unicorn.org.cn/cephalon/user-center/v1/signs/today"

# 2. 你的 Token (记得填入！)
token = "Bearer "

# 3. 请求头
headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
   'Content-Type': 'application/json',
   'Authorization': token,
   'Origin': 'https://cephalon.cloud',
   'Referer': 'https://cephalon.cloud/'
}

# 4. ✅ 数据部分变简单了：只要发一个空括号 {} 就行，不需要 UUID 了
payload = "{}" 

print(f"正在连接: {url}")

try:
    # 发送请求
    response = requests.post(url, headers=headers, data=payload)
    
    print("状态码:", response.status_code)
    print("返回内容:", response.text)
    
    # 判定逻辑
    if response.status_code == 200:
        res_json = response.json()
        if res_json.get("code") == 20000:
            print("✅ 签到成功！")
        elif res_json.get("code") == 20002:
            print("✅ 今天已经签过了 (无需重复)")
        else:
            print(f"⚠️ 未知状态: {res_json.get('msg')}")
    else:
        print("❌ 请求失败")
        
except Exception as e:
    print("❌ 运行出错:", e)

