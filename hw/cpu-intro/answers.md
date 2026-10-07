# OSTEP Ch.4 Homework Answers
## Q1
- Prediction / 预测: 总时间 10，CPU 利用率 100%，状态表如下
```
Time  PID 0    PID 1    CPU  IOs
1     RUN:cpu  READY    1
2     RUN:cpu  READY    1
3     RUN:cpu  READY    1
4     RUN:cpu  READY    1
5     RUN:cpu  READY    1
6     DONE     RUN:cpu  1
7     DONE     RUN:cpu  1
8     DONE     RUN:cpu  1
9     DONE     RUN:cpu  1
10    DONE     RUN:cpu  1
```
- Reasoning / 理由: 两个进程都只有 CPU 指令，没有 I/O。PID 0 先跑，因为没有 I/O，系统不会中途换进程，所以 PID 0 一口气跑完 5 条，PID 1 只能在旁边等（READY）。PID 0 做完（DONE）以后才轮到 PID 1 跑它的 5 条。整个过程 CPU 一直有活干，没有空闲的 tick，所以一共 10 个 tick，CPU 利用率 100%。
- Verified result / 验证结果: q1.txt：Total Time 10，CPU Busy 10（100.00%），IO Busy 0（0.00%）
- Analysis / 分析: 预测正确，状态表和 q1.txt 每一行都一样。两个进程都没有 I/O，所以每个 tick 都有进程在用 CPU，IO Busy 是 0。这题说明只有 CPU 工作时，进程只是排队轮流用 CPU，CPU 不会空闲。

## Q2
- Prediction / 预测: 总时间 11，CPU 利用率 6/11 ≈ 54.55%，状态表如下
```
Time  PID 0    PID 1        CPU  IOs
1     RUN:cpu  READY        1
2     RUN:cpu  READY        1
3     RUN:cpu  READY        1
4     RUN:cpu  READY        1
5     DONE     RUN:io       1
6     DONE     BLOCKED           1
7     DONE     BLOCKED           1
8     DONE     BLOCKED           1
9     DONE     BLOCKED           1
10    DONE     BLOCKED           1
11*   DONE     RUN:io_done  1
```
- Reasoning / 理由: PID 0 是 4 条 CPU 指令，PID 1 只做一次 I/O。PID 0 先跑，没有 I/O 就不会切换，所以它连续跑 4 个 tick，PID 1 只能等（READY）。PID 0 结束后，PID 1 在第 5 个 tick 发起 I/O（RUN:io），然后 BLOCKED 等 5 个 tick。这时 PID 0 已经结束，没有别的进程可以用 CPU，所以 CPU 空闲了 5 个 tick。第 11 个 tick I/O 完成，PID 1 再用 1 个 tick 处理完成（RUN:io_done）。一次 I/O 一共要 1 + 5 + 1 = 7 个 tick，所以总时间 = 4 + 7 = 11，CPU 忙 6 个 tick，利用率 6/11 ≈ 54.55%。
- Verified result / 验证结果: q2.txt：Total Time 11，CPU Busy 6（54.55%），IO Busy 5（45.45%）
- Analysis / 分析: 预测正确。关键是一次 I/O 要算 RUN:io 1 + BLOCKED 5 + RUN:io_done 1 = 7 个 tick，不是只有 5 个。I/O 放在最后才做，等 I/O 的 5 个 tick 里 PID 0 已经结束，没有进程可以用 CPU，所以利用率只有 54.55%。

