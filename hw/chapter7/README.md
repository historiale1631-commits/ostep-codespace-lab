# Chapter 7: Scheduling

Compares FIFO, SJF, and RR for OSTEP Chapter 7 questions 1-7.

- analysis.md: English explanations, formulas, and experiment tables.
- data/: problem and verified simulator outputs, two files per experiment.
- results.json: commands, independent calculations, simulator averages, and provenance.
- run_experiments.py: reproducible experiment generator. Run from the repository root; it refuses to overwrite existing report files. Use a separate copy of the repository to rerun.

All tasks arrive at zero; no I/O or context-switch cost is modeled. Commands and results are recorded for reproducibility. Explicit job lists are used, so the seed does not change the chosen workloads.

Highlights: SJF and FIFO match for an already sorted workload. RR with q=1 gives faster first response on the chosen workloads. A tight RR first-response upper bound is (N-1)q; it is not always an equality.
