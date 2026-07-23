# Bismillah.

# Computer Architecture, Digital Logic, and Microprocessors — Core-Complete Viva Recall

This file treats hardware as one of your strengths. It builds one continuous story:

```text
Boolean logic -> combinational blocks -> state/flip-flops -> registers and FSMs
-> datapath and control -> instruction set -> pipeline/cache/memory -> I/O
-> microprocessor/microcontroller embedded system
```

In a viva, do not merely name components. Draw signals, state the clock/timing assumption, calculate one example, and connect the circuit to its software-visible behavior.

## Source-scope note

No dedicated Architecture, DLD, or Microprocessor academic folder is present in this workspace. This module is therefore a standard-core supplement guided by the reported BRACU questions (cache, asynchronous counter, microprocessor versus microcontroller) and by your stated hardware strength. It is intentionally kept separate from claims about the locally read course-slide sequence.

## Part I — Digital Logic Design

## 1. Number systems and digital representation

### P0 — Positional representation

For base `r`, digits represent powers of `r`. Convert integer parts by repeated division or weighted sum; convert fractional parts by repeated multiplication or negative powers.

Hexadecimal is compact binary: one hex digit represents four bits. Octal represents three bits. Always specify bit width—`1111` can be unsigned 15 or signed two’s-complement -1.

### P0 — Unsigned and signed integers

For `n` bits:

- unsigned range: `0` to `2^n - 1`;
- two’s-complement signed range: `-2^(n-1)` to `2^(n-1)-1`.

To negate an `n`-bit two’s-complement number: invert bits and add one, discarding carry beyond width. Zero has one representation, and the negative range contains one extra value.

### P0 — Carry vs signed overflow

Carry-out indicates unsigned overflow. Signed two’s-complement overflow occurs when adding operands of the same sign produces a result of the opposite sign. Equivalent hardware test: carry into the sign bit differs from carry out.

Example in 4 bits: `0111 (7) + 0001 (1) = 1000`, which represents `-8`; signed overflow occurred even though the bit addition is valid modulo 16.

### P1 — Fixed point and floating point

Fixed point chooses an implied binary-point position; it is predictable and efficient but has limited dynamic range. IEEE-style floating point represents sign, biased exponent, and fraction/significand, with normal, subnormal, infinity, and NaN cases. Floating point provides wide dynamic range but finite precision; addition is not mathematically associative because of rounding.

### P1 — Codes

- BCD stores each decimal digit in four bits; six of sixteen patterns are invalid.
- Gray code changes one bit between adjacent values, useful when transition ambiguity matters, such as some encoders.
- ASCII/Unicode are character-encoding concepts; Unicode assigns abstract code points while UTF-8/UTF-16 encode them.
- Parity detects any odd number of bit flips but cannot correct and misses even-count changes.

## 2. Boolean algebra and logic minimization

### P0 — Fundamental operations and laws

Know identity, null, idempotent, complement, involution, commutative, associative, distributive, absorption, and De Morgan:

```text
NOT(A AND B) = (NOT A) OR (NOT B)
NOT(A OR B)  = (NOT A) AND (NOT B)
```

De Morgan is essential when implementing with NAND/NOR. NAND and NOR are **functionally complete**: any Boolean function can be built using only one of them.

### P0 — SOP, POS, minterms, maxterms

- A minterm is true for exactly one input assignment; canonical SOP is OR of selected minterms.
- A maxterm is false for exactly one assignment; canonical POS is AND of selected maxterms.
- Canonical forms include every variable in each term; minimized forms may not.

### P0 — Karnaugh map

Place cells in Gray-code adjacency. Group `1,2,4,8,...` adjacent 1s for SOP or 0s for POS, wrap around edges, use the largest useful groups, and allow overlap when it reduces literals. Don’t-care entries may be used or ignored to simplify.

A K-map gives a two-level simplification for small variable counts. It does not automatically optimize propagation delay, fan-in, hazards, or a multilevel technology mapping.

### P1 — Static hazards

A static-1 hazard briefly drops output from 1 due to unequal path delays; in an SOP network it can be removed by adding a consensus term covering adjacent 1-regions. Synchronous systems often sample after settling, but asynchronous/control signals may require hazard-free design.

## 3. Combinational circuits

### P0 — Combinational vs sequential

A combinational circuit’s output depends only on current inputs after propagation delay. A sequential circuit’s output/state depends on current inputs and stored past state.

