# Bismillah.

# Operating Systems — Slide-Complete Viva Recall

This is the **full OS preparation layer**. It follows the current CSE 313 sources: OS structure, processes and threads, scheduling, IPC and synchronization, deadlock, memory virtualization, I/O and storage, RAID, file systems, crash consistency, multiprocessor/distributed ideas, and the command-line shell.

The current academic folder was re-read page by page. It contains only the following three main PDFs; no removed textbook, duplicate deck, or old note is counted.

### Exact canonical-slide coverage

| Current source | Pages | Main range |
|---|---:|---|
| `Rimpi_Maam_Merged.pdf` | 241 | introduction, processes/threads, scheduling, IPC/synchronization and deadlock |
| `KRV_Merged.pdf` | 445 | address spaces through paging/swapping, I/O/storage/RAID, file systems and crash consistency |
| `Shell_Commands.pdf` | 66 | paths, files, streams, pipes, permissions, search, processes, packages and scripts |
| **Total current sequence** | **752** | **complete current OS folder represented below** |

For a viva answer, use this order: **definition → mechanism/invariant → example → trade-off**. When the panel gives numbers, draw the timeline or address split before calculating.

## 1. The operating-system mental model

### P0 — What is an operating system?

An operating system is privileged software that sits between applications and hardware. It has two complementary roles:

1. **Resource manager:** allocates CPU time, memory, storage, and I/O devices while enforcing protection and fairness.
2. **Abstraction provider:** turns awkward hardware into useful abstractions—processes, virtual address spaces, files, sockets, and virtual machines.

Virtualization does not mean everything is a hardware VM. The OS virtualizes the CPU by rapidly scheduling processes, virtualizes memory through per-process address spaces, and virtualizes persistent storage through files and directories.

### P0 — Kernel mode and user mode

The processor provides at least two privilege levels. Application code normally executes in **user mode**, where privileged instructions and arbitrary physical-memory access are forbidden. The kernel executes in **kernel/supervisor mode**.

A transition to the kernel can occur through:

- a **system call** deliberately requested by a program;
- an **exception/trap**, such as divide-by-zero or a page fault, caused synchronously by the current instruction;
- an **interrupt**, such as timer or I/O completion, caused asynchronously by hardware.

The CPU saves enough state to resume later, switches to a protected kernel entry point, and changes privilege. A system call is therefore not an ordinary function call even if a library exposes it as one.

**Trap:** do not say that every mode switch is a process context switch. A system call may enter and leave the kernel while returning to the same process. A context switch changes the running execution context and is usually more expensive.

### P0 — Why is the timer interrupt essential?

Without a timer interrupt, a CPU-bound or malicious process could keep the CPU indefinitely in a preemptive system. The OS programs a timer; when it fires, control returns to the kernel, which may continue the process or schedule another one.

### P1 — Common kernel structures

- **Monolithic kernel:** most services run in kernel space. Calls between subsystems are fast, but a bug has a large failure domain. Linux is monolithic but modular.
- **Microkernel:** keeps a small mechanism-focused kernel and moves services such as drivers/filesystems to user processes. Isolation and extensibility improve; IPC/context-transition overhead and design complexity can increase.
- **Layered/modular/hybrid:** practical systems combine ideas rather than matching one pure category.

Mechanism answers **how** something can be done; policy answers **which choice** should be made. For example, a context-switch mechanism lets the OS change processes, while the scheduling policy chooses the next process.

## 2. Programs, processes, and threads

### P0 — Program vs process

A program is passive code and static data stored in a file. A process is a running instance with execution state and resources: program counter, registers, address space, stack, heap, open files, credentials, and scheduling state. Multiple processes may run the same program but have separate state.

Typical process states are:

```text
new -> ready -> running -> terminated
        ^        |
        |        +-> blocked/waiting --event completes--> ready
        +-------- preemption/time slice ------------------+
```

- **Ready:** can run but is waiting for CPU.
- **Blocked:** cannot make progress until an event, usually I/O or synchronization.

### P0 — PCB and context switch

The **process control block** stores kernel metadata such as PID, state, saved registers/program counter, scheduling information, memory-map references, credentials, and open-resource references.

During a context switch, the kernel saves the outgoing context, chooses another runnable task, restores its context, and may switch address spaces. Costs include kernel work, pipeline disruption, cache/TLB disturbance, and lost locality. The exact hardware state is architecture-dependent.

### P0 — Process vs thread

Threads within a process share code, heap, address space, and open resources, but each thread has its own program counter, registers, stack, and scheduling state.

| Separate processes | Threads in one process |
|---|---|
| Stronger isolation | Cheap communication through shared memory |
| IPC is explicit | Races are easier to create |
| Failure often contained | One corrupting thread can damage the process |
| Separate address spaces | Shared address space |

Use processes for isolation/security boundaries; use threads when concurrent activities need efficient shared state—while controlling synchronization.

### P1 — User-level vs kernel-level threads

User-level threading can schedule without entering the kernel and can support custom runtimes. If the kernel sees only one schedulable entity, however, one blocking call may block the entire process and parallel execution on several cores may be unavailable. Kernel threads are visible to the OS and can run in parallel, but creation and switching involve kernel management. Modern systems/runtimes use various one-to-one or multiplexed mappings.

### P1 — `fork`, `exec`, and copy-on-write

On Unix-like systems, `fork` creates a child process with a logically copied address space; implementations normally use **copy-on-write**, sharing physical pages read-only until one side writes. `exec` replaces the current process image with a new program while retaining the process identity and selected resources. A shell often performs `fork`, redirection setup, then `exec`.

## 3. CPU scheduling

### P0 — Metrics

For process `i`:

```text
turnaround_i = completion_i - arrival_i
waiting_i    = turnaround_i - total_CPU_burst_i
response_i   = first_run_i - arrival_i
```

