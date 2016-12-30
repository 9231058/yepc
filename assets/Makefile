all: yepc-output

yepc-output: output.o stack.o
	$(CC) -o $@ $^ $(CFLAGS) $(LDLIBS)

%.o: %.c functions.h
	$(CC) -c -o $@ $< $(CFLAGS)

.PHONY: clean
clean:
	rm output.o stack.o