### P0 — Half/full adder and subtractor

Half adder:

```text
sum   = A XOR B
carry = A AND B
```

Full adder:

```text
sum  = A XOR B XOR Cin
Cout = AB + Cin(A XOR B)
```

Cascade full adders for ripple-carry addition; worst-case delay grows with word width because carry ripples. Carry-lookahead computes generate/propagate relationships in parallel at greater hardware complexity.

Subtraction `A-B` can use `A + two_complement(B)`, allowing one adder-subtractor with XOR-controlled inversion and initial carry-in.

### P0 — Multiplexer

A `2^k-to-1` MUX selects one data input using `k` select bits. It can implement Boolean functions by assigning variables to select lines and wiring data inputs to constants/remaining variables. A MUX is a data selector; a demultiplexer routes one input to one selected output.

### P0 — Decoder and encoder

- Decoder: `n` input code activates one of up to `2^n` outputs, often with enable; used in address/chip select and minterm generation.
- Encoder: inverse-style operation that codes an active input; a priority encoder resolves multiple active inputs and usually exposes a valid bit.

### P1 — Comparator and ALU

A magnitude comparator determines `<`, `=`, `>`; wide comparison cascades from most significant differences. An ALU selects arithmetic/logic functions and produces flags such as zero, negative/sign, carry, and overflow. Flags must be interpreted according to signed/unsigned operation.

### Board — Implement a function

Given truth table or `F(A,B,C)=Σm(...)`:

1. write canonical SOP;
2. minimize with K-map;
3. implement using AND/OR/NOT;
4. transform to NAND-only using double negation and De Morgan;
5. discuss propagation levels and any hazard.

## 4. Sequential circuits and timing

### P0 — Latch vs flip-flop

A latch is level-sensitive: while enable is active, output can follow input. A flip-flop is edge-triggered: it samples at a clock edge. Both store state, but timing behavior differs.

### P0 — Common flip-flops

| Type | Next-state behavior |
|---|---|
| SR | set/reset; basic form has a forbidden/ambiguous combination |
| D | `Q_next = D` |
| JK | hold, reset, set, toggle; `Q_next = J*NOT(Q) + NOT(K)*Q` |
| T | hold when 0, toggle when 1; `Q_next = T XOR Q` |

Know characteristic tables (input/state to next state) and excitation tables (current/desired next state to required input). D is easiest for synthesized state machines; T is natural for counters.

### P0 — Setup, hold, and clock-to-Q

- Setup time: input must be stable before the active edge.
- Hold time: input must remain stable after it.
- Clock-to-Q: delay from sampling edge to output change.
- Combinational delay: maximum/minimum data-path delay between registers.

A simplified single-cycle timing constraint is:

```text
Tclock >= t_clk_to_Q + t_comb_max + t_setup + t_skew_margin
```

Hold is a minimum-delay constraint and cannot normally be fixed just by slowing the clock.

### P0 — Metastability

If setup/hold is violated, a flip-flop can enter a metastable analog state before resolving. It cannot be eliminated completely; synchronizer chains reduce the probability that metastability propagates when sampling an asynchronous single-bit signal. Multi-bit clock-domain crossing needs a protocol such as handshake, Gray-coded counter, or asynchronous FIFO—not independent synchronizers for every bit.

### P1 — Race-around and master-slave idea

In a level-triggered JK device with `J=K=1` and a clock pulse longer than propagation behavior, repeated toggling can make final state uncertain. Edge-triggered/master-slave structures avoid the classical race-around issue.

## 5. Registers and counters

### P0 — Registers

A register is a group of flip-flops storing a word. Shift registers move data per clock:

- SISO, SIPO, PISO, PIPO;
- bidirectional/universal shift register;
- applications include serialization, delay, sequence generation, and arithmetic shifts.

Logical shift inserts zeros; arithmetic right shift replicates sign bit for two’s-complement signed division-like behavior, with rounding caveats. Rotate wraps bits around.

### P0 — Asynchronous/ripple counter

Only the first flip-flop receives the external clock; each later stage is clocked by a previous output. Each toggling stage divides frequency by two, but transitions ripple, causing cumulative delay and temporary invalid decoded states.

For a 32 kHz clock and four actual divide-by-two stages:

```text
Q1 = 16 kHz
Q2 =  8 kHz
Q3 =  4 kHz
Q4 =  2 kHz
```

