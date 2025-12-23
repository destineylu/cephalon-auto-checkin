import requests
import os
import json

# 1. 获取账号密码
email = os.environ.get("IKUUU_EMAIL")
password = os.environ.get("IKUUU_PASSWORD")

if not email or not password:
    print("❌ 错误: 未找到 IKUUU_EMAIL 或 IKUUU_PASSWORD，请在 GitHub Secrets 中配置。")
    exit(1)

# 2. 初始化 Session (这就像打开了一个浏览器窗口，会自动保存 Cookie)
session = requests.Session()

# 模拟真实的浏览器头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://ikuuu.de",
    "Referer": "https://ikuuu.de/auth/login",
    "X-Requested-With": "XMLHttpRequest", # 关键：告诉服务器这是 Ajax 请求
}

def login():
    print("🚀 正在尝试登录...")
    login_url = "https://ikuuu.de/auth/login"
    
    # 构造登录表单数据
    login_data = {
        "email": email,
        "passwd": password,  # 注意：根据抓包分析，字段名是 passwd 而不是 password
        "code": "",          # 2FA 验证码，如果没开启 2FA 则留空
        "remember_me": "week"
    }

    try:
        response = session.post(login_url, headers=headers, data=login_data, timeout=15)
        try:
            res_json = response.json()
            print(f"📝 登录接口返回: {res_json}")
            
            if res_json.get('ret') == 1:
                print("✅ 登录成功！")
                return True
            else:
                print(f"❌ 登录失败: {res_json.get('msg')}")
                return False
        except json.JSONDecodeError:
            print(f"❌ 登录失败，响应非 JSON (可能是 Cloudflare 拦截): {response.text[:100]}...")
            return False

    except Exception as e:
        print(f"❌ 登录请求发生错误: {e}")
        return False

def checkin():
    print("\n🚀 正在尝试签到...")
    checkin_url = "https://ikuuu.de/user/checkin"
    
    # 签到时通常不需要再次发送 Content-Type，Referer 改为用户中心
    checkin_headers = headers.copy()
    checkin_headers["Referer"] = "https://ikuuu.de/user"
    
    try:
        # 使用同一个 session 发送请求，它会自动带上刚才登录获取的 Cookie
        response = session.post(checkin_url, headers=checkin_headers, timeout=15)
        try:
            res_json = response.json()
            print(f"📝 签到接口返回: {res_json}")
            
            if res_json.get('ret') == 1:
                print("✅ 签到成功！")
                print(f"🎉 信息: {res_json.get('msg')}")
            else:
                # ret=0 通常代表已经签到过了，或者其他提示
                print(f"⚠️ 提示: {res_json.get('msg')}")
                
        except json.JSONDecodeError:
            print(f"❌ 签到失败，响应非 JSON: {response.text[:100]}...")

    except Exception as e:
        print(f"❌ 签到请求发生错误: {e}")

if __name__ == "__main__":
    if login():
        checkin()
    else:
        exit(1) # 登录失败则退出并报错
