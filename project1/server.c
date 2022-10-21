#include <math.h>
#include <rpc/rpc.h>
#include "stat.h"

double average_1(int **arr, int *size)
{
    static double sum = 0;

    for (int i = 0; i < (*size); ++i)
    {
        sum += *arr[i];
    }

    return sum / (*size);
}

int minimum_2(int **arr, int *size)
{
    static int min = 2147483647;

    for (int i = 0; i < (*size); ++i)
    {
        if (min > *arr[i])
        {
            min = *arr[i];
        }
    }

    return min;
}

int maximum_3(int **arr, int *size)
{
    static int max = -1;

    for (int i = 0; i < (*size); ++i)
    {
        if (max < *arr[i])
        {
            max = *arr[i];
        }
    }

    return max;
}

double stddev_4(int **arr, int *size)
{
    double sum_mean = 0;

    for (int i = 0; i < (*size); ++i)
    {
        sum_mean += *arr[i];
    }

    double mean = sum_mean / (*size);
    double sum = 0;

    for (int i = 0; i < (*size); ++i)
    {
        sum += pow(*arr[i] - mean, 2);
    }

    static double res = 0;
    res = sqrt(sum / (*size));
    return res;
}

double variance_5(int **arr, int *size)
{
    double sum_mean = 0;

    for (int i = 0; i < (*size); ++i)
    {
        sum_mean += *arr[i];
    }

    static double sum = 0;
    double mean = sum / (*size);
    for (int i = 0; i < (*size); ++i)
    {
        sum += pow(*arr[i] - mean, 2);
    }

    return sum / (*size);
}