Thus **the fourth flip-flop output is 2 kHz**. The reported 4 kHz answer is the third-stage output or uses a different counting convention. Draw and label stages before answering.

### P0 — Synchronous counter

All flip-flops receive the same clock; combinational next-state logic determines which toggle. It is faster and avoids ripple accumulation, though next-state logic grows. A modulo-`M` counter needs at least `ceil(log2 M)` flip-flops and must handle unused states deliberately.

For a synchronous binary up-counter using T flip-flops:

```text
T0 = 1
T1 = Q0
T2 = Q1 Q0
T3 = Q2 Q1 Q0
```

### P1 — Ring and Johnson counters

A ring counter circulates one hot bit; `n` flip-flops give up to `n` states and simple decoding. A Johnson/twisted-ring counter feeds inverted last output to first and produces up to `2n` states. Both use more flip-flops than a binary counter but can simplify decoding/timing.

### Board — Design a modulo counter

1. determine number of flip-flops;
2. list states and desired transitions;
3. choose D/JK/T flip-flops;
4. use excitation table and K-map for input equations;
5. decide what unused states do—self-correct or reset;
6. draw clock/reset and discuss synchronous vs asynchronous reset.

## 6. Finite-state machines

### P0 — Moore vs Mealy

- Moore output depends only on state; often changes after a clock edge and is easier to keep glitch-free.
- Mealy output depends on state and current input; may respond within the cycle with fewer states, but input glitches can affect output.

Design steps:

1. define behavior/overlap policy;
2. create state diagram;
3. make state/output table;
4. minimize equivalent states if useful;
5. assign binary/one-hot encoding;
6. derive next-state/output logic;
7. verify reset and all input/state combinations.

### Board — Sequence detector

Design an overlapping detector for `101`. Explain why after recognizing `101`, the final `1` may also be the prefix of the next pattern. Produce Moore and Mealy versions and compare state count/output timing.

## Part II — Computer Architecture

## 7. Architecture, organization, and ISA

### P0 — Architecture vs organization

- **ISA/architecture:** programmer-visible contract—operations, registers, types, addressing, instruction encodings, memory/exception/privilege behavior.
- **Microarchitecture/organization:** implementation—pipeline, cache, branch predictor, buses, execution units, control logic.

Different processors can implement the same ISA with different performance/power; binaries remain compatible within defined extensions and system conventions.

### P0 — Von Neumann vs Harvard

A classic Von Neumann design uses a shared memory/address path for instructions and data; a Harvard design separates them. Modern CPUs often present a unified address space while using split L1 instruction/data caches—modified Harvard organization. The “Von Neumann bottleneck” refers to limited instruction/data transfer relative to computation.

### P0 — RISC vs CISC

RISC traditionally emphasizes regular, simple instructions, load/store operation, and easier pipelining; CISC emphasizes richer, variable-format instructions and memory operations. Modern designs blur the boundary: a CISC ISA may decode into internal micro-operations, and RISC ISAs gain extensions. Compare actual ISA and implementation, not slogans like “RISC is always faster.”

### P0 — Instruction formats and addressing modes

Fields may encode opcode, source/destination registers, immediate, and function bits. Common addressing:

- immediate;
- register;
- direct/absolute;
- register indirect;
- base + displacement;
- indexed/scaled indexed;
- PC-relative;
- stack/implied.

Effective-address calculation belongs to the ISA. PC-relative addressing supports relocatable branches; base+offset is common for stack frames/arrays/structures.

## 8. Datapath and control

### P0 — Instruction cycle

Conceptually:

```text
fetch -> decode/register read -> execute/address calculation
-> memory access if required -> write back -> next PC
```

Interrupt/exception checks and precise state rules integrate with this sequence.

### P0 — Basic datapath

Draw program counter, instruction memory/cache, register file, sign/immediate generator, ALU, data memory/cache, multiplexers, and control. For each instruction ask:

1. which values are read?
2. what ALU operation/effective address is needed?
3. is memory read/written?
4. what writes back?
5. how is next PC chosen?

### P0 — Hardwired vs microprogrammed control

Hardwired control derives control signals with logic/FSMs—fast but harder to modify for complex instruction sets. Microprogrammed control stores microinstructions in control memory—flexible/structured but adds control-store sequencing overhead. Modern CPUs may combine hardwired common paths and microcode for complex operations/patches.

### P1 — Single-cycle vs multicycle

