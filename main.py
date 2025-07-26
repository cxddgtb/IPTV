import urllib.request
from urllib.parse import urlparse
import re
import os
from datetime import datetime, timedelta, timezone
import time
import opencc
import socket

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
jlp_lines = []  # 纪录片
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
other_lines = []  # 其他频道

# ========== 国际频道分类 ========== 
jp_lines = []  # 日本频道
kr_lines = []  # 韩国频道
us_lines = []  # 美国频道
fr_lines = []  # 法国频道
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

# ========== 新增娱乐类型频道分类 ==========
yl_lines = []  # 娱乐综合频道
xp_lines = []  # 小品频道
xs_lines = []  # 相声频道
ak_lines = []  # AKtv频道
sg_english_lines = []  # 新加坡式英语频道

# ========== 频道字典直接内联在代码中 ==========
# 主频道
ys_dictionary = [
    "CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV5", "CCTV5+", "CCTV6", "CCTV7", "CCTV8", "CCTV9", 
    "CCTV10", "CCTV11", "CCTV12", "CCTV13", "CCTV14", "CCTV15", "CCTV16", "CCTV17", "CCTV4K", "CCTV8K",
    "CGTN英语", "CGTN纪录", "CGTN法语", "CGTN俄语", "CGTN西班牙语", "CGTN阿拉伯语"
]

ws_dictionary = [
    "北京卫视", "湖南卫视", "浙江卫视", "东方卫视", "江苏卫视", "天津卫视", "山东卫视", "广东卫视", "深圳卫视", "黑龙江卫视",
    "辽宁卫视", "安徽卫视", "河南卫视", "湖北卫视", "四川卫视", "重庆卫视", "东南卫视", "江西卫视", "广西卫视", "陕西卫视",
    "吉林卫视", "云南卫视", "山西卫视", "甘肃卫视", "海南卫视", "贵州卫视", "内蒙古卫视", "青海卫视", "宁夏卫视", "新疆卫视",
    "西藏卫视", "河北卫视", "厦门卫视", "海峡卫视"
]

ty_dictionary = [
    "CCTV5", "CCTV5+", "广东体育", "五星体育", "北京体育", "劲爆体育", "全纪实", "足球", "篮球", "高尔夫网球",
    "冬奥纪实", "体育赛事", "ESPN", "卫视体育", "NBA TV", "英超", "西甲", "德甲", "法甲", "意甲"
]

dy_dictionary = [
    "CCTV6", "CHC家庭影院", "CHC动作电影", "CHC高清电影", "好莱坞电影", "动作电影", "喜剧电影", "爱情电影", "科幻电影", "恐怖电影",
    "经典电影", "4K电影", "卫视电影", "星空电影", "龙华电影", "美亚电影", "寰宇电影", "天映电影", "华纳电影", "迪士尼电影"
]

dsj_dictionary = [
    "CCTV8", "湖南卫视电视剧", "浙江卫视剧场", "东方卫视剧场", "江苏卫视幸福剧场", "北京卫视品质剧场", "安徽卫视海豚剧场", "山东卫视花漾剧场",
    "天津卫视快乐生活剧场", "江西卫视金牌剧场", "深圳卫视黄金剧场", "广西卫视美丽剧场", "四川卫视合家欢剧场", "重庆卫视雾都剧场", "东南卫视东南剧苑",
    "贵州卫视黄金剧场", "云南卫视浪漫剧场", "河北卫视民生剧场", "湖北卫视长江剧场", "辽宁卫视北方剧场"
]

gat_dictionary = [
    "凤凰卫视", "凤凰资讯", "凤凰中文", "凤凰香港", "凤凰电影", "星空卫视", "澳视澳门", "澳视体育", "澳视高清", "澳视综艺",
    "香港卫视", "香港财经", "香港国际", "香港开电视", "ViuTV", "有线新闻", "有线财经", "有线娱乐", "有线电影", "有线体育",
    "澳门卫视", "澳门资讯", "澳门体育", "澳门综艺", "澳门影视", "澳亚卫视"
]

gj_dictionary = [
    "CNN", "BBC", "NHK", "KBS", "MBC", "SBS", "TVB", "ABC", "NBC", "FOX",
    "HBO", "Discovery", "国家地理", "历史频道", "CNBC", "DW", "France24", "RT", "AlJazeera", "Arirang"
]

