---
chapter: 1
title: Programming
subtitle: Algorithms, Pascal and the Evolution of Programming Languages
---

:::learning-objectives
By the end of this chapter, you will be able to:
- Analyse any problem by identifying its Input, Process and Output
- Develop algorithms using Sequence, Selection and Repetition control structures
- Represent algorithms using Flowcharts and Pseudo Codes
- Write Pascal programs using variables, constants, data types and operators
- Use Selection structures: IF–THEN, IF–THEN–ELSE, Nested IF and CASE
- Use Repetition structures: FOR–DO, WHILE–DO and REPEAT–UNTIL
- Identify programming paradigms: Procedural, Declarative, Object-Oriented
- Explain the role of Assembler, Interpreter and Compiler as language translators
:::

## 1.1 Analysing a Problem

:::section-goals
- Define Input, Process and Output for any problem
- Analyse everyday and mathematical problems using IPO decomposition
- Identify alternative solutions and understand the concept of solution space
:::

Before writing any program, a programmer must fully understand the problem. Every problem can be broken down into three components: **Input** (the data provided), **Process** (the operations performed), and **Output** (the result produced). This is called **IPO decomposition**.

:::figure
![The Input → Process → Output model](placeholder:fig-1-1-ipo-model)
Figure 1.1  The Input → Process → Output model
:::

### Alternative Solutions and Solution Space

Many problems have more than one correct solution. The complete set of all valid solutions for a given problem is called the **solution space**. A good programmer evaluates multiple solutions and selects the most efficient one based on speed, memory use, and readability.

## 1.2 Problem Solving Using Algorithms

:::section-goals
- Define an algorithm and explain its purpose
- Develop algorithms for real-world and mathematical problems
- Identify and describe the three control structures: Sequence, Selection and Repetition
:::

An algorithm is the plan you create before writing a program. Just like a recipe is a plan for cooking a meal, an algorithm is a precise, step-by-step set of instructions for solving a problem.

### 1.2.1 Control Structures

All algorithms are built from three fundamental control structures.

#### i. Sequence

In a sequence, every step is executed one after another from start to finish, in strict order. There are no decisions or repetitions — each instruction runs exactly once.

#### ii. Selection

Selection is a control structure where a step is executed only if a condition is satisfied. If the condition is false, that step is skipped or an alternative step is taken.

#### iii. Repetition

Repetition is a control structure where one or more steps are repeated until a condition is met. This avoids writing the same instruction many times.

:::figure
![Three Control Structures — visual summary](placeholder:fig-1-2-control-structures)
Figure 1.2  Three Control Structures — visual summary
:::

## 1.3 Representation of an Algorithm

:::section-goals
- Draw flowcharts using correct symbols for sequence, selection and repetition
- Write pseudo codes using standard keywords
- Convert between flowcharts and pseudo codes
:::

An algorithm can be expressed in different ways. Two of the most widely used tools are **flowcharts** and **pseudo codes**.

### 1.3.1 Flowcharts

A flowchart is a diagram that shows the steps of an algorithm using standardised symbols connected by arrows showing the flow of control.

:::table-note
Table 1.1 — Flowchart symbols and their functions
:::

| Symbol | Shape | Function |
|---|---|---|
| Terminal | Rounded rectangle | Start / End |
| Process | Rectangle | Calculation or assignment |
| Decision | Diamond | Yes/No condition |
| Input/Output | Parallelogram | Read / Write data |
| Arrow | Line with arrowhead | Direction of flow |

:::figure
![All flowchart symbols displayed with names](placeholder:fig-1-3-flowchart-symbols)
Figure 1.3  All flowchart symbols displayed with names
:::

### 1.3.2 Pseudo Codes

A pseudo code is an informal, English-like description of an algorithm. It is not tied to any specific programming language and uses plain keywords to describe each step.

:::table-note
Table 1.2 — Standard pseudo code keywords
:::

#### Pseudo Code Examples

**Example 1 — Area of a circle:**

```
BEGIN
  READ radius
  area ← 3.14159 × radius × radius
  WRITE area
END
```

