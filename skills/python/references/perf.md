# Python Performance Optimization

Profile first, optimize second. Use for CPU, memory, I/O, database, and data-pipeline bottlenecks.

## Use When

- reducing latency or resource use
- finding CPU hotspots
- reducing memory growth/leaks
- improving DB/query performance
- speeding I/O/data processing
- deciding if caching, async, multiprocessing, or native code is justified

## Rule

Never optimize from vibes. Measure representative workload, change one thing, remeasure.

## Profiling Choice

| Need                       | Tool/Pattern                         |
| -------------------------- | ------------------------------------ |
| function-level CPU         | `cProfile`, `pstats`                 |
| line-level CPU             | `line_profiler`                      |
| production sampling        | `py-spy`                             |
| memory allocation/leak     | `memory_profiler`, `tracemalloc`     |
| microbenchmark             | `timeit`, `pytest-benchmark`         |
| DB query plan              | `EXPLAIN`, ORM/query logging         |
| I/O wait/concurrency       | timing around awaits/calls + metrics |

## Baseline Commands

```bash
python -m cProfile -o output.prof script.py
python -m pstats output.prof
py-spy top --pid <pid>
py-spy record -o profile.svg -- python script.py
pytest test_perf.py --benchmark-only
```

Inside `pstats`: `sort cumtime`, then `stats 10`.

## Metrics

- wall time
- CPU time
- peak memory
- allocation count
- I/O wait
- query count/latency
- throughput
- p95/p99 latency for services

## Optimization Order

1. algorithm/data structure
2. reduce I/O/query count
3. batch work
4. cache pure/repeated computation
5. stream/generate instead of materializing
6. remove hot-loop overhead
7. parallelize only after proving CPU/I/O shape
8. native extension only for stable hot path

## Python Patterns

Prefer:

- list/dict/set comprehensions for simple transformations
- generator expressions for streaming/large inputs
- `"".join(parts)` for many string fragments
- dict/set lookup over linear search
- local variable binding in tight loops only when measured
- `functools.lru_cache` for pure repeated calls
- `dataclass(slots=True)` or `__slots__` for many small objects

Avoid:

- building giant lists when iteration is enough
- repeated string concatenation in loops
- broad caching with unbounded keys
- optimizing readability away without measured gain
- multiprocessing for I/O-bound work
- async for CPU-bound work

## Memory

- stream files and API responses
- use iterators/generators for large sequences
- release large temporaries promptly
- inspect object retention with `tracemalloc`
- use weakrefs only when object lifecycle requires it
- prefer bounded caches

## Database

- batch inserts/updates
- select only needed columns
- add indexes for common filters/joins
- inspect query plans
- avoid N+1 queries
- paginate unbounded reads
- measure ORM overhead before bypassing it

## Concurrency Choice

| Workload     | Use                                         |
| ------------ | ------------------------------------------- |
| CPU-bound    | multiprocessing, native code, vectorization |
| I/O-bound    | async I/O or thread pool                    |
| DB-bound     | better queries, batching, pooling           |
| memory-bound | streaming, smaller objects, chunking        |

## Benchmark Hygiene

- warm up when relevant
- use representative data size
- isolate noise
- compare before/after in same env
- report confidence/variance when using benchmark tools
- keep perf tests separate from normal fast unit suite unless cheap

## Review Checklist

- [ ] baseline captured
- [ ] bottleneck identified by tool output
- [ ] change targets hotspot
- [ ] correctness tests still pass
- [ ] before/after measurement recorded
- [ ] complexity increase justified by measurable gain
- [ ] rollback path clear

## Red Flags

- no benchmark or profiler output
- "faster" change touches many unrelated modules
- unbounded cache
- async mixed into sync path without end-to-end design
- large memory materialization from convenience helper
- query inside loop
- premature native-code dependency
