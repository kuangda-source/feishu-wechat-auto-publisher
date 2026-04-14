#!/usr/bin/env python3
"""
测试飞书 webhook 通知功能
"""

import requests
import json

# 测试 webhook URL
TEST_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/9e3a92a4-f85f-4b00-bb41-c97a161f3d8c"

def test_webhook():
    """发送测试消息"""
    print("🧪 测试飞书 webhook 通知功能")
    print("=" * 60)
    
    message = {
        "msg_type": "text",
        "content": {
            "text": "📢 推文已保存至草稿箱，请闵老师审核\n\n标题：【测试】飞书文档自动转公众号推文功能测试"
        }
    }
    
    print(f"📤 发送消息到：{TEST_WEBHOOK_URL}")
    print(f"📝 消息内容：\n{json.dumps(message, indent=2, ensure_ascii=False)}")
    
    try:
        resp = requests.post(TEST_WEBHOOK_URL, json=message, timeout=10)
        print(f"\n📡 响应状态码：{resp.status_code}")
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"📋 响应内容：{json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("code") == 0:
                print("\n✅ 测试成功！消息已发送到飞书群")
                return True
            else:
                print(f"\n❌ 测试失败：{result}")
                return False
        else:
            print(f"\n❌ 请求失败：{resp.status_code}")
            print(f"响应内容：{resp.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        return False

if __name__ == "__main__":
    success = test_webhook()
    print("\n" + "=" * 60)
    if success:
        print("✅ webhook 测试通过，可以正式使用")
    else:
        print("❌ webhook 测试失败，请检查配置")