jlp_dictionary = [
    "CCTV9", "CGTN纪录", "Discovery", "国家地理", "历史频道", "BBCEarth", "动物星球", "全纪实", "求索纪录", "金鹰纪实",
    "世界地理", "寰宇地理", "爱奇艺纪录片", "优酷纪录片", "腾讯纪录片", "B站纪录片", "央视文化精品", "老故事", "发现之旅", "中学生"
]

xq_dictionary = [
    "CCTV11", "梨园", "七彩戏剧", "欢笑剧场", "央视戏曲", "河南戏曲", "陕西戏曲", "安徽戏曲", "山西戏曲", "河北戏曲",
    "天津戏曲", "北京戏曲", "江苏戏曲", "浙江戏曲", "福建戏曲", "广东戏曲", "四川戏曲", "云南戏曲", "湖南戏曲", "湖北戏曲"
]

js_dictionary = [
    "体育解说", "电竞解说", "足球解说", "篮球解说", "赛车解说", "围棋解说", "象棋解说", "电竞直播", "游戏解说", "赛事分析",
    "电竞分析", "体育评论", "游戏评论", "电竞评论", "体育脱口秀", "游戏脱口秀", "电竞脱口秀", "体育新闻", "游戏新闻", "电竞新闻"
]

cw_dictionary = ["春晚回放", "历年春晚", "春晚集锦", "春晚特别节目", "春晚倒计时", "春晚预告", "春晚花絮", "春晚彩排", "春晚幕后", "春晚采访"]

newtv_dictionary = [
    "NewTV动作电影", "NewTV家庭影院", "NewTV爱情喜剧", "NewTV惊悚悬疑", "NewTV古装剧场", "NewTV军旅剧场", "NewTV乡村剧场", "NewTV都市剧场",
    "NewTV少儿动画", "NewTV精品体育", "NewTV电竞世界", "NewTV明星大片", "NewTV海外剧场", "NewTV韩剧", "NewTV日剧", "NewTV泰剧"
]

ihot_dictionary = [
    "iHot动作", "iHot喜剧", "iHot爱情", "iHot科幻", "iHot恐怖", "iHot战争", "iHot武侠", "iHot警匪", "iHot悬疑", "iHot动漫",
    "iHot综艺", "iHot体育", "iHot音乐", "iHot纪录片", "iHot少儿", "iHot教育", "iHot生活", "iHot时尚", "iHot旅游", "iHot美食"
]

et_dictionary = [
    "CCTV14", "卡酷少儿", "金鹰卡通", "优漫卡通", "嘉佳卡通", "炫动卡通", "哈哈炫动", "宝贝家", "少儿动画", "动漫秀场",
    "卡通剧场", "动漫世界", "少儿剧场", "亲子频道", "教育频道", "宝宝巴士", "贝瓦儿歌", "小小优酷", "小企鹅乐园", "芒果TV少儿"
]

zy_dictionary = [
    "CCTV3", "湖南卫视", "浙江卫视", "东方卫视", "江苏卫视", "北京卫视", "安徽卫视", "山东卫视", "天津卫视", "江西卫视",
    "深圳卫视", "广西卫视", "四川卫视", "重庆卫视", "东南卫视", "贵州卫视", "云南卫视", "河北卫视", "湖北卫视", "辽宁卫视"
]

mdd_dictionary = [
    "埋堆堆粤语", "埋堆堆港剧", "埋堆堆综艺", "埋堆堆电影", "埋堆堆动画", "埋堆堆音乐", "埋堆堆娱乐", "埋堆堆新闻", "埋堆堆体育", "埋堆堆纪录片"
]

yy_dictionary = [
    "CCTV15", "MTV", "ChannelV", "音乐风云榜", "流行音乐", "经典音乐", "摇滚音乐", "爵士音乐", "古典音乐", "民族音乐",
    "K歌频道", "演唱会", "音乐现场", "音乐资讯", "音乐故事", "音乐MV", "音乐排行榜", "音乐电台", "网络音乐", "原创音乐"
]

