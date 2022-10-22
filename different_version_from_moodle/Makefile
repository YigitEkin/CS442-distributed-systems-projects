all: server client

server: server.c sample_svc.c sample.h 
	gcc -Wall -c server.c
	gcc -Wall -c sample_svc.c
	gcc -Wall -c sample_xdr.c
	gcc -o server server.o sample_svc.o sample_xdr.o


client: client.c sample_clnt.c sample.h
	gcc -Wall -c client.c
	gcc -Wall -c sample_clnt.c
	gcc -Wall -c sample_xdr.c
	gcc -o client client.o sample_clnt.o sample_xdr.o

clean:
	rm -f *.o server client sample_clnt.c sample_svc.c sample.h sample_xdr.c



