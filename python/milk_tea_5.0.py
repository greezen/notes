"""
    项目名称:小象奶茶馆结算系统
    作者:greezen
    时间:2018-04-16
    版本:4.0
    新增功能:
        1、记录顾客到店日期，并记入会员信息、顾客购物信息记录中。
        2、延长系统服务天数，设置为 30 天。
        3、要求会员手机号输入长度为 11。
        4、会员信息记录新增生日、性别、星座、所在地，新增信息（包括今日日期）与手机号一起以列表的形式作为每位会员字典信息中的 value 值。
        5、所有会员信息写入一个 csv 文件，包含文字标题行。
        6、顾客购物信息每天写入一个 csv 文件，包含文字标题行。
"""

# 奶茶种类
g_product = ['原味冰奶茶', '香蕉冰奶茶', '草莓冰奶茶', '蒟蒻冰奶茶', '珍珠冰奶茶']
# vip 客户信息
g_vip_list = []
# 顾客消费信息
g_customer_list = []
# 购物车中的商品
g_buy_car_list = {}
# 所有顾客购物历史信息
g_history_list = {}


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
    tea_no_list = []
    for product_number, number in product_list.items():
        customer_info = {
            "product_number": product_number,
            "product": g_product[product_number - 1],
            "number": number,
            "price": get_product_price(product_number),
            "total_price": total_price,
            "vip_no": vip_no
        }

        tea_no_list.append(product_number)

        g_customer_list.append(customer_info)
        info += '品类:{product_number}){product} 数量:{number} 单价:{price}\n'.format(**customer_info)

    g_history_list[vip_no] = set(tea_no_list)

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


def recommend(vip_no, goods):
    """
    推荐产品
    :param vip_no:
    :param goods:
    :return:
    """

    if len(g_history_list) == 0:
        return []

    recommend_list = []
    for no, items in g_history_list.items():
        if no != vip_no:
            same_goods = goods & items
            count_same_goods = len(same_goods)
            if count_same_goods > 0:
                sub_goods = items - goods
                recommend_item = {'count': count_same_goods, 'goods': sub_goods}
                recommend_list.append(recommend_item)

    # 购买产品相同数多的推荐给用户
    recommend_list.sort(key=lambda product: product['count'], reverse=True)
    return recommend_list


def show_recommend(recommend_list):
    """
    显示推荐商品
    :param recommend_list:
    :return:
    """
    for item in recommend_list:
        print('推荐商品:{}'.format(item))


def main():
    customer_count = 0
    while True:
        print('奶茶口味如下:')
        for key, item in enumerate(g_product):
            print('{}){} {}元'.format(key + 1, item, get_product_price(key + 1)))

        get_hot = input('爆款 蒟蒻冰奶茶是否想尝试一下?请输入(y/n):')
        if get_hot.lower() == 'y':
            product_number = 4

        try:
            goods_list = {}
            while True:
                print(product_number)
                if product_number == 0:
                    product_number = int(input('请输入1-5来选择口味:'))

                    if product_number not in range(1, 6):
                        print('Woops!我们只售卖以上五种奶茶哦!新品敬请期待!')
                        return

                number = int(input('请输入您要购买的数量:'))
                if product_number in goods_list.keys():
                    goods_list[product_number] += number
                else:
                    goods_list[product_number] = number

                product_number = 0
                is_exit = input('停止选购请输入Q:')
                if is_exit.upper() == 'Q':
                    break

            vip_no = input('请输入您的会员编号')
            if not is_vip(vip_no):
                phone = input('请输入您的手机号:')
            else:
                phone = False

            # 推荐商品
            recommend_list = recommend(vip_no, set(goods_list.keys()))
            show_recommend(recommend_list)

            g_buy_car_list[vip_no] = goods_list

            total_price = 0
            for goods_key, goods_num in goods_list.items():
                price = get_product_price(goods_key)
                total_price += calc_total_price(price, goods_num)

            show_detail_info(goods_list, total_price, vip_no, phone)

        except Exception as e:
           print(e)
        else:
            print('购买成功!快递小哥很快会送到您手上!')
            customer_count += 1
        if customer_count > 3:
            print('今日已闭店,欢迎您明天光临!')
            break

    print(g_customer_list)


if __name__ == '__main__':
    main()