## Q3
- Prediction / 预测: 总时间 7，CPU 利用率 6/7 ≈ 85.71%，状态表如下
```
Time  PID 0        PID 1    CPU  IOs
1     RUN:io       READY    1
2     BLOCKED      RUN:cpu  1    1
3     BLOCKED      RUN:cpu  1    1
4     BLOCKED      RUN:cpu  1    1
5     BLOCKED      RUN:cpu  1    1
6     BLOCKED      DONE          1
7*    RUN:io_done  DONE     1
```
- Reasoning / 理由: 这次 PID 0 先做 I/O。它在第 1 个 tick 发起 I/O（RUN:io）后进入 BLOCKED，默认规则 SWITCH_ON_IO 会在发起 I/O 时马上切换，所以 PID 1 可以在 tick 2~5 用 CPU 跑完 4 条指令，这段时间 CPU 和 I/O 同时在工作。PID 0 要 BLOCKED 满 5 个 tick（tick 2~6），所以 tick 6 PID 1 已经结束，PID 0 还在等，CPU 空闲 1 个 tick。tick 7 I/O 完成，PID 0 用 1 个 tick 处理完成（RUN:io_done）。总时间 7，CPU 忙 1 + 4 + 1 = 6 个 tick，利用率 6/7 ≈ 85.71%。和 Q2 的工作量一样，只换了顺序，总时间就从 11 减少到 7。
- Verified result / 验证结果: q3.txt：Total Time 7，CPU Busy 6（85.71%），IO Busy 5（71.43%）
- Analysis / 分析: 预测正确。和 Q2 相比只是先做 I/O，PID 1 的 CPU 工作就和 PID 0 的 I/O 等待重叠了，总时间从 11 变成 7。只有 tick 6 CPU 空闲，因为 PID 1 只有 4 条指令，比 5 个 tick 的 I/O 等待少 1 个。IO Busy 也从 45.45% 提高到 71.43%。

## Q4
- Prediction / 预测: 总时间 11，CPU 利用率 6/11 ≈ 54.55%，状态表如下
```
Time  PID 0        PID 1    CPU  IOs
1     RUN:io       READY    1
2     BLOCKED      READY         1
3     BLOCKED      READY         1
4     BLOCKED      READY         1
5     BLOCKED      READY         1
6     BLOCKED      READY         1
7*    RUN:io_done  READY    1
8     DONE         RUN:cpu  1
9     DONE         RUN:cpu  1
10    DONE         RUN:cpu  1
11    DONE         RUN:cpu  1
```
- Reasoning / 理由: -S SWITCH_ON_END 表示只有进程结束才切换，发起 I/O 时不切换。PID 0 在 tick 1 发起 I/O 后，tick 2~6 一直 BLOCKED，但系统不会把 CPU 交给 PID 1，所以 PID 1 只能 READY，CPU 空闲 5 个 tick。tick 7 PID 0 处理完 I/O 结束后，PID 1 才在 tick 8~11 跑完 4 条指令。总时间 = 7 + 4 = 11，CPU 忙 6 个 tick，利用率 6/11 ≈ 54.55%。
- Verified result / 验证结果: q4.txt：Total Time 11，CPU Busy 6（54.55%），IO Busy 5（45.45%）
- Analysis / 分析: 预测正确。要注意 tick 2~6 PID 1 是 READY 而不是 BLOCKED，因为它不是在等 I/O，而是在等 CPU。SWITCH_ON_END 让 CPU 在 I/O 等待时白白空闲，所以虽然进程顺序和 Q3 一样，结果却和 Q2 一样是 11 个 tick。

