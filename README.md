# pc-build-part-picker

## Introduction

Given a list of PC parts with a price and an "experience score" in a csv file and a budget (in euros) attempt to pick
a build using 1 part from each category that is within budget and has the highes total experience score.

Here is an example list of parts

```
       category                 name  cost  experience_score
0          case          base case 1    30                 3
1          case           mid case 2    50                 6
2          case      high-end case 3    75                 8
3          case       very-base case     5                 2
4   motherboard            base mb 1    50                 5
5   motherboard             mid mb 2    75                 8
6   motherboard        high-end mb 3   120                12
7           cpu           base cpu 1   150                12
8           cpu            mid cpu 2   200                20
9           cpu       high-end cpu 3   300                30
10     graphics      base graphics 1    80                 8
11     graphics       mid graphics 2   120                12
12     graphics  high-end graphics 3   200                16
13      storage       base storage 1    40                 5
14      storage        mid storage 2    80                 7
15      storage   high-end storage 3   120                 9
16       memory        base memory 1   100                 8
17       memory         mid memory 2   150                12
18       memory    high-end memory 3   200                14

```

Here is the output for a budget of €900.00

```
########## Selected Parts ##########
      category                 name  cost  experience_score  selected  exp/cost
2  motherboard        high-end mb 3   120                12      True     0.100
3       memory    high-end memory 3   200                14      True     0.070
4     graphics  high-end graphics 3   200                16      True     0.080
5          cpu       high-end cpu 3   300                30      True     0.100
6         case       very-base case     5                 2      True     0.400
8      storage       base storage 1    40                 5      True     0.125
########################################
Total Budget: €900.00
Total Cost: €865.00
Remaining Budget: €35.00
Total Experience Score: 79
########################################

```
## Current Implementation
- Find the best setup for an unlimited budget (highest experience score per part)
- Sort by ascending experience score for selected parts
- If over budget
    - swap out the lowest experience score part for another (cheaper) part for that category
    - check if under budget
    - repeat swapping out parts (keeping the swapped out parts each time)
    - Note: Assumes that there is a strong correlation between price and experience score 

The above is a very crude attempt to find the best possible setup. A better solution would use a more formal algorithm.
One similar problem that has algorithmic solutions is the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)

## Setup

```bash
pipenv sync
pipenv shell
```

## Run

### Find parts using default sort (experience score/cost)
```bash
cd pcbuildpartpicker
./pcbuildpartpicker.py -f test-parts.csv -b 900
```

### Find parts usin sort by experience score
```bash
cd pcbuildpartpicker
./pcbuildpartpicker.py -f test-parts.csv -b 900 -s 'experience_score' 
```

### Tests

There are a small number of basic unit tests under development. They can be run by
```bash
cd pcbuildparpicker
pytest test_pcbuildpartpicker.py
``` 
