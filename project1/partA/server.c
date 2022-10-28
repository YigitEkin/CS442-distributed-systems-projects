#include "stat.h"
#include "stdio.h"
#include <math.h>
#include <rpc/rpc.h>

static double varianceResult;
static double averageResult;
static double stddevResult;
static double maximumResult;
static double minimumResult;

double * variance_1_svc(data *dp, struct svc_req *rq){
    int sum = 0;
    int sum1 = 0;
    int len = 0;
    int avg = 0;
    int *p;

    p = dp-> data.data_val;
    len = dp-> data.data_len;

    for(int i = 0; i < len; i++){
        sum = sum + p[i];
    }

    avg = sum / (float) len;

    for(int i = 0; i < len; i++){
        sum1 = sum1 + pow((p[i] - avg), 2);
    }

    varianceResult = sum1 / (float)len;
    return (&varianceResult);
}

double * average_1_svc(data *dp, struct svc_req *rq){
    int sum = 0;
    int len = 0;
    int *p;

    p = dp-> data.data_val;
    len = dp-> data.data_len;

    for(int i = 0; i < len; i++){
        sum = sum + p[i];
    }

    averageResult = sum / (float) len;

    return (&averageResult);
}

double * stddev_1_svc(data *dp, struct svc_req *rq){
    int sum = 0;
    int sum1 = 0;
    int len = 0;
    int avg = 0;
    int var = 0;
    int *p;

    p = dp-> data.data_val;
    len = dp-> data.data_len;

    for(int i = 0; i < len; i++){
        sum = sum + p[i];
    }

    avg = sum / (float) len;

    for(int i = 0; i < len; i++){
        sum1 = sum1 + pow((p[i] - avg), 2);
    }

    var = sum1 / (float)len;
    stddevResult = sqrt(var);
    return (&stddevResult);
}

double * maximum_1_svc(data *dp, struct svc_req *rq){
    int max;
    int len = 0;
    int *p;

    p = dp->data.data_val;
    len =  dp->data.data_len;

    max = p[0];
    for(int i = 0; i < len; i++){
        if(max < p[i]){
            max = p[i];
        }
    }

    maximumResult = max;
    return (&maximumResult);
}

double * minimum_1_svc(data *dp, struct svc_req *rq){
    int min;
    int len = 0;
    int *p;

    p = dp->data.data_val;
    len =  dp->data.data_len;

    min = p[0];
    for(int i = 0; i < len; i++){
        if(min > p[i]){
            min = p[i];
        }
    }

    minimumResult = min;
    return (&minimumResult);
}