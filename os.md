# 🖥️ Operating Systems: Processes, Threads & Context Switching

An Operating System (OS) is the software layer that manages the computer's hardware and provides an environment in which applications can run.

When you open:

```text
Chrome
VS Code
Spotify
Python
Terminal
```

you might think each application simply "runs."

Underneath, the Operating System is constantly managing:

* 🧠 CPU
* 💾 Memory
* 📁 Files
* 🔌 Devices
* 🌐 Network resources
* ⚙️ Processes
* 🧵 Threads

This README explores how the OS actually manages programs while they are running.

---

# 🧩 1. What is an Operating System?

A simplified computer system looks like:

```text
┌───────────────────────────────┐
│        Applications           │
│ Chrome │ VS Code │ Python     │
├───────────────────────────────┤
│       Operating System        │
├───────────────────────────────┤
│ Hardware                      │
│ CPU │ RAM │ Disk │ Devices    │
└───────────────────────────────┘
```

The OS acts as a bridge between applications and hardware.

Instead of applications directly controlling every hardware component, they request services from the OS.

---

# ⚙️ 2. Program vs Process

These two terms are extremely important.

## Program

A program is a passive set of instructions stored somewhere, such as a file on disk.

For example:

```text
calculator.exe
```

or:

```text
python_script.py
```

It isn't necessarily running.

## Process

A process is a **program that is currently executing**.

```text
Program
   ↓
Execution
   ↓
Process
```

For example:

```text
python.py
    ↓
Run
    ↓
Python Process
```

A process contains much more than just the program's instructions.

---

# 🧠 3. What Does a Process Contain?

A running process generally has:

```text
Process
   │
   ├── Program Code
   ├── Data
   ├── Stack
   ├── Heap
   ├── CPU Registers
   └── Process State
```

Conceptually:

```text
┌─────────────────────┐
│       Process       │
├─────────────────────┤
│ Code                │
├─────────────────────┤
│ Data                │
├─────────────────────┤
│ Heap                │
├─────────────────────┤
│ Stack               │
├─────────────────────┤
│ Registers / State   │
└─────────────────────┘
```

---

# 🔄 4. Process States

A process doesn't simply have two states:

```text
Running
Not Running
```

Operating Systems typically model several states.

A simplified model is:

```text
       ┌──────────┐
       │   New    │
       └────┬─────┘
            ↓
       ┌──────────┐
       │  Ready   │
       └────┬─────┘
            ↓
       ┌──────────┐
       │ Running  │
       └────┬─────┘
         ↙       ↘
        ↓         ↓
   Waiting       Exit
        ↓
     Ready
```

---

# 🟢 5. New

The process has been created.

For example:

```text
You open VS Code
       ↓
OS creates process
       ↓
Process = NEW
```

---

# 🟡 6. Ready

The process is ready to execute but is waiting for CPU time.

Imagine:

```text
CPU
 ↑
 │
 ├── Process A
 ├── Process B
 ├── Process C
 └── Process D
```

Only some process can actually use a particular CPU core at a time.

The others wait in the ready queue.

---

# 🔴 7. Running

The CPU is currently executing instructions belonging to the process.

```text
CPU
 ↓
Process A
 ↓
Instruction
 ↓
Instruction
 ↓
Instruction
```

---

# 🟠 8. Waiting / Blocked

A process may need something that isn't immediately available.

For example:

```text
Process
   ↓
Read from Disk
   ↓
Waiting...
```

There is no point wasting CPU time while waiting for a slow I/O operation.

So the OS can move the process into a waiting state.

```text
Running
   ↓
I/O Request
   ↓
Waiting
```

Once the operation completes:

```text
Waiting
   ↓
Ready
```

---

# ⚫ 9. Terminated

When a process finishes:

```text
Running
   ↓
Exit
   ↓
Terminated
```

The OS can then clean up the resources associated with the process.

---

