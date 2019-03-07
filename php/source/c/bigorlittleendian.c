#include<stdio.h>

void isBig()
{
	union _u {
		int a;
		char b;
	} u;
	u.a = 1;

	if (u.b == 1)
	{
		printf("is little endian\n");
	} else {
		printf("is big endian\n");
	}
}

int main(int argc, char const *argv[])
{
	isBig();
	return 0;
}