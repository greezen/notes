#include <stdio.h>

int main()
{
    struct _s{
        char a;
        int b;
        long c;
        void* d;
        int e;
        char* f;
    } s;
    s.a = 'a';
    s.b = 1;
    s.c = 2;
    s.d = NULL;
    s.e = 3;
    s.f = &s.a;

    printf("size of struct s is %d\n", sizeof(s));
    return 0;
}