# 🧠 10. Process Control Block

The OS needs to keep track of every process.

It does this using a data structure commonly called the:

> **Process Control Block (PCB)**

A PCB may contain information such as:

```text
┌────────────────────────────┐
│ Process Control Block      │
├────────────────────────────┤
│ Process ID                 │
│ Process State              │
│ Program Counter            │
│ CPU Registers              │
│ Scheduling Information     │
│ Memory Information         │
│ I/O Information            │
└────────────────────────────┘
```

The PCB is essentially the OS's record of the process.

---

# 🆔 11. Process ID

Every process needs an identifier.

This is commonly called:

```text
PID
```

For example:

```text
Chrome → PID 4210
Python → PID 5321
VS Code → PID 7124
```

The exact IDs depend on the system and change over time.

---

# 🧮 12. Program Counter

The Program Counter (PC) stores the address of the next instruction that should be executed.

Imagine:

```text
Instruction 1
Instruction 2
Instruction 3  ← Current
Instruction 4
Instruction 5
```

The program counter tells the CPU where execution should continue.

This becomes extremely important during context switching.

---

# 🧵 13. What is a Thread?

A thread is a unit of execution within a process.

A process can contain:

```text
One thread
```

or:

```text
Multiple threads
```

For example:

```text
Process
   │
   ├── Thread 1
   ├── Thread 2
   ├── Thread 3
   └── Thread 4
```

This allows different tasks within the same application to execute concurrently.

---

# 🆚 14. Process vs Thread

A useful simplified comparison:

| Process                             | Thread                                   |
| ----------------------------------- | ---------------------------------------- |
| Independent execution environment   | Execution unit inside a process          |
| More isolated                       | Shares process resources                 |
| Usually more expensive to create    | Usually cheaper to create                |
| Has its own address space           | Threads of a process share address space |
| Communication can be more expensive | Communication can be easier              |

Think:

```text
Process = House 🏠

Threads = People working inside the house 👨‍💻👩‍💻
```

The people share the same house but can perform different tasks.

---

# 🚀 15. Why Multiple Threads?

Imagine a web browser.

It might need to:

```text
Download data
Render a page
Handle user input
Play audio
Run JavaScript
```

Doing everything sequentially could make the application feel unresponsive.

Multiple threads can allow different activities to make progress concurrently.

```text
Browser Process
      │
 ┌────┼─────┬─────┐
 ↓    ↓     ↓     ↓
UI  Network Audio  JS
```

---

# 🧠 16. CPU Scheduling

Suppose we have:

```text
Process A
Process B
Process C
Process D
```

but only one CPU core.

Which process gets the CPU?

That's the job of the:

> **CPU Scheduler**

```text
Ready Queue
     │
     ↓
┌──────────────┐
│   Scheduler  │
└──────┬───────┘
       ↓
      CPU
```

The scheduler selects a process to execute.

---

# ⏱️ 17. Why Scheduling is Necessary

Imagine a restaurant with one chef:

```text
Chef 👨‍🍳
  │
  ├── Order A
  ├── Order B
  ├── Order C
  └── Order D
```

The chef needs some strategy for deciding which order to prepare.

Similarly:

```text
CPU
 │
 ├── Process A
 ├── Process B
 ├── Process C
 └── Process D
```

The OS needs a scheduling policy.

---

# 📚 18. FCFS Scheduling

FCFS means:

> **First Come, First Served**

The process that arrives first gets executed first.

Example:

```text
P1 → P2 → P3
```

Execution:

```text
P1 → P2 → P3
```

It's simple but can produce poor waiting times.

---

# ⚡ 19. Shortest Job First

SJF selects the process with the shortest expected CPU burst.

Example:

```text
P1 = 8 ms
P2 = 3 ms
P3 = 5 ms
```

Order:

```text
P2 → P3 → P1
```

This can minimize average waiting time under ideal assumptions, but the OS may not know future burst lengths perfectly.

