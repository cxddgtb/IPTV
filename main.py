import urllib.request
from urllib.parse import urlparse
import re
import os
from datetime import datetime, timedelta, timezone
import time
import opencc  # 简繁转换
import socket  # 用于测速

# 执行开始时间
timestart = datetime.now()

# 读取文本方法
def read_txt_to_array(file_name):
    """读取文本文件到数组"""
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"文件未找到: '{file_name}'")
        return []
    except Exception as e:
        print(f"读取文件出错: {e}")
        return []

# 定义多个对象用于存储不同内容的行文本
# 主频道
ys_lines = []  # 央视频道
ws_lines = []  # 卫视频道
ty_lines = []  # 体育频道
dy_lines = []  # 电影频道
dsj_lines = []  # 电视剧频道
gat_lines = []  # 港澳台
gj_lines = []  # 国际台
jlp_lines = []  # 记录片
xq_lines = []  # 戏曲
js_lines = []  # 解说
newtv_lines = []  # NewTV
ihot_lines = []  # iHot
et_lines = []  # 儿童
zy_lines = []  # 综艺频道
mdd_lines = []  # 埋堆堆
yy_lines = []  # 音乐频道
game_lines = []  # 游戏频道
radio_lines = []  # 收音机频道
zb_lines = []  # 直播中国
cw_lines = []  # 春晚
mtv_lines = []  # MTV
migu_lines = []  # 咪咕直播
other_lines = []  # 其他频道（新增）

# 新增国际频道分类
jp_lines = []  # 日本频道 [citation:4]
kr_lines = []  # 韩国频道 [citation:9]
us_lines = []  # 美国频道 [citation:7]
fr_lines = []  # 法国频道 [citation:6]
uk_lines = []  # 英国频道
de_lines = []  # 德国频道
ru_lines = []  # 俄罗斯频道
ca_lines = []  # 加拿大频道
au_lines = []  # 澳大利亚频道
in_lines = []  # 印度频道
ph_lines = []  # 菲律宾频道
sg_lines = []  # 新加坡频道
my_lines = []  # 马来西亚频道
th_lines = []  # 泰国频道
vn_lines = []  # 越南频道

# 地方台
sh_lines = []  # 地方台-上海频道
zj_lines = []  # 地方台-浙江频道
jsu_lines = []  # 地方台-江苏频道
gd_lines = []  # 地方台-广东频道
hn_lines = []  # 地方台-湖南频道
ah_lines = []  # 地方台-安徽频道
hain_lines = []  # 地方台-海南频道
nm_lines = []  # 地方台-内蒙频道
hb_lines = []  # 地方台-湖北频道
ln_lines = []  # 地方台-辽宁频道
sx_lines = []  # 地方台-陕西频道
shanxi_lines = []  # 地方台-山西频道
shandong_lines = []  # 地方台-山东频道
yunnan_lines = []  # 地方台-云南频道
bj_lines = []  # 地方台-北京频道
cq_lines = []  # 地方台-重庆频道
fj_lines = []  # 地方台-福建频道
gs_lines = []  # 地方台-甘肃频道
gx_lines = []  # 地方台-广西频道
gz_lines = []  # 地方台-贵州频道
heb_lines = []  # 地方台-河北频道
hen_lines = []  # 地方台-河南频道
hlj_lines = []  # 地方台-黑龙江频道
jl_lines = []  # 地方台-吉林频道
jx_lines = []  # 地方台-江西频道
nx_lines = []  # 地方台-宁夏频道
qh_lines = []  # 地方台-青海频道
sc_lines = []  # 地方台-四川频道
tj_lines = []  # 地方台-天津频道
xj_lines = []  # 地方台-新疆频道

