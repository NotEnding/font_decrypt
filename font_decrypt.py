# -*- coding: utf-8 -*- 
"""
Project: PyProject
Creator: SF
Create time: 2021-06-17 12:36
IDE: PyCharm
Introduction: 黄页88网站 手机号字体加密解密
"""
import base64
import re
import requests
from fontTools.ttLib import TTFont

base_mapping = {
    'seven': 7, 'three': 3, 'five': 5, 'two': 2, 'nine': 9, 'one': 1, 'six': 6, 'zero': 0, 'four': 4, 'eight': 8
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
}

# 方法一,动态获取每次请求的网页源码中的字体文件
def get_font_map(font_text):
    """
    :param font_text: 字体文件的base64字符
    :return:
    """
    with open('world.ttf', 'wb') as f:
        f.write(base64.b64decode(font_text))
    font = TTFont('world.ttf')
    font.saveXML('world.xml')  # 可以不保存xml文件
    best_cmap = TTFont("world.ttf")['cmap'].getBestCmap()
    new_font_map = dict()
    for key in best_cmap.keys():
        value = best_cmap[key] if best_cmap[key] not in list(base_mapping.keys()) else base_mapping[best_cmap[key]]
        if isinstance(value, int):
            new_font_map[hex(key)] = value
    return new_font_map


# 第二种形式-----直接解码加密的串
def decrypt_phone(encrypt_number):
        """
        :param encrypt_number: 加密后的手机号
        :return:
        """
        code_string = encrypt_number.strip(';')
        # 替换 &# 为 0，用于后面直接转换为10进制数
        code_string = code_string.replace("&#", "0")
        # 转换成列表
        code_list = code_string.split(';')
        print(f"code_list:{code_list},{len(code_list)}")

        # 手机号 >标准手机号形式
        int_list = None
        if len(code_list) == 11:
            # 第一个号码为1对应的10进制值
            c1 = int(code_list[0], base=16)
            # 创建0-9对应的10进制值
            int_list = range(c1 - 1, c1 + 9)
        # 带区号的电话形式
        elif len(code_list) == 13:
            # 第一个号码为0对应的10进制值
            c1 = int(code_list[0], base=16)
            # 创建0-9对应的10进制值
            int_list = range(c1, c1 + 10)

        # 将其转换为hex
        hex_list = [str(hex(i)) for i in int_list]
        # 创建0-9的数字对应列表
        str_list = [str(i) for i in range(0, 10)]
        # 组装成字典方便对应
        code_dict = dict(zip(hex_list, str_list))
        # 把电话号码拼接起来(需要处理带区号的那种电话号码情况)
        phone = ""
        for p in code_list:
            if p == "0x2d":
                num = '-'
            else:
                num = code_dict.get(p)
            phone += num
        print(phone)
        return phone


if __name__ == '__main__':
    # 方法一
    # content = requests.get('http://fuzhongqipei.b2b.huangye88.com/company_detail.html', headers=headers).text
    content = requests.get('http://b2b.huangye88.com/gongsi/company561409/detail.html', headers=headers).text

    # 提取手机号码加密串
    phone_text = re.search("<span class='secret'>(.*?)</span>", content)
    if phone_text:
        code_list = phone_text.group(1).replace("&#", "0").split(';')[:-1]
        print(code_list)
        phone_number = ""

        # 提取字体文件 base64 串
        font_data_b64 = re.search('base64,(.*?)"\)', content)
        if font_data_b64:
            font_data = font_data_b64.group(1)
            # 获取字体映射关系
            font_map = get_font_map(font_data)
            for code in code_list:
                if code == "0x2d":
                    num = '-'
                else:
                    num = str(font_map.get(code))
                phone_number += num
        print(phone_number)

    # 方法二
    en1 = '&#x88343;&#x88347;&#x8834a;&#x88342;&#x88342;&#x88347;&#x88342;&#x8834b;&#x88348;&#x88345;&#x88342;'
    en2 = '&#x880d9;&#x880db;&#x880e0;&#x880dc;&#x880dd;&#x880db;&#x880e1;&#x880df;&#x880df;&#x880e1;&#x880e0;'
    en3 = '&#x88120;&#x88127;&#x88129;&#x88121;&#x2d;&#x88128;&#x88126;&#x88125;&#x88120;&#x88128;&#x88123;&#x88120;&#x88126;'
    en4 = '&#x882df;&#x882e6;&#x882e8;&#x882e0;&#x2d;&#x882e7;&#x882e5;&#x882e4;&#x882df;&#x882e7;&#x882e2;&#x882df;&#x882e5;'
    decrypt_phone(en1)
    decrypt_phone(en2)
    decrypt_phone(en3)
    decrypt_phone(en4)
