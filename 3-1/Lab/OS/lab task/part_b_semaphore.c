/*
 * Part B: Limited-Capacity Transaction Server using a Semaphore
 *
 * KEY IDEAS:
 *
 * 1. COUNTING SEMAPHORE
 *    Holds an integer N, initialised to 3 (server capacity).
 *
 *    sem_wait(s):  if N > 0 -> decrement N and proceed immediately.
 *                  if N == 0 -> BLOCK until someone posts.
 *    sem_post(s):  increment N; wakes one blocked thread if any.
 *
 *    Think of 3 server desks with ticket numbers.
 *    C1, C2, C3 grab a ticket (N: 3->2->1->0).
 *    C4, C5, C6 queue at sem_wait — they can't proceed until
 *    someone at a desk finishes and calls sem_post.
 *
 * 2. STATUS ARRAY + MUTEX
 *    served[6] — boolean array, served[i]=1 means client i is active.
 *    status_mutex protects it so the monitor never reads a half-written array.
 *
 * 3. MONITOR THREAD
 *    Loops every 400 ms: locks, prints all 6 booleans, unlocks.
 *
 * EXPECTED TIMELINE:
 *   t=0 s : C1,C2,C3 acquire semaphore. C4,C5,C6 block.
 *            Monitor: C1=True, C2=True, C3=True, C4=False, C5=False, C6=False
 *   t=1 s : C1,C2,C3 release. C4,C5,C6 immediately acquire.
 *            Monitor: C1=False, C2=False, C3=False, C4=True, C5=True, C6=True
 *   t=2 s : C4,C5,C6 release. All done.
 */

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_CLIENTS   6
#define SERVER_CAP    3       /* semaphore initial value */
#define SERVICE_TIME  1       /* seconds each client holds a slot */
#define MONITOR_US    400000  /* monitor print interval (400 ms) */

sem_t           server_sem;
int             served[NUM_CLIENTS];   /* 0 or 1 */
pthread_mutex_t status_mutex;
int             all_done = 0;          /* tells monitor to stop */

/* Monitor: repeatedly prints the served[] array */
void *monitor(void *arg) {
    while (!all_done) {
        pthread_mutex_lock(&status_mutex);
        for (int i = 0; i < NUM_CLIENTS; i++) {
            printf("C%d=%s", i + 1, served[i] ? "True " : "False");
            if (i < NUM_CLIENTS - 1) printf(", ");
        }
        printf("\n");
        pthread_mutex_unlock(&status_mutex);
        usleep(MONITOR_US);
    }
    return NULL;
}

/* Client: wait for slot, work 1 second, release slot */
void *client(void *arg) {
    int id = *(int *)arg;   /* 0-based */

    sem_wait(&server_sem);  /* ACQUIRE — blocks if server full */

    pthread_mutex_lock(&status_mutex);
    served[id] = 1;
    pthread_mutex_unlock(&status_mutex);

    sleep(SERVICE_TIME);    /* simulate service */

    pthread_mutex_lock(&status_mutex);
    served[id] = 0;
    pthread_mutex_unlock(&status_mutex);

    sem_post(&server_sem);  /* RELEASE — lets a waiting client in */
    return NULL;
}

int main(void) {
    sem_init(&server_sem, 0, SERVER_CAP);   /* init semaphore to 3 */
    pthread_mutex_init(&status_mutex, NULL);
    for (int i = 0; i < NUM_CLIENTS; i++) served[i] = 0;

    pthread_t monitor_tid;
    pthread_create(&monitor_tid, NULL, monitor, NULL);

    pthread_t tids[NUM_CLIENTS];
    int       ids[NUM_CLIENTS];
    for (int i = 0; i < NUM_CLIENTS; i++) {
        ids[i] = i;
        pthread_create(&tids[i], NULL, client, &ids[i]);
        usleep(5000);   /* tiny stagger for predictable ordering */
    }

    for (int i = 0; i < NUM_CLIENTS; i++)
        pthread_join(tids[i], NULL);

    all_done = 1;
    pthread_join(monitor_tid, NULL);

    printf("All clients served. Server idle.\n");
    sem_destroy(&server_sem);
    pthread_mutex_destroy(&status_mutex);
    return 0;
}