# 读取频道字典
# 主频道
ys_dictionary = read_txt_to_array('主频道/央视频道.txt')
ws_dictionary = read_txt_to_array('主频道/卫视频道.txt')
ty_dictionary = read_txt_to_array('主频道/体育频道.txt')
dy_dictionary = read_txt_to_array('主频道/电影.txt')
dsj_dictionary = read_txt_to_array('主频道/电视剧.txt')
gat_dictionary = read_txt_to_array('主频道/港澳台.txt')
gj_dictionary = read_txt_to_array('主频道/国际台.txt')
jlp_dictionary = read_txt_to_array('主频道/纪录片.txt')
xq_dictionary = read_txt_to_array('主频道/戏曲频道.txt')
js_dictionary = read_txt_to_array('主频道/解说频道.txt')
cw_dictionary = read_txt_to_array('主频道/春晚.txt')
newtv_dictionary = read_txt_to_array('主频道/NewTV.txt')
ihot_dictionary = read_txt_to_array('主频道/iHOT.txt')
et_dictionary = read_txt_to_array('主频道/儿童频道.txt')
zy_dictionary = read_txt_to_array('主频道/综艺频道.txt')
mdd_dictionary = read_txt_to_array('主频道/埋堆堆.txt')
yy_dictionary = read_txt_to_array('主频道/音乐频道.txt')
game_dictionary = read_txt_to_array('主频道/游戏频道.txt')
radio_dictionary = read_txt_to_array('主频道/收音机频道.txt')
zb_dictionary = read_txt_to_array('主频道/直播中国.txt')
mtv_dictionary = read_txt_to_array('主频道/MTV.txt')
migu_dictionary = read_txt_to_array('主频道/咪咕直播.txt')

# 新增国际频道字典 [citation:1][citation:3][citation:4]
jp_dictionary = read_txt_to_array('主频道/日本频道.txt')  # NHK, 富士电视台, 东京电视台等 [citation:4]
kr_dictionary = read_txt_to_array('主频道/韩国频道.txt')  # KBS, MBC, SBS等 [citation:9]
us_dictionary = read_txt_to_array('主频道/美国频道.txt')  # NBC, CBS, ABC, Fox, CNN, HBO等 [citation:7]
fr_dictionary = read_txt_to_array('主频道/法国频道.txt')  # TF1, France 2, M6等 [citation:6]
uk_dictionary = read_txt_to_array('主频道/英国频道.txt')  # BBC, Sky News, ITV等
de_dictionary = read_txt_to_array('主频道/德国频道.txt')  # ARD, ZDF, RTL等
ru_dictionary = read_txt_to_array('主频道/俄罗斯频道.txt')  # 第一频道, 俄罗斯24, NTV等
ca_dictionary = read_txt_to_array('主频道/加拿大频道.txt')  # CBC, CTV, Global等
au_dictionary = read_txt_to_array('主频道/澳大利亚频道.txt')  # ABC, SBS, Seven Network等
in_dictionary = read_txt_to_array('主频道/印度频道.txt')  # DD National, Star Plus, Zee TV等
ph_dictionary = read_txt_to_array('主频道/菲律宾频道.txt')  # ABS-CBN, GMA, TV5等
sg_dictionary = read_txt_to_array('主频道/新加坡频道.txt')  # Channel 5, Channel 8, CNA等
my_dictionary = read_txt_to_array('主频道/马来西亚频道.txt')  # TV3, Astro Awani, Bernama TV等
th_dictionary = read_txt_to_array('主频道/泰国频道.txt')  # Channel 7, Thai PBS, PPTV等
vn_dictionary = read_txt_to_array('主频道/越南频道.txt')  # VTV1, VTV3, HTV等