A single-cycle design completes every instruction in one long clock, so clock period must accommodate the slowest instruction and hardware may be duplicated. A multicycle design reuses units across shorter steps with control state; instructions take different cycle counts. Pipelining overlaps steps of different instructions.

## 9. Performance analysis

### P0 — CPU-time equation

```text
CPU time = instruction count × CPI × clock cycle time
         = instruction count × CPI / clock rate
```

Clock rate alone does not determine performance. An optimization can change instruction count, CPI, and clock period. Use execution time for a defined workload.

### P0 — Latency, throughput, speedup

Latency is time for one task; throughput is tasks per unit time. Pipelining ideally improves throughput after filling, not the intrinsic latency of one instruction. Speedup is `old_time/new_time`.

### P0 — Amdahl’s law

If fraction `f` is improved by factor `s`:

```text
overall speedup = 1 / ((1-f) + f/s)
```

The unimproved fraction limits total speedup. Accelerating 90% infinitely gives at most 10×. For parallelism, clarify serial fraction and overhead; real scaling also has communication/contention.

### P1 — CPI composition

Average CPI is weighted by instruction mix plus stall contributions:

```text
CPI = base CPI + memory-stall CPI + branch-stall CPI + other stalls
```

This connects cache misses and branch prediction to execution time.

## 10. Pipelining

### P0 — Five-stage pipeline

Typical educational stages: IF, ID, EX, MEM, WB. Pipeline registers isolate stages. Ideal steady-state CPI approaches 1 for a single-issue pipeline, but fill/drain and hazards add cycles.

### P0 — Hazards

- **Structural:** two operations need same hardware resource; duplicate, multiport, or schedule it.
- **Data:** an instruction depends on another.
- **Control:** next PC uncertain due to branch/jump/exception.

In a simple in-order pipeline:

- RAW (read after write) is the main true dependency;
- WAR and WAW do not normally occur with in-order read/write stages, but appear in out-of-order execution.

Forwarding/bypassing routes a produced value directly to a later pipeline stage without waiting for register write-back. A load-use dependency may still require a bubble because data arrives after memory stage. Compiler scheduling can fill delay opportunities when ISA/compiler permits.

### P0 — Branch handling

Options include stall until resolved, predict static/dynamic, compute target early, and speculatively execute. On misprediction, wrong-path work is flushed. Deeper/wider pipelines can have larger penalties. A branch predictor predicts direction; a branch target buffer predicts/holds target; a return-address stack helps returns.

### P1 — Superscalar and out-of-order

Superscalar processors issue several instructions per cycle if dependencies/resources permit. Register renaming removes false WAR/WAW name dependencies. Out-of-order execution schedules ready operations while preserving architectural correctness, commonly committing in order through a reorder structure for precise exceptions.

### Board — Pipeline trace

Trace five instructions in a stage table. Mark a RAW dependency, forwarding path, one load-use stall, branch resolution, and flush. Calculate total cycles, not just ideal `n+k-1`.

## 11. Memory hierarchy and cache

### P0 — Why hierarchy works

Fast memory is expensive/small; large memory is slower/cheaper. Temporal and spatial locality let small upper levels serve most accesses. Typical hierarchy: registers, L1/L2/L3 caches, DRAM, SSD/HDD.

### P0 — Cache address fields

For byte-addressed memory:

```text
number of sets = cache_size / (block_size × associativity)
offset bits    = log2(block_size)
index bits     = log2(number of sets)
tag bits       = address_bits - index_bits - offset_bits
```

Example: 32-bit addresses, 32 KiB cache, 64-byte block, 4-way:

```text
sets = 32768/(64×4)=128
offset=6, index=7, tag=19 bits
```

### P0 — Mapping organizations

- Direct mapped: one possible line per block; simple/fast, more conflict misses.
- Fully associative: any line; minimal mapping conflict, expensive lookup/replacement.
- Set associative: block maps to one set and any way in it; practical compromise.

Miss types: compulsory/cold, capacity, and conflict; coherence misses are added in multiprocessors. Increasing associativity mainly reduces conflict misses but can affect hit time/energy.

### P0 — Write policy

- Write-through: update next level on every hit, usually with write buffer; simpler coherence/durability path but more traffic.
- Write-back: update cached block and mark dirty; write to next level on eviction; reduces traffic but complicates replacement/coherence.
- Write-allocate: on write miss fetch block then write, common with write-back.
- No-write-allocate/write-around: write lower level without filling, often paired with write-through.

