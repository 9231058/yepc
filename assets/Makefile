CFLAGS=-Wall -O0 -g -std=gnu11

all: yepc-output

yepc-output: main.o stack.o
	$(CC) -o $@ $^ $(CFLAGS) $(LDLIBS)

%.o: %.c stack.h
	$(CC) -c -o $@ $< $(CFLAGS)

.PHONY: clean
clean:
	rm yepc-output main.o stack.o
