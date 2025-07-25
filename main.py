import urllib.request
from urllib.parse import urlparse
import re
import os
from datetime import datetime, timedelta, timezone
import random
import time

# 执行开始时间
timestart = datetime.now()

# 读取文本文件到数组
def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"文件未找到: '{file_name}'")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

# 频道分类
ys_lines = []  # 央视频道
ws_lines = []  # 卫视频道
other_lines = []  # 其他频道

# 频道字典（用于分类）
ys_dictionary = read_txt_to_array('主频道/央视频道.txt')
ws_dictionary = read_txt_to_array('主频道/卫视频道.txt')

# 自定义源
urls = read_txt_to_array('assets/urls.txt')

# URL响应时间缓存（避免重复测速）
speed_cache = {}

# 测试URL响应时间
def test_url_speed(url, timeout=2):
    """
    测试URL的响应时间
    :param url: 要测试的URL
    :param timeout: 超时时间（秒）
    :return: 响应时间（毫秒），如果超时或出错返回None
    """
    # 检查缓存
    if url in speed_cache:
        return speed_cache[url]
    
    # 创建请求对象并添加自定义header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers=headers)
        # 打开URL并读取少量数据（只测试连接速度）
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # 只读取1KB数据来测试连接
            _ = response.read(1024)
        end_time = time.time()
        
        # 计算响应时间（毫秒）
        response_time = (end_time - start_time) * 1000
        # 缓存结果
        speed_cache[url] = response_time
        return response_time
    except Exception as e:
        # 出错或超时
        speed_cache[url] = None
        return None

# M3U格式判断
def is_m3u_content(text):
    """检查内容是否为M3U格式"""
    lines = text.splitlines()
    if lines:
        first_line = lines[0].strip()
        return first_line.startswith("#EXTM3U")
    return False

# M3U转TXT格式
def convert_m3u_to_txt(m3u_content):
    """将M3U内容转换为TXT格式"""
    lines = m3u_content.split('\n')
    txt_lines = []
    channel_name = ""
    
    for line in lines:
        if line.startswith("#EXTM3U"):
            continue
        if line.startswith("#EXTINF"):
            # 获取频道名称
            channel_name = line.split(',')[-1].strip()
        elif line.startswith("http") or line.startswith("rtmp") or line.startswith("p3p"):
            # 过滤无效URL
            if "://" in line:
                txt_lines.append(f"{channel_name},{line.strip()}")
        # 处理非标准格式
        if "#genre#" not in line and "," in line and "://" in line:
            pattern = r'^[^,]+,[^\s]+://[^\s]+$'
            if bool(re.match(pattern, line)):
                txt_lines.append(line)
    
    return '\n'.join(txt_lines)

# 清理频道名称
def clean_channel_name(channel_name):
    """清理频道名称中的特殊字符"""
    removal_list = ["「IPV4」", "「IPV6」", "[ipv6]", "[ipv4]", "_电信", "电信", 
                   "（HD）", "[超清]", "高清", "超清", "-HD", "(HK)", "AKtv", "@", 
                   "IPV6", "🎞️", "🎦", " ", "[BD]", "[VGA]", "[HD]", "[SD]", 
                   "(1080p)", "(720p)", "(480p)"]
    
    for item in removal_list:
        channel_name = channel_name.replace(item, "")
    
    # 标准化名称
    replacements = {
        "CCTV-": "CCTV",
        "CCTV0": "CCTV",
        "PLUS": "+",
        "NewTV-": "NewTV",
        "iHOT-": "iHOT",
        "NEW": "New",
        "New_": "New"
    }
    
    for old, new in replacements.items():
        channel_name = channel_name.replace(old, new)
    
    return channel_name.strip()

# 处理频道行
def process_channel_line(line):
    """
    处理频道行，分类到央视、卫视或其他
    并进行严格测速（响应时间<2秒）
    """
    if "#genre#" not in line and "," in line and "://" in line:
        parts = line.split(',', 1)
        if len(parts) < 2:
            return
            
        channel_name = parts[0].strip()
        channel_url = parts[1].strip()
        
        # 清理频道名称
        channel_name = clean_channel_name(channel_name)
        
        # 测试URL响应速度（严格模式）
        response_time = test_url_speed(channel_url)
        
        # 只保留响应时间<2000ms的源
        if response_time is not None and response_time < 2000:
            # 分类处理
            if channel_name in ys_dictionary:
                ys_lines.append(f"{channel_name},{channel_url}")
            elif channel_name in ws_dictionary:
                ws_lines.append(f"{channel_name},{channel_url}")
            else:
                other_lines.append(f"{channel_name},{channel_url}")

# 处理URL源
def process_url(url):
    """处理单个URL源"""
    print(f"处理URL: {url}")
    try:
        # 创建请求对象
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = urllib.request.Request(url, headers=headers)
        
        # 打开URL并读取内容
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            
            # 尝试不同编码解码
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = data.decode('gbk')
                except UnicodeDecodeError:
                    try:
                        text = data.decode('iso-8859-1')
                    except UnicodeDecodeError:
                        print("无法确定合适的编码格式")
                        return
            
            # 处理M3U格式
            if is_m3u_content(text):
                text = convert_m3u_to_txt(text)
            
            # 逐行处理内容
            lines = text.split('\n')
            print(f"找到 {len(lines)} 行内容")
            
            for line in lines:
                # 处理带#的多源格式
                if "#genre#" not in line and "," in line and "://" in line:
                    if "#" not in line:
                        process_channel_line(line)
                    else:
                        parts = line.split(',', 1)
                        if len(parts) < 2:
                            continue
                            
                        channel_name = parts[0]
                        url_part = parts[1]
                        
                        # 分割多个URL
                        url_list = url_part.split('#')
                        for channel_url in url_list:
                            if channel_url.strip():
                                process_channel_line(f"{channel_name},{channel_url}")

    except Exception as e:
        print(f"处理URL时出错: {e}")

# 处理所有URL源
for url in urls:
    if url.startswith("http"):
        process_url(url)

# 生成时间戳
beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
formatted_time = beijing_time.strftime("%Y%m%d %H:%M")
version = f"更新时间,#genre#\n{formatted_time},https://gcalic.v.myalicdn.com/gc/wgw05_1/index.m3u8?contentid=2820180516001"

# 合并所有频道数据
all_lines = [version, '\n',
             "央视频道,#genre#"] + sorted(ys_lines) + ['\n',
             "卫视频道,#genre#"] + sorted(ws_lines) + ['\n',
             "其他频道,#genre#"] + sorted(other_lines)

# 写入文件
output_file = "live.txt"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(str(line) + '\n')
    print(f"频道列表已保存到: {output_file}")
    
    # 统计信息
    print(f"央视频道数: {len(ys_lines)}")
    print(f"卫视频道数: {len(ws_lines)}")
    print(f"其他频道数: {len(other_lines)}")
    print(f"总频道数: {len(ys_lines) + len(ws_lines) + len(other_lines)}")

except Exception as e:
    print(f"保存文件时出错: {e}")

# 执行结束时间
timeend = datetime.now()

# 计算执行时间
elapsed_time = timeend - timestart
total_seconds = elapsed_time.total_seconds()
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

print(f"执行时间: {minutes} 分 {seconds} 秒")