### P0 — AMAT

```text
AMAT = hit time + miss rate × miss penalty
```

For multiple levels, expand miss penalty recursively. Use rates conditional on reaching that level. A small miss-rate reduction can dominate if penalty is large.

### P1 — Replacement and prefetching

LRU is feasible only approximately/at low associativity; pseudo-LRU, random, and adaptive policies are common. Prefetching can hide latency but may waste bandwidth, pollute cache, or fetch unused data.

### P0 — Cache coherence

Private multicore caches may hold copies. Coherence protocols maintain per-block write serialization/visibility, often with states such as Modified, Exclusive, Shared, Invalid. **False sharing** occurs when independent variables on the same cache line cause coherence traffic. Coherence does not itself provide correct synchronization or a simple global ordering of all memory operations.

## 12. Main memory and virtual memory interface

### P1 — SRAM vs DRAM vs nonvolatile storage

SRAM uses bistable cells, is fast and no refresh but larger/costlier—used for caches. DRAM stores charge, needs refresh, is dense—used for main memory. Flash is nonvolatile with erase/write constraints—used for storage and embedded program memory.

### P1 — DRAM organization

DRAM is organized into channels, ranks, banks, rows, and columns. A row buffer makes accesses to an open row faster; controllers schedule requests for locality and timing constraints. Bandwidth and latency are distinct.

### P0 — Cache vs TLB vs page table

- Cache maps physical or virtual-address-related blocks to cached **data/instructions**.
- TLB caches recent **address translations/permissions**.
- Page table is the authoritative in-memory translation/protection structure managed by OS/hardware.

A TLB miss can be a page-table hit; a cache miss can occur with a TLB hit; a page fault is much more expensive and enters the OS.

## 13. I/O, buses, and interrupts

### P0 — Bus/interconnect concepts

An interconnect carries addresses/requests, data, and control/response. Key issues are width, bandwidth, arbitration, synchronous/asynchronous timing, latency, protocol, and multiple masters. Modern systems use point-to-point packetized interconnects as well as traditional buses.

### P0 — Memory-mapped vs isolated I/O

Memory-mapped I/O gives device registers addresses in the normal address space and uses load/store instructions; regions require special ordering/cache attributes. Isolated/port-mapped I/O uses a separate address space and instructions. MMIO pointers must be treated with the platform/language’s volatile and ordering rules, but `volatile` alone does not create thread synchronization.

### P0 — Polling, interrupt, and DMA

- Polling repeatedly reads status—low setup, wastes CPU for long waits.
- Interrupt lets a device notify CPU—better for infrequent events, incurs handler/context overhead.
- DMA moves blocks between device and memory after CPU setup—efficient for bulk transfer; coherence, pinning/mapping, and completion must be managed.

### P0 — Interrupt sequence

Device asserts request; controller prioritizes/masks and supplies vector or cause; CPU completes/precisely stops at an architectural boundary, saves context, enters privileged handler, acknowledges/services source, and returns. Exact sequence is architecture-specific.

- Maskable interrupts can be disabled/prioritized.
- Non-maskable interrupts are reserved for critical events.
- Exceptions are synchronous; interrupts are normally asynchronous.

### P1 — Interrupt latency

Latency includes current-instruction completion, masking/priority, pipeline effects, context save, handler dispatch, and higher-priority work. Real-time design bounds the worst case, keeps ISRs short, and defers substantial work.

## Part III — Microprocessors and Microcontrollers

## 14. Microprocessor, microcontroller, and SoC

### P0 — Precise comparison

| Microprocessor | Microcontroller |
|---|---|
| CPU-centric, often requires external RAM/storage/peripherals | CPU + flash/RAM + GPIO/timers/serial/ADC on one chip |
| General-purpose/high-performance systems | Embedded control, deterministic I/O, low power/cost |
| Rich OS/MMU/cache often expected | May run bare-metal or RTOS; capabilities vary |
| Flexible large memory/system expansion | Integrated but resource-limited |

A system-on-chip integrates one or more processors plus controllers/accelerators/interconnect and may be far more capable than a traditional MCU. Categories overlap; compare a specific device and application.

### P0 — Why can a microcontroller be cheap?

System-level integration reduces chip count, PCB area, external buses, power circuitry, packaging, assembly, and memory requirements. Simpler cores, modest clocks, small on-chip memories, mature fabrication nodes, and enormous volume also help. A high-end MCU can cost more than a low-end microprocessor, so “always cheaper” is wrong.

