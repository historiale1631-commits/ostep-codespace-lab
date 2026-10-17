"""Run the course's installed simulator; write reproducible Chapter 7 results.
No submission or Git mutation. Run from the Codespaces repository root.
"""
from pathlib import Path
from collections import deque
import subprocess,sys,json,re,hashlib,datetime

root=Path.cwd();scheduler=root/'ext/ostep-homework/cpu-sched/scheduler.py'
if not scheduler.is_file():raise SystemExit('Run from the course repository root; scheduler.py is missing.')
out=root/'hw/chapter7';data=out/'data';data.mkdir(parents=True,exist_ok=True)
for name in ['analysis.md','README.md','run_experiments.py','results.json']:
 if (out/name).exists() and (out/name).resolve()!=Path(__file__).resolve():raise SystemExit('Refusing to replace existing work: '+str(out/name))

cases=[]
def add(name,jobs,policy,q=1):cases.append(dict(id=name,jobs=jobs,policy=policy,quantum=q))
for p in ['FIFO','SJF']:
 add('q1_'+p.lower(),[200]*3,p);add('q2_'+p.lower(),[100,200,300],p)
add('q3_rr_equal',[200]*3,'RR');add('q3_rr_different',[100,200,300],'RR')
for n,j in [('sorted',[50,100,200]),('unsorted',[300,100,200])]:
 for p in ['FIFO','SJF']:add('q4_'+n+'_'+p.lower(),j,p)
for p in ['SJF','RR']:add('q5_sorted_'+p.lower(),[100,200,300],p,300)
add('q5_sorted_rr_q200',[100,200,300],'RR',200)
for p in ['SJF','RR']:add('q5_unsorted_'+p.lower(),[300,100,200],p,300)
for length in [10,100,1000]:add('q6_length_'+str(length),[length]*3,'SJF')
for q in [1,2,5,10,50,100,200,300]:add('q7_q_'+str(q),[100,200,300],'RR',q)
for n in [2,3,5]:add('q7_n_'+str(n),[100]*n,'RR',5)
add('q7_short_jobs',[1,1,100],'RR',10)

def theoretical(jobs,policy,q):
 remaining=list(jobs);first=[None]*len(jobs);finish=[None]*len(jobs);t=0
 queue=deque(sorted(range(len(jobs)),key=lambda i:jobs[i]) if policy=='SJF' else range(len(jobs)))
 while queue:
  i=queue.popleft()
  if first[i] is None:first[i]=t
  use=min(q,remaining[i]) if policy=='RR' else remaining[i]
  remaining[i]-=use;t+=use
  if remaining[i]>0:queue.append(i)
  else:finish[i]=t
 wait=[finish[i]-jobs[i] for i in range(len(jobs))]
 avg=lambda x:sum(x)/len(x)
 return {'response':first,'turnaround':finish,'wait':wait,'average':[avg(first),avg(finish),avg(wait)]}

num=r'([0-9]+(?:\.[0-9]+)?)'
pattern=r'Average\s*--\s*Response:?\s*'+num+r'\s+Turnaround:?\s*'+num+r'\s+Wait:?\s*'+num
results={}
for c in cases:
 args=[sys.executable,str(scheduler),'-l',','.join(map(str,c['jobs'])),'-p',c['policy'],'-s','1234']
 if c['policy']=='RR':args+=['-q',str(c['quantum'])]
 expectation=theoretical(c['jobs'],c['policy'],c['quantum'])
 for suffix,extra in [('problem',[]),('solution',['-c'])]:
  p=subprocess.run(args+extra,capture_output=True,text=True,encoding='utf-8')
  if p.returncode:raise RuntimeError(p.stderr or p.stdout)
  target=data/(c['id']+('_problem' if suffix=='problem' else '')+'.txt')
  if target.exists():raise RuntimeError('Existing result: '+str(target))
  target.write_text(p.stdout,'utf-8')
  if suffix=='solution':
   m=re.search(pattern,p.stdout)
   if not m:raise RuntimeError('Unexpected simulator output: '+p.stdout[-1500:])
   actual=list(map(float,m.groups()))
   assert all(abs(x-y)<0.011 for x,y in zip(expectation['average'],actual)),(c,actual,expectation)
 c.update(expectation,simulator_average=actual,command='python3 ./ext/ostep-homework/cpu-sched/scheduler.py '+' '.join(args[2:])+' -c')
 results[c['id']]=c
 print('Verified',c['id'],actual,flush=True)

def table(ids):
 lines=['| Experiment | Jobs | Policy | q | Avg response | Avg turnaround | Avg wait |','|---|---|---|---:|---:|---:|---:|']
 for id_ in ids:
  c=results[id_];a=c['simulator_average'];lines.append('| '+id_+' | '+','.join(map(str,c['jobs']))+' | '+c['policy']+' | '+(str(c['quantum']) if c['policy']=='RR' else '-')+' | '+' | '.join(f'{v:.2f}' for v in a)+' |')
 return '\n'.join(lines)
def t(prefix):return table([c['id'] for c in cases if c['id'].startswith(prefix)])