## Q5
- Prediction / 预测: 总时间 7，CPU 利用率 6/7 ≈ 85.71%，状态表如下
```
Time  PID 0        PID 1    CPU  IOs
1     RUN:io       READY    1
2     BLOCKED      RUN:cpu  1    1
3     BLOCKED      RUN:cpu  1    1
4     BLOCKED      RUN:cpu  1    1
5     BLOCKED      RUN:cpu  1    1
6     BLOCKED      DONE          1
7*    RUN:io_done  DONE     1
```
- Reasoning / 理由: SWITCH_ON_IO 是默认规则，所以这题和 Q3 是同一个命令，结果也一样。PID 0 一发起 I/O，系统就切换给 PID 1，PID 1 的 4 个 CPU tick 和 PID 0 等 I/O 的时间重叠了。和 Q4 比，同样的工作只要 7 个 tick，少了 4 个 tick，CPU 利用率从 54.55% 提高到 85.71%。所以在 I/O 时切换进程，可以让 CPU 在等待 I/O 的时候也有事做。
- Verified result / 验证结果: q5.txt：Total Time 7，CPU Busy 6（85.71%），IO Busy 5（71.43%）
- Analysis / 分析: 预测正确，结果和 Q3 完全一样，说明 SWITCH_ON_IO 就是默认设置。和 Q4 对比，在 I/O 时切换进程让总时间从 11 减到 7，CPU 利用率从 54.55% 提高到 85.71%。

## Q6
- Prediction / 预测: 总时间 31，CPU 利用率 21/31 ≈ 67.74%，状态表如下
```
Time  PID 0        PID 1    PID 2    PID 3    CPU  IOs
1     RUN:io       READY    READY    READY    1
2     BLOCKED      RUN:cpu  READY    READY    1    1
3     BLOCKED      RUN:cpu  READY    READY    1    1
4     BLOCKED      RUN:cpu  READY    READY    1    1
5     BLOCKED      RUN:cpu  READY    READY    1    1
6     BLOCKED      RUN:cpu  READY    READY    1    1
7*    READY        DONE     RUN:cpu  READY    1
8     READY        DONE     RUN:cpu  READY    1
9     READY        DONE     RUN:cpu  READY    1
10    READY        DONE     RUN:cpu  READY    1
11    READY        DONE     RUN:cpu  READY    1
12    READY        DONE     DONE     RUN:cpu  1
13    READY        DONE     DONE     RUN:cpu  1
14    READY        DONE     DONE     RUN:cpu  1
15    READY        DONE     DONE     RUN:cpu  1
16    READY        DONE     DONE     RUN:cpu  1
17    RUN:io_done  DONE     DONE     DONE     1
18    RUN:io       DONE     DONE     DONE     1
19    BLOCKED      DONE     DONE     DONE          1
20    BLOCKED      DONE     DONE     DONE          1
21    BLOCKED      DONE     DONE     DONE          1
22    BLOCKED      DONE     DONE     DONE          1
23    BLOCKED      DONE     DONE     DONE          1
24*   RUN:io_done  DONE     DONE     DONE     1
25    RUN:io       DONE     DONE     DONE     1
26    BLOCKED      DONE     DONE     DONE          1
27    BLOCKED      DONE     DONE     DONE          1
28    BLOCKED      DONE     DONE     DONE          1
29    BLOCKED      DONE     DONE     DONE          1
30    BLOCKED      DONE     DONE     DONE          1
31*   RUN:io_done  DONE     DONE     DONE     1
```
- Reasoning / 理由: PID 0 在 tick 1 发起 I/O 后切换给 PID 1。PID 0 的 I/O 在 tick 7 完成，但 IO_RUN_LATER 规则下它只是变成 READY，要排队。PID 1 结束后轮到 PID 2，PID 2 结束后按顺序先轮到 PID 3，所以 PID 0 一直等到 tick 17 才运行。这时 PID 1~3 都已经结束，PID 0 后面两次 I/O 的 BLOCKED 期间（tick 19~23、26~30）没有别的进程可以用 CPU，CPU 空闲 10 个 tick。而 tick 7~18 又没有 I/O 在进行，I/O 设备也是空闲的。总时间 31，CPU 忙 21 个 tick，利用率 21/31 ≈ 67.74%。所以系统资源没有被有效利用：CPU 和 I/O 设备没有同时工作。
- Verified result / 验证结果: q6.txt：Total Time 31，CPU Busy 21（67.74%），IO Busy 15（48.39%）
- Analysis / 分析: 预测正确。q6.txt 里 tick 7~16 PID 0 一直是 READY，说明 IO_RUN_LATER 下 I/O 完成的进程要排队，等 PID 2、PID 3 都跑完才轮到它。结果 IO Busy 只有 48.39%，I/O 设备一半以上的时间没事干，CPU 也空了 10 个 tick，两种资源都没有被充分利用。