### P0 — Minimum embedded system

An MCU-based design needs suitable clock/reset, power/decoupling, programming/debug path, and application I/O. Firmware configures pin multiplexing, direction, pull-ups, timers, interrupts, and peripherals. Watchdog and brown-out reset improve resilience.

## 15. Processor registers, stack, and assembly reasoning

### P0 — Register categories

- general-purpose/data registers;
- program counter/instruction pointer;
- stack pointer;
- status/flags register;
- control/system registers;
- index/base/address registers depending on ISA.

Calling conventions specify argument/return registers, caller/callee-saved registers, stack alignment, return address, and stack-frame rules. They are an ABI/software convention layered on the ISA.

### P0 — Stack operation

The stack supports calls, returns, local storage, saved registers, and interrupt context. Stack direction and whether SP points to last-used/next-free are ISA-specific. A buffer overflow can corrupt control data when protection/compiler/runtime controls fail; stack and heap are memory-management regions, not different physical memory technologies.

### P1 — Assembly trace

When given code:

1. write initial register/memory values;
2. determine operand width and signedness;
3. calculate effective address;
4. update destination;
5. update only flags defined by the instruction;
6. follow branch condition precisely.

Do not infer high-level types that assembly does not carry.

## 16. Classic 8086 concepts

### P1 — Why 20-bit address from 16-bit registers?

On the original 8086, the address adder forms `segment << 4` plus the offset and the 20-bit address bus exposes the low 20 bits:

```text
physical = (segment × 16 + offset) mod 2^20
```

Thus ordinary real-mode addresses cover a 1 MiB space. If the arithmetic exceeds `FFFFFh`, the original 8086 discards the carry and wraps; for example, `FFFFh:0010h` wraps to physical `00000h`. Later x86 systems can expose addresses just above 1 MiB when the A20 line is enabled, but that is not the classic 8086-bus answer. Segments can overlap; many segment:offset pairs name the same physical address. Typical segment registers are CS, DS, SS, ES with IP and offset/index registers.

Example: `1234h:0010h -> 12340h + 0010h = 12350h`.

### P1 — BIU and EU

The Bus Interface Unit fetches instructions, forms physical addresses, and handles bus activity; the Execution Unit decodes/executes using registers/ALU. The prefetch queue overlaps fetch and execution, an early pipeline-like optimization. A control transfer flushes/refills the queue.

### P1 — Interrupts

8086 supports hardware/software/internal exceptions through an interrupt vector table. On interrupt, it saves flags and return location, adjusts interrupt/trap control as defined, loads handler CS:IP, then `IRET` restores. Exact signal/vector behavior distinguishes NMI, INTR, software `INT`, and exceptions.

## 17. Microcontroller peripherals

### P0 — GPIO

GPIO pin configuration includes input/output mode, pull-up/down, drive type/strength, alternate function, and sometimes open-drain. A floating digital input can produce unpredictable transitions and power use; a pull resistor defines idle level.

### P0 — Timer/counter and PWM

A timer counts internal clock ticks; a counter may count external events. Prescaler divides clock. Compare registers can generate interrupt or output transitions. PWM represents duty cycle:

```text
duty = high_time / period
```

Used for motor power, LED brightness, and DAC-like filtering. Frequency and resolution trade off for a fixed timer clock/counter width.

### P0 — ADC and DAC

An `n`-bit ADC ideally maps the reference range into `2^n` codes; nominal LSB size is about `Vref/2^n` depending on endpoint convention. Accuracy also depends on reference, noise, sampling time, input impedance, offset/gain error, INL/DNL, and effective number of bits. Sampling must respect signal bandwidth/anti-aliasing; Nyquist’s rate condition alone does not build the filter.

### P0 — UART, SPI, and I2C

| UART | SPI | I2C |
|---|---|---|
| asynchronous, TX/RX, agreed baud/frame | synchronous, clock + data + chip select, full duplex | two-wire open-drain clock/data, addressed shared bus |
| point-to-point/common serial | high speed, more select wires | multi-device, arbitration/ACK, pull-ups |

UART uses start/data/optional parity/stop framing and no shared clock. SPI modes depend on clock polarity/phase. I2C devices use start/stop, address, ACK/NACK; open-drain outputs require pull-ups and allow wired arbitration.

### P0 — Watchdog