Other goals include throughput, CPU utilization, deadline satisfaction, fairness, and low variance. Interactive systems value response time; batch systems may value throughput/turnaround; real-time systems value predictable deadline behavior.

### P0 — Preemptive vs non-preemptive

- **Non-preemptive:** a running task keeps the CPU until it blocks, exits, or voluntarily yields.
- **Preemptive:** the OS may stop it, usually on a timer or higher-priority arrival.

Preemption improves responsiveness but adds synchronization concerns and switching overhead.

### P0 — Scheduling algorithms

#### FCFS/FIFO

Runs in arrival order. It is simple and starvation-free, but a long CPU-bound job can delay short jobs—the **convoy effect**.

#### SJF and SRTF

Shortest Job First minimizes average waiting time when all jobs are available together and burst lengths are known. Shortest Remaining Time First is its preemptive form. Real systems estimate future bursts, often using exponential averaging:

```text
tau_next = alpha * actual_burst + (1-alpha) * tau_previous
```

Long jobs may starve without aging.

#### Round Robin

Each ready task receives at most quantum `q` in cyclic order. A very large `q` approaches FCFS; a very small `q` improves responsiveness but raises context-switch overhead. It does not automatically minimize average waiting time.

#### Priority scheduling

Runs the highest-priority task. It may be preemptive or non-preemptive. Low-priority starvation can be reduced by **aging**, which gradually increases the priority of waiting tasks.

### P0 — Multilevel Feedback Queue (MLFQ)

MLFQ tries to approximate SJF/SRTF without knowing burst lengths and preserve interactive response:

1. multiple queues have decreasing priority and usually increasing time quanta;
2. the scheduler chooses from the highest nonempty queue;
3. a job that uses its CPU allotment is demoted, suggesting CPU-bound behavior;
4. a job that blocks/yields after a short burst stays high under a carefully designed accounting rule;
5. periodic priority boosts prevent starvation and adapt to phase changes.

**Gaming problem:** if a task can yield just before its quantum expires and retain priority, it can game the policy. Track total CPU allotment at a level, not only uninterrupted bursts.

**Board answer:** draw three queues `Q0`, `Q1`, `Q2` with quanta `4`, `8`, `16`; simulate an interactive job that repeatedly blocks and a CPU-bound job that gets demoted. Then mention periodic boost.

### P1 — Multiprocessor scheduling

With several cores, the OS must balance load while preserving **processor affinity** because a task may have warm caches on its previous core. Per-core run queues reduce contention but require load balancing. NUMA systems also care which memory node holds a task’s pages.

### P1 — Real-time scheduling

- **Rate Monotonic:** fixed priority; shorter period means higher priority, under standard periodic-task assumptions.
- **Earliest Deadline First:** dynamic priority; earliest absolute deadline first. On an ideal preemptive uniprocessor under its assumptions, EDF can use the processor up to full utilization.

Real-time correctness concerns deadlines and bounded latency, not merely high average speed.

## 4. Concurrency and synchronization

### P0 — Race condition and critical section

A race condition occurs when the result depends on an uncontrolled interleaving of concurrent operations. `counter++` is not necessarily atomic; it is conceptually read, modify, write. Two threads can lose an update.

A correct critical-section solution aims for:

- **mutual exclusion:** at most one participant inside;
- **progress:** if nobody is inside, eligible contenders can decide without irrelevant indefinite delay;
- **bounded waiting:** a requester is not postponed forever.

### P0 — Atomic operations and locks

Hardware instructions such as test-and-set or compare-and-swap allow an atomic state transition. A **spinlock** repeatedly checks the lock and wastes CPU while waiting, but can be reasonable for extremely short kernel critical sections or when sleeping is impossible. A blocking mutex lets the waiter sleep, which is better for longer waits but adds scheduler overhead.

Locks protect **invariants**, not merely lines of code. Define which shared data and relationship the lock protects. Keep a consistent lock order to reduce deadlock risk.

### P0 — Semaphore

A semaphore is an integer synchronization object changed only through atomic operations:

- `wait/P/down`: decrement if possible; otherwise block;
- `signal/V/up`: increment and wake an eligible waiter.

A binary semaphore can provide mutual exclusion, but ownership semantics may differ from a mutex. A counting semaphore represents multiple identical resources or available items.

Producer-consumer with buffer capacity `N`:

```text
semaphore empty = N, full = 0, mutex = 1

producer: wait(empty); wait(mutex); insert(); signal(mutex); signal(full)
consumer: wait(full);  wait(mutex); remove(); signal(mutex); signal(empty)
```

The order matters. Holding the mutex while blocking on `empty`/`full` can deadlock.

### P0 — Monitor and condition variable

A monitor packages shared state and procedures with implicit mutual exclusion. A condition variable lets a thread sleep until a predicate may have become true:

```text
lock(m)
while (!condition())
    wait(cv, m)    // atomically releases m and sleeps; reacquires before return
use_or_modify_state()
unlock(m)
```

Use `while`, not usually `if`, because wakeups may be spurious or another thread may consume the condition before this one reacquires the lock. `signal` means “the condition may now be true,” not “transfer ownership of the lock immediately” in common Mesa-style semantics.

### P1 — Classic synchronization problems

- **Readers-writers:** allow concurrent readers but exclusive writers; policies trade reader/writer starvation and fairness.
- **Dining philosophers:** naïve acquisition of left then right forks can deadlock. Impose resource ordering, allow at most `N-1` contenders, or use a waiter.
- **Sleeping barber:** coordinates bounded waiting-room capacity, customer availability, and barber sleep/wakeup.

### P0 — IPC mechanisms

- **Pipe/FIFO:** byte stream, simple; ordinary pipe is often related-process and one-direction oriented.
- **Message queue/mailbox:** preserves message boundaries and decouples sender/receiver.
- **Shared memory:** fastest data path after setup because processes access common pages, but requires synchronization.
- **Socket:** local or network communication with a standard endpoint abstraction.
- **Signals/events:** lightweight notification, poor for transferring complex data.
- **RPC:** presents remote communication like a procedure call, but must not hide partial failure, latency, serialization, retries, or duplicate execution.