## Q7
- Prediction / 预测: 总时间 21，CPU 利用率 21/21 = 100%，状态表如下
```
Time  PID 0        PID 1    PID 2    PID 3    CPU  IOs
1     RUN:io       READY    READY    READY    1
2     BLOCKED      RUN:cpu  READY    READY    1    1
3     BLOCKED      RUN:cpu  READY    READY    1    1
4     BLOCKED      RUN:cpu  READY    READY    1    1
5     BLOCKED      RUN:cpu  READY    READY    1    1
6     BLOCKED      RUN:cpu  READY    READY    1    1
7*    RUN:io_done  DONE     READY    READY    1
8     RUN:io       DONE     READY    READY    1
9     BLOCKED      DONE     RUN:cpu  READY    1    1
10    BLOCKED      DONE     RUN:cpu  READY    1    1
11    BLOCKED      DONE     RUN:cpu  READY    1    1
12    BLOCKED      DONE     RUN:cpu  READY    1    1
13    BLOCKED      DONE     RUN:cpu  READY    1    1
14*   RUN:io_done  DONE     DONE     READY    1
15    RUN:io       DONE     DONE     READY    1
16    BLOCKED      DONE     DONE     RUN:cpu  1    1
17    BLOCKED      DONE     DONE     RUN:cpu  1    1
18    BLOCKED      DONE     DONE     RUN:cpu  1    1
19    BLOCKED      DONE     DONE     RUN:cpu  1    1
20    BLOCKED      DONE     DONE     RUN:cpu  1    1
21*   RUN:io_done  DONE     DONE     DONE     1
```
- Reasoning / 理由: IO_RUN_IMMEDIATE 让 I/O 完成的进程马上运行。PID 0 的 I/O 在 tick 7 完成后立刻抢回 CPU，处理完成（io_done）后在 tick 8 马上发起下一次 I/O，然后切换给 PID 2。之后每次 PID 0 等 I/O 的 5 个 tick，正好有一个 CPU 进程跑 5 条指令，CPU 和 I/O 一直同时工作，CPU 没有空闲过。总时间 21，CPU 利用率 100%。和 Q6 相比少了 10 个 tick。让刚完成 I/O 的进程马上运行是好主意，因为这种进程只需要用很短的 CPU 就会发起下一次 I/O，让它先跑，I/O 设备就能早点开始工作，CPU 在它等 I/O 时还可以去跑别的进程。
- Verified result / 验证结果: q7.txt：Total Time 21，CPU Busy 21（100.00%），IO Busy 15（71.43%）
- Analysis / 分析: 预测正确。tick 7 和 tick 14 PID 0 的 I/O 一完成就抢到 CPU，原本要运行的进程变回 READY。和 Q6 相比，CPU 利用率从 67.74% 提高到 100%，IO Busy 从 48.39% 提高到 71.43%，CPU 和 I/O 设备都更忙了，总时间少了 10 个 tick。这说明对频繁做 I/O 的进程，I/O 完成后马上运行能让 CPU 和 I/O 更好地重叠。

## Q8
- Prediction / 预测: 每个种子先看指令列表，再分别预测 3 种设置（default = SWITCH_ON_IO + IO_RUN_LATER）

### seed 1
指令列表：PID 0 = cpu, io, io_done, io, io_done；PID 1 = cpu, cpu, cpu