game_dictionary = [
    "游戏风云", "电竞天堂", "斗鱼游戏", "虎牙游戏", "企鹅电竞", "网易CC", "战旗TV", "火猫TV", "熊猫游戏", "游戏竞技",
    "网游天地", "单机游戏", "手游直播", "主机游戏", "电竞新闻", "游戏攻略", "游戏评测", "游戏资讯", "游戏赛事", "游戏解说"
]

radio_dictionary = [
    "中国之声", "经济之声", "音乐之声", "经典音乐", "台海之声", "神州之声", "大湾区之声", "民族之声", "文艺之声", "老年之声",
    "藏语广播", "阅读之声", "维吾尔语广播", "香港之声", "中国交通广播", "中国乡村之声", "哈萨克语广播", "国家应急广播", "轻松调频", "劲曲调频"
]

zb_dictionary = [
    "直播中国", "中国直播", "现场直播", "直播现场", "实时直播", "直播新闻", "直播体育", "直播娱乐", "直播音乐", "直播游戏",
    "直播旅游", "直播美食", "直播购物", "直播教育", "直播健康", "直播科技", "直播财经", "直播农业", "直播汽车", "直播房产"
]

mtv_dictionary = [
    "MTV中文", "MTV国际", "MTV音乐", "MTV现场", "MTV经典", "MTV流行", "MTV摇滚", "MTV舞曲", "MTV嘻哈", "MTV亚洲",
    "MTV欧美", "MTV日韩", "MTV华语", "MTV排行榜", "MTV演唱会", "MTV颁奖", "MTV幕后", "MTV资讯", "MTV特别节目", "MTV点播"
]

migu_dictionary = [
    "咪咕视频", "咪咕体育", "咪咕影院", "咪咕动漫", "咪咕综艺", "咪咕音乐", "咪咕游戏", "咪咕直播", "咪咕剧场", "咪咕纪实",
    "咪咕少儿", "咪咕健康", "咪咕教育", "咪咕购物", "咪咕汽车", "咪咕旅游", "咪咕美食", "咪咕时尚", "咪咕财经", "咪咕科技"
]

# ========== 国际频道字典 ==========
jp_dictionary = [
    "NHK综合", "NHK教育", "NHKBS1", "NHKBS4K", "NHKBS8K", "日本电视台", "朝日电视台", "TBS电视台", "东京电视台", "富士电视台",
    "WOWOW", "BS朝日", "BS东京", "BS-TBS", "BS富士", "BS日本", "BS11", "东京MX", "大阪电视台", "爱知电视台"
]

kr_dictionary = [
    "KBS1", "KBS2", "KBSWorld", "MBC", "SBS", "EBS", "MBN", "TV朝鲜", "JTBC", "ChannelA",
    "YTN", "Arirang", "KBS드라마", "KBSN스포츠", "MBC드라마", "SBS플러스", "SBS골프", "MBC에브리원", "MBCM", "SBSfunE"
]

us_dictionary = [
    "ABC", "CBS", "NBC", "FOX", "CW", "PBS", "CNN", "FoxNews", "MSNBC", "CNBC",
    "HBO", "Showtime", "Starz", "Cinemax", "AMC", "FX", "USA", "TNT", "TBS", "ESPN"
]

fr_dictionary = [
    "TF1", "France2", "France3", "France4", "France5", "M6", "Arte", "C8", "W9", "TMC",
    "TFX", "NRJ12", "LCP", "BFMTV", "CNews", "FranceInfo", "Gulli", "France24", "TV5Monde", "Canal+"
]

uk_dictionary = [
    "BBC1", "BBC2", "BBC3", "BBC4", "BBCNews", "BBCParliament", "CBBC", "CBeebies", "ITV", "Channel4",
    "Channel5", "SkyNews", "SkySports", "SkyCinema", "SkyAtlantic", "SkyOne", "SkyTwo", "SkyArts", "Discovery", "NationalGeographic"
]

de_dictionary = [
    "DasErste", "ZDF", "RTL", "Sat1", "ProSieben", "VOX", "Kabel1", "RTL2", "SuperRTL", "NTV",
    "Phoenix", "Arte", "3sat", "KiKA", "DisneyChannel", "MTV", "VIVA", "Sport1", "Eurosport", "DW"
]

