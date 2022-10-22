const MAXDATALEN  = 200;

struct data {
  int data<200>;
};

program STATISTICSPROG {
    version STATISTICSVERS {
        double AVERAGE(int *arr, int size) = 1;
        int MINIMUM(int *arr, int size) = 2;
        int MAX(int *arr, int size) = 3;
        double STDDEV(int *arr, int size) = 4;
        double VARIANCE(int *arr, int size) = 5;
    } = 1;
} = 99;