**default：总时间 15，CPU 利用率 8/15 ≈ 53.33%**
```
Time  PID 0        PID 1    CPU  IOs
1     RUN:cpu      READY    1
2     RUN:io       READY    1
3     BLOCKED      RUN:cpu  1    1
4     BLOCKED      RUN:cpu  1    1
5     BLOCKED      RUN:cpu  1    1
6     BLOCKED      DONE          1
7     BLOCKED      DONE          1
8*    RUN:io_done  DONE     1
9     RUN:io       DONE     1
10    BLOCKED      DONE          1
11    BLOCKED      DONE          1
12    BLOCKED      DONE          1
13    BLOCKED      DONE          1
14    BLOCKED      DONE          1
15*   RUN:io_done  DONE     1
```

**-I IO_RUN_IMMEDIATE：总时间 15，CPU 利用率 8/15 ≈ 53.33%，状态表和 default 完全一样**

**-S SWITCH_ON_END：总时间 18，CPU 利用率 8/18 ≈ 44.44%**
```
Time  PID 0        PID 1    CPU  IOs
1     RUN:cpu      READY    1
2     RUN:io       READY    1
3     BLOCKED      READY         1
4     BLOCKED      READY         1
5     BLOCKED      READY         1
6     BLOCKED      READY         1
7     BLOCKED      READY         1
8*    RUN:io_done  READY    1
9     RUN:io       READY    1
10    BLOCKED      READY         1
11    BLOCKED      READY         1
12    BLOCKED      READY         1
13    BLOCKED      READY         1
14    BLOCKED      READY         1
15*   RUN:io_done  READY    1
16    DONE         RUN:cpu  1
17    DONE         RUN:cpu  1
18    DONE         RUN:cpu  1
```

seed 1 理由：PID 0 在 tick 2 发起第 1 次 I/O 后切换给 PID 1，PID 1 的 3 个 CPU tick（3~5）和 I/O 重叠。但 PID 1 只有 3 条指令，tick 6~7 PID 0 还在等，CPU 空闲。PID 0 第 2 次 I/O（tick 10~14）时 PID 1 已经结束，CPU 又空闲 5 个 tick。IO_RUN_IMMEDIATE 结果一样，因为 PID 0 的 I/O 完成时 PID 1 已经结束，没有正在运行的进程可以被抢。SWITCH_ON_END 时 PID 1 要等 PID 0 全部做完（1 + 7 + 7 = 15 个 tick）才能运行，所以总时间变成 15 + 3 = 18。
### seed 2
指令列表：PID 0 = io, io_done, io, io_done, cpu；PID 1 = cpu, io, io_done, io, io_done

**default：总时间 16，CPU 利用率 10/16 = 62.50%**
```
Time  PID 0        PID 1        CPU  IOs
1     RUN:io       READY        1
2     BLOCKED      RUN:cpu      1    1
3     BLOCKED      RUN:io       1    1
4     BLOCKED      BLOCKED           2
5     BLOCKED      BLOCKED           2
6     BLOCKED      BLOCKED           2
7*    RUN:io_done  BLOCKED      1    1
8     RUN:io       BLOCKED      1    1
9*    BLOCKED      RUN:io_done  1    1
10    BLOCKED      RUN:io       1    1
11    BLOCKED      BLOCKED           2
12    BLOCKED      BLOCKED           2
13    BLOCKED      BLOCKED           2
14*   RUN:io_done  BLOCKED      1    1
15    RUN:cpu      BLOCKED      1    1
16*   DONE         RUN:io_done  1
```

**-I IO_RUN_IMMEDIATE：总时间 16，CPU 利用率 10/16 = 62.50%，状态表和 default 完全一样**