ru_dictionary = [
    "Первый", "Россия1", "МатчТВ", "НТВ", "Пятый", "РоссияК", "Россия24", "Карусель", "ОТР", "ТВЦентр",
    "РенТВ", "Спас", "СТС", "Домашний", "ТВ3", "Звезда", "Мир", "ТНТ", "МузТВ", "2x2"
]

ca_dictionary = [
    "CBC", "CTV", "Global", "Citytv", "Omni", "TVO", "TFO", "RadioCanada", "TeleQuebec", "CPAC",
    "CBCNews", "CTVNews", "GlobalNews", "WeatherNetwork", "Sportsnet", "TSN", "RDS", "TVA", "Zeste", "CanalD"
]

au_dictionary = [
    "ABC", "SBS", "Seven", "Nine", "Ten", "ABCNews", "SBSNews", "7News", "9News", "10News",
    "ABCKids", "ABCMe", "ABCTVPlus", "SBSFood", "SBSSport", "SBSTurkish", "SBSChinese", "SBSArabic", "SBSItalian", "SBSKorean"
]

in_dictionary = [
    "DDNational", "DDNews", "DDIndia", "DDRetro", "DDUrdu", "DDKisan", "DDChandana", "Sony", "StarPlus", "ZeeTV",
    "Colors", "SunTV", "Vijay", "Asianet", "ETV", "ABPNews", "RepublicTV", "TimesNow", "NDTV", "IndiaTV"
]

ph_dictionary = [
    "ABS-CBN", "GMA", "TV5", "CNNPhilippines", "ANC", "PTV", "IBC", "UNTV", "NET25", "SMNINews",
    "TAP", "CineMo", "A2Z", "GTV", "HeartofAsia", "Hallypop", "IHeartMovies", "PinoyBoxOffice", "SariSari", "Knowledge"
]

sg_dictionary = [
    "Channel5", "Channel8", "ChannelU", "Suria", "Vasantham", "CNA", "Okto", "ChannelNewsAsia", "BBCKnowledge", "BBCLifestyle",
    "FOX", "HBO", "StarWorld", "AXN", "Animax", "Disney", "CartoonNetwork", "Discovery", "NationalGeographic", "History"
]

my_dictionary = [
    "RTM1", "RTM2", "TV3", "NTV7", "8TV", "TV9", "AstroAwani", "BernamaTV", "TVAlhijrah", "TVOkey",
    "TVSukan", "TVIQ", "TVBerita", "TVBual", "TVFilem", "TVHiburan", "TVPendidikan", "TVAgama", "TVKeluarga", "TVAnak"
]

th_dictionary = [
    "Channel7", "Channel3", "Channel5", "Channel8", "Channel9", "NBT", "ThaiPBS", "PPTV", "Workpoint", "GMM25",
    "One31", "AmarinTV", "TNN24", "SpringNews", "VoiceTV", "JKN18", "MONO29", "ThairathTV", "T-Sports", "True4U"
]

vn_dictionary = [
    "VTV1", "VTV2", "VTV3", "VTV4", "VTV5", "VTV6", "VTV7", "VTV8", "VTV9", "HTV1",
    "HTV2", "HTV3", "HTV4", "HTV7", "HTV9", "THVL1", "THVL2", "QPVN", "HanoiTV", "HaiPhongTV"
]

# 地方台
sh_dictionary = [
    "东方卫视", "上海新闻综合", "上海都市", "上海东方影视", "上海娱乐", "上海电视剧", "上海纪实", "上海外语", "上海哈哈炫动", "上海第一财经",
    "上海五星体育", "上海艺术人文", "上海生活时尚", "上海法治天地", "上海七彩戏剧", "上海东方购物", "上海教育", "上海嘉定", "上海松江", "上海浦东"
]

zj_dictionary = [
    "浙江卫视", "浙江钱江都市", "浙江经济生活", "浙江教育科技", "浙江影视娱乐", "浙江民生休闲", "浙江公共新闻", "浙江少儿", "浙江国际", "杭州综合",
    "杭州西湖明珠", "杭州生活", "杭州影视", "杭州少儿", "宁波新闻", "宁波经济", "宁波社会生活", "宁波影视", "宁波少儿", "温州新闻"
]

