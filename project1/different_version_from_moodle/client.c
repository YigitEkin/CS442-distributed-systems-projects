#include <stdio.h>
#include <stdlib.h>
#include <rpc/rpc.h>
#include "sample.h"

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

    if (argc > MAXDATALEN + 2)
    {
        printf("Two many input values\n");
        exit(1);
    }

    host = argv[1];

    d.data.data_val = (int *)malloc(MAXDATALEN * sizeof(int));
    ip = d.data.data_val;
    datalen = (argc - 2);
    d.data.data_len = datalen;

    for (i = 0; i < datalen; ++i)
    {
        x = atoi(argv[i + 2]);
        d.data.data_val[i] = x;
    }

    number = atoi(argv[2]);
    clnt = clnt_create(host, SAMPLEPROG,
                       SAMPLEVERS, "tcp");

    if (clnt == NULL)
    {
        clnt_pcreateerror(host);
        exit(1);
    }

    resp = average_1_svc(&d, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("average: %d\n", r);

    resp = variance_2_svc(&d, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("variance: %d\n", r);

    resp = stddev_3_svc(&d, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("stddev: %d\n", r);

    resp = minimum_4_svc(&d, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("minimum: %d\n", r);

    resp = maximum_5_svc(&d, clnt); // calling the remote procedure
    if (resp == (int *)NULL)
    {
        clnt_perror(clnt, "call failed");
    }
    r = *resp;

    printf("maximum: %d\n", r);

    clnt_destroy(clnt);

    return (1);
}
