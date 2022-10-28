#include "stat.h"
#include "stdio.h"
#include <rpc/rpc.h>

double res;

int main(int argc, char *argv[]){
    char *host;
    CLIENT *clnt;
    double *resp;
    data d;
    int datalen;
    int *arr;

    if(argc < 3){
        printf("not enough arguments");
        exit(1);
    }

    if(argc > MAXDATALEN + 2){
        printf("Input array exceeds maximum length of 200");
        exit(1);
    }

    datalen = argc - 2;

    // allocating the array, getting the pointer
    d.data.data_val = (int *)malloc((datalen)*sizeof(int));
    arr = d.data.data_val;
    d.data.data_len = datalen;
    host = argv[1];


    // copying the array from arguments into the array pointer
    for(int i = 0; i < datalen; i++){
        arr[i] = atoi(argv[i+2]);
    }

    // creating the client
    clnt = clnt_create(host, STATPROG, VERSIONS, "tcp");
    if (clnt == NULL) {
        clnt_pcreateerror(host);
        exit(1);
    }

    // calculating the average
    resp = average_1(&d, clnt);
    if(resp == NULL){
        clnt_perror (clnt, "call failed");
    }
    printf("average: %.2f\n", *resp);

    // calculating the variance
    resp = variance_1(&d, clnt);
    if(resp == NULL){
        clnt_perror (clnt, "call failed");
    }
    printf("variance: %.2f\n", *resp);

    // calculating the stddev
    resp = stddev_1(&d, clnt);
    if(resp == NULL){
        clnt_perror (clnt, "call failed");
    }
    printf("stddev: %.2f\n", *resp);

    // calculating the min
    resp = minimum_1(&d, clnt);
    if(resp == NULL){
        clnt_perror (clnt, "call failed");
    }
    printf("min: %.2f\n", *resp);

    // calculating the max
    resp = maximum_1(&d, clnt);
    if(resp == NULL){
        clnt_perror (clnt, "call failed");
    }
    printf("max: %.2f\n", *resp);

    clnt_destroy(clnt);
    free(d.data.data_val);
    return 1;
}