jsu_dictionary = [
    "江苏卫视", "江苏城市", "江苏综艺", "江苏影视", "江苏公共新闻", "江苏教育", "江苏体育休闲", "江苏国际", "南京新闻", "南京教科",
    "南京娱乐", "南京生活", "南京影视", "南京少儿", "南京十八", "苏州新闻", "苏州社会经济", "苏州文化生活", "苏州电影", "无锡新闻"
]

gd_dictionary = [
    "广东卫视", "珠江台", "广东体育", "广东新闻", "广东公共", "广东经济科教", "广东影视", "广东少儿", "广东国际", "南方卫视",
    "深圳卫视", "深圳都市", "深圳电视剧", "深圳娱乐", "深圳体育健康", "深圳公共", "深圳少儿", "广州综合", "广州新闻", "广州影视"
]

hn_dictionary = [
    "湖南卫视", "湖南经视", "湖南都市", "湖南娱乐", "湖南电视剧", "湖南公共", "湖南国际", "湖南教育", "长沙新闻", "长沙政法",
    "长沙女性", "长沙经贸", "长沙移动", "湘潭新闻", "株洲新闻", "衡阳新闻", "岳阳新闻", "常德新闻", "张家界新闻", "益阳新闻"
]

ah_dictionary = [
    "安徽卫视", "安徽经视", "安徽公共", "安徽影视", "安徽综艺", "安徽农业科教", "安徽国际", "合肥新闻", "合肥生活", "合肥教育",
    "合肥财经", "芜湖新闻", "蚌埠新闻", "淮南新闻", "马鞍山新闻", "淮北新闻", "铜陵新闻", "安庆新闻", "黄山新闻", "阜阳新闻"
]

hain_dictionary = [
    "海南卫视", "海南综合", "海南文旅", "海南公共", "海南影视", "海南少儿", "海口新闻", "海口生活", "海口娱乐", "三亚新闻",
    "三亚生活", "三沙卫视", "琼海新闻", "儋州新闻", "文昌新闻", "万宁新闻", "东方新闻", "五指山新闻", "乐东新闻", "澄迈新闻"
]

nm_dictionary = [
    "内蒙古卫视", "内蒙古蒙语", "内蒙古新闻", "内蒙古经济", "内蒙古影视", "内蒙古少儿", "呼和浩特新闻", "包头新闻", "呼伦贝尔新闻", "兴安盟新闻",
    "通辽新闻", "赤峰新闻", "锡林郭勒新闻", "乌兰察布新闻", "鄂尔多斯新闻", "巴彦淖尔新闻", "乌海新闻", "阿拉善新闻", "满洲里新闻", "二连浩特新闻"
]

hb_dictionary = [
    "湖北卫视", "湖北综合", "湖北经视", "湖北影视", "湖北教育", "湖北生活", "湖北公共", "湖北垄上", "武汉新闻", "武汉电视剧",
    "武汉文体", "武汉外语", "武汉少儿", "武汉教育", "黄石新闻", "十堰新闻", "宜昌新闻", "襄阳新闻", "鄂州新闻", "荆门新闻"
]

ln_dictionary = [
    "辽宁卫视", "辽宁都市", "辽宁影视", "辽宁生活", "辽宁公共", "辽宁教育", "辽宁体育", "辽宁经济", "沈阳新闻", "沈阳公共",
    "沈阳影视", "大连新闻", "大连公共", "大连文体", "大连影视", "鞍山新闻", "抚顺新闻", "本溪新闻", "丹东新闻", "锦州新闻"
]

sx_dictionary = [
    "陕西卫视", "陕西新闻", "陕西都市", "陕西影视", "陕西公共", "陕西体育", "陕西生活", "西安新闻", "西安都市", "西安影视",
    "西安商务", "西安教育", "宝鸡新闻", "咸阳新闻", "渭南新闻", "铜川新闻", "延安新闻", "榆林新闻", "汉中新闻", "安康新闻"
]

shanxi_dictionary = [
    "山西卫视", "山西新闻", "山西经济", "山西影视", "山西公共", "山西少儿", "山西黄河", "太原新闻", "太原文体", "太原影视",
    "太原教育", "大同新闻", "阳泉新闻", "长治新闻", "晋城新闻", "朔州新闻", "晋中新闻", "运城新闻", "忻州新闻", "临汾新闻"
]