# 地方台
sh_dictionary = read_txt_to_array('地方台/上海频道.txt')
zj_dictionary = read_txt_to_array('地方台/浙江频道.txt')
jsu_dictionary = read_txt_to_array('地方台/江苏频道.txt')
gd_dictionary = read_txt_to_array('地方台/广东频道.txt')
hn_dictionary = read_txt_to_array('地方台/湖南频道.txt')
ah_dictionary = read_txt_to_array('地方台/安徽频道.txt')
hain_dictionary = read_txt_to_array('地方台/海南频道.txt')
nm_dictionary = read_txt_to_array('地方台/内蒙频道.txt')
hb_dictionary = read_txt_to_array('地方台/湖北频道.txt')
ln_dictionary = read_txt_to_array('地方台/辽宁频道.txt')
sx_dictionary = read_txt_to_array('地方台/陕西频道.txt')
shanxi_dictionary = read_txt_to_array('地方台/山西频道.txt')
shandong_dictionary = read_txt_to_array('地方台/山东频道.txt')
yunnan_dictionary = read_txt_to_array('地方台/云南频道.txt')
bj_dictionary = read_txt_to_array('地方台/北京频道.txt')
cq_dictionary = read_txt_to_array('地方台/重庆频道.txt')
fj_dictionary = read_txt_to_array('地方台/福建频道.txt')
gs_dictionary = read_txt_to_array('地方台/甘肃频道.txt')
gx_dictionary = read_txt_to_array('地方台/广西频道.txt')
gz_dictionary = read_txt_to_array('地方台/贵州频道.txt')
heb_dictionary = read_txt_to_array('地方台/河北频道.txt')
hen_dictionary = read_txt_to_array('地方台/河南频道.txt')
hlj_dictionary = read_txt_to_array('地方台/黑龙江频道.txt')
jl_dictionary = read_txt_to_array('地方台/吉林频道.txt')
jx_dictionary = read_txt_to_array('地方台/江西频道.txt')
nx_dictionary = read_txt_to_array('地方台/宁夏频道.txt')
qh_dictionary = read_txt_to_array('地方台/青海频道.txt')
sc_dictionary = read_txt_to_array('地方台/四川频道.txt')
tj_dictionary = read_txt_to_array('地方台/天津频道.txt')
xj_dictionary = read_txt_to_array('地方台/新疆频道.txt')

# 自定义源
urls = read_txt_to_array('assets/urls.txt')

# 简繁转换
def traditional_to_simplified(text: str) -> str:
    """繁体转简体"""
    converter = opencc.OpenCC('t2s')
    return converter.convert(text)

# M3U格式判断
def is_m3u_content(text):
    """判断内容是否为M3U格式"""
    lines = text.splitlines()
    return lines[0].strip().startswith("#EXTM3U") if lines else False

def convert_m3u_to_txt(m3u_content):
    """将M3U内容转换为TXT格式"""
    lines = m3u_content.split('\n')
    txt_lines = []
    channel_name = ""
    
    for line in lines:
        if line.startswith("#EXTM3U"):
            continue
        if line.startswith("#EXTINF"):
            channel_name = line.split(',')[-1].strip()
        elif line.startswith("http") or line.startswith("rtmp") or line.startswith("p3p"):
            txt_lines.append(f"{channel_name},{line.strip()}")
        
        # 处理后缀名为m3u，但是内容为txt的文件
        if "#genre#" not in line and "," in line and "://" in line:
            pattern = r'^[^,]+,[^\s]+://[^\s]+$'
            if re.match(pattern, line):
                txt_lines.append(line)
    
    return '\n'.join(txt_lines)

# URL测速函数（严格测速）
def check_speed(url, timeout=2):
    """检查URL响应速度，返回响应时间(毫秒)或-1（超时）"""
    # 跳过本地地址
    if "127.0.0.1" in url or "localhost" in url:
        return 0
    
    # 解析URL获取主机和端口
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    
    try:
        # 创建socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        start_time = time.time()
        sock.connect((host, port))
        
        # 如果是HTTP/HTTPS，发送HEAD请求
        if parsed.scheme in ['http', 'https']:
            request = f"HEAD {parsed.path or '/'} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
            # 读取部分响应以确保连接正常
            sock.recv(1024)
        
        end_time = time.time()
        sock.close()
        
        return int((end_time - start_time) * 1000)  # 返回毫秒
    except Exception as e:
        return -1  # 超时或连接失败