analysis='''# Chapter 7: CPU Scheduling Analysis

## Method and assumptions

All jobs arrive at t = 0, use only the CPU, and have positive known execution lengths. There is no context-switch overhead in this simulator. Response time = first start - arrival; turnaround time = completion - arrival; wait time = turnaround - CPU execution length.

For each experiment, the expected times are calculated from the scheduling rules and compared with scheduler.py. The data directory contains both the problem run (without -c) and the verification run (with -c). Reported averages agree with the independent calculations.

## Q1: Three jobs of length 200, FIFO and SJF

Equal lengths give the same ordering (ties keep job order). First starts are 0, 200, 400; completions are 200, 400, 600. Thus average response = 200 and average turnaround = 400. Average wait is also 200.

{{Q1}}

## Q2: Jobs of length 100, 200, 300

The input is already shortest-first, so FIFO and SJF coincide. First starts are 0, 100, 300; completions are 100, 300, 600. Average response = 400/3 = 133.33; average turnaround = 1000/3 = 333.33.

{{Q2}}

## Q3: Round-robin with q = 1

Both workloads from Q1/Q2 are included. The first round starts jobs at 0, 1, 2, giving average response = 1. For 200,200,200, completions are 598,599,600, giving average turnaround = 599. For 100,200,300, completions are 298,499,600, giving average turnaround = 1397/3 = 465.67. RR improves initial response here while delaying completion relative to SJF/FIFO. These observations are for these workloads, not a universal claim for every workload.

{{Q3}}

## Q4: When does SJF have the same turnaround as FIFO?

With all jobs present at time zero, FIFO gives the same per-job turnaround times when the queue is already in nondecreasing length order (allowing ties). Equal job lengths are a special case. If unequal jobs are out of order, SJF moves short jobs ahead, removing long-job blocking and reducing average turnaround. The unsorted example illustrates this convoy effect.

{{Q4}}

## Q5: When do SJF and RR have the same response times?

A sufficient condition is a queue already in nondecreasing length order with q at least the longest job. RR then finishes every job on its first visit, so it is the same schedule as SJF. More precisely, for sorted positive lengths L1 <= ... <= LN, all per-job first-response times coincide if q >= L(N-1), because the last job's remaining execution cannot affect any job's first start. For N = 1, the response is always zero. The q=200 example with 100,200,300 demonstrates this refinement. If the queue is unsorted, a large q makes RR behave like FIFO, not necessarily like SJF.

{{Q5}}

## Q6: Increasing SJF job lengths

For N equal jobs of length L, the starts are 0,L,...,(N-1)L, so average response = (N-1)L/2. For N=3 this equals L; lengths 10,100,1000 therefore give average responses 10,100,1000. More generally, scaling every job length by k scales SJF response times by k. A long job can still wait behind many shorter jobs even though SJF minimizes average turnaround under these assumptions.

{{Q6}}

## Q7: RR quantum and worst-case response

For a fixed queue order and all arrivals at zero, the first response of job k is R_k = sum(i=1..k-1) min(L_i,q). Increasing q cannot decrease these first-response times; values saturate once q is at least the earlier jobs' lengths.

Worst-case first response is R_max <= (N-1)q, with equality when the N-1 jobs ahead each run for a full quantum. If every job lasts at least q, average response = (N-1)q/2. The first inequality is a tight upper bound, not an equality for every workload. Short jobs may finish before their quantum, reducing the delay: 1,1,100 with q=10 gives starts 0,1,2, so R_max=2 rather than 20. If each switch costs s, an additional switch-cost model would be required; this simulator does not include it. Response means first service, not completion time or waiting between every later turn.

{{Q7}}

## References and reproducibility

- OSTEP Chapter 7, Homework (Simulation), questions 1-7: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
- Official simulator: https://github.com/remzi-arpacidusseau/ostep-homework/tree/master/cpu-sched
- Use the installed course-pinned simulator. Its SHA-256 and captured revision are in results.json.
- Each data/*_problem.txt is a no-c run; the corresponding data/*.txt is the -c verification output. Commands and independent per-job calculations are in results.json.
'''
for i in range(1,8):analysis=analysis.replace('{{Q'+str(i)+'}}',t('q'+str(i)+'_'))
(out/'analysis.md').write_text(analysis,'utf-8')
(out/'README.md').write_text('''# Chapter 7: Scheduling

Compares FIFO, SJF, and RR for OSTEP Chapter 7 questions 1-7.

- analysis.md: English explanations, formulas, and experiment tables.
- data/: problem and verified simulator outputs, two files per experiment.
- results.json: commands, independent calculations, simulator averages, and provenance.
- run_experiments.py: reproducible experiment generator. Run from the repository root; it refuses to overwrite existing report files. Use a separate copy of the repository to rerun.

All tasks arrive at zero; no I/O or context-switch cost is modeled. Commands and results are recorded for reproducibility. Explicit job lists are used, so the seed does not change the chosen workloads.

Highlights: SJF and FIFO match for an already sorted workload. RR with q=1 gives faster first response on the chosen workloads. A tight RR first-response upper bound is (N-1)q; it is not always an equality.
''','utf-8')
rev=subprocess.run(['git','-C',str(scheduler.parents[1]),'rev-parse','HEAD'],capture_output=True,text=True)
meta={'scheduler_sha256':hashlib.sha256(scheduler.read_bytes()).hexdigest(),'scheduler_revision':rev.stdout.strip() if rev.returncode==0 else 'unavailable','python_version':sys.version,'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'experiment_count':len(cases),'all_averages_verified':True,'experiments':cases}
(out/'results.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),'utf-8')
this=Path(__file__)
if this.is_file():(out/'run_experiments.py').write_bytes(this.read_bytes())
print('DONE:',len(cases),'experiments;',len(cases)*2,'raw files. No Git commit or push performed.',flush=True)