## 5. Deadlock, starvation, and livelock

### P0 — Necessary conditions for deadlock

All four Coffman conditions must hold:

1. **mutual exclusion** for some resource;
2. **hold and wait**;
3. **no preemption** of held resources;
4. **circular wait**.

Breaking any one prevents deadlock. A cycle in a resource-allocation graph is necessary; with one instance per resource type it is also sufficient. With multiple instances, a cycle alone may not prove deadlock.

### P0 — Four handling strategies

1. **Ignore:** acceptable if rare and recovery/restart is cheap.
2. **Prevention:** structurally break a Coffman condition, e.g. total resource ordering breaks circular wait.
3. **Avoidance:** grant a request only if the resulting state remains safe; Banker’s algorithm needs declared maximum demand.
4. **Detection and recovery:** allow deadlock, detect it, then preempt/rollback/terminate selected work.

A **safe state** has some completion ordering for all processes. Unsafe does not mean already deadlocked; it means future requests may force deadlock.

### P0 — Banker’s algorithm idea

Given `Available`, `Allocation`, and `Max`, compute `Need = Max - Allocation`. Repeatedly find an unfinished process whose `Need <= Work`; pretend it completes and returns its allocation. If all can finish, a safe sequence exists.

### P0 — Distinctions

- **Deadlock:** a set waits in a cycle and none can progress.
- **Starvation:** a task is continually denied service while others progress.
- **Livelock:** participants keep reacting/changing state but do no useful work.
- **Priority inversion:** a high-priority task waits for a lock held by a low-priority task while medium-priority tasks run. Priority inheritance can temporarily boost the lock holder.

## 6. Address spaces and virtual memory

### P0 — Why virtual memory?

Each process sees a private, contiguous-looking virtual address space even though pages may be scattered in RAM, shared, protected, or temporarily absent. Benefits include isolation, relocation, controlled sharing, sparse address spaces, and the ability to run working sets larger than available physical memory—with performance limits.

An address generated by the CPU is virtual; the MMU translates it. Protection bits enforce read/write/execute and user/kernel access.

### P0 — Base-and-bound and segmentation

With dynamic relocation, `physical = base + virtual` if `virtual < bound`. It is simple but a single contiguous region limits growth and causes external fragmentation.

Segmentation represents logical regions such as code, heap, and stack. A virtual address includes segment number and offset; each segment has base, limit, and protection. Segments support logical sharing/protection but variable sizes cause external fragmentation.

**Internal fragmentation** wastes space inside an allocated unit; **external fragmentation** leaves enough total free space but split into unsuitable holes.

### P0 — Paging and address translation

Paging divides virtual memory into fixed-size pages and physical memory into equal-size frames. For page size `2^p`, split a virtual address into virtual page number and `p`-bit offset. The page-table entry maps VPN to PFN plus valid, protection, referenced/accessed, dirty, and other bits.

Example: a 32-bit virtual address with 4 KiB (`2^12`) pages has a 12-bit offset and 20-bit VPN. A flat table has `2^20` entries; at 4 bytes each, it needs 4 MiB per address space, motivating multilevel/sparse page tables.

### P0 — TLB

The Translation Lookaside Buffer caches recent virtual-to-physical translations. On a TLB hit, translation is fast; on a miss, hardware or software walks the page table and may insert the result. A TLB miss is **not necessarily a page fault**: the page may be in RAM but its translation is not cached.

Context switches may flush non-global entries or use address-space identifiers to distinguish processes. TLB reach is approximately `number_of_entries × page_size`.

### P1 — Page-table organizations

- **Multilevel:** allocates lower-level tables only for used virtual regions.
- **Hashed/inverted:** reduce per-process table size in very large address spaces, with different lookup complexity.
- **Huge pages:** increase TLB reach and reduce table overhead, but raise internal fragmentation and allocation/migration cost.

### P0 — Demand paging and page-fault path

On access to a nonresident valid page:

1. hardware traps to the kernel;
2. kernel validates the address and permissions;
3. selects a free frame or victim;
4. writes a dirty victim if necessary;
5. reads/constructs the needed page;
6. updates page table/TLB state;
7. restarts the faulting instruction.

Page faults are extremely expensive relative to memory accesses, so locality and working-set control matter.

### P0 — Page replacement

- **Optimal/MIN:** evict the page used farthest in the future; theoretical benchmark, not implementable online.
- **FIFO:** simple; can show **Belady’s anomaly**, where more frames cause more faults.
- **LRU:** uses past recency as a locality predictor; exact LRU is costly, so systems approximate it.
- **Clock/second chance:** circularly scans reference bits, clearing recent pages before evicting an unreferenced one.

Stack algorithms such as true LRU and OPT do not exhibit Belady’s anomaly because the pages resident with `n` frames are a subset of those with `n+1` under the same reference sequence.

### P0 — Thrashing

Thrashing occurs when active working sets exceed physical memory, so the system spends most time paging rather than executing. Symptoms include high fault rate and low useful CPU progress. Adding more processes can worsen it. Responses include reducing multiprogramming, allocating more frames, working-set/page-fault-frequency control, or adding RAM.

### P1 — Copy-on-write and memory mapping

Copy-on-write shares pages until a write fault creates a private copy. Memory-mapped files map file contents into a process address space; ordinary loads/stores then access cached file pages. `mmap` can simplify random access and sharing, but durability still requires appropriate synchronization/flush semantics.

## 7. I/O and persistent storage

### P0 — Device interaction

A device controller exposes registers/queues. A driver translates generic OS operations into device-specific commands.

- **Polling:** repeatedly check status; simple, good for very short predictable waits, wastes CPU otherwise.
- **Interrupt-driven I/O:** device interrupts on completion; frees CPU during longer waits, adds interrupt overhead.
- **DMA:** a controller transfers blocks between device and memory with limited CPU involvement; CPU sets up the operation and handles completion.

