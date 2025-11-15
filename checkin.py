import requests
import json
import os
from datetime import datetime

# 从环境变量读取 Token（安全做法）
TOKEN = os.environ.get('CHECKIN_TOKEN')

if not TOKEN:
    print("❌ 错误：未找到 CHECKIN_TOKEN 环境变量")
    exit(1)

BASE_URL = "https://prod.unicorn.org.cn/cephalon/user-center/v1"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
    'Authorization': TOKEN,
    'Origin': 'https://cephalon.cloud',
    'Referer': 'https://cephalon.cloud/'
}

def log(msg, level="INFO"):
    """打印日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"[{timestamp}] {symbols.get(level, '')} {msg}")

def checkin():
    """执行签到"""
    log("开始签到...")

    try:
        response = requests.post(
            f"{BASE_URL}/signs/today",
            headers=HEADERS,
            data="{}",
            timeout=30
        )

        log(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            code = result.get("code")
            msg = result.get("msg", "")

            if code == 20000:
                log(f"🎉 签到成功！{msg}", "SUCCESS")
                return True, "签到成功"
            elif code == 20002:
                log(f"✅ 今天已签到：{msg}", "WARNING")
                return True, "今天已签到"
            else:
                log(f"未知状态 (code: {code}): {msg}", "WARNING")
                return False, f"未知状态: {msg}"
        else:
            log(f"请求失败: HTTP {response.status_code}", "ERROR")
            return False, f"HTTP {response.status_code}"

    except Exception as e:
        log(f"签到异常: {e}", "ERROR")
        return False, str(e)

def get_sign_info():
    """获取签到信息"""
    log("获取签到信息...")

    try:
        response = requests.get(f"{BASE_URL}/signs", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                latest = data['data'][-1]
                days = latest.get('continuous_days', 0)
                log(f"连续签到: {days} 天", "SUCCESS")
                return days
        return 0
    except Exception as e:
        log(f"获取信息失败: {e}", "WARNING")
        return 0

def main():
    print("=" * 60)
    print("🚀 Cephalon 自动签到 (GitHub Actions)")
    print("=" * 60)
    print()

    # 执行签到
    success, message = checkin()

    print()

    # 获取签到信息
    days = get_sign_info()

    print()
    print("=" * 60)
    print(f"📊 运行结果: {'成功' if success else '失败'}")
    print(f"📝 消息: {message}")
    print(f"📅 连续签到: {days} 天")
    print("=" * 60)

    # 如果签到失败，返回非零退出码（GitHub Actions 会标记为失败）
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
