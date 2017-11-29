# Market Basket Analysis

A Python3 implementation of market basket analysis on transaction data.
Reference: http://paulallen.ca/apriori-algorithm-generating-candidate-fis/

###### Input:
A text file with one transaction per line. Each transaction is a space seperated string of SKUs

###### Arguments:
- Input file
- Minimum number of SKUs per item set, n. Default = 3
- Minimum support value, sigma. Default = 4
- Output file. Default = output.txt
- An optional 'verbose' argument to display debug info to the command line

###### Output:
An output file with the info of one frequent item-set per line.
Each line is of the following format,
> <item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>

###### How to run
For detailed help, 
```
> python apriori.py -h
```

To run by passing a transaction log as input
```buildoutcfg
> python apriori.py input_file -v
```
`-v` displays debug text onto the screen