shandong_dictionary = [
    "山东卫视", "山东齐鲁", "山东体育", "山东影视", "山东生活", "山东公共", "山东少儿", "山东国际", "济南新闻", "济南都市",
    "济南影视", "济南生活", "青岛新闻", "青岛生活", "青岛影视", "青岛都市", "淄博新闻", "枣庄新闻", "东营新闻", "烟台新闻"
]

yunnan_dictionary = [
    "云南卫视", "云南都市", "云南娱乐", "云南影视", "云南公共", "云南少儿", "云南国际", "昆明新闻", "昆明春城民生", "昆明影视频道",
    "曲靖新闻", "玉溪新闻", "保山新闻", "昭通新闻", "丽江新闻", "普洱新闻", "临沧新闻", "楚雄新闻", "红河新闻", "文山新闻"
]

bj_dictionary = [
    "北京卫视", "北京新闻", "北京财经", "北京影视", "北京科教", "北京生活", "北京文艺", "北京青年", "北京卡酷", "北京纪实",
    "北京冬奥", "北京国际", "BRTV新闻", "BRTV财经", "BRTV影视", "BRTV生活", "BRTV科教", "BRTV文艺", "BRTV青年", "BRTV卡酷"
]

cq_dictionary = [
    "重庆卫视", "重庆新闻", "重庆影视", "重庆文体娱乐", "重庆社会法制", "重庆时尚生活", "重庆公共", "重庆少儿", "重庆国际", "万州新闻",
    "涪陵新闻", "渝中新闻", "大渡口新闻", "江北新闻", "沙坪坝新闻", "九龙坡新闻", "南岸新闻", "北碚新闻", "渝北新闻", "巴南新闻"
]

fj_dictionary = [
    "东南卫视", "福建综合", "福建新闻", "福建电视剧", "福建公共", "福建经济", "福建体育", "福建少儿", "福建国际", "福州新闻",
    "福州生活", "福州少儿", "福州影视", "厦门卫视", "厦门新闻", "厦门生活", "厦门影视", "厦门少儿", "泉州新闻", "莆田新闻"
]

gs_dictionary = [
    "甘肃卫视", "甘肃新闻", "甘肃经济", "甘肃文化影视", "甘肃公共", "甘肃少儿", "兰州新闻", "兰州生活", "兰州综艺", "兰州公共",
    "嘉峪关新闻", "金昌新闻", "白银新闻", "天水新闻", "武威新闻", "张掖新闻", "平凉新闻", "酒泉新闻", "庆阳新闻", "定西新闻"
]

gx_dictionary = [
    "广西卫视", "广西新闻", "广西综艺", "广西影视", "广西公共", "广西国际", "南宁新闻", "南宁都市", "南宁影视", "南宁公共",
    "柳州新闻", "桂林新闻", "梧州新闻", "北海新闻", "防城港新闻", "钦州新闻", "贵港新闻", "玉林新闻", "百色新闻", "贺州新闻"
]

gz_dictionary = [
    "贵州卫视", "贵州新闻", "贵州公共", "贵州影视", "贵州旅游", "贵州科教", "贵阳新闻", "贵阳生活", "贵阳法制", "贵阳旅游",
    "贵阳都市", "遵义新闻", "六盘水新闻", "安顺新闻", "毕节新闻", "铜仁新闻", "黔东南新闻", "黔南新闻", "黔西南新闻", "贵安新闻"
]

heb_dictionary = [
    "河北卫视", "河北经济", "河北影视", "河北都市", "河北公共", "河北少儿", "河北农民", "河北导视", "石家庄新闻", "石家庄娱乐",
    "石家庄影视", "石家庄生活", "唐山新闻", "秦皇岛新闻", "邯郸新闻", "邢台新闻", "保定新闻", "张家口新闻", "承德新闻", "沧州新闻"
]

hen_dictionary = [
    "河南卫视", "河南新闻", "河南民生", "河南电视剧", "河南公共", "河南国际", "河南法制", "河南教育", "郑州新闻", "郑州都市",
    "郑州影视", "郑州教育", "郑州文体", "洛阳新闻", "开封新闻", "安阳新闻", "鹤壁新闻", "新乡新闻", "焦作新闻", "濮阳新闻"
]