### P0 — HDD behavior and scheduling

HDD access time includes seek, rotational delay, and transfer. Scheduling algorithms include FCFS, SSTF, SCAN/elevator, and C-SCAN. SSTF reduces immediate seek but can starve distant requests; SCAN provides more predictable sweeping service.

### P0 — SSD differences

SSDs have no mechanical seek, but flash pages are written in larger erase-block constraints. A flash translation layer performs logical-to-physical mapping, garbage collection, and wear leveling. Write amplification and limited program/erase cycles matter. TRIM/discard informs the device that logical blocks no longer hold live data.

### P0 — RAID

RAID combines disks for performance and/or fault tolerance; it is not a backup.

| Level | Core idea | Usable capacity with `N` equal disks | Tolerates |
|---|---|---:|---:|
| RAID 0 | striping only | `N` disks | 0 failures |
| RAID 1 | mirroring | commonly about `N/2` | normally one per mirror set |
| RAID 5 | block striping + distributed single parity | `N-1` | 1 disk |
| RAID 6 | distributed double parity | `N-2` | 2 disks |
| RAID 10 | stripe across mirrors | about `N/2` | depends which disks fail |

Small RAID-5 writes can require read-old-data, read-old-parity, compute, and write new data/parity—the write penalty. Rebuilds run under degraded risk/performance. Backup protects against deletion, corruption, malware, site loss, and other events RAID does not.

## 8. File systems and crash consistency

### P0 — File-system responsibilities

A filesystem maps human-readable paths and file offsets onto persistent blocks while managing metadata, free space, protection, caching, concurrency, and crash recovery.

An inode-like structure stores file type, owner/mode, size, timestamps, link count, and block pointers. A directory maps names to inode/object identifiers. Therefore the filename is typically in the directory entry, not in the inode itself.

### P0 — Hard link vs symbolic link

- A **hard link** is another directory entry to the same inode/object; it normally cannot cross filesystems and generally cannot link directories. Removing one name does not delete data while links/open references remain.
- A **symbolic link** is a separate file containing a path; it can cross filesystems and can dangle.

### P1 — Allocation strategies

- **Contiguous allocation:** fast sequential/random access, but growth and external fragmentation are difficult.
- **Linked allocation/FAT-like:** easy growth, poor random access and pointer reliability concerns.
- **Indexed allocation/inodes/extents:** central index or extents support random access and growth at metadata cost.

Free space can be tracked by bitmaps, free lists, grouping, or extent structures.

### P1 — Locality and Fast File System idea

Placement policy matters. Group related inodes, directory entries, and data blocks so common accesses require less movement and exploit locality. Large sequential transfers improve throughput, while allocation should avoid excessive fragmentation.

### P0 — Crash-consistency problem

One logical operation may require several persistent writes. For example, appending a block may update a data block, allocation bitmap, and inode. A crash between them can leave leaks, stale pointers, or metadata disagreement.

- **fsck/checker:** scans after crash and repairs inconsistencies; recovery time grows with filesystem size.
- **Journaling/write-ahead logging:** first records intended metadata/data changes in a log, commits the transaction, then checkpoints to home locations. Recovery replays committed work and ignores incomplete transactions.
- **Copy-on-write filesystem:** writes new blocks and atomically switches roots/pointers, enabling snapshots but requiring careful space management.
- **Log-structured filesystem:** writes updates sequentially to a log and later cleans segments; converts random writes into sequential ones but cleaning/live-data movement is central.

**Trap:** journaling improves consistency/recovery; it does not mean application data has definitely reached durable media unless the application and filesystem use the required write/flush ordering.

### P1 — Data integrity and protection

Permissions/ACLs control authorized access; checksums detect corruption; redundancy may repair it; encryption protects confidentiality at rest; backups and snapshots support recovery. These solve different threats. Checksums are not encryption, RAID is not backup, and access control does not prevent physical-media disclosure without encryption.

## 9. Multiprocessor and distributed-system essentials

### P1 — Concurrency vs parallelism

Concurrency means multiple tasks make overlapping progress; parallelism means they execute simultaneously on different processing units. A single-core system can be concurrent without parallel execution.

### P1 — Cache coherence and memory ordering

On multicore hardware, private caches must maintain a coherent view of a memory location, often using invalidation protocols. Coherence answers how writes to one location become visible; memory consistency/order constrains the observed ordering across multiple operations. Language-level atomic/lock semantics are required—`volatile` alone is not a universal substitute.

### P1 — Distributed systems are not just “remote OS”

Nodes have independent failure and clocks; messages can be delayed, lost, duplicated, or reordered. Important ideas:

- partial failure: one component fails while others continue;
- timeout gives suspicion, not certainty;
- retries require idempotency or duplicate detection;
- replication trades consistency, availability behavior, latency, and complexity;
- consensus coordinates a value/order despite failures under specified assumptions.

## 10. Board-ready demonstrations

### Board 1 — Scheduling table

Given arrival and burst times:

1. state whether the policy is preemptive;
2. draw a Gantt chart;
3. record each completion and first-run time;
4. compute turnaround, waiting, and response separately;
5. average only after individual values are checked.

Common error: treating response time as waiting time. They coincide only in some non-preemptive cases.

### Board 2 — MLFQ

Draw three queues, explain priority/quanta, demotion, I/O-like behavior, allotment accounting, periodic boost, and starvation prevention. End with: “MLFQ learns behavior from execution history; it does not know true future burst lengths.”

### Board 3 — Producer-consumer

Draw a bounded buffer and three semaphores `empty=N`, `full=0`, `mutex=1`. Explain why resource semaphore is acquired before mutex and why insertion/removal occurs under mutual exclusion.

### Board 4 — Virtual-address translation

