#include <stdio.h>

int main()
{
    union _u {
        char a;
        int b;
        long c;
        void* d;
        int e;
        char* f;
    } u;
    u.a = 'a';
    u.b = 1;
    u.c = 2;
    u.d = NULL;
    u.e = 3;
    u.f = &u.a;

    printf("size of union u is %d\n", sizeof(u));
    return 0;
}
