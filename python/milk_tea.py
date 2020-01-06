"""
    1)原味冰奶茶 3元
    2)香蕉冰奶茶 5元
    3)草莓冰奶茶 5元
    4)蒟蒻冰奶茶 7元
    5)珍珠冰奶茶 7元
    请您帮助小象奶茶馆的收银小妹设计一款价格结算系统,要求:
    1.顾客输入1-5来选择奶茶口味,输入其它数字则输出:'Woops!我们只售卖以上五种奶茶哦!新品敬请期待!'
    2.顾客可输入购买数量,根据奶茶口味和数量计算总价
    3.顾客可输入是否会为本馆会员,会员可以享受9折优惠
    4.输出顾客购买的详细信息,包括奶茶口味 购买数量 总价.若是会员输出会员价.建议大家使用格式化输出
"""

product = ['原味冰奶茶', '香蕉冰奶茶', '草莓冰奶茶', '蒟蒻冰奶茶', '珍珠冰奶茶']


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


def calc_total_price(price, num, is_vip=False):
    """
    计算总价格
    :param price:单价
    :param num:数量
    :param is_vip:是否为会员
    :return:
    """
    if is_vip:
        total_price = price * num * 0.9
    else:
        total_price = price * num

    return total_price


def show_detail_info(product_number, number, total_price, is_vip):
    """
    显示顾客购买的奶茶信息
    :param product_number:
    :param total_price:
    :param is_vip:
    :return:
    """

    if is_vip:
        info = '您购买的奶茶信息如下:\n 品类:{}\n 数量:{}\n 单价:{}\n 总价:{}\n 会员价:{}'.format(product[product_number-1], number, get_product_price(product_number), total_price, total_price * 0.9)
    else:
        info = '您购买的奶茶信息如下:\n 品类:{}\n 数量:{}\n 单价:{}\n 总价:{}'.format(product[product_number-1], number, get_product_price(product_number), total_price)

    print(info)


def main():
    print('奶茶口味如下:')
    for key, item in enumerate(product):
        print('{}){} {}元'.format(key + 1, item, get_product_price(key + 1)))

    try:
        product_number = int(input('请输入1-5来选择口味:'))

        if product_number not in range(1, 6):
            print('Woops!我们只售卖以上五种奶茶哦!新品敬请期待!')
            return

        number = int(input('请输入您要购买的数量:'))
        is_vip = input('请输入您是否为会员(Y/N)')
        if is_vip == 'Y':
            is_vip = True
        else:
            is_vip = False

        price = get_product_price(product_number)
        total_price = calc_total_price(price, number)
        show_detail_info(product_number, number, total_price, is_vip)
    except:
        print('请输入正确的参数')
    else:
        print('购买成功!快递小哥很快会送到您手上!')


if __name__ == '__main__':
    main()