**-S SWITCH_ON_END：总时间 30，CPU 利用率 10/30 ≈ 33.33%**
```
Time  PID 0        PID 1        CPU  IOs
1     RUN:io       READY        1
2     BLOCKED      READY             1
3     BLOCKED      READY             1
4     BLOCKED      READY             1
5     BLOCKED      READY             1
6     BLOCKED      READY             1
7*    RUN:io_done  READY        1
8     RUN:io       READY        1
9     BLOCKED      READY             1
10    BLOCKED      READY             1
11    BLOCKED      READY             1
12    BLOCKED      READY             1
13    BLOCKED      READY             1
14*   RUN:io_done  READY        1
15    RUN:cpu      READY        1
16    DONE         RUN:cpu      1
17    DONE         RUN:io       1
18    DONE         BLOCKED           1
19    DONE         BLOCKED           1
20    DONE         BLOCKED           1
21    DONE         BLOCKED           1
22    DONE         BLOCKED           1
23*   DONE         RUN:io_done  1
24    DONE         RUN:io       1
25    DONE         BLOCKED           1
26    DONE         BLOCKED           1
27    DONE         BLOCKED           1
28    DONE         BLOCKED           1
29    DONE         BLOCKED           1
30*   DONE         RUN:io_done  1
```

seed 2 理由：两个进程都有 2 次 I/O。default 下 PID 0 在 tick 1 发起 I/O 后切换给 PID 1，PID 1 跑 1 条 cpu 后在 tick 3 也发起 I/O，所以 tick 4~6 两个 I/O 同时进行（IOs = 2），但两个进程都在 BLOCKED，CPU 空闲。之后 tick 11~13 又是两个都在等，CPU 再空闲 3 个 tick。总时间 16，CPU 利用率 10/16 = 62.50%。IO_RUN_IMMEDIATE 结果一样，因为每次 I/O 完成时另一个进程不是 BLOCKED 就是 DONE，没有正在运行的进程可以被抢。SWITCH_ON_END 时两个进程完全不能重叠，PID 0 自己要 7 + 7 + 1 = 15 个 tick，PID 1 也要 1 + 7 + 7 = 15 个 tick，加起来 30，CPU 利用率只有 33.33%。

### seed 3
指令列表：PID 0 = cpu, io, io_done, cpu；PID 1 = io, io_done, io, io_done, cpu

**default：总时间 18，CPU 利用率 9/18 = 50.00%**
```
Time  PID 0        PID 1        CPU  IOs
1     RUN:cpu      READY        1
2     RUN:io       READY        1
3     BLOCKED      RUN:io       1    1
4     BLOCKED      BLOCKED           2
5     BLOCKED      BLOCKED           2
6     BLOCKED      BLOCKED           2
7     BLOCKED      BLOCKED           2
8*    RUN:io_done  BLOCKED      1    1
9*    RUN:cpu      READY        1
10    DONE         RUN:io_done  1
11    DONE         RUN:io       1
12    DONE         BLOCKED           1
13    DONE         BLOCKED           1
14    DONE         BLOCKED           1
15    DONE         BLOCKED           1
16    DONE         BLOCKED           1
17*   DONE         RUN:io_done  1
18    DONE         RUN:cpu      1
```

**-I IO_RUN_IMMEDIATE：总时间 17，CPU 利用率 9/17 ≈ 52.94%**
```
Time  PID 0        PID 1        CPU  IOs
1     RUN:cpu      READY        1
2     RUN:io       READY        1
3     BLOCKED      RUN:io       1    1
4     BLOCKED      BLOCKED           2
5     BLOCKED      BLOCKED           2
6     BLOCKED      BLOCKED           2
7     BLOCKED      BLOCKED           2
8*    RUN:io_done  BLOCKED      1    1
9*    READY        RUN:io_done  1
10    READY        RUN:io       1
11    RUN:cpu      BLOCKED      1    1
12    DONE         BLOCKED           1
13    DONE         BLOCKED           1
14    DONE         BLOCKED           1
15    DONE         BLOCKED           1
16*   DONE         RUN:io_done  1
17    DONE         RUN:cpu      1
```