# 处理带$的URL
def clean_url(url):
    """清理URL中的多余参数"""
    last_dollar_index = url.rfind('$')
    return url[:last_dollar_index] if last_dollar_index != -1 else url

# 清理频道名称
removal_list = ["「IPV4」", "「IPV6」", "[ipv6]", "[ipv4]", "_电信", "电信", "（HD）", "[超清]", "高清", "超清", "-HD", "(HK)", "AKtv", "@", "IPV6", "🎞️", "🎦", " ", "[BD]", "[VGA]", "[HD]", "[SD]", "(1080p)", "(720p)", "(480p)"]
def clean_channel_name(channel_name, removal_list):
    """清理频道名称中的特殊字符"""
    for item in removal_list:
        channel_name = channel_name.replace(item, "")
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
    return channel_name

# 加载频道名称纠错
def load_corrections_name(filename):
    """加载频道名称纠错规则"""
    corrections = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) > 1:
                    correct_name = parts[0]
                    for name in parts[1:]:
                        corrections[name] = correct_name
    except Exception as e:
        print(f"加载纠错文件出错: {e}")
    return corrections

# 应用频道名称纠错
corrections_name = load_corrections_name('assets/corrections_name.txt')
def correct_name_data(name):
    """纠正频道名称"""
    return corrections_name.get(name, name)

