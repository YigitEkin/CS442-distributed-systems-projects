#include <rpc/rpc.h>
#include "stat.h"
#include <stdio.h>
#include <stdlib.h>

int number;
int r;

int main(int argc, char *argv[])
{
    char *host;
    CLIENT *clnt;
    int *resp;
    data d;
    int datalen;
    int *ip;
    int x;
    int i;

    if (argc < 3)
    {
        printf("Invalid number of arguments");
        exit(1);
    }

    if (argc > MAXDATALEN + 2)
    {
        printf("Too many input values\n");
        exit(1);
    }

    host = argv[1];

    d.data = (int *)malloc(MAXDATALEN * sizeof(int));
    datalen = (argc - 2);

    for (i = 0; i < datalen; ++i)
    {
        x = atoi(argv[i + 2]);
        d.data[i] = x;
    }

    clnt = clnt_create(host, SAMPLEPROG,
                       SAMPLEVERS, "tcp");

    if (clnt == NULL)
    {
        clnt_pcreateerror(host);
        exit(1);
    }
    printf("connected to the server\n");

    resp = average_1(&d.data, &datalen, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;
    printf("average: %d\n", r);

    resp = variance_5(&d, &datalen, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("variance: %d\n", r);

    resp = stddev_4(&d, &datalen, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("stddev: %d\n", r);

    resp = minimum_2(&d, &datalen, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("minimum: %d\n", r);

    resp = maximum_3(&d, &datalen, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("maximum: %d\n", r);

    clnt_destroy(clnt);

    return (1);
}