hlj_dictionary = [
    "黑龙江卫视", "黑龙江新闻", "黑龙江都市", "黑龙江影视", "黑龙江公共", "黑龙江少儿", "黑龙江导视", "哈尔滨新闻", "哈尔滨生活", "哈尔滨娱乐",
    "哈尔滨影视", "哈尔滨都市", "齐齐哈尔新闻", "牡丹江新闻", "佳木斯新闻", "大庆新闻", "伊春新闻", "鸡西新闻", "鹤岗新闻", "双鸭山新闻"
]

jl_dictionary = [
    "吉林卫视", "吉林新闻", "吉林生活", "吉林影视", "吉林公共", "吉林乡村", "吉林教育", "吉林国际", "长春新闻", "长春都市",
    "长春娱乐", "长春影视", "长春市民", "长春汽车", "吉林市新闻", "四平新闻", "辽源新闻", "通化新闻", "白山新闻", "松原新闻"
]

jx_dictionary = [
    "江西卫视", "江西新闻", "江西都市", "江西影视", "江西公共", "江西经济", "江西少儿", "江西教育", "南昌新闻", "南昌都市",
    "南昌影视", "南昌生活", "景德镇新闻", "萍乡新闻", "九江新闻", "新余新闻", "鹰潭新闻", "赣州新闻", "吉安新闻", "宜春新闻"
]

nx_dictionary = [
    "宁夏卫视", "宁夏公共", "宁夏影视", "宁夏经济", "宁夏少儿", "银川新闻", "银川生活", "银川文体", "石嘴山新闻", "吴忠新闻",
    "固原新闻", "中卫新闻", "灵武新闻", "青铜峡新闻", "永宁新闻", "贺兰新闻", "平罗新闻", "盐池新闻", "同心新闻", "海原新闻"
]

qh_dictionary = [
    "青海卫视", "青海新闻", "青海经济", "青海影视", "青海生活", "青海少儿", "青海安多", "西宁新闻", "西宁生活", "海东新闻",
    "海西新闻", "海南新闻", "海北新闻", "黄南新闻", "果洛新闻", "玉树新闻", "格尔木新闻", "德令哈新闻", "大通新闻", "湟中新闻"
]

sc_dictionary = [
    "四川卫视", "四川新闻", "四川经济", "四川影视", "四川公共", "四川科技", "四川国际", "四川妇女儿童", "成都新闻", "成都经济",
    "成都影视", "成都公共", "成都少儿", "绵阳新闻", "自贡新闻", "攀枝花新闻", "泸州新闻", "德阳新闻", "广元新闻", "遂宁新闻"
]

tj_dictionary = [
    "天津卫视", "天津新闻", "天津文艺", "天津影视", "天津都市", "天津体育", "天津科教", "天津公共", "天津少儿", "天津国际",
    "滨海新闻", "滨海都市", "滨海影视", "滨海生活", "滨海少儿", "武清新闻", "宝坻新闻", "宁河新闻", "静海新闻", "蓟州新闻"
]

xj_dictionary = [
    "新疆卫视", "新疆汉语", "新疆维语", "新疆哈语", "新疆少儿", "新疆经济", "新疆影视", "新疆体育", "乌鲁木齐新闻", "乌鲁木齐维语",
    "乌鲁木齐哈语", "克拉玛依新闻", "吐鲁番新闻", "哈密新闻", "昌吉新闻", "博尔塔拉新闻", "巴音郭楞新闻", "阿克苏新闻", "克孜勒苏新闻", "喀什新闻"
]

# ========== 新增娱乐类型频道字典 ==========
# 娱乐综合频道
yl_dictionary = [
    "湖南娱乐", "东方娱乐", "江苏综艺", "浙江娱乐", "北京文艺", "安徽综艺", "山东综艺", "天津文艺",
    "江西娱乐", "深圳娱乐", "广西综艺", "四川文艺", "重庆时尚", "东南娱乐", "贵州影视", "云南娱乐",
    "河北影视", "湖北综合", "辽宁文艺", "陕西生活", "快乐购", "风尚购物", "好享购物", "家家购物",
    "时尚剧场", "情感剧场", "都市剧场", "欢笑剧场", "魅力音乐", "劲爆体育", "游戏风云", "动漫秀场"
]

