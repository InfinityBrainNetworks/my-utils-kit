---
chapter: 1
title: Programming
subtitle: Algorithms, Pascal and the Evolution of Programming Languages
grade: Grade 11
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

:::key-term Input, Process and Output
**Input:** The raw materials or data used to solve the problem.

**Process:** The sequence of steps that transforms the input into the output.

**Output:** The result produced after the process is complete.
:::

:::figure
![The Input → Process → Output model](placeholder:fig-1-1-ipo-model)
Figure 1.1  The Input → Process → Output model
:::

:::worked-example Problem 1: Posting a Letter
**Input:** Paper, pen, envelope, stamp, glue

**Process:**
1. Write the letter
2. Fold and insert into envelope
3. Paste the envelope
4. Write recipient's address
5. Stick the stamp
6. Post the letter

**Output:** Letter delivered to the recipient
:::

:::activity Practice — IPO Analysis
Identify the Input, Process and Output for each of the following:

11. Dividing 100 toffees equally among 20 people.
12. Making a kite.
13. Finding the area of a circle given its radius.
:::

### Alternative Solutions and Solution Space

Many problems have more than one correct solution. The complete set of all valid solutions for a given problem is called the **solution space**.

:::key-term Solution Space
The complete set of all valid alternative solutions to a problem. Examining the full solution space helps you choose the most efficient solution.
:::

## 1.2 Problem Solving Using Algorithms

:::section-goals
- Define an algorithm and explain its purpose
- Develop algorithms for real-world and mathematical problems
- Identify and describe the three control structures: Sequence, Selection and Repetition
:::

An algorithm is the plan you create before writing a program. Just like a recipe is a plan for cooking a meal, an algorithm is a plan for solving a computational problem.

:::key-term Algorithm
**Algorithm:** A step-by-step procedure for solving a problem. An algorithm must be clear, unambiguous, and produce the correct result in a finite number of steps.
:::

:::worked-example Algorithm 1: Posting a Letter
1. Write the letter
2. Fold the letter
3. Insert the letter into the envelope
4. Write the address on the envelope
5. Stick the stamp
6. Post the letter

*Steps 1–3 must be in strict order. Steps 4 and 5 can be interchanged.*
:::

:::remember
Key fact: Pseudo code is not a programming language and cannot be run on a computer. It is a planning tool only.
:::

:::did-you-know
Pascal was created by Niklaus Wirth in 1970 and named after the French mathematician Blaise Pascal. It was designed specifically as a teaching language.
:::

### 1.2.1 Control Structures

All algorithms are built from three fundamental control structures.

#### i. Sequence

In a sequence, every step is executed one after another from start to finish, in strict order.

#### ii. Selection

Selection is a control structure where a step is executed only if a condition is satisfied.

#### iii. Repetition

Repetition is a control structure where one or more steps are repeated until a condition is met.

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

| Symbol Shape | Name | Function |
|---|---|---|
| Oval / Rounded Rectangle | Start / End | Marks the beginning or end of the algorithm |
| Parallelogram | Input / Output | Reading input from user or displaying output |
| Rectangle | Process | A calculation, assignment or operation |
| Diamond | Decision | A condition with Yes and No branches |
| Arrow | Flow Direction | Shows the direction of execution |
| Small Circle | Connector | Connects parts of the flowchart (e.g. across pages) |

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

:::exam-tip
O/L Exam Tip: Always use ENDWHILE to close a WHILE loop and UNTIL to close a REPEAT loop. Missing terminators are a common source of marks lost in exams.
:::

## 1.4 Pascal Programming

:::section-goals
- Write valid Pascal identifiers following all naming rules
- Declare variables and constants with correct data types
- Use arithmetic, comparison and logical operators
- Read and write the basic structure of a Pascal program
:::

Pascal is a high-level structured programming language designed to be easy to read and to enforce good programming habits.

### 1.4.1 Identifiers

An identifier is a name used to represent a variable, constant or program in Pascal.

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

A variable is an identifier whose value can change during program execution.

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

```pascal
IF mark >= 50 THEN
  writeln('Pass')
ENDIF;
```

:::code-note
Code 1.3 — IF…THEN example
:::

#### IF … THEN … ELSE … ENDIF

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

:::remember Understanding Variables vs Constants
Use a **variable** when the value changes during execution. Use a **constant** when the value is always the same. A common mistake is declaring `PI` as a variable — it should always be a constant.
:::

#### FOR … TO … DO

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

A computer can only directly understand Machine Language — instructions in binary.

### 1.5.1 Low-Level Programming Languages

#### Machine Language

Machine Language is the only language a computer understands directly. All instructions are written in binary (0s and 1s).

:::key-term Machine Language
The lowest-level programming language. Programs consist entirely of binary digits (0s and 1s). Machine language is machine-dependent — programs written for one processor will not run on a different processor without modification.
:::

#### Assembly Language

Assembly Language uses short mnemonic codes (such as `MOV`, `ADD`, `JMP`) instead of binary. An **Assembler** translates Assembly Language programs into Machine Language.

### 1.5.2 Language Translators

#### Assembler

Translates Assembly Language programs into Machine Language.

#### Interpreter

Translates and executes a high-level language program **one line at a time**. If an error is found, execution stops immediately at that line.

#### Compiler

Translates the **entire** source program into an executable file before any execution begins.

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

:::exam-tip
Final Revision Checklist: Know the difference between compiler and interpreter. Know all three loop types (FOR, WHILE, REPEAT). Know the three control structures. Know IPO for any problem.
:::

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

2. **For each scenario, state whether it illustrates Sequence, Selection, or Repetition:**

   (a) A student reads each page of a 300-page textbook from page 1 to page 300.

   (b) A cash machine dispenses money only if the account balance is sufficient.

3. **State TWO differences between a Compiler and an Interpreter.**

:::section-b
:::

4. **(a)** Draw a flowchart to find the perimeter (P = 2(L+W)) and area (A = L×W) of a rectangle.

   **(b)** Write the equivalent pseudo code for the same algorithm.

5. **Write a complete Pascal program that reads a student mark (0–100) and displays the grade:**

   - A (75–100),  B (65–74),  C (50–64),  S (35–49),  W (0–34)
   - For marks outside 0–100, display 'Invalid Mark'.
