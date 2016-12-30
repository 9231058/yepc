all: yepc-output

yepc-output: main.o stack.o
	$(CC) -o $@ $^ $(CFLAGS) $(LDLIBS)

%.o: %.c stack.h
	$(CC) -c -o $@ $< $(CFLAGS)

.PHONY: clean
clean:
	rm yepc-output main.o stack.o