A watchdog timer resets or interrupts the system unless software services it within a window. Service it only after confirming critical tasks are healthy; blindly kicking it from an unrelated timer hides failures.

### P1 — Debouncing

Mechanical switches bounce, producing rapid transitions. Debounce with RC/Schmitt hardware or software sampling/time validation. An ISR should not normally busy-wait through the entire debounce interval.

### P1 — Bare metal vs RTOS

Bare-metal superloop is simple and low overhead but becomes difficult as concurrency/timing grows. An RTOS provides tasks, priorities, timers, queues, semaphores, and scheduling, but introduces context switching, stack sizing, priority inversion, and concurrency design. Hard real-time means provable deadlines, not simply using an RTOS.

## 18. Hardware/software co-design and reliability

### P1 — Choosing hardware

Consider computation, memory, I/O/peripherals, deadline/latency, power/energy, cost, environment, certification, security, toolchain, lifecycle, and supply. “Fastest CPU” may increase cost/power without solving ADC accuracy or real-time response.

### P1 — Reset and clock-domain design

Power-on reset initializes a known state. Asynchronous assertion with synchronous deassertion is common because release near a clock edge can violate timing. Clock gating saves dynamic power but must avoid glitches; use dedicated cells/enables rather than arbitrary combinational clock logic.

### P1 — Faults and protections

- brown-out detector for low voltage;
- watchdog for stalled software;
- ECC/parity for memory/data integrity;
- CRC for communication/storage error detection;
- MPU/MMU for region/process protection;
- secure boot verifies authorized firmware;
- debug-port locking and key protection;
- redundancy/fail-safe state for safety requirements.

Security and safety overlap but differ: safety protects people/environment from accidental failure; security handles malicious behavior. A secure design can still be unsafe and vice versa.

## 19. Board-ready exercises

1. Minimize a four-variable Boolean function using K-map; implement NAND-only.
2. Build a full adder from half adders and derive carry.
3. Convert JK/T excitation requirements into a modulo-6 synchronous counter.
4. Draw an overlapping `101` Moore/Mealy detector.
5. Calculate four-stage ripple-counter frequencies from 32 kHz.
6. Draw a single-cycle datapath for load, store, arithmetic, and branch.
7. Trace pipeline hazards with forwarding, one load stall, and a branch flush.
8. Calculate CPU time/CPI and apply Amdahl’s law.
9. Split cache address into tag/index/offset and calculate AMAT.
10. Trace polling vs interrupt vs DMA for an input device.
11. Compute an 8086 segment:offset physical address and identify registers.
12. Configure conceptually an MCU timer for periodic interrupt/PWM.
13. Compare UART, SPI, and I2C for a sensor and justify one.

## 20. High-yield comparisons

| Pair | Strong distinction |
|---|---|
| Combinational vs sequential | current inputs only vs stored state/history |
| Latch vs flip-flop | level-sensitive vs edge-triggered |
| Synchronous vs ripple counter | shared clock/parallel transition vs chained clocks/delay |
| Moore vs Mealy | output from state vs state + input |
| Carry vs overflow | unsigned width overflow vs signed range error |
| Architecture vs organization | programmer contract vs implementation |
| RISC vs CISC | design traditions, not universal speed ranking |
| Single-cycle vs pipeline | one long cycle per instruction vs overlapped stages |
| Latency vs throughput | time per task vs tasks per time |
| RAW vs WAR/WAW | true dependency vs name dependencies |
| Direct vs associative cache | one location vs many possible locations |
| Write-through vs write-back | immediate lower update vs dirty eviction |
| Cache vs TLB | data/instructions vs address translations |
| Polling vs interrupt | repeated checking vs device notification |
| Interrupt vs exception | asynchronous external vs synchronous instruction-related |
| Microprocessor vs MCU | CPU-centric system vs integrated embedded controller |
| UART vs SPI vs I2C | async point link vs synchronous selected bus vs addressed two-wire bus |

## 21. Rapid oral questions

