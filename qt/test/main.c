#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <error.h>

int count_str(char *src, char *sub, int *count)
{
    int ret = 0;
    char *p = src;
    int tmpCount = 0;

    if(src == NULL || sub == NULL || count == NULL){
        return -1;
    }
    while ((p = strstr(p, sub)) != NULL) {

        p = p + strlen(sub);
        if (strlen(p) == 0){
            break;
        }
        printf("%s\n", p);
        tmpCount++;
    }

    *count = tmpCount;
    return ret;
}

int main()
{
    char *src = "666sdda666iiksl666wwrrr666pppp666";
    char *sub = NULL;
    int count = 0;
    int res = 0;

    res = count_str(src, sub, &count);
    if(res != 0){
        printf("error:\n");
    }

    printf("%s,str count %d\n", src, count);
    return 0;
}
