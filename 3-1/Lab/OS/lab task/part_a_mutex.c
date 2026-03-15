/*
 * Part A: Multi-Account Transfer System using Mutexes
 *
 * KEY IDEAS TO UNDERSTAND:
 *
 * 1. MUTEX = "Mutual Exclusion Lock"
 *    Like a toilet door lock. Only ONE thread can hold it at a time.
 *    Other threads that call pthread_mutex_lock() on a held mutex
 *    will BLOCK (freeze/wait) until the holder calls pthread_mutex_unlock().
 *
 * 2. WHY ONE MUTEX PER ACCOUNT (not one global mutex)?
 *    One global mutex -> only one thread runs at a time = no real concurrency.
 *    Per-account mutexes -> T1 (touching A,B) and T3 (touching C,A) can
 *    partially overlap because they don't always share the same locks.
 *
 * 3. DEADLOCK PREVENTION via Lock Ordering
 *    Imagine:
 *      T1 holds lock(A), waits for lock(B)
 *      T2 holds lock(B), waits for lock(A)   <- circular wait = DEADLOCK
 *    Fix: always lock accounts in ascending index order (A=0, B=1, C=2).
 *    If you always lock the smaller index first, circular waits can't form.
 *
 * 4. ALL-OR-NOTHING (Atomic Transfer)
 *    Hold BOTH account locks before touching any balance.
 *    No thread can see or modify either account mid-transfer.
 */

#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define A 0
#define B 1
#define C 2
#define NUM_ACCOUNTS 3

int balance[NUM_ACCOUNTS] = {1000, 1000, 1000};
const char *acct_name[] = {"A", "B", "C"};

pthread_mutex_t acc_mutex[NUM_ACCOUNTS]; /* one mutex per account */
pthread_mutex_t log_mutex;               /* keeps printf lines clean */

void print_balances(const char *label) {
    /* Caller must hold log_mutex */
    printf("[%-6s] A=%4d  B=%4d  C=%4d  (sum=%d)\n",
           label, balance[A], balance[B], balance[C],
           balance[A] + balance[B] + balance[C]);
}

/*
 * transfer() — the heart of Part A
 *
 * Steps:
 *   1. Pick lock order (smaller index first) -> no deadlock
 *   2. Lock both accounts
 *   3. Check source has enough (no negatives)
 *   4. Subtract from source, add to destination
 *   5. Print log line (under log_mutex so it doesn't interleave)
 *   6. Unlock both accounts
 */
int transfer(int src, int dst, int amount, const char *tname) {
    /* Step 1 */
    int first  = (src < dst) ? src : dst;
    int second = (src < dst) ? dst : src;

    /* Step 2 */
    pthread_mutex_lock(&acc_mutex[first]);
    pthread_mutex_lock(&acc_mutex[second]);

    /* Steps 3 & 4 */
    int ok = 0;
    if (balance[src] >= amount) {
        balance[src] -= amount;
        balance[dst] += amount;
        ok = 1;

        /* Step 5 */
        pthread_mutex_lock(&log_mutex);
        printf("[%-2s] %3d : %s->%s | A=%4d B=%4d C=%4d\n",
               tname, amount, acct_name[src], acct_name[dst],
               balance[A], balance[B], balance[C]);
        pthread_mutex_unlock(&log_mutex);
    }

    /* Step 6 */
    pthread_mutex_unlock(&acc_mutex[second]);
    pthread_mutex_unlock(&acc_mutex[first]);
    return ok;
}

void *thread_T1(void *arg) {
    for (int i = 0; i < 10; i++)
        transfer(A, B, 100, "T1");          /* 100 x 10 = 1000 total moved */

    pthread_mutex_lock(&log_mutex);
    printf("\n--- T1 done ---\n"); print_balances("T1-end"); printf("\n");
    pthread_mutex_unlock(&log_mutex);
    return NULL;
}

void *thread_T2(void *arg) {
    for (int i = 0; i < 20; i++)
        transfer(B, C, 50, "T2");           /* 50 x 20 = 1000 total moved */

    pthread_mutex_lock(&log_mutex);
    printf("\n--- T2 done ---\n"); print_balances("T2-end"); printf("\n");
    pthread_mutex_unlock(&log_mutex);
    return NULL;
}

void *thread_T3(void *arg) {
    for (int i = 0; i < 40; i++)
        transfer(C, A, 25, "T3");           /* 25 x 40 = 1000 total moved */

    pthread_mutex_lock(&log_mutex);
    printf("\n--- T3 done ---\n"); print_balances("T3-end"); printf("\n");
    pthread_mutex_unlock(&log_mutex);
    return NULL;
}

int main(void) {
    for (int i = 0; i < NUM_ACCOUNTS; i++)
        pthread_mutex_init(&acc_mutex[i], NULL);
    pthread_mutex_init(&log_mutex, NULL);

    printf("=== Initial State ===\n");
    print_balances("start");
    printf("\n");

    pthread_t t1, t2, t3;
    pthread_create(&t1, NULL, thread_T1, NULL);
    pthread_create(&t2, NULL, thread_T2, NULL);
    pthread_create(&t3, NULL, thread_T3, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    printf("=== Final State ===\n");
    print_balances("final");

    for (int i = 0; i < NUM_ACCOUNTS; i++)
        pthread_mutex_destroy(&acc_mutex[i]);
    pthread_mutex_destroy(&log_mutex);
    return 0;
}