---

# 🔄 20. Round Robin

Round Robin gives each process a small time slice called a:

> **Time Quantum**

Example:

```text
Quantum = 2 ms
```

Processes:

```text
P1
P2
P3
```

Execution might look like:

```text
P1 → P2 → P3 → P1 → P2 → P3 ...
```

Each process gets a turn.

This is particularly useful for interactive systems where responsiveness matters.

---

# 🎯 21. Context Switching

Now we reach one of the most important OS concepts.

Suppose:

```text
CPU is running Process A
```

Then the scheduler decides:

```text
Switch to Process B
```

But the CPU was already in the middle of executing Process A.

How can it safely switch?

The OS must save Process A's execution state.

This is called:

> **Context Switching**

---

# 🔄 22. Context Switch Step-by-Step

Suppose CPU is executing:

```text
Process A
```

The OS:

```text
1. Pause Process A
2. Save its CPU state
3. Store the state in its PCB
4. Load Process B's saved state
5. Resume Process B
```

Diagram:

```text
Process A
    │
    ↓
Save Context
    │
    ↓
PCB of A
    │
    │
    └──────────┐
               ↓
        Load Context
               ↑
               │
          PCB of B
               │
               ↓
           Process B
```

---

# 🧠 23. What is the "Context"?

The context contains information required to resume execution correctly.

For example:

```text
CPU Registers
Program Counter
Stack Pointer
Process State
```

Simplified:

```text
Context
   │
   ├── Program Counter
   ├── Registers
   ├── Stack Pointer
   └── Other CPU State
```

Without this information, the process wouldn't know where to continue.

---

# ⚠️ 24. Context Switching Has a Cost

Context switching is not free.

The CPU spends time:

```text
Saving State
     +
Loading State
     +
Scheduler Work
```

instead of doing useful application work.

Therefore:

```text
Too many switches
       ↓
More overhead
       ↓
Potentially lower efficiency
```

This is called:

> **Context-switch overhead**

---

# 🧠 25. Multitasking

You might wonder:

> "How can my computer run Chrome, Spotify, VS Code, and dozens of background processes simultaneously?"

On a single CPU core, the OS rapidly switches between processes.

```text
Time →

A | B | C | A | D | B | C | A
```

The switching happens extremely quickly.

To humans, it appears that everything is running simultaneously.

This is called:

> **Multitasking**

---

# ⚡ 26. Concurrency vs Parallelism

These terms are often confused.

## Concurrency

Multiple tasks are making progress during overlapping periods.

```text
Task A
████    ████

Task B
    ████    ████
```

## Parallelism

Multiple tasks are literally executing at the same time on different processing units.

```text
CPU Core 1 → Task A
CPU Core 2 → Task B
```

So:

```text
Concurrency ≠ necessarily simultaneous execution

Parallelism = simultaneous execution
```

---

# 🧮 27. Multi-Core CPUs

Modern processors contain multiple cores.

For example:

```text
┌──────────────────────────┐
│          CPU             │
├──────┬──────┬──────┬─────┤
│Core1 │Core2 │Core3 │Core4│
└──────┴──────┴──────┴─────┘
```

Now multiple threads can actually execute in parallel.

```text
Core 1 → Thread A
Core 2 → Thread B
Core 3 → Thread C
Core 4 → Thread D
```

The OS scheduler decides how work is distributed across available CPU resources.

---

# 🔐 28. The Problem with Shared Memory

Threads inside the same process can share memory.

That's powerful.

But it creates danger.

Suppose two threads modify:

```text
counter = 0
```

Thread A:

```text
counter = counter + 1
```

Thread B:

```text
counter = counter + 1
```

You might expect:

```text
counter = 2
```

But depending on the exact interleaving, both threads can read the same old value and overwrite each other's updates.

This is a:

> **Race Condition**

---

# 🚨 29. Race Condition

Imagine:

