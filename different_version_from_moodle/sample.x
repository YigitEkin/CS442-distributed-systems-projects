const MAXDATALEN  = 200;

struct data {
  int data<200>;
};


typedef struct data data;

program SAMPLEPROG {
	version SAMPLEVERS {
		double AVERAGE(data) = 1;
        double VARIANCE(data) = 2;
        double STDDEV(data) = 3;
        double MINIMUM(data) = 4;
        double MAXIMUM(data) = 5;
	} = 1;
} = 21678;