# 小品频道
xp_dictionary = [
    "央视小品", "欢乐小品", "喜剧小品", "经典小品", "小品精选", "赵本山小品", "宋小宝小品", "沈腾小品",
    "贾玲小品", "岳云鹏小品", "陈佩斯小品", "朱时茂小品", "潘长江小品", "蔡明小品", "冯巩小品", "黄宏小品",
    "郭冬临小品", "大兵小品", "巩汉林小品", "范伟小品", "东北小品", "天津小品", "北京小品", "海派小品",
    "粤语小品", "相声小品", "晚会小品", "情景喜剧", "搞笑短剧", "幽默集锦"
]

# 相声频道
xs_dictionary = [
    "央视相声", "德云社", "相声大会", "经典相声", "相声精选", "郭德纲相声", "于谦相声", "岳云鹏相声",
    "孙越相声", "郭麒麟相声", "孟鹤堂相声", "周九良相声", "张云雷相声", "杨九郎相声", "烧饼相声", "曹鹤阳相声",
    "张鹤伦相声", "郎鹤炎相声", "高峰相声", "栾云平相声", "谢金相声", "李鹤东相声", "单口相声", "对口相声",
    "群口相声", "天津相声", "北京相声", "东北相声", "海派相声", "相声新势力"
]

# AKtv频道
ak_dictionary = [
    "AKtv综合", "AKtv电影", "AKtv电视剧", "AKtv综艺", "AKtv动漫", "AKtv音乐", "AKtv体育", "AKtv新闻",
    "AKtv财经", "AKtv纪录片", "AKtv娱乐", "AKtv少儿", "AKtv生活", "AKtv时尚", "AKtv旅游", "AKtv美食",
    "AKtv健康", "AKtv教育", "AKtv科技", "AKtv汽车", "AKtv房产", "AKtv游戏", "AKtv文化", "AKtv戏曲",
    "AKtv军事", "AKtv农业", "AKtv国际", "AKtv4K", "AKtv8K", "AKtvVR"
]

# 新加坡式英语频道
sg_english_dictionary = [
    "新加坡英语", "Singlish频道", "新加坡娱乐", "新加坡新闻", "新加坡电影", "新加坡电视剧", "新加坡综艺",
    "新加坡音乐", "新加坡文化", "狮城频道", "新传媒", "Channel 5", "Channel 8", "Channel U", "CNA",
    "Okto", "Suria", "Vasantham", "亚洲新闻台", "新加坡体育", "新加坡财经", "新加坡旅游", "新加坡美食",
    "新加坡教育", "新加坡科技", "新加坡时尚", "新加坡健康", "新加坡生活", "新加坡戏剧", "新加坡卡通"
]

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
            
        # 国际频道分类
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
            
        # ========== 新增娱乐类型分类 ==========
        elif channel_name in yl_dictionary:
            yl_lines.append(line)
        elif channel_name in xp_dictionary:
            xp_lines.append(line)
        elif channel_name in xs_dictionary:
            xs_lines.append(line)
        elif channel_name in ak_dictionary:
            ak_lines.append(line)
        elif channel_name in sg_english_dictionary:
            sg_english_lines.append(line)
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

# 添加国际频道分类
add_category("日本频道", jp_lines, jp_dictionary)
add_category("韩国频道", kr_lines, kr_dictionary)
add_category("美国频道", us_lines, us_dictionary)
add_category("法国频道", fr_lines, fr_dictionary)
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

# ========== 添加新增娱乐类型分类 ==========
add_category("娱乐综合", yl_lines, yl_dictionary)
add_category("小品天地", xp_lines, xp_dictionary)
add_category("相声精选", xs_lines, xs_dictionary)
add_category("AKtv频道", ak_lines, ak_dictionary)
add_category("新加坡英语", sg_english_lines, sg_english_dictionary)

# 添加其他频道分类（如果有内容）
if other_lines:
    other_lines.append("其他,#genre#")
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
print(f"国际频道: {len(jp_lines)+len(kr_lines)+len(us_lines)+len(fr_lines)+len(uk_lines)}")
print(f"地方频道: {len(sh_lines)+len(zj_lines)+len(gd_lines)}")
print(f"娱乐频道: {len(yl_lines)+len(xp_lines)+len(xs_lines)+len(ak_lines)}")
print(f"其他频道: {len(other_lines)}")
print(f"总频道数: {len(all_lines)}")