For a 16-bit address and 1 KiB pages: offset is 10 bits, VPN is 6 bits. Split a sample address, look up PFN, concatenate PFN with unchanged offset. Then distinguish TLB miss from page fault.

### Board 5 — Deadlock

Draw two processes and two single-instance resources: each holds one and requests the other. Map the four Coffman conditions and show that a total resource ordering eliminates circular wait.

## 11. High-yield viva comparisons

| Question | Strong distinction |
|---|---|
| Process vs program | executing resource container vs passive code |
| Process vs thread | isolated address space vs shared process resources |
| User vs kernel mode | restricted application execution vs privileged OS execution |
| Interrupt vs exception | asynchronous external event vs synchronous current-instruction event |
| Mode switch vs context switch | privilege transition vs changing running context |
| Mutex vs semaphore | ownership-oriented mutual exclusion vs signaling/resource count |
| Spinlock vs mutex | busy waiting vs blocking |
| Deadlock vs starvation | circular/no progress set vs indefinite denial while system progresses |
| Paging vs segmentation | fixed physical units vs variable logical regions |
| TLB miss vs page fault | translation not cached vs page not resident/invalid mapping event |
| Internal vs external fragmentation | waste inside unit vs scattered free holes |
| Cache vs virtual memory | speed/locality hierarchy vs address-space abstraction/protection/capacity |
| RAID vs backup | availability/performance during disk faults vs independent recovery copy |
| Hard vs symbolic link | same inode/object vs path-containing separate object |

## 12. Rapid oral questions

1. **Why can threads be cheaper than processes?** They share an address space/resources, so creation, communication, and often switching require less setup; the exact cost is implementation-dependent.
2. **Can a process have zero threads?** In the usual execution model, a live executable process has at least one execution thread; terminology differs for kernel objects/zombies.
3. **What is a zombie?** A terminated child whose exit status has not yet been collected by its parent.
4. **What is an orphan?** A living child whose parent terminates; the OS reparents/adopts it according to system policy.
5. **Why is SJF optimal for average waiting?** An exchange argument shows swapping an adjacent longer-before-shorter pair cannot reduce total waiting.
6. **Why can Round Robin be bad?** Poor quantum choice causes FCFS-like latency or excessive switching; it also ignores job length and priority needs.
7. **Does a semaphore guarantee fairness?** Not inherently; queueing/wakeup policy determines fairness.
8. **Why use `while` around condition wait?** The predicate may still be false after a spurious wakeup or competition before lock reacquisition.
9. **Can deadlock occur with one process?** Yes, for example a non-reentrant lock acquired twice by the same thread with no release path.
10. **Is every unsafe state deadlocked?** No; it lacks a guaranteed safe completion sequence but may still finish depending on future requests.
11. **Why is paging popular?** Fixed-size allocation avoids external fragmentation and supports simple placement, protection, sharing, and demand paging.
12. **Does paging eliminate fragmentation?** It eliminates external fragmentation of frames but can cause internal fragmentation and page-table overhead.
13. **Why are page sizes powers of two?** Address split becomes direct bit partitioning between page number and offset.
14. **Can a page fault be good?** It is part of useful mechanisms such as demand allocation, copy-on-write, and mapped files, though still costly.
15. **What is locality?** Programs tend to reuse recently accessed locations (temporal) and nearby locations (spatial).
16. **Why does FIFO show Belady’s anomaly?** Its resident set with more frames need not contain the smaller-frame resident set.
17. **Why does RAID 0 not improve reliability?** Any member failure loses part of the striped data; more disks can increase aggregate failure exposure.
18. **Why is `fsync` relevant?** It requests that required buffered updates reach the durability boundary, subject to OS/device semantics.
19. **What does an inode not normally contain?** The ordinary filename; directories associate names with inode numbers.
20. **What is the biggest distributed-systems trap?** Treating a timeout as proof of failure or retrying a non-idempotent operation without duplicate control.

## 13. Common wrong answers to avoid

- “The OS only provides a GUI.” The kernel’s core role is protected resource management and abstractions.
- “Blocked and ready are the same because both are not running.” Ready needs only CPU; blocked needs an external event.
- “More threads always make a program faster.” Dependencies, overhead, contention, memory bandwidth, and core count limit speedup.
- “SJF is always practical and fair.” Future bursts are not known and long jobs may starve.
- “A binary semaphore and mutex are identical.” Similar use is possible, but ownership and intended semantics differ.
- “Deadlock means high CPU usage.” Deadlocked tasks are usually waiting; livelock/spinning can consume CPU.
- “A cycle always proves deadlock.” Only under single-instance resource assumptions.
- “Virtual memory is just disk space.” It is primarily the address-space abstraction and translation/protection system.
- “TLB stores data.” It stores translations and related permissions, not ordinary cache-line data.
- “LRU is always implemented exactly.” Practical systems usually approximate it.
- “SSD has no access cost because there is no seek.” Flash translation, erase, garbage collection, and queueing remain.
- “RAID is backup.” It does not protect against many logical and site-level failures.
- “Journaling means no data loss.” It targets consistency and bounded recovery; durability depends on mode, ordering, and application calls.

## 14. Core-subject self-test

You are ready only if you can do these without notes:

- [ ] Draw user-to-kernel transitions and distinguish syscall, trap, interrupt, and context switch.
- [ ] Draw process states and explain PCB, `fork`, `exec`, and copy-on-write.
- [ ] Solve FCFS, SJF/SRTF, RR, and priority scheduling tables accurately.
- [ ] Teach MLFQ, including gaming, allotment, boost, and starvation.
- [ ] Explain races and implement bounded producer-consumer with semaphores/conditions.
- [ ] Compare locks, semaphores, monitors, and IPC mechanisms.
- [ ] State all Coffman conditions and work a Banker safe-sequence example.
- [ ] Translate a virtual address through paging and explain TLB/page-fault behavior.
- [ ] Compare FIFO, LRU, Clock, and OPT and explain Belady’s anomaly/thrashing.
- [ ] Explain interrupts, DMA, HDD/SSD trade-offs, and RAID 0/1/5/6/10.
- [ ] Explain inode/directory structure, hard/symbolic links, journaling, and LFS.
- [ ] Give a careful one-minute answer on multiprocessor scheduling or distributed partial failure.