# 频道处理函数
def process_channel_line(line):
    """处理单行频道数据"""
    if "#genre#" not in line and "#EXTINF:" not in line and "," in line and "://" in line:
        parts = line.split(',', 1)
        if len(parts) < 2:
            return
        
        channel_name = parts[0]
        channel_address = clean_url(parts[1].strip())
        
        # 跳过空地址
        if not channel_address:
            return
        
        # 测速检查（严格模式）
        response_time = check_speed(channel_address)
        if response_time == -1 or response_time > 2000:  # 超过2秒视为无效
            print(f"源测速失败或超时: {channel_name} ({response_time}ms)")
            return
        
        # 频道名称处理
        channel_name = traditional_to_simplified(channel_name)  # 繁转简
        channel_name = clean_channel_name(channel_name, removal_list)  # 清理特殊字符
        channel_name = correct_name_data(channel_name).strip()  # 应用纠错
        
        # 重新构建行
        line = f"{channel_name},{channel_address}"
        
        # 根据频道名称分发到不同分类
        if channel_name in ys_dictionary:
            ys_lines.append(line)
        elif channel_name in ws_dictionary:
            ws_lines.append(line)
        elif channel_name in ty_dictionary:
            ty_lines.append(line)
        elif channel_name in dy_dictionary:
            dy_lines.append(line)
        elif channel_name in dsj_dictionary:
            dsj_lines.append(line)
        elif channel_name in gat_dictionary:
            gat_lines.append(line)
        elif channel_name in gj_dictionary:
            gj_lines.append(line)
        elif channel_name in jlp_dictionary:
            jlp_lines.append(line)
        elif channel_name in xq_dictionary:
            xq_lines.append(line)
        elif channel_name in js_dictionary:
            js_lines.append(line)
        elif channel_name in newtv_dictionary:
            newtv_lines.append(line)
        elif channel_name in ihot_dictionary:
            ihot_lines.append(line)
        elif channel_name in et_dictionary:
            et_lines.append(line)
        elif channel_name in zy_dictionary:
            zy_lines.append(line)
        elif channel_name in mdd_dictionary:
            mdd_lines.append(line)
        elif channel_name in yy_dictionary:
            yy_lines.append(line)
        elif channel_name in game_dictionary:
            game_lines.append(line)
        elif channel_name in radio_dictionary:
            radio_lines.append(line)
        elif channel_name in zb_dictionary:
            zb_lines.append(line)
        elif channel_name in cw_dictionary:
            cw_lines.append(line)
        elif channel_name in mtv_dictionary:
            mtv_lines.append(line)
        elif channel_name in migu_dictionary:
            migu_lines.append(line)
            
        # 新增国际频道分类 [citation:1][citation:3][citation:4]
        elif channel_name in jp_dictionary:
            jp_lines.append(line)
        elif channel_name in kr_dictionary:
            kr_lines.append(line)
        elif channel_name in us_dictionary:
            us_lines.append(line)
        elif channel_name in fr_dictionary:
            fr_lines.append(line)
        elif channel_name in uk_dictionary:
            uk_lines.append(line)
        elif channel_name in de_dictionary:
            de_lines.append(line)
        elif channel_name in ru_dictionary:
            ru_lines.append(line)
        elif channel_name in ca_dictionary:
            ca_lines.append(line)
        elif channel_name in au_dictionary:
            au_lines.append(line)
        elif channel_name in in_dictionary:
            in_lines.append(line)
        elif channel_name in ph_dictionary:
            ph_lines.append(line)
        elif channel_name in sg_dictionary:
            sg_lines.append(line)
        elif channel_name in my_dictionary:
            my_lines.append(line)
        elif channel_name in th_dictionary:
            th_lines.append(line)
        elif channel_name in vn_dictionary:
            vn_lines.append(line)
            
        # 地方台分类
        elif channel_name in sh_dictionary:
            sh_lines.append(line)
        elif channel_name in zj_dictionary:
            zj_lines.append(line)
        elif channel_name in jsu_dictionary:
            jsu_lines.append(line)
        elif channel_name in gd_dictionary:
            gd_lines.append(line)
        elif channel_name in hn_dictionary:
            hn_lines.append(line)
        elif channel_name in ah_dictionary:
            ah_lines.append(line)
        elif channel_name in hain_dictionary:
            hain_lines.append(line)
        elif channel_name in nm_dictionary:
            nm_lines.append(line)
        elif channel_name in hb_dictionary:
            hb_lines.append(line)
        elif channel_name in ln_dictionary:
            ln_lines.append(line)
        elif channel_name in sx_dictionary:
            sx_lines.append(line)
        elif channel_name in shanxi_dictionary:
            shanxi_lines.append(line)
        elif channel_name in shandong_dictionary:
            shandong_lines.append(line)
        elif channel_name in yunnan_dictionary:
            yunnan_lines.append(line)
        elif channel_name in bj_dictionary:
            bj_lines.append(line)
        elif channel_name in cq_dictionary:
            cq_lines.append(line)
        elif channel_name in fj_dictionary:
            fj_lines.append(line)
        elif channel_name in gs_dictionary:
            gs_lines.append(line)
        elif channel_name in gx_dictionary:
            gx_lines.append(line)
        elif channel_name in gz_dictionary:
            gz_lines.append(line)
        elif channel_name in heb_dictionary:
            heb_lines.append(line)
        elif channel_name in hen_dictionary:
            hen_lines.append(line)
        elif channel_name in hlj_dictionary:
            hlj_lines.append(line)
        elif channel_name in jl_dictionary:
            jl_lines.append(line)
        elif channel_name in jx_dictionary:
            jx_lines.append(line)
        elif channel_name in nx_dictionary:
            nx_lines.append(line)
        elif channel_name in qh_dictionary:
            qh_lines.append(line)
        elif channel_name in sc_dictionary:
            sc_lines.append(line)
        elif channel_name in tj_dictionary:
            tj_lines.append(line)
        elif channel_name in xj_dictionary:
            xj_lines.append(line)
        else:
            # 添加到"其他"分类
            other_lines.append(line)

