import time
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
import eventlet
eventlet.monkey_patch()
now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('[%m/%d %H:%M]Updated.')
urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iTWVpemhvdSI%3D",#梅州
    "https://fofa.info/result?qbase64=Ii9pcHR2L2xpdmUvemhfY24uanMiICYmIGNvdW50cnk9IkNOIiAmJiBvcmc9IkNoaW5hbmV0Ig%3D%3D"#全国
    ##"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJHdWFuZ2Rvbmci",#Guangdong
    ##"https://fofa.info/result?qbase64=ImlwdHYiICYmIGNpdHk9Ill1bGluIiAmJiBwb3J0PSI4MTgxIg%3D%3D"#广西玉林
]
  
def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    #pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+|http://\w+\.\w+\.\w+:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    x_urls.append("http://113.64.92.1:9901")
    x_urls.append("http://113.64.93.1:9901")
    x_urls.append("http://119.125.44.1:9901")
    x_urls.append("http://119.125.128.1:9901")
    x_urls.append("http://119.125.129.1:9901")
    x_urls.append("http://119.125.130.1:9901")
    x_urls.append("http://119.125.131.1:9901")
    x_urls.append("http://119.125.134.1:9901")
    x_urls.append("http://119.125.135.1:9901")
    x_urls.append("http://120.238.84.1:9901")
    x_urls.append("http://183.237.246.1:9931")
    x_urls.append("http://183.239.226.1:9901")
    x_urls.append("http://120.196.171.1:9901")
    x_urls.append("http://59.32.50.1:9901")
    x_urls.append("http://59.32.94.1:9901")
    x_urls.append("http://59.32.95.1:9901")
    x_urls.append("http://59.32.96.1:9901")
    x_urls.append("http://59.32.97.1:9901")
    x_urls.append("http://59.32.98.1:9901")
    x_urls.append("http://59.32.99.1:9901")
    x_urls.append("http://59.32.100.1:9901")
    x_urls.append("http://59.32.101.1:9901")
    x_urls.append("http://59.32.102.1:9901")
    x_urls.append("http://59.32.103.1:9901")
    x_urls.append("http://61.146.188.1:9901")
    urls = set(x_urls)  # 去重得到唯一的URL列表

    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)

    for url in valid_urls:
        print(f'{url} 【 有 效 】')
    # 遍历网址列表，获取JSON文件并解析
    for url in valid_urls:
        try:
            # 发送GET请求获取JSON文件，设置超时时间为0.5秒
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]  # http:// or https://
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"

            json_url = f"{url}"
            response = requests.get(json_url, timeout=0.5)
            json_data = response.json()
            if json_data['count'] == 0:
                print(f'{url} 【 待 测 试 】')
            try:
                # 解析JSON文件，获取name和url字段
                for item in json_data['data']:
                    if isinstance(item, dict):
                        name = item.get('name')
                        urlx = item.get('url')
                        num = item.get('chid')
                        if ',' in urlx:
                            urlx=f"aaaaaaaa"
                        #if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                        if 'http' in urlx:
                            urld = f"{urlx}"
                        elif 'udp' in urlx:          #找出udp并组合
                            urld = f"{url_x}/tsfile/live/{num}_1.m3u8?key=txiptv&playlive=1&down=1"
                        else:  
                            urld = f"{url_x}{urlx}"  
                            
                        if name and urlx:
                            # 删除特定文字
                            name = name.replace("广东嘉佳卡通", "嘉佳卡通")
                            name = name.replace("星河频道", "TVB星河")
                            name = name.replace("珠江卫视", "广东珠江")
                            name = name.replace("珠江台", "广东珠江")
                            name = name.replace("cctv", "CCTV")
                            name = name.replace("中央", "CCTV")
                            name = name.replace("频道", "")
                            name = name.replace("精品", "")
                            name = name.replace("央视台球", "央视台球频道")
                            name = name.replace("央视文化", "央视文化精品")
                            name = name.replace("央视", "CCTV")
                            name = name.replace("CCTVCCTV", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("搞清", "")
                            name = name.replace("超高", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("-", "")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace(")", "")
                            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV4欧洲", "CCTV4")
                            name = name.replace("CCTV5体育赛事", "CCTV5+")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7农业", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("CCTV16奥运匹克", "CCTV16")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV17农业", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            name = name.replace("广东科教", "经济科教")
                            name = name.replace("广东经济科教", "经济科教")
                            name = name.replace("广东移动", "移动")
                            name = name.replace("广东国际", "国际")
                            name = name.replace("广东南方购物", "南方购物")
                            name = name.replace("广东南方卫视", "大湾区卫视")
                            name = name.replace("南方卫视", "大湾区卫视")
                            name = name.replace("广东综艺", "综艺")
                            name = name.replace("广东嘉佳", "嘉佳卡通")
                            name = name.replace("广东公共", "广东民生")
                            name = name.replace("广东珠江1", "广东珠江")
                            name = name.replace("北京纪实卫视", "北京纪实")
                            name = name.replace("上海东方", "东方")
                            name = name.replace("上海卫视", "东方卫视")
                            name = name.replace("综合卫视", "综合")
                            name = name.replace("康巴卫视", "")
                            name = name.replace("安多卫视", "")
                            name = name.replace("文华", "文化") 
                            name = name.replace("回放", "") 
                            name = name.replace("编码", "") 
                            name = name.replace("旅游卫视", "旅游") 
                    
                            results.append(f"{name},{urld}")
                            
            except:
                continue
        except:
            continue



channels = []
for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        if '广东' in channel_name or 'TVB' in channel_name or '翡翠' in channel_name or '嘉佳' in channel_name or '卫视' in channel_name or 'CCTV' in channel_name:
            channels.append((channel_name, channel_url))

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

error_channels = []


# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url, timeout = 0.8).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout = 0.8).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                # print(f"文件大小：{file_size} 字节")
                download_speed = file_size / response_time / 1024
                # print(f"下载速度：{download_speed:.3f} kB/s")
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                #print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 12
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
#print(results)
def shunxu(x):
  if '翡翠' in x[0]:
    return  1
  if '星河' in x[0]:
    return  2
  if '广东卫视' in x[0]:
    return  3
  if '珠江' in x[0]:
    return  4
  if '体育' in x[0]:
    return  5
  if '大湾区' in x[0]:
    return  6
  if '新闻' in x[0]:
    return  7  
  if '影视' in x[0]:
    return  8
  if '民生' in x[0]:
    return  9
  if '少儿' in x[0]:
    return  10
  if '嘉佳' in x[0]:
    return  11
  return 999999
#results.sort()
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))
results.sort(key=shunxu)

