CC=gcc
CFLAGS=-O2 -Wall
OBJ=mydig.o
TARGET=mydig

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

$(TARGET): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm $(TARGET) $(OBJ)
