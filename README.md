# Implementatin of scheduling algorithms in Python

## Why this project exists

As my final task at the ending of cource "Operating systems" I got task to implement FCFS and SJF scheduling algorithms. While I was completing my task I noticed that
this is such an interesting topic and I decided to expand my project, add some more functionality to it and place on GitHub.

## What you will find in this repository

You can find implementation of two scheduling algorithms and report that explains how them work. Report is writen in Polish, implementation of both algorithms is in English,
all code and comments are in English.

### What is the main idea of FCFS scheduling algorithm

The idea of FCFS (First Come First Serve) scheduling algorithm is pretty simple. We just take first coming process and execute it, then we take the second one and so on.

### What is the main idea of SJF scheduling algorithm

The idea of preemptive version of SJF (Shortest Job First) scheduling algorithm is to always execute the shortest process from all processes that are ready for execution, preemptive
means that we can stop execution of process and put it back to queue in case if more shorter process arrived.

## Is there some features in this program?

Yes, I implemented function that allows you to write down data of all processes that you tested to CSV file, and function that reads this data ftom CSV file.
