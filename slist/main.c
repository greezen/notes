#include <stdio.h>
#include <stdlib.h>

struct slist
{
    int data;
    struct slist *next;
};

/**
 * 创建链表接点
 * @brief create_slist
 * @return
 */
struct slist *create_node()
{
   return calloc(sizeof(struct slist), 1);
}

/**
 * 输出所有节点
 * @brief print_slist
 * @param sl
 */
void print_slist(const struct slist *sl)
{
    while (sl) {
        printf("%d\n", sl->data);
        sl = sl->next;
    }
}

/**
 * 为链表新增一个节点
 * @brief insert_node
 * @param sl
 * @param index
 * @param data
 * @return
 */
struct slist *insert_node(struct slist *sl, int index, int data)
{
    //找到第index所在的节点
    while (sl && index--) {
        sl = sl->next;
    }

    //未找到指定的位置
    if(sl == NULL){
        return NULL;
    }
    struct slist *node = create_node();
    node->data = data;
    node->next = sl->next;
    sl->next = node;
    return sl;
}

/**
 * 链表的节点数
 * @brief count_node
 * @param sl
 * @return
 */
int count_node(struct slist *sl)
{
    int count = 0;
    while (sl) {
        sl = sl->next;
        count++;
    }
    return count;
}

/**
 * 查询指定节点值在链表中的位置
 * @brief search_node
 * @param sl
 * @param data
 * @return
 */
int search_node(struct slist *sl, int data)
{
    int count = 0,index = -1;
    while (sl) {
        if(sl->data == data)
        {
            index = count;
            break;
        }
        sl = sl->next;
        count++;
    }

    return index;
}

/**
 * 移除指定值的节点
 * @brief remove_node
 * @param sl
 * @param data
 * @return
 */
int remove_node(struct slist *sl, int data)
{
    if(sl->data == data)
    {
        free(sl);
        return 0;
    }

    struct slist *pre = sl;
    while(sl)
    {
        pre = sl;
        sl = sl->next;
        if(sl->data == data)
        {
            pre->next = sl->next;
            free(sl);
            break;
        }
    }
    return 0;
}


int main()
{
    struct slist *first = create_node();
    first->data = 1;
    first->next = NULL;

    insert_node(first, 0, 4);
    insert_node(first, 0, 3);
    insert_node(first, 0, 2);

    print_slist(first);
    printf("slist length is %d, %d\n", count_node(first), search_node(first, 6));
    remove_node(first, 3);
    print_slist(first);
    printf("slist length is %d, %d\n", count_node(first), search_node(first, 6));
    return 0;
}
