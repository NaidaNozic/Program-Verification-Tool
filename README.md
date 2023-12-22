# Program Verification Tool

<p>The project is a <strong>static analysis tool</strong>, which processes a given program to then prove its correctness.</p>
<p><strong>Tools:</strong> Python 3.11, z3-solver, <a href="https://www.antlr.org/" target="_blank">ANTLR</a> (a lexer and parser generation tool) </p>

<h2>Key Features:</h2>
  <ul>
    <li><strong>Deadlock detection:</strong> Implemented under the "assignment1". The application checks whether the programs contains deadlocks, which occur when two or more threads are blocked forever, each waiting for the other to release a resource. To achieve this a lock tree data structure is implemented.</li>
    <li><strong>Hoare logic:</strong> Implemented under the "assignment2". Application generates and proves verification conditions for a given program, by utilizing the 
<a href="https://en.wikipedia.org/wiki/Hoare_logic" target="_blank">Hoare logic</a>. To achieve this, it uses aspects like precondition, postcondition, loop invariants and decreases clauses. </li>
  </ul>

<h2>Usage</h2>

<p>In order to run the Deadlock detection tool, run:</p>

```
python3 run assignment1.py--file-1 PATH-1--file-2 PATH-2
```

<p>where PATH-1 is replaced with the path to the first program’s file and PATH-2 has to be substituted with the location of the file containing the second program.</p>

<p>In order to run the Hoare logic verification tool run:</p>

```
python3 run assignment2.py--file PATH
```

<p>where PATH corresponds to the path of the program to analyze.</p>