**-S SWITCH_ON_END：总时间 24，CPU 利用率 9/24 = 37.50%**
```
Time  PID 0        PID 1        CPU  IOs
1     RUN:cpu      READY        1
2     RUN:io       READY        1
3     BLOCKED      READY             1
4     BLOCKED      READY             1
5     BLOCKED      READY             1
6     BLOCKED      READY             1
7     BLOCKED      READY             1
8*    RUN:io_done  READY        1
9     RUN:cpu      READY        1
10    DONE         RUN:io       1
11    DONE         BLOCKED           1
12    DONE         BLOCKED           1
13    DONE         BLOCKED           1
14    DONE         BLOCKED           1
15    DONE         BLOCKED           1
16*   DONE         RUN:io_done  1
17    DONE         RUN:io       1
18    DONE         BLOCKED           1
19    DONE         BLOCKED           1
20    DONE         BLOCKED           1
21    DONE         BLOCKED           1
22    DONE         BLOCKED           1
23*   DONE         RUN:io_done  1
24    DONE         RUN:cpu      1
```

seed 3 理由：default 下 tick 4~7 两个进程都在等 I/O，CPU 空闲。tick 9 PID 1 的 I/O 完成，但 PID 0 正在运行，RUN_LATER 规则下 PID 0 继续跑完最后一条 cpu，PID 1 到 tick 11 才发起第 2 次 I/O，这次等待时 PID 0 已经结束，CPU 又空闲 5 个 tick，总时间 18。IO_RUN_IMMEDIATE 时 PID 1 在 tick 9 马上抢回 CPU，tick 10 就发起第 2 次 I/O，PID 0 的最后一条 cpu 挪到 tick 11，和 PID 1 的 I/O 重叠，所以总时间少 1 个 tick，变成 17。SWITCH_ON_END 时不能重叠，PID 0 要 1 + 7 + 1 = 9 个 tick，PID 1 要 7 + 7 + 1 = 15 个 tick，总时间 24。

- Reasoning / 理由: 总结：SWITCH_ON_END 在 3 个种子里都是最慢的（18、30、24），因为进程等 I/O 时不切换，CPU 只能空着，CPU 和 I/O 不能重叠。IO_RUN_IMMEDIATE 只有在 I/O 完成的那一刻刚好有别的进程在运行时才有区别：seed 1 和 seed 2 每次 I/O 完成时另一个进程都不在运行，所以结果和 default 一样；seed 3 在 tick 9 PID 1 的 I/O 完成时 PID 0 正在运行，马上运行 PID 1 能让它早 1 个 tick 发起下一次 I/O，所以总时间从 18 降到 17。
- Verified result / 验证结果:
  - seed 1：default 15（CPU 53.33%，IO 66.67%）；IO_RUN_IMMEDIATE 15（CPU 53.33%，IO 66.67%）；SWITCH_ON_END 18（CPU 44.44%，IO 55.56%）
  - seed 2：default 16（CPU 62.50%，IO 87.50%）；IO_RUN_IMMEDIATE 16（CPU 62.50%，IO 87.50%）；SWITCH_ON_END 30（CPU 33.33%，IO 66.67%）
  - seed 3：default 18（CPU 50.00%，IO 61.11%）；IO_RUN_IMMEDIATE 17（CPU 52.94%，IO 64.71%）；SWITCH_ON_END 24（CPU 37.50%，IO 62.50%）
- Analysis / 分析: 9 个结果全部预测正确，seed 1、seed 2 的 IO_RUN_IMMEDIATE 和 default 的状态表也确实完全一样。SWITCH_ON_END 每次都最慢，seed 2 甚至从 16 变成 30，因为两个进程都有很多 I/O，不切换就完全不能重叠。另外 seed 2 的 IO Busy 最高（87.50%），CPU 利用率却只有 62.50%，因为两个进程经常同时在等 I/O，这时不管用什么调度规则，CPU 都没有进程可以运行。IO_RUN_IMMEDIATE 只在 seed 3 有用，因为只有 seed 3 出现了"I/O 完成时另一个进程正在运行"的情况。

