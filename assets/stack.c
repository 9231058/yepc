#include <stdlib.h>
#include <string.h>

#include "stack.h"

struct stack *stack_create(void)
{
	struct stack *ret;

	ret = malloc(sizeof(struct stack));
	ret->top = NULL;

	return ret;
}

void stack_push(struct stack *stack, const void *source, size_t type_size)
{
	struct node *new_node;
	
	/* Build our new node :) */
	new_node = malloc(sizeof(struct node));
	new_node->data = malloc(type_size);
	new_node->next = NULL;

	/* Read data from source */
	memcpy(new_node->data, source, type_size);
	
	/* Push new node on top of given stack */
	new_node->next = stack->top;
	stack->top = new_node;
}

void stack_pop(struct stack *stack, void *sink, size_t type_size)
{
	struct node *old_node;

	/* Pop old node from top of given stack */
	old_node = stack->top;
	stack->top = stack->top->next;

	/* Write data into sink */
	if (sink) {
		memcpy(sink, old_node->data, type_size);
	}
}

void stack_seek(struct stack *stack, int location, void *sink, size_t type_size)
{
	struct node *current;
	int i;
	
	/* seek and find :) */
	current = stack->top;
	for (i = 0; i < location && current->next; i++)
		current = current->next;

	/* Write data into sink */
	if (sink) {
		memcpy(sink, current->data, type_size);
	}
}