```text
Initial counter = 0
```

Thread A:

```text
Read 0
```

Thread B:

```text
Read 0
```

Thread A:

```text
Write 1
```

Thread B:

```text
Write 1
```

Final value:

```text
1
```

instead of:

```text
2
```

The result depends on timing.

That's the danger of concurrent access to shared state.

---

# 🔒 30. Critical Section

A critical section is a portion of code where shared data is accessed or modified.

Example:

```python
counter += 1
```

If multiple threads execute this simultaneously, synchronization may be necessary.

Conceptually:

```text
Thread A ──┐
           ↓
       [ LOCK ]
           ↓
    Critical Section
           ↓
       [UNLOCK]
           ↑
Thread B ──┘
```

---

# 🔐 31. Mutex

A mutex provides mutual exclusion.

The basic idea:

```text
Lock
  ↓
Only one thread enters
  ↓
Perform operation
  ↓
Unlock
```

Example concept:

```text
Thread A → 🔒 → Critical Section → 🔓
Thread B → waits
```

After Thread A releases the lock:

```text
Thread B → 🔒 → Critical Section
```

---

# 🧮 32. Semaphore

A semaphore is another synchronization mechanism.

Unlike a simple mutex, a semaphore can represent multiple available resources.

Imagine:

```text
3 database connections available
```

A semaphore could initially have:

```text
count = 3
```

Three threads can acquire access.

```text
Thread A → Connection 1
Thread B → Connection 2
Thread C → Connection 3
Thread D → Wait
```

When one connection becomes free:

```text
Thread A releases
      ↓
Thread D gets access
```

---

# 💀 33. Deadlock

Synchronization introduces another problem:

> **Deadlock**

Imagine:

```text
Thread A owns Lock 1
Thread B owns Lock 2
```

Then:

```text
Thread A waits for Lock 2
Thread B waits for Lock 1
```

Neither can continue.

```text
       ┌──────────────┐
       ↓              │
Thread A            Thread B
   │                    │
   │ waits              │ waits
   ↓                    ↓
 Lock 2              Lock 1
   ↑                    │
   └────────────────────┘
```

Both are stuck.

---

# 🔥 34. The Four Conditions for Deadlock

A classic deadlock requires four conditions:

### 1. Mutual Exclusion

A resource can be held by only one process at a time.

### 2. Hold and Wait

A process holds one resource while waiting for another.

### 3. No Preemption

Resources cannot simply be forcibly taken away.

### 4. Circular Wait

Processes form a circular dependency.

```text
P1 → waits for P2
P2 → waits for P3
P3 → waits for P1
```

Break one of these conditions and deadlock can potentially be prevented.

---

# 🧠 35. System Calls

Applications don't normally access hardware directly.

Instead, they request OS services through:

> **System Calls**

For example:

```text
Application
    ↓
System Call
    ↓
Operating System
    ↓
Hardware
```

A program might request:

```text
Open a file
Read data
Create a process
Allocate memory
Send network data
```

---

# 🏠 36. User Mode vs Kernel Mode

Modern operating systems separate execution into privilege levels.

Simplified:

```text
┌─────────────────────────┐
│       User Mode         │
│ Applications            │
├─────────────────────────┤
│      Kernel Mode        │
│ Operating System        │
├─────────────────────────┤
│ Hardware                │
└─────────────────────────┘
```

Normal applications run with restricted privileges.

The kernel has much greater access to hardware and system resources.

---

# 🚪 37. System Call Transition

Suppose a program wants to read a file.

```text
Application
     ↓
read()
     ↓
System Call
     ↓
Kernel
     ↓
Storage Device
     ↓
Kernel
     ↓
Application
```

The application doesn't simply reach into the disk hardware itself.

The OS mediates the operation.

---

# 💾 38. Memory Management

The OS also manages RAM.

Imagine:

