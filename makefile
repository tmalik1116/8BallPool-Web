EXPORT_PATH = export LD_LIBRARY_PATH=`pwd` && 
CC = clang
CFLAGS = -Wall -std=c99 -g -pedantic
PYTHON_INCLUDE = /usr/include/python3.11/
PYTHON_LIB = /usr/lib/python3.11

all: a1 

clean:
	rm -f *.o *.so  *.svg *.db *txt a1

libphylib.so: phylib.o
	$(CC) $(CFLAGS) -lm phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

phylib_wrap.c: phylib.i phylib.o
	swig -python phylib.i

phylib.py: phylib.i phylib.o
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

main.o: A1test1.c phylib.h _phylib.so
	$(CC) $(CFLAGS) -c A1test1.c -o main.o

#make separate targets
a1: main.o libphylib.so 
	$(CC) $(CFLAGS) -lm main.o -L. -Wl,-rpath=. -lphylib -o a1
	