# 处理URL源
def process_url(url):
    """处理单个URL源"""
    print(f"处理URL源: {url}")
    try:
        # 创建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # 打开URL并读取内容
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            
            # 尝试不同编码
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = data.decode('gbk')
                except UnicodeDecodeError:
                    try:
                        text = data.decode('iso-8859-1')
                    except:
                        print("无法解码内容")
                        return
            
            # 处理M3U格式
            if is_m3u_content(text):
                text = convert_m3u_to_txt(text)
            
            # 处理每行数据
            lines = text.split('\n')
            print(f"发现 {len(lines)} 行数据")
            for line in lines:
                if "#genre#" not in line and "," in line and "://" in line:
                    parts = line.split(',', 1)
                    if len(parts) < 2:
                        continue
                    
                    channel_name, channel_address = parts
                    # 处理多个URL分隔符
                    if '#' in channel_address:
                        url_list = channel_address.split('#')
                        for url_part in url_list:
                            if url_part.strip():
                                new_line = f"{channel_name},{url_part.strip()}"
                                process_channel_line(new_line)
                    else:
                        process_channel_line(line)
    
    except Exception as e:
        print(f"处理URL出错: {e}")

# 数据排序
def sort_data(order, data):
    """按指定顺序排序数据"""
    order_dict = {name: i for i, name in enumerate(order)}
    
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    return sorted(data, key=sort_key)

# 处理所有URL源
for url in urls:
    if url.startswith("http"):
        process_url(url)

# 生成时间戳
utc_time = datetime.now(timezone.utc)
beijing_time = utc_time + timedelta(hours=8)
formatted_time = beijing_time.strftime("%Y%m%d %H:%M")
version = f"{formatted_time},https://gcalic.v.myalicdn.com/gc/wgw05_1/index.m3u8?contentid=2820180516001"

# 构建完整频道列表（只包含有频道的分类）
all_lines = [
    "更新时间,#genre#", version, ''
]

# 按分类添加频道（只添加有频道的分类）
def add_category(category_name, lines_list, dictionary=None):
    """添加分类到最终列表（如果分类中有频道）"""
    if lines_list:
        all_lines.append(f"{category_name},#genre#")
        if dictionary:
            all_lines.extend(sort_data(dictionary, lines_list))
        else:
            all_lines.extend(sorted(lines_list))
        all_lines.append('')

# 添加主频道分类
add_category("央视频道", ys_lines, ys_dictionary)
add_category("卫视频道", ws_lines, ws_dictionary)
add_category("港澳台", gat_lines, gat_dictionary)
add_category("电影频道", dy_lines, dy_dictionary)
add_category("电视剧频道", dsj_lines, dsj_dictionary)
add_category("综艺频道", zy_lines, zy_dictionary)
add_category("NewTV", newtv_lines, newtv_dictionary)
add_category("iHOT", ihot_lines, ihot_dictionary)
add_category("体育频道", ty_lines, ty_dictionary)
add_category("咪咕直播", migu_lines, migu_dictionary)
add_category("埋堆堆", mdd_lines, mdd_dictionary)
add_category("音乐频道", yy_lines)
add_category("游戏频道", game_lines)
add_category("解说频道", js_lines)
add_category("儿童", et_lines, et_dictionary)
add_category("国际台", gj_lines, gj_dictionary)

# 添加国际频道分类 [citation:1][citation:3][citation:4]
add_category("日本频道", jp_lines, jp_dictionary)  # NHK, 富士电视台等 [citation:4]
add_category("韩国频道", kr_lines, kr_dictionary)  # KBS, MBC等 [citation:9]
add_category("美国频道", us_lines, us_dictionary)  # NBC, CBS, ABC等 [citation:7]
add_category("法国频道", fr_lines, fr_dictionary)  # TF1, France 2等 [citation:6]
add_category("英国频道", uk_lines, uk_dictionary)
add_category("德国频道", de_lines, de_dictionary)
add_category("俄罗斯频道", ru_lines, ru_dictionary)
add_category("加拿大频道", ca_lines, ca_dictionary)
add_category("澳大利亚频道", au_lines, au_dictionary)
add_category("印度频道", in_lines, in_dictionary)
add_category("菲律宾频道", ph_lines, ph_dictionary)
add_category("新加坡频道", sg_lines, sg_dictionary)
add_category("马来西亚频道", my_lines, my_dictionary)
add_category("泰国频道", th_lines, th_dictionary)
add_category("越南频道", vn_lines, vn_dictionary)

