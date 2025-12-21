import requests
import os
import json

# 读取环境变量
cookie = os.environ.get("IKUUU_COOKIE")

def checkin():
    if not cookie:
        print("❌ 错误: 未检测到 IKUUU_COOKIE 环境变量")
        exit(1)

    url = "https://ikuuu.de/user/checkin"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://ikuuu.de/user",
        "Origin": "https://ikuuu.de",
        "Cookie": cookie,
        "Content-Type": "application/json;charset=UTF-8"
    }

    try:
        response = requests.post(url, headers=headers)
        try:
            res_json = response.json()
            print(f"📡 状态码: {response.status_code}")
            print(f"📝 返回信息: {res_json}")
            
            if res_json.get('ret') == 1:
                 print("✅ 签到成功！")
            else:
                 print(f"⚠️ 提示: {res_json.get('msg')}")
                 
        except json.JSONDecodeError:
            print(f"⚠️ 响应非 JSON: {response.text}")

    except Exception as e:
        print(f"❌ 请求错误: {e}")

if __name__ == "__main__":
    checkin()