---

# 15. Slide-derived algorithm and code workbook

## 15.1 Scheduling metrics and one complete trace

For process `i`:

$$
T_i=C_i-A_i,
\qquad
W_i=T_i-B_i,
\qquad
R_i=F_i-A_i,
$$

where `A` is arrival, `B` total CPU burst, `F` first scheduled time, and `C` completion. The waiting formula assumes the simple model in which the listed burst is all CPU service; with repeated I/O bursts, waiting must be accumulated from time actually spent ready.

Example:

| Process | Arrival | Burst |
|---|---:|---:|
| P1 | 0 | 5 |
| P2 | 1 | 3 |
| P3 | 2 | 1 |

FCFS:

```text
0        5        8  9
|   P1   |   P2   |P3|
```

- completion: `C1=5,C2=8,C3=9`;
- turnaround: `5,7,7`;
- waiting: `0,4,6`;
- response equals waiting here because each process runs only once.

SRTF:

```text
0  1  2  3    5        9
|P1|P2|P3| P2 |   P1   |
```

At each arrival/completion choose the smallest remaining time. Recalculate carefully: a preempted process’s response is still its **first** run delay, while waiting accumulates across ready intervals.

Round Robin with quantum `q` maintains a FIFO ready queue. New arrivals join according to the stated event convention; ambiguity at an exact quantum boundary can change the trace, so state the convention. Small `q` improves response but raises context-switch overhead; as `q→∞`, RR approaches FCFS.

## 15.2 MLFQ as an explicit algorithm

An implementable policy follows five rules:

1. if priorities differ, run the higher-priority ready job;
2. among equal priorities, use round robin;
3. a new job starts at the highest queue;
4. after consuming its CPU allotment at a level—even across voluntary yields—it is demoted;
5. periodically boost all jobs to the top to prevent starvation and forget stale behavior.

Why it works: interactive/I/O-bound jobs often relinquish CPU early and remain responsive; CPU-bound jobs consume allotments and migrate down. Why naive MLFQ fails: a job may game the scheduler by yielding just before its quantum, or a changed workload may remain permanently low. Cumulative allotment and periodic priority boost address these failures.

## 15.3 Ticket/lottery intuition

If process `i` owns `t_i` tickets out of `T`, its expected CPU share is

$$
\mathbb E[share_i]=t_i/T.
$$

Lottery scheduling is probabilistic; short-run allocations can deviate from expectation. Stride scheduling uses deterministic virtual passes to approximate proportional share. Neither automatically meets a hard real-time deadline.

## 15.4 Process creation trace

```c
pid_t pid = fork();
if (pid < 0) {
    perror("fork");
} else if (pid == 0) {
    execlp("ls", "ls", "-l", (char *)NULL);
    perror("exec");      /* reached only if exec failed */
    _exit(127);
} else {
    int status;
    if (waitpid(pid, &status, 0) < 0) perror("waitpid");
}
```

`fork` creates a child execution context, commonly with copy-on-write mappings. It returns `0` in child and child PID in parent. `exec` replaces the current process image; it does not create a second process. `wait` reaps termination status. A terminated unreaped child is a zombie; an orphan is a living child whose parent exited and is reparented/adopted according to the OS.

## 15.5 Race condition trace

`count++` is conceptually read–modify–write:

```text
T1: read count=5
T2: read count=5
T1: write 6
T2: write 6
```

Two increments produced one. A critical-section solution aims for mutual exclusion, progress, and bounded waiting under its model. Disabling interrupts is not a general user-space/multiprocessor lock: another core still runs, and arbitrary user code must not control interrupts.

## 15.6 Semaphore bounded buffer

For `N` slots:

```text
semaphore empty = N
semaphore full  = 0
semaphore mutex = 1

producer(item):
    wait(empty)
    wait(mutex)
    put(item)
    signal(mutex)
    signal(full)

consumer():
    wait(full)
    wait(mutex)
    item = get()
    signal(mutex)
    signal(empty)
    return item
```

Acquiring `mutex` before `empty/full` can deadlock: a producer may hold the mutex while waiting for space, preventing the consumer from acquiring mutex to create space. Counting semaphores represent resource counts; the binary `mutex` protects buffer state.

## 15.7 Condition-variable pattern

```text
lock(m)
while (!predicate):
    wait(cv, m)      # atomically releases m and sleeps; reacquires before return
modify shared state
signal/broadcast(cv)
unlock(m)
```

Use `while`, not `if`: wakeups may be spurious, another thread may consume the condition first, or multiple waiters may race after a broadcast. The predicate belongs to shared state protected by the mutex; the condition variable itself does not store the condition.

## 15.8 Deadlock detection and Banker safety

Coffman conditions: mutual exclusion, hold-and-wait, no preemption, circular wait. All are necessary for the classic model; breaking one prevents that form of deadlock.

Banker safety algorithm:

```text
Work = Available
Finish[i] = false for every process
repeat:
    find unfinished i with Need[i] <= Work
    if none exists: stop
    Work += Allocation[i]
    Finish[i] = true
safe iff every Finish[i] is true
```

`Need=Max-Allocation`. A **safe state** has at least one completion order under declared maximum claims. An unsafe state is not necessarily already deadlocked; it lacks a guaranteed safe sequence. A resource request is tentatively allocated only if it does not exceed Need/Available and the resulting state remains safe.

## 15.9 Base-and-bounds and segmentation

For base-and-bounds:

```text
if virtual_address >= bound: protection fault
physical_address = base + virtual_address
```

