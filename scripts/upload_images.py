#!/usr/bin/env python3
"""
上传本地图片到微信服务器，并替换 Markdown 中的图片路径
"""

import argparse
import json
import re
import requests
from pathlib import Path

WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
WECHAT_UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"

def get_wechat_token(app_id, app_secret):
    """获取微信公众号 access token"""
    resp = requests.get(
        WECHAT_TOKEN_URL,
        params={"grant_type": "client_credential", "appid": app_id, "secret": app_secret},
        timeout=30
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        raise Exception(f"获取 token 失败：{data}")
    return data["access_token"]

def upload_image(token, image_path):
    """上传图片到微信服务器"""
    with open(image_path, "rb") as f:
        files = {"media": (image_path.name, f, "image/jpeg")}
        resp = requests.post(
            WECHAT_UPLOAD_URL,
            params={"access_token": token, "type": "image"},
            files=files,
            timeout=60
        )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        raise Exception(f"上传图片失败：{data}")
    return data["url"]  # 微信返回的是图片 URL

def process_markdown(md_path, config_path, output_path=None):
    """处理 Markdown 文件，上传图片并替换路径"""
    # 加载配置
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    wechat_config = config.get("wechat", {})
    app_id = wechat_config.get("app_id")
    app_secret = wechat_config.get("app_secret")
    
    if not app_id or not app_secret:
        raise Exception("未配置微信公众号 credentials")
    
    # 获取 token
    print("🔑 获取微信公众号 token...")
    token = get_wechat_token(app_id, app_secret)
    
    # 读取 Markdown
    md_text = Path(md_path).read_text(encoding="utf-8")
    md_dir = Path(md_path).parent
    
    # 查找所有图片
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, md_text)
    
    if not matches:
        print("✅ 未发现图片")
        return md_text
    
    print(f"📸 发现 {len(matches)} 张图片")
    
    # 上传每张图片
    uploaded_images = {}
    for alt, src in matches:
        if src.startswith("http"):
            print(f"  ⏭️  跳过网络图片：{src}")
            continue
        
        # 解析本地路径
        img_path = md_dir / src
        if not img_path.exists():
            print(f"  ⚠️  图片不存在：{img_path}")
            continue
        
        print(f"  📤 上传：{img_path.name}")
        try:
            img_url = upload_image(token, img_path)
            uploaded_images[src] = img_url
            print(f"     ✅ {img_url}")
        except Exception as e:
            print(f"     ❌ 失败：{e}")
    
    # 替换 Markdown 中的图片路径
    def replace_image(match):
        alt = match.group(1)
        src = match.group(2)
        if src in uploaded_images:
            return f"![{alt}]({uploaded_images[src]})"
        return match.group(0)
    
    new_md_text = re.sub(image_pattern, replace_image, md_text)
    
    # 保存结果
    if output_path:
        Path(output_path).write_text(new_md_text, encoding="utf-8")
        print(f"\n✅ 已保存：{output_path}")
    
    return new_md_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="上传 Markdown 图片到微信服务器")
    parser.add_argument("md_file", help="Markdown 文件路径")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--output", help="输出文件路径（默认覆盖原文件）")
    
    args = parser.parse_args()
    
    output_path = args.output or args.md_file
    process_markdown(args.md_file, args.config, output_path)
