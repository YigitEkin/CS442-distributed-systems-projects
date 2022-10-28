all: server client

server: server.c stat_svc.c stat.h 
	gcc -Wall -c server.c
	gcc -Wall -c stat_svc.c
	gcc -Wall -c stat_xdr.c
	gcc -o server server.o stat_svc.o stat_xdr.o -lm


client: client.c stat_clnt.c stat.h
	gcc -Wall -c -g client.c
	gcc -Wall -c stat_clnt.c
	gcc -Wall -c stat_xdr.c
	gcc -o client client.o stat_clnt.o stat_xdr.o

clean:
	rm -f server client stat_clnt.c stat_svc.c stat_xdr.c stat.h