:::code-note
Pseudo Code 1.1 — Area of a circle
:::

## 1.4 Pascal Programming

:::section-goals
- Write valid Pascal identifiers following all naming rules
- Declare variables and constants with correct data types
- Use arithmetic, comparison and logical operators
- Read and write the basic structure of a Pascal program
:::

Pascal is a high-level structured programming language designed to be easy to read and to enforce good programming habits. It uses clearly structured `BEGIN...END` blocks and requires all variables to be declared before use.

### 1.4.1 Identifiers

An identifier is a name used to represent a variable, constant or program in Pascal. Every identifier must follow strict naming rules.

:::table-note
Table 1.3 — Rules for Pascal identifiers
:::

| Rule | Valid example | Invalid example |
|---|---|---|
| Must begin with a letter | `TotalMarks` | `5thPlace` |
| Letters, digits, underscore only | `Average_Score` | `My-Name` |
| Cannot be a reserved word | `StudentAge` | `end` |
| No spaces allowed | `ICT2025` | `ICT 2025` |

### 1.4.2 Variables and Constants

#### Variables

A variable is an identifier whose value can change during program execution. Variables must be declared in the `VAR` section before the `BEGIN` block.

```pascal
VAR
  studentName : String;
  age         : Integer;
  mark        : Real;
```

:::code-note
Code 1.1 — Declaring variables in Pascal
:::

#### Constants

A constant is an identifier whose value is fixed and cannot be changed during program execution.

```pascal
CONST
  PI    = 3.14159;
  GRADE = 'A';
```

:::code-note
Code 1.2 — Declaring constants in Pascal
:::

### 1.4.3 Selection in Pascal

#### IF … THEN … ENDIF

The statement(s) inside the IF block execute only if the condition is true. If the condition is false, the program skips the block and continues after ENDIF.

```pascal
IF mark >= 50 THEN
  writeln('Pass')
ENDIF;
```

:::code-note
Code 1.3 — IF…THEN example
:::

#### IF … THEN … ELSE … ENDIF

When the condition is true, Statement 1 executes. When false, Statement 2 executes.

```pascal
IF mark >= 50 THEN
  writeln('Pass')
ELSE
  writeln('Fail')
ENDIF;
```

:::code-note
Code 1.4 — IF…THEN…ELSE example
:::

### 1.4.4 Repetition in Pascal

Pascal provides three repetition structures. The choice depends on whether you know how many times to repeat and whether the condition is checked before or after the loop body.

#### FOR … TO … DO

Used when the number of repetitions is known in advance.

```pascal
FOR counter := 1 TO 10 DO
BEGIN
  writeln(counter);
END;
```

:::code-note
Code 1.5 — FOR…TO…DO loop
:::

#### WHILE … DO

The WHILE loop checks its condition **before** running the loop body each time. If the condition is false at the start, the body never runs.

```pascal
WHILE count <= 10 DO
BEGIN
  writeln(count);
  count := count + 1;
END;
```

:::code-note
Code 1.6 — WHILE…DO loop
:::

#### REPEAT … UNTIL

The REPEAT…UNTIL loop checks its condition **after** running the loop body. The body always runs at least once.

```pascal
REPEAT
  readln(number);
UNTIL number > 0;
```

:::code-note
Code 1.7 — REPEAT…UNTIL loop
:::

:::table-note
Table 1.4 — Comparison of Pascal loop structures
:::

| Loop | Condition checked | Minimum runs | Use when… |
|---|---|---|---|
| FOR…TO…DO | Before | 0 | Number of repetitions is known |
| WHILE…DO | Before | 0 | Number of repetitions is unknown, may not run |
| REPEAT…UNTIL | After | 1 | Body must run at least once |

## 1.5 Evolution of Programming Languages

:::section-goals
- Describe Machine Language and Assembly Language (low-level languages)
- Describe high-level languages and list examples
- Identify and compare programming paradigms
- Explain the role of Assembler, Interpreter and Compiler
:::

A computer can only directly understand Machine Language — instructions in binary. All other languages must be translated before the computer can execute them.

### 1.5.1 Low-Level Programming Languages

#### Machine Language

Machine Language is the only language a computer understands directly. All instructions are written in binary (0s and 1s). It is machine-dependent — a program written for one processor will not work on a different processor without modification.

#### Assembly Language

Assembly Language uses short mnemonic codes (such as `MOV`, `ADD`, `JMP`) instead of binary. An **Assembler** translates Assembly Language programs into Machine Language.

:::figure
![Assembly Language → Assembler → Machine Language](placeholder:fig-1-4-assembly-to-machine)
Figure 1.4  Assembly Language → Assembler → Machine Language
:::

### 1.5.2 Language Translators

#### Assembler

Translates Assembly Language programs into Machine Language. Used only for assembly language programs.

#### Interpreter

Translates and executes a high-level language program **one line at a time**. If an error is found, execution stops immediately at that line. Used in Python and JavaScript.

#### Compiler

Translates the **entire** source program into an executable file before any execution begins. If errors exist, the program does not run at all. Used in Pascal, C and Java.

:::table-note
Table 1.5 — Interpreter vs Compiler comparison
:::

| Feature | Interpreter | Compiler |
|---|---|---|
| Translation | Line by line | Whole program at once |
| Error detection | Stops at first error | Reports all errors together |
| Speed of execution | Slower (translates each run) | Faster (translated once) |
| Output | No standalone file | Produces executable file |
| Examples | Python, JavaScript | Pascal, C, Java |

{pagebreak}

:::chapter-summary
**Chapter 1 — Programming**

- Every problem has **Input**, **Process** and **Output**. IPO decomposition clarifies what a program must do before any code is written.
- An **algorithm** is a precise, step-by-step plan for solving a problem.
- The three control structures are **Sequence** (steps in order), **Selection** (conditional steps), and **Repetition** (repeated steps).
- Algorithms can be expressed as **flowcharts** (using standard symbols) or **pseudo codes** (using English-like keywords).
- **Pascal** is a structured high-level language. All variables must be declared before use in the VAR section.
- Identifiers must begin with a letter, contain only letters/digits/underscores, and must not be reserved words.
- **Compilers** translate the entire program before execution; **Interpreters** translate and execute line by line.
- Programming paradigms include **Procedural**, **Declarative** and **Object-Oriented** approaches.
:::

:::key-terms
- **Algorithm** — a finite, ordered set of instructions for solving a problem
- **IPO** — Input, Process, Output: the three components of any computational problem
- **Flowchart** — a diagrammatic representation of an algorithm using standard symbols
- **Pseudo code** — an informal, English-like description of an algorithm
- **Identifier** — a name for a variable, constant or program in Pascal
- **Variable** — a named memory location whose value can change during execution
- **Constant** — a named memory location whose value is fixed
- **Compiler** — translates the whole source program to machine code before execution
- **Interpreter** — translates and executes source code one line at a time
- **Assembler** — translates Assembly Language to Machine Language
:::

:::review-questions
Answer all questions. For programming questions, write complete, syntactically correct Pascal code.
:::

:::section-a
:::

1. **Identify the Input, Process and Output for each of the following:**

   (a) Finding the average of three numbers.

   (b) Converting Celsius to Fahrenheit using: F = (9/5 × C) + 32.

   (c) Sorting 10 numbers from smallest to largest.

2. **For each scenario, state whether it illustrates Sequence, Selection, or Repetition:**

   (a) A student reads each page of a 300-page textbook from page 1 to page 300.

   (b) A cash machine dispenses money only if the account balance is sufficient.

   (c) A computer prints the numbers from 1 to 100.

3. **State TWO differences between a Compiler and an Interpreter.**

:::section-b
:::

4. **(a)** Draw a flowchart to find the perimeter (P = 2(L+W)) and area (A = L×W) of a rectangle.

   **(b)** Write the equivalent pseudo code for the same algorithm.

5. **Write a complete Pascal program that reads a student mark (0–100) and displays the grade:**

   - A (75–100),  B (65–74),  C (50–64),  S (35–49),  W (0–34)
   - For marks outside 0–100, display 'Invalid Mark'.
