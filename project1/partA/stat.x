const MAXDATALEN = 200;

struct data {
    int data<MAXDATALEN>;
};

typedef struct data data;

program STATPROG {
    version VERSIONS {
        double VARIANCE(data) = 1;
        double AVERAGE(data) = 2;
        double STDDEV(data) = 3;
        double MAXIMUM(data) = 4;
        double MINIMUM(data) = 5;
    } = 1;
} = 9;