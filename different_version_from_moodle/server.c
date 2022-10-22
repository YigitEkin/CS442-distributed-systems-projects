#include <stdio.h>
#include <math.h>
#include <rpc/rpc.h>
#include "sample.h"

static double average_result;
static double variance_result;
static double stddev_result;
static double min_result;
static double max_result;

double *average_1_svc(data *dp, struct svc_req *rqstp)
{
    int i;
    double sum = 0.0;
    for (i = 0; i < dp->data.data_len; i++)
    {
        sum += dp->data.data_val[i];
    }
    average_result = sum / dp->data.data_len;
    return &average_result;
}
double *variance_2_svc(data *dp, struct svc_req *rqstp)
{
    int i;
    double sum = 0.0;
    double avg = average_result;
    for (i = 0; i < dp->data.data_len; i++)
    {
        sum += (dp->data.data_val[i] - avg) * (dp->data.data_val[i] - avg);
    }
    variance_result = sum / dp->data.data_len;
    return &variance_result;
}
double *stddev_3_svc(data *dp, struct svc_req *rqstp)
{
    stddev_result = sqrt(variance_result);
    return &stddev_result;
}
double *minimum_4_svc(data *dp, struct svc_req *rqstp)
{
    int i;
    min_result = dp->data.data_val[0];
    for (i = 1; i < dp->data.data_len; i++)
    {
        if (dp->data.data_val[i] < min_result)
        {
            min_result = dp->data.data_val[i];
        }
    }
    return &min_result;
}

double *maximum_5_svc(data *dp, struct svc_req *rqstp)
{
    int i;
    int *p;
    int len;

    p = dp->data.data_val;
    len = dp->data.data_len;

    max_result = 0;
    for (i = 0; i < len; i++)
    {
        if (max_result < *p)
            max_result = *p;
        p++;
    }
    return (&max_result);
}