It provides relocation/protection but a single contiguous region and external fragmentation. Segmentation uses separate logical regions such as code/heap/stack, each with base, bound, and permissions. It supports sparse logical organization but still suffers external fragmentation.

## 15.10 Paging numeric example

With 4 KiB pages, offset has `log2(4096)=12` bits. For a 32-bit virtual address:

```text
VPN = VA >> 12             (20 bits)
offset = VA & 0xFFF        (12 bits)
PTE = page_table[VPN]
if invalid: page fault
PA = (PFN << 12) | offset
```

Example `VA=0x12345`:

```text
VPN = 0x12
offset = 0x345
if PTE maps VPN 0x12 to PFN 0xA7,
PA = 0xA7345
```

The TLB caches the mapping/permissions. On a TLB miss, hardware/software walks the page table; a valid PTE produces a TLB fill. A **page fault** means the translation requires OS handling (not-present, protection, copy-on-write, etc.), which is distinct from a mere TLB miss.

## 15.11 TLB effective access time

For a simplified single-level table where TLB lookup overlaps/negligibly costs and memory access is `M`, hit ratio `h`:

$$
EAT=hM+(1-h)(2M)=(2-h)M.
$$

If TLB lookup cost `T` is separate:

$$
EAT=h(T+M)+(1-h)(T+2M),
$$

excluding page faults. State the assumed page-table depth and lookup overlap; blindly memorizing `hM+(1-h)2M` is unsafe for multilevel walks.

## 15.12 Page-fault service sequence

1. hardware detects invalid/not-present/protection condition and traps;
2. kernel validates the address/access;
3. illegal access terminates/signals the process;
4. otherwise locate the backing data or create zero/COW page;
5. select a free frame or victim;
6. write back a dirty victim if required;
7. read/prepare the page and block the faulting task during I/O;
8. update PTE/TLB state;
9. restart the faulting instruction.

This cost is orders of magnitude above a normal memory access, motivating locality and low page-fault rate.

## 15.13 Replacement algorithms and Belady anomaly

- **OPT/MIN:** evict page used farthest in future; unattainable online, useful lower-bound benchmark.
- **FIFO:** evict oldest arrival; simple, may show Belady’s anomaly.
- **LRU:** evict least recently used; stack property avoids Belady anomaly, exact implementation expensive.
- **Clock/second chance:** circular hand checks reference bit; referenced pages get a second chance by clearing bit.

For a reference string, show the frame contents after **every** reference and mark hits/faults. Do not conflate number of distinct pages with number of frames. Working-set/clock-like policies approximate recency to avoid thrashing.

## 15.14 Free-space allocator

An allocator maintains blocks and metadata. On `malloc`, choose a fit, split if useful, return aligned payload. On `free`, mark available and coalesce adjacent free blocks.

- first fit: first adequate block;
- best fit: smallest adequate block, potentially many small fragments;
- segregated lists: size-class bins;
- buddy: power-of-two splitting/coalescing.

Internal fragmentation wastes space inside allocated blocks; external fragmentation leaves free space split into unusable pieces. Paging removes external fragmentation of physical frames but still has internal waste in a final page.

## 15.15 I/O path and DMA

```text
application read/write
 -> system call / VFS / driver
 -> device request queue
 -> controller registers/descriptors
 -> DMA transfers between device and memory
 -> interrupt/completion
 -> wake process / return
```

Programmed I/O makes CPU move/check data repeatedly; interrupt-driven I/O notifies completion; DMA handles bulk transfer after CPU setup. DMA still requires driver setup, mapping/pinning/cache coherence, completion, and error handling.

## 15.16 HDD scheduling

Approximate service time:

$$
T_{IO}=T_{queue}+T_{seek}+T_{rotation}+T_{transfer}+T_{controller}.
$$

- FCFS: fair by arrival but poor head motion;
- SSTF: nearest request, can starve distant requests;
- SCAN: elevator sweeps both ways;
- C-SCAN: services one direction and wraps, more uniform waiting;
- LOOK/C-LOOK: reverse/wrap at last pending request rather than physical end.

SSDs remove mechanical seek but still have page read/program, block erase, garbage collection, wear leveling, queueing, write amplification, and finite endurance.

## 15.17 RAID capacity and failure tolerance

For `N` equal disks of capacity `S`:

| Level | Usable capacity | Tolerates | Core idea |
|---|---:|---:|---|
| RAID 0 | `NS` | 0 disk failures | striping only |
| RAID 1 | commonly `NS/2` | one per mirror group | mirroring |
| RAID 5 | `(N-1)S` | 1 | distributed single parity |
| RAID 6 | `(N-2)S` | 2 | dual parity |
| RAID 10 | commonly `NS/2` | depends which disks | stripe across mirrors |

Small RAID-5 write penalty conceptually needs old data + old parity reads and new data + new parity writes unless full-stripe/optimized. RAID improves availability/performance under some failures; it is not backup against deletion, corruption, ransomware, software error, or site loss.

## 15.18 Inodes, directories, and block mapping

A directory maps names to inode numbers/identifiers. An inode stores metadata and block pointers, usually not the ordinary filename. A hard link adds another directory entry to the same inode; it normally cannot cross filesystems and directories are restricted. A symbolic link is a separate inode containing a pathname and can dangle/cross filesystems.

With `D` direct pointers and single indirect block containing `K` pointers, reachable data blocks begin as `D+K`; double indirect adds `K^2`, triple adds `K^3`. Maximum file size multiplies reachable data blocks by block size, adjusted for the filesystem’s exact scheme.

## 15.19 Crash consistency, journaling, and LFS

A multi-block operation such as file creation may update directory entry, inode, allocation bitmap, and data. A crash between writes can leave contradictions.

- **fsck:** scan after crash and repair invariants; recovery grows with filesystem size.
- **write-ahead journaling:** log intended metadata/data transaction before installing home-location updates; commit record defines replayable completion.
- **metadata journaling:** logs metadata; data ordering mode determines stale/new data exposure.
- **copy-on-write filesystem:** write new blocks and atomically switch roots, subject to implementation/durability rules.