result_counter = 8  # 每个频道需要的个数

with open("test.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    #results.sort()
    file.write('广东频道,#genre#\n')
    file.write('纬来体育,http://hls.szsummer.cn/live/446035/playlist.m3u8?k=32f9ec7c13e4b390289143a8e1b2a898&t=1840341130\n')
    file.write('TVBPlus,https://ha.jmied.com/aa/aa.flv?auth_key=1661958232-0-0-3d9174957759709f8b53448167c0b6f6\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '广东' in channel_name or 'TVB' in channel_name or '翡翠' in channel_name or '嘉佳' in channel_name or '大湾区卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    #results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
    #results.sort(key=lambda x: channel_key(x[0]))
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write(f'{now},#genre#\n')
    file.write("Auto-update,http:// \n")
with open("test.m3u", 'w', encoding='utf-8') as file:
    #results.sort()
    channel_counters = {}
    file.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '广东' in channel_name or 'TVB' in channel_name or '翡翠' in channel_name or '嘉佳' in channel_name or '大湾区卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 tvg-name={channel_name} tvg-logo=\"https://live.fanmingming.com/tv/{channel_name}.png\" group-title=\"广东频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 tvg-name={channel_name} tvg-logo=\"https://live.fanmingming.com/tv/{channel_name}.png\" group-title=\"广东频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    file.write(f"#EXTINF:-1 tvg-name=\"\" tvg-logo=\"\" group-title=\"{now}\",Auto-update\n")
    file.write("http:// \n")
