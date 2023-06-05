# -*- coding: utf-8 -*-
from time import sleep
import requests
from datetime import datetime
import subprocess
import random
import re

def get_dr():#用以得到当前时间戳
    current_time = datetime.now()
    timestamp = int(current_time.timestamp() * 1000)
    return str(timestamp)
def get_jQuery():
    return ''.join(random.choice('0123456789') for _ in range(21))
# 定义一个函数，用于获取当前已连接的Wi-Fi名称
def get_available_wifi_networks():
    # 使用netsh命令获取可用的WiFi网络
    command = 'netsh wlan show networks mode=Bssid'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    output_lines = result.stdout.splitlines()
    wifi_networks = []
    current_network = {}

    for line in output_lines:
        if line.strip().startswith("SSID"):
            if current_network:
                wifi_networks.append(current_network)
                current_network = {}
            current_network['SSID'] = line.split(":")[1].strip()
        elif line.strip().startswith("BSSID"):
            current_network['BSSID'] = line.split(":")[1].strip()

    if current_network:
        wifi_networks.append(current_network)

    return [network['SSID'] for network in wifi_networks]


# 获取并显示可用的WiFi网络
output = subprocess.check_output("netsh wlan show interfaces", shell=True, universal_newlines=True)
def connect_to_wifi(ssid):
    # 使用netsh命令连接WiFi
    command = 'netsh wlan connect ssid='+ssid+' name='+ssid
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if result.returncode == 0:
        print("WiFi连接成功！")
    else:
        print("WiFi连接失败:",result)
def get_connected_wifi_name():#返回已连接的Wifi名
    try:
        # 使用subprocess.check_output执行系统命令"netsh wlan show interfaces"
        # 并将命令的输出结果以字符串的形式返回
        output = subprocess.check_output("netsh wlan show interfaces", shell=True, universal_newlines=True)

        # 使用split("\n")将输出结果按行分割成一个列表
        lines = output.split("\n")
        
        # 遍历列表中的每一行
        for line in lines:
            # 查找包含"SSID"但不包含"BSSID"的行
            if "SSID" in line and "BSSID" not in line:
                # 使用split(":")[1]将行按":"分割，并取分割后的第二部分（索引为1）作为Wi-Fi名称
                wifi_name = line.split(":")[1]
                # 使用strip()去除Wi-Fi名称前后的空白字符，并返回结果
                return wifi_name.strip()

    # 如果执行系统命令时发生错误，则捕获异常
    except subprocess.CalledProcessError as e:
        # 如果发生异常，则返回"未连接到Wi-Fi"
        return None

def connect_PPSUC(mac,account,passwd):
    url_mac='http://192.168.8.123:801/eportal/?c=Portal&a=del_pass&callback=jQuery%s_%s&mac=%s&_=%s'%(get_jQuery(),get_dr(),mac,get_dr())
    url_connect="http://192.168.8.123/drcom/login?callback=dr%s&DDDDD=%s&upass=%s&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_=%s"%(get_dr(),account,passwd,get_dr())
    requests.get(url_mac)
    requests.get(url_connect)

def is_connect():
    try:
        response = requests.get('http://www.baidu.com', timeout=1)
        if response.status_code == 200:
            if '限制非哆点客户端登陆' in response.text:
                return False
            else:
                return True
        else:
            return False
    except:
        return False
def get_mac_address():
    # 使用ipconfig命令获取本地网络接口信息
    command = 'ipconfig /all'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    output_lines = result.stdout.splitlines()
    mac_address =None
    flag=0
    for line in output_lines:
        if '无线局域网适配器 WLAN' in line:
            flag=1
        if "物理地址" in line and flag==1:
            match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
            if match:
                mac_address=match.group(0)
                break
    
    return mac_address.replace('-','').lower()
count=0
while(1):
    try:
        sleep(1)#每次循环sleep 1秒
        if(is_connect()):#若连接到互联网了，直接continue，sleep 10 秒
            print('已连接到互联网')
            sleep(10)
            count+=1
            print('第%d次循环结束' % count)
            continue
        connected_wifi=get_connected_wifi_name()
        if(connected_wifi==None):
            #若没有连接到网络且没有链接到校园网，手机Wifi热点以及家里的wifi,尝试连接之
            available_wifi=get_available_wifi_networks()
            if('PPSUC_5Ghz' in available_wifi):
                connect_to_wifi('PPSUC_5Ghz')
                print('连接到互联网 PPSUC5G')
                sleep(1)
            elif('PPSUC' in available_wifi):
                connect_to_wifi('PPSUC')
                print('连接到互联网 PPSUC')
                sleep(1)
        if(('PPSUC_5Ghz' == connected_wifi or 'PPSUC' == connected_wifi) and not is_connect()):
            #若链接校园网，尝试输入账号密码登录，此处可能存在安全隐患
            connect_PPSUC(mac=get_mac_address(),account='',passwd='')
            print('登录成功')
            sleep(1)
        count+=1
        print('第%d次循环结束' % count)
    except:
        sleep(3)
        continue




