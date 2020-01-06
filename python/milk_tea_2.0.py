"""
    项目名称:小象奶茶馆结算系统
    作者:greezen
    时间:2018-04-08
    版本:2.0
    新增功能:
        1.顾客输入会员号,可判断是否为本馆会员.新会员直接设置会员号,但第二次购买才可享受会员价.(将会员记录在列表中,使用in语句判断是否为会员)
        2.使用列表记录每位顾客的消费信息.
        3.使用嵌套列表记录所有顾客的消费信息.
        4.本店每日只接待20位顾客,并在顾客光临时输出顾客的序号,第5位顾客购买完毕后输出:今日已闭店,欢迎您明天光临!
"""

# 奶茶种类
product = ['原味冰奶茶', '香蕉冰奶茶', '草莓冰奶茶', '蒟蒻冰奶茶', '珍珠冰奶茶']
# vip 客户信息
vip_list = []
# 顾客消费信息
customer_list = []


def get_product_price(product_number):
    """
    根据产品编号获取产品价格
    :param product_number:
    :return: price 价格
    """
    price = 0
    if product_number == 1:
        price = 3
    elif product_number == 2:
        price = 5
    elif product_number == 3:
        price = 5
    elif product_number == 4:
        price = 7
    elif product_number == 5:
        price = 7

    return price


def calc_total_price(price, num):
    """
    计算总价格
    :param price:单价
    :param num:数量
    :return:
    """

    total_price = price * num

    return total_price


def show_detail_info(product_number, number, total_price, vip_no):
    """
    显示顾客购买的奶茶信息
    :param product_number:
    :param number:
    :param total_price:
    :param vip_no:
    :return:
    """

    customer_info = {
        "product": product[product_number - 1],
        "number": number,
        "price": get_product_price(product_number),
        "total_price": total_price,
        "vip_no": vip_no
    }

    if vip_no in vip_list:
        customer_info['vip_price'] = total_price * 0.9
        info = '您购买的奶茶信息如下:\n 品类:{product}\n 数量:{number}\n 单价:{price}\n 总价:{total_price}\n 会员价:{vip_price}\n 会员号{vip_no}'.format(**customer_info)
    else:
        vip_list.append(vip_no)
        info = '您购买的奶茶信息如下:\n 品类:{product}\n 数量:{number}\n 单价:{price}\n 总价:{total_price}\n 会员号{vip_no}'.format(**customer_info)

    customer_list.append(customer_info)
    print(info)


def main():
    customer_count = 0
    while True:
        print('奶茶口味如下:')
        for key, item in enumerate(product):
            print('{}){} {}元'.format(key + 1, item, get_product_price(key + 1)))

        try:
            product_number = int(input('请输入1-5来选择口味:'))

            if product_number not in range(1, 6):
                print('Woops!我们只售卖以上五种奶茶哦!新品敬请期待!')
                return

            number = int(input('请输入您要购买的数量:'))
            vip_no = input('请输入您的会员编号(0x123)')

            price = get_product_price(product_number)
            total_price = calc_total_price(price, number)
            show_detail_info(product_number, number, total_price, vip_no)
        except:
            print('请输入正确的参数')
        else:
            print('购买成功!快递小哥很快会送到您手上!')
            customer_count += 1
        if customer_count > 4:
            print('今日已闭店,欢迎您明天光临!')
            break

    print(customer_list)


if __name__ == '__main__':
    main()