1. **Why is XOR useful in an adder?** It produces sum without carry for two bits; parity-like odd-one behavior extends with carry-in.
2. **Can NAND build NOT?** Tie inputs together: `NAND(A,A)=NOT A`.
3. **Why Gray code in an encoder?** Adjacent positions change one bit, reducing ambiguous multi-bit transitions.
4. **Does K-map always give globally best hardware?** It minimizes two-level literals for small functions, not every timing/technology objective.
5. **Why not gate a clock with ordinary AND logic?** Glitches/skew can create unintended edges; use clock-enable/dedicated gating structures.
6. **Can metastability be eliminated?** No; probability can be reduced to an acceptable level with proper CDC design.
7. **Why is synchronous counter faster?** All state elements share the edge; logic delay does not accumulate through clocked stages.
8. **How many flip-flops for modulo 10?** At least 4 because `2^3<10<=2^4`; handle six unused states.
9. **Why can Mealy need fewer states?** Output can depend directly on input rather than encoding response in a separate state.
10. **Does higher clock rate mean faster CPU?** Not alone; instruction count and CPI matter.
11. **Why can a pipeline be slower for one instruction?** Pipeline-register overhead and stage partitioning can increase individual latency even as throughput improves.
12. **What is a precise exception?** Architectural state appears as if all older instructions completed and no younger instruction did.
13. **What does forwarding solve?** Many RAW hazards by routing result before register write-back; not all timing cases such as immediate load-use.
14. **What is false sharing?** Different cores update independent data sharing one cache line, causing coherence invalidations.
15. **Why is fully associative cache expensive?** A tag may need comparison against every line/way and replacement tracking.
16. **Does write-back lose data?** Dirty data is vulnerable to failures before reaching durable storage; systems define persistence and protection separately.
17. **Why use DMA?** Bulk transfer without CPU copying each word, improving CPU availability and throughput.
18. **Why does an MCU still need decoupling capacitors?** Local transient current and supply-noise control for reliable switching.
19. **Can UART devices communicate at arbitrary different baud rates?** They must agree closely enough on baud and framing for sampling tolerance.
20. **Why is I2C open-drain?** Devices can safely share lines, acknowledge, and arbitrate without driving opposite levels; pull-ups restore high.

## 22. Common wrong answers

- “Digital 0 and 1 are exactly 0 V and 5 V.” They are logic ranges depending on technology/supply.
- “Sequential circuits always need a clock.” Asynchronous sequential circuits exist; synchronous design is dominant.
- “Four flip-flops at 32 kHz output 4 kHz.” The fourth divide-by-two output is 2 kHz; label counting.
- “Asynchronous counters are faster.” Ripple delay makes them slower for larger/high-speed designs.
- “A microprocessor has no memory.” It has registers/caches; the distinction is system integration, not absolute absence.
- “Microcontrollers are always 8-bit and slow.” Modern MCUs include powerful 32/64-bit cores, DSP, accelerators, and rich peripherals.
- “RISC uses fewer instructions in a program.” It means a design philosophy; dynamic instruction count can be greater or smaller.
- “Pipelining reduces execution time of every instruction.” It mainly increases throughput.
- “Cache stores the most recently used data only.” Placement and replacement policy approximate locality under constraints.
- “Virtual memory and cache are the same.” One is address abstraction/protection/capacity management; the other is mainly speed hierarchy.
- “Interrupt is always faster than polling.” High-rate/tiny work can make polling efficient; workload matters.
- “DMA means CPU is uninvolved.” CPU/driver sets up, synchronizes, maps buffers, and handles completion/errors.
- “An RTOS makes a system real-time.” Schedulability and bounded worst-case behavior do.

## 23. Hardware core-subject self-test

- [ ] Convert signed/unsigned numbers and detect carry/overflow.
- [ ] Minimize Boolean functions and implement NAND/NOR-only.
- [ ] Derive adders, MUX/decoder designs, and an ALU slice.
- [ ] Explain flip-flop equations/excitation and setup/hold/metastability.
- [ ] Design synchronous modulo counters and Moore/Mealy sequence detectors.
- [ ] Draw an ISA-to-datapath explanation and compare control implementations.
- [ ] Calculate CPU time, CPI, speedup, and Amdahl limits.
- [ ] Trace pipeline hazards, forwarding, stalls, prediction, and flushes.
- [ ] Calculate cache fields, miss types, write policies, AMAT, and false sharing.
- [ ] Explain DRAM, virtual-memory interface, buses, MMIO, interrupt, and DMA.
- [ ] Defend microprocessor vs MCU/SoC and explain why integration affects cost.
- [ ] Trace registers/stack/calling convention and an 8086 segment address.
- [ ] Explain GPIO, timer/PWM, ADC, UART, SPI, I2C, watchdog, and RTOS trade-offs.
- [ ] Complete at least five board exercises cleanly within five minutes each.
