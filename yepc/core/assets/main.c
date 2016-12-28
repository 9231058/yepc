#include <stdio.h>

#include "stack.h"


int main(int argc, const char *argv[])
{
	struct stack *s = stack_create();

	int a = 10;
	double b = 18.20;

	stack_push(s, &a, sizeof(a));
	stack_push(s, &b, sizeof(b));

	printf("%d %g\n", a, b);

	int a_new;
	double b_new;

	stack_pop(s, &b_new, sizeof(b_new));
	stack_pop(s, &a_new, sizeof(a_new));

	printf("%d %g\n", a_new, b_new);
}