```text
RAM
┌────────────────────────┐
│ Process A              │
├────────────────────────┤
│ Process B              │
├────────────────────────┤
│ Operating System       │
├────────────────────────┤
│ Process C              │
└────────────────────────┘
```

The OS tracks which memory belongs to which process.

This helps provide:

* Isolation
* Protection
* Efficient memory usage

---

# 🧠 39. Virtual Memory

Processes often behave as if they have a large private memory space.

This is enabled through:

> **Virtual Memory**

Conceptually:

```text
Process
   ↓
Virtual Address
   ↓
Memory Management Unit
   ↓
Physical Memory
```

Different processes can use virtual addresses without directly knowing the physical RAM locations.

---

# 📦 40. Paging

Virtual memory is commonly implemented using pages.

Memory can be divided into:

```text
Virtual Memory
┌────┬────┬────┬────┬────┐
│ P1 │ P2 │ P3 │ P4 │ P5 │
└────┴────┴────┴────┴────┘
```

Physical memory contains frames:

```text
Physical RAM
┌────┬────┬────┬────┬────┐
│ F1 │ F2 │ F3 │ F4 │ F5 │
└────┴────┴────┴────┴────┘
```

The OS and hardware memory-management mechanisms map virtual pages to physical frames.

---

# 🔄 41. The Complete Journey

When you launch a program:

```text
Executable File
      ↓
Operating System
      ↓
Create Process
      ↓
Allocate Virtual Address Space
      ↓
Load Program
      ↓
Create/Initialize Threads
      ↓
Ready Queue
      ↓
CPU Scheduler
      ↓
CPU Execution
      ↓
Context Switches
      ↓
I/O / Synchronization
      ↓
More Execution
      ↓
Process Exit
      ↓
Resources Released
```

A simple double-click hides an enormous amount of operating-system machinery.

---

# 🧠 42. The Big Picture

The operating system is constantly coordinating:

```text
                 Operating System
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      CPU            Memory          Files
        │              │              │
    Scheduling       Paging         Storage
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                    Processes
                       │
                     Threads
                       │
                Synchronization
                       │
                  Applications
```

---

# 🚀 43. Why This Matters for Programmers

Understanding operating systems changes how you think about code.

Instead of seeing:

```python
x = x + 1
```

you start asking:

```text
Where is x stored?

Which thread is accessing it?

Can another thread modify it?

What happens when the process blocks?

What happens during a context switch?

Which CPU core executes this?

How does memory get mapped?

```

This is where programming starts connecting with the actual machine.

---

# 💡 Key Takeaways

### 🖥️ Operating System

Manages hardware and provides services to applications.

### ⚙️ Process

A program currently executing.

### 🧵 Thread

A unit of execution within a process.

### 📋 PCB

Stores important information about a process.

### 🧠 Scheduler

Decides which ready process/thread should execute.

### 🔄 Context Switch

Saves one execution context and loads another.

### 🔐 Mutex

Provides mutual exclusion for shared resources.

### 🚦 Semaphore

Controls access to a limited number of resources.

### 💀 Deadlock

Processes become permanently stuck waiting for one another.

### 💾 Virtual Memory

Provides processes with an abstraction of memory and helps isolate them.

### 🚪 System Call

Allows applications to request services from the OS.

---

# 🌟 Final Thought

Your computer looks like it's doing everything simultaneously:

```text
🎵 Music
🌐 Browser
💻 VS Code
🐍 Python
📁 File Manager
🛡️ Antivirus
```

But underneath, the Operating System is constantly coordinating:

```text
Processes
     ↓
Threads
     ↓
CPU Scheduling
     ↓
Context Switching
     ↓
Memory Management
     ↓
I/O
     ↓
Synchronization
```

And all of this happens millions of times while you casually move your mouse around.

> **An Operating System is essentially the traffic controller of a computer — deciding who gets the CPU, who waits, who gets memory, who can access resources, and how everything keeps running without crashing into everything else.** 🚀