Ordering sketch:

```text
write log records -> flush/order -> write commit -> flush/order
-> checkpoint to home locations -> later reclaim log
```

The log-structured filesystem writes new segments sequentially, treats the log as the primary layout, and cleans live blocks from old segments. It converts small random writes to large sequential writes but pays cleaning/write-amplification and indexing/recovery costs. Journaling and LFS both use logs but for different primary purposes.

## 15.20 Distributed-system traps from the KRV scope

- partial failure: one node/link fails while others run;
- a timeout gives uncertainty, not proof the remote operation did not occur;
- retries require idempotency, request IDs/deduplication, or transactional semantics;
- network partitions force explicit availability/consistency choices;
- clock readings are not a perfect global event order;
- replication improves availability/read scale but creates consistency/failover problems;
- “exactly once” effects usually require coordination/deduplication around at-least-once delivery, not a magical packet guarantee.

For an RPC timeout, enumerate possibilities: request lost, server not reached, server executed but reply lost, reply delayed, or server crashed before/after durable effect. That uncertainty is why payment/domain-registration APIs need idempotency keys and reconciliation.

---

# 16. Linux Shell and Command-Line Recall

## 16.1 Shell, terminal, command, and path

A **terminal** is the interface carrying text input and output; a **shell** such as Bash is the command interpreter. The shell parses quoting, expansion, redirection, pipelines and control operators, then runs built-ins itself or starts external programs. `$PATH` is the ordered list of directories searched for an unqualified command name; `which cmd` shows the executable selected in common cases.

- `/` is the file-system root; `~` is the current user's home.
- An **absolute path** starts at `/`; a **relative path** starts at the current working directory.
- `.` means current directory, `..` parent, and `cd -` previous directory.
- `./script` explicitly names a file in the current directory; the shell normally does not search `.` unless it is in `$PATH`.

## 16.2 Essential commands from the 66-page shell deck

| Goal | Commands / important options |
|---|---|
| locate and navigate | `pwd`, `cd`, `ls -laF`, `which`, `find` |
| create/copy/move/remove | `touch`, `mkdir -p`, `cp -r`, `mv -i`, `rm -i` |
| inspect text | `cat`, `less`, `head`, `tail -f`, `wc` |
| transform/search | `sort`, `uniq -c`, `tr`, `grep -inrw`, `cut` |
| processes/resources | `ps`, `htop`, `kill`, `df`, `du` |
| ownership/access | `chmod`, `chown`, `chgrp`, `whoami`, `sudo` |
| documentation/packages | `man`, `--help`, `apt update/install/remove`, `dpkg -i` |

Wildcards such as `*.txt` are expanded by the shell before the command runs. By contrast, `grep` interprets a regular expression inside file contents. Quote a wildcard when you want another program—such as `find -name "*.txt"`—to interpret it.

## 16.3 Standard streams, redirection, and pipes

Every process conventionally starts with file descriptors:

| Descriptor | Stream | Default |
|---:|---|---|
| 0 | standard input | terminal keyboard |
| 1 | standard output | terminal display |
| 2 | standard error | terminal display |

```bash
program < input.txt          # stdin from file
program > output.txt         # truncate then write stdout
program >> output.txt        # append stdout
program 2> error.txt         # stderr only
program > all.txt 2>&1       # point stderr where stdout now points
producer | consumer          # producer stdout becomes consumer stdin
```

`|` connects processes; `>>` appends to a file. A pipeline is compositional because each tool can read a stream and write a stream:

```bash
tr -c '[:alnum:]' '\n' < file.txt |
  tr '[:upper:]' '[:lower:]' |
  sort | uniq -c | sort -nr | head -10
```

Why does `sudo echo hello > /protected/file` fail? `sudo` elevates `echo`, but the unprivileged shell performs `>` first. Use `echo hello | sudo tee /protected/file`.

## 16.4 Permissions

`-rwxr-xr--` has a type character followed by owner, group and other triplets. `r=4`, `w=2`, `x=1`, so:

```bash
chmod 754 file       # owner rwx, group r-x, others r--
chmod u+x file       # symbolic form
```

For a regular file, `r/w/x` mean read contents, modify contents and execute. For a directory:

- `r` permits listing names;
- `w` permits creating/removing directory entries;
- `x` permits traversal/search through the directory.

Whether a user can access a file depends on ownership, the applicable permission triplet, enclosing-directory permissions, ACLs and possible privilege—not just the displayed bit pattern.

## 16.5 Script execution and safe search

The first line `#!/usr/bin/env bash` selects an interpreter through the environment. A script also needs execute permission when launched as `./script`; `bash script` only needs Bash to be able to read it.

```bash
#!/usr/bin/env bash
set -euo pipefail
for file in "$@"; do
    printf '%s: ' "$file"
    wc -l < "$file"
done
```

Quoting `"$@"` preserves each original argument. `find` is recursive and can filter by name, type, size and modification time:

```bash
find . -type f -name "*.log" -size +1M
find . -type f -name "*.txt" -exec grep -nH "TODO" {} +
```

For arbitrary filenames, prefer `-exec ... {} +` or NUL-delimited `-print0 | xargs -0`; plain `find ... | xargs ...` breaks on spaces/newlines. Before any destructive `find -exec rm`, run the same predicate with `-print` and inspect the exact targets.

## 16.6 Shell viva traps

- A directory stores name-to-inode mappings; the inode stores metadata and block locations, not the filename.
- A symbolic link stores a target path and can dangle; a hard link is another directory entry for the same inode.
- `Ctrl-C` normally sends `SIGINT`; it is not the same as closing the terminal.
- A shell built-in such as `cd` must affect the current shell; an external child process could not change its parent's working directory.
- `kill` sends a signal; it does not necessarily mean `SIGKILL`, and graceful termination is preferable when possible.