add_category("纪录片", jlp_lines, jlp_dictionary)
add_category("戏曲频道", xq_lines, xq_dictionary)

# 添加地方台分类
add_category("上海频道", sh_lines, sh_dictionary)
add_category("湖南频道", hn_lines, hn_dictionary)
add_category("湖北频道", hb_lines, hb_dictionary)
add_category("广东频道", gd_lines, gd_dictionary)
add_category("浙江频道", zj_lines, zj_dictionary)
add_category("山东频道", shandong_lines, shandong_dictionary)
add_category("江苏频道", jsu_lines)
add_category("安徽频道", ah_lines)
add_category("海南频道", hain_lines)
add_category("内蒙频道", nm_lines)
add_category("辽宁频道", ln_lines)
add_category("陕西频道", sx_lines)
add_category("山西频道", shanxi_lines)
add_category("云南频道", yunnan_lines)
add_category("北京频道", bj_lines)
add_category("重庆频道", cq_lines)
add_category("福建频道", fj_lines)
add_category("甘肃频道", gs_lines)
add_category("广西频道", gx_lines)
add_category("贵州频道", gz_lines)
add_category("河北频道", heb_lines)
add_category("河南频道", hen_lines)
add_category("黑龙江频道", hlj_lines)
add_category("吉林频道", jl_lines)
add_category("江西频道", jx_lines)
add_category("宁夏频道", nx_lines)
add_category("青海频道", qh_lines)
add_category("四川频道", sc_lines)
add_category("天津频道", tj_lines)
add_category("新疆频道", xj_lines)

add_category("春晚", cw_lines, cw_dictionary)
add_category("直播中国", zb_lines)
add_category("MTV", mtv_lines)
add_category("收音机频道", radio_lines, radio_dictionary)

# 添加其他频道分类（如果有内容）
add_category("其他", other_lines)

# 生成M3U文件
def make_m3u(txt_content, m3u_file):
    """从文本内容生成M3U文件"""
    try:
        output_text = '#EXTM3U x-tvg-url="https://epg.112114.xyz/pp.xml.gz"\n'
        lines = txt_content.strip().split("\n")
        
        group_name = ""
        for line in lines:
            parts = line.split(",")
            if len(parts) == 2 and "#genre#" in line:
                group_name = parts[0]
            elif len(parts) == 2:
                channel_name = parts[0]
                channel_url = parts[1]
                logo_url = f"https://epg.112114.xyz/logo/{channel_name}.png"
                
                output_text += f'#EXTINF:-1 tvg-name="{channel_name}" tvg-logo="{logo_url}" group-title="{group_name}",{channel_name}\n'
                output_text += f"{channel_url}\n"
        
        with open(m3u_file, "w", encoding='utf-8') as file:
            file.write(output_text)
        print(f"M3U文件 '{m3u_file}' 生成成功")
    except Exception as e:
        print(f"生成M3U文件出错: {e}")

# 保存文件
try:
    # 生成TXT文件
    with open("live.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(all_lines))
    print("频道文件已保存: live.txt")
    
    # 生成M3U文件
    make_m3u("\n".join(all_lines), "live.m3u")
    
except Exception as e:
    print(f"保存文件出错: {e}")

# 计算执行时间
timeend = datetime.now()
elapsed_time = timeend - timestart
total_seconds = elapsed_time.total_seconds()
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

# 统计信息
print(f"执行时间: {minutes}分{seconds}秒")
print(f"央视频道: {len(ys_lines)}")
print(f"卫视频道: {len(ws_lines)}")
print(f"港澳台频道: {len(gat_lines)}")
print(f"国际频道: {len(jp_lines)+len(kr_lines)+len(us_lines)+len(fr_lines)}")
print(f"其他频道: {len(other_lines)}")
print(f"总频道数: {len(all_lines)}")
