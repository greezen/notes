"""
    项目名称:小象奶茶馆结算系统
    作者:greezen
    时间:2018-04-16
    版本:3.0
    新增功能:
        1、增加每位顾客的购买品种，可多次输入奶茶编号（每次一种）和数量，并设置退出选项。
        2、将每位顾客的购买信息（奶茶品种和数量）记录在字典中，使用字典计算总消费额。
        3、顾客购物信息打印时，分别显示每种口味奶茶的编号和数量，末尾显示总金额。
        4、非会员顾客要求设置会员号及手机号，并且将会员号与手机号记录为字典形式。
        5、将每位顾客的每条购物信息记录为一个字典（每种口味一个字典，分别记录会员号、奶茶编号、购买数量），并将所有顾客的购物信息记入列表。
        6、将顾客的购物过程、购物信息打印、购物详情记录分别封装为函数。
        7、设置主函数，在主函数中调用上条所定义的函数。
"""

# 奶茶种类
g_product = ['原味冰奶茶', '香蕉冰奶茶', '草莓冰奶茶', '蒟蒻冰奶茶', '珍珠冰奶茶']
# vip 客户信息
g_vip_list = []
# 顾客消费信息
g_customer_list = []
# 购物车中的商品
g_buy_car_list = {}


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


def show_detail_info(product_list, total_price, vip_no, phone):
    """
    显示顾客购买的奶茶信息
    :param product_list:
    :param total_price:
    :param vip_no:
    :param phone:
    :return:
    """

    info = ''
    for product_number, number in product_list.items():
        customer_info = {
            "product_number": product_number,
            "product": g_product[product_number - 1],
            "number": number,
            "price": get_product_price(product_number),
            "total_price": total_price,
            "vip_no": vip_no
        }

        g_customer_list.append(customer_info)
        info += '品类:{product_number}){product} 数量:{number} 单价:{price}\n'.format(**customer_info)

    print('********************************************')
    print('您购买的奶茶信息如下:')
    print(info)
    if is_vip(vip_no):
        vip_price = total_price * 0.9
        print('总价为:{}, 会员价为:{}'.format(total_price, vip_price))
    else:
        g_vip_list.append({'vip_no': vip_no, 'phone': phone})
        print('总价为:{}'.format(total_price))

    print('您的会员号是:{}'.format(vip_no))
    print('********************************************')


def is_vip(vip_no):
    """
    判断用户是否为会员
    :param vip_no:
    :return:bool
    """
    vip_no_list = []
    for vip in g_vip_list:
        vip_no_list.append(vip['vip_no'])
    if vip_no in vip_no_list:
        return True
    else:
        return False


def main():
    customer_count = 0
    while True:
        print('奶茶口味如下:')
        for key, item in enumerate(g_product):
            print('{}){} {}元'.format(key + 1, item, get_product_price(key + 1)))

        try:
            goods_list = {}
            while True:
                product_number = int(input('请输入1-5来选择口味:'))

                if product_number not in range(1, 6):
                    print('Woops!我们只售卖以上五种奶茶哦!新品敬请期待!')
                    return

                number = int(input('请输入您要购买的数量:'))
                if product_number in goods_list.keys():
                    goods_list[product_number] += number
                else:
                    goods_list[product_number] = number

                is_exit = input('停止选购请输入Q:')
                if is_exit.upper() == 'Q':
                    break

            vip_no = input('请输入您的会员编号')
            if not is_vip(vip_no):
                phone = input('请输入您的手机号:')
            else:
                phone = False

            g_buy_car_list[vip_no] = goods_list

            total_price = 0
            for goods_key, goods_num in goods_list.items():
                price = get_product_price(goods_key)
                total_price += calc_total_price(price, goods_num)

            show_detail_info(goods_list, total_price, vip_no, phone)

        except:
            print('请输入正确的参数')
        else:
            print('购买成功!快递小哥很快会送到您手上!')
            customer_count += 1
        if customer_count > 3:
            print('今日已闭店,欢迎您明天光临!')
            break

    print(g_customer_list)


if __name__ == '__main__':
    main()
