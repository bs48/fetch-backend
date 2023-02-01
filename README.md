## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Assumptions on data](#assumptions-on-data)
- [Setup instructions](#setup-instructions)
  - [Python installation](#python)
- [Execution instructions](#execution-instructions)
- [Testing :](#testing-)
- [Usage :](#usage-)
    - [***1. Success case***](#1-success-case)
    - [***2. Case when points to be spent exceeds points supplied by payers***](#2-case-when-points-to-be-spent-exceeds-points-supplied-by-payers)
    - [***3. Corner case***](#3-corner-case)

## Introduction

This is a takehome assignment for Fetch backend Engineering Intern Role [Transaction Processing](https://docs.google.com/document/d/1Yn_xAonwLOINma3MquU5ag6KoNMkrH3uA-99pJvqaWs/edit)

## Assumptions on data 

1. The data is considered to be of the format 'payer', 'points', 'timestamp' and no validity checks have been done so any other format will throw an error.

2. Thenegative values in the transactions are considered as debit from the user side.
    1. This means that in the below transaction lists
    "DANNON",200,"2020-11-02T14:00:00Z"
    "UNILEVER",100,"2020-10-31T11:00:00Z"
    "DANNON",-200,"2020-10-31T15:00:00Z",
    "DANNON" cannot give any money to the user when we iterate over the first occurence of "DANNON" 

3. To take this into account all the transactions are first grouped in terms of the payer and then the negative values are subtracted from the positive values inorder to find the effective amount the payer cna pay the user
4. Only valid inputs are assumed for each payer. ie No negative points can appear first ( as per timestamp ) as it is not possible to return points to the payer without them contributing first.
   
5. **Given the limited amount of time all test cases haven't been exhaustively tested but there are tests for every situations mentioned above**


## Setup instructions

The code has been developed and tested using python 3.9.12 and pip 21.2.4 **but it is likely to work on all latest python versions**. 

### Python installation


Please follow the link given to install python 3.9.12 https://www.python.org/downloads/release/python-3912/


to verify the installation of python and pip

```
~ python3 --version
Python 3.9.12
~ pip3 --version
pip 21.2.4
```

Once they are installed, from the root directory of the folder run, 

```
~ pip3 install -r requirements.txt
```

This installs dependency **pytest** which is used for unit testing

## Execution instructions

Please ensure the presence of transactions.csv is present in the current working directory

if its not present then the following will be displayed

```
~ python3 main.py 5000
File not found!
```

## Testing :

Four unit testcases have been written to ensure the proper functioning of the script. To run all testcases just do the following
```
~ pytest
```

## Usage :
the usage of the program can be found using the -h command like this

```
~ python3 main.py -h
usage: Process Transactions [-h] [--check-for-insufficiency CHECK_FOR_INSUFFICIENCY] points

Deducts the points the user wants to use and gives the remaining points as per the payer

positional arguments:
  points                number of points the user wants to spend

options:
  -h, --help            show this help message and exit
  --check-for-insufficiency CHECK_FOR_INSUFFICIENCY
                        Check for insufficient balance

```

the last argument is optional to check weather the user has enough amount of points to spend.

#### ***1. Success case***

```
~ cat transactions.csv
"payer","points","timestamp"
"DANNON",1000,"2020-11-02T14:00:00Z"
"UNILEVER",200,"2020-10-31T11:00:00Z"
"DANNON",-200,"2020-10-31T15:00:00Z"
"MILLER COORS",10000,"2020-11-01T14:00:00Z"
"DANNON",300,"2020-10-31T10:00:00Z"% 

~ python3 main.py 5000
{
  "DANNON": 1000,
  "UNILEVER": 0,
  "MILLER COORS": 5300
}
```


#### ***2. When the amount of points the payers can pay exceeds the amount the user wants to spend***
```
~ python3 main.py 100000 --check-for-insufficiency True 
Insufficient Balance!
```
```
~ python3 main.py 100000  
{
    "DANNON": 0,
    "UNILEVER": 0,
    "MILLER COORS": 0
}
```

#### ***3. Handling the negative values present in the transactions***

There is a -200 that the user spent on DANNON in this situation, so that DANNON cannot pay the entire amount first. As a result, DANNON pays 100 points and UNILEVER pays the remaining 200.

```
~ python3 main.py 300
{
    "DANNON": 1000,
    "UNILEVER": 0,
    "MILLER COORS": 10000
}
```


