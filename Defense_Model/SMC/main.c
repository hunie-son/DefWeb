#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

#include <time.h>
#include <sys/time.h>

extern void smc(void *bufferPtr, void *bufferEndPtr);

#define BILLION 1000000000L

uint64_t prev_time_value, time_value, time_diff;

uint64_t get_clock_time()
{
	struct timespec ts;

	if (clock_gettime (CLOCK_MONOTONIC, &ts) == 0)
		return (uint64_t) (ts.tv_sec * 1000000 + ts.tv_nsec / 1000);
	else
		return 0;
}


int main()
{
    struct timespec start, stop;
    double accum;
    
    int repeat, sleep_time;

    const int BUFFER_LENGTH = 4096;
    
    void *bufferPtr = mmap(0, BUFFER_LENGTH, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
    void *bufferEndPtr = bufferPtr + BUFFER_LENGTH;
//    printf("Instruction block buffer: %p, %s\n", bufferPtr, strerror(errno));    
    //clock_gettime(CLOCK_REALTIME, &start);
    scanf("%d", &repeat);  
    //printf("Repeat = %d",repeat);
   
    scanf("%d", &sleep_time);  
    //printf("  sleep = %d\n",sleep_time);
     
    for (int i=0; i < repeat; i++){
      //prev_time_value = get_clock_time();
      //clock_gettime(CLOCK_REALTIME, &start);
      smc(bufferPtr, bufferEndPtr);
      //clock_gettime(CLOCK_REALTIME, &stop);
      //time_value = get_clock_time();
      //accum = (stop.tv_nsec - start.tv_nsec) / 1000000;
      //printf("%lf\n", accum);
      usleep(sleep_time);
    }
    //clock_gettime(CLOCK_REALTIME, &stop);
    //accum = (stop.tv_nsec - start.tv_nsec) / 1000000;
    //printf("%lf\n", accum);
    return 0;
}

