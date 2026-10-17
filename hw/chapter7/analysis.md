# Chapter 7: CPU Scheduling Analysis

## Method and assumptions

All jobs arrive at t = 0, use only the CPU, and have positive known execution lengths. There is no context-switch overhead in this simulator. Response time = first start - arrival; turnaround time = completion - arrival; wait time = turnaround - CPU execution length.

For each experiment, the expected times are calculated from the scheduling rules and compared with scheduler.py. The data directory contains both the problem run (without -c) and the verification run (with -c). Reported averages agree with the independent calculations.

## Q1: Three jobs of length 200, FIFO and SJF

Equal lengths give the same ordering (ties keep job order). First starts are 0, 200, 400; completions are 200, 400, 600. Thus average response = 200 and average turnaround = 400. Average wait is also 200.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q1_fifo | 200,200,200 | FIFO | - | 200.00 | 400.00 | 200.00 |
| q1_sjf | 200,200,200 | SJF | - | 200.00 | 400.00 | 200.00 |

## Q2: Jobs of length 100, 200, 300

The input is already shortest-first, so FIFO and SJF coincide. First starts are 0, 100, 300; completions are 100, 300, 600. Average response = 400/3 = 133.33; average turnaround = 1000/3 = 333.33.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q2_fifo | 100,200,300 | FIFO | - | 133.33 | 333.33 | 133.33 |
| q2_sjf | 100,200,300 | SJF | - | 133.33 | 333.33 | 133.33 |

## Q3: Round-robin with q = 1

Both workloads from Q1/Q2 are included. The first round starts jobs at 0, 1, 2, giving average response = 1. For 200,200,200, completions are 598,599,600, giving average turnaround = 599. For 100,200,300, completions are 298,499,600, giving average turnaround = 1397/3 = 465.67. RR improves initial response here while delaying completion relative to SJF/FIFO. These observations are for these workloads, not a universal claim for every workload.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q3_rr_equal | 200,200,200 | RR | 1 | 1.00 | 599.00 | 399.00 |
| q3_rr_different | 100,200,300 | RR | 1 | 1.00 | 465.67 | 265.67 |

## Q4: When does SJF have the same turnaround as FIFO?

With all jobs present at time zero, FIFO gives the same per-job turnaround times when the queue is already in nondecreasing length order (allowing ties). Equal job lengths are a special case. If unequal jobs are out of order, SJF moves short jobs ahead, removing long-job blocking and reducing average turnaround. The unsorted example illustrates this convoy effect.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q4_sorted_fifo | 50,100,200 | FIFO | - | 66.67 | 183.33 | 66.67 |
| q4_sorted_sjf | 50,100,200 | SJF | - | 66.67 | 183.33 | 66.67 |
| q4_unsorted_fifo | 300,100,200 | FIFO | - | 233.33 | 433.33 | 233.33 |
| q4_unsorted_sjf | 300,100,200 | SJF | - | 133.33 | 333.33 | 133.33 |

## Q5: When do SJF and RR have the same response times?

A sufficient condition is a queue already in nondecreasing length order with q at least the longest job. RR then finishes every job on its first visit, so it is the same schedule as SJF. More precisely, for sorted positive lengths L1 <= ... <= LN, all per-job first-response times coincide if q >= L(N-1), because the last job's remaining execution cannot affect any job's first start. For N = 1, the response is always zero. The q=200 example with 100,200,300 demonstrates this refinement. If the queue is unsorted, a large q makes RR behave like FIFO, not necessarily like SJF.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q5_sorted_sjf | 100,200,300 | SJF | - | 133.33 | 333.33 | 133.33 |
| q5_sorted_rr | 100,200,300 | RR | 300 | 133.33 | 333.33 | 133.33 |
| q5_sorted_rr_q200 | 100,200,300 | RR | 200 | 133.33 | 333.33 | 133.33 |
| q5_unsorted_sjf | 300,100,200 | SJF | - | 133.33 | 333.33 | 133.33 |
| q5_unsorted_rr | 300,100,200 | RR | 300 | 233.33 | 433.33 | 233.33 |

## Q6: Increasing SJF job lengths

For N equal jobs of length L, the starts are 0,L,...,(N-1)L, so average response = (N-1)L/2. For N=3 this equals L; lengths 10,100,1000 therefore give average responses 10,100,1000. More generally, scaling every job length by k scales SJF response times by k. A long job can still wait behind many shorter jobs even though SJF minimizes average turnaround under these assumptions.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q6_length_10 | 10,10,10 | SJF | - | 10.00 | 20.00 | 10.00 |
| q6_length_100 | 100,100,100 | SJF | - | 100.00 | 200.00 | 100.00 |
| q6_length_1000 | 1000,1000,1000 | SJF | - | 1000.00 | 2000.00 | 1000.00 |

## Q7: RR quantum and worst-case response

For a fixed queue order and all arrivals at zero, the first response of job k is R_k = sum(i=1..k-1) min(L_i,q). Increasing q cannot decrease these first-response times; values saturate once q is at least the earlier jobs' lengths.

Worst-case first response is R_max <= (N-1)q, with equality when the N-1 jobs ahead each run for a full quantum. If every job lasts at least q, average response = (N-1)q/2. The first inequality is a tight upper bound, not an equality for every workload. Short jobs may finish before their quantum, reducing the delay: 1,1,100 with q=10 gives starts 0,1,2, so R_max=2 rather than 20. If each switch costs s, an additional switch-cost model would be required; this simulator does not include it. Response means first service, not completion time or waiting between every later turn.

| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |
|---|---|---|---:|---:|---:|---:|
| q7_q_1 | 100,200,300 | RR | 1 | 1.00 | 465.67 | 265.67 |
| q7_q_2 | 100,200,300 | RR | 2 | 2.00 | 464.67 | 264.67 |
| q7_q_5 | 100,200,300 | RR | 5 | 5.00 | 461.67 | 261.67 |
| q7_q_10 | 100,200,300 | RR | 10 | 10.00 | 456.67 | 256.67 |
| q7_q_50 | 100,200,300 | RR | 50 | 50.00 | 416.67 | 216.67 |
| q7_q_100 | 100,200,300 | RR | 100 | 100.00 | 366.67 | 166.67 |
| q7_q_200 | 100,200,300 | RR | 200 | 133.33 | 333.33 | 133.33 |
| q7_q_300 | 100,200,300 | RR | 300 | 133.33 | 333.33 | 133.33 |
| q7_n_2 | 100,100 | RR | 5 | 2.50 | 197.50 | 97.50 |
| q7_n_3 | 100,100,100 | RR | 5 | 5.00 | 295.00 | 195.00 |
| q7_n_5 | 100,100,100,100,100 | RR | 5 | 10.00 | 490.00 | 390.00 |
| q7_short_jobs | 1,1,100 | RR | 10 | 1.00 | 35.00 | 1.00 |

## References and reproducibility

- OSTEP Chapter 7, Homework (Simulation), questions 1-7: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
- Official simulator: https://github.com/remzi-arpacidusseau/ostep-homework/tree/master/cpu-sched
- Use the installed course-pinned simulator. Its SHA-256 and captured revision are in results.json.
- Each data/*_problem.txt is a no-c run; the corresponding data/*.txt is the -c verification output. Commands and independent per-job calculations are in results.json.
