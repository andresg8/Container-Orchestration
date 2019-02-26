# Container-Orchestration

[![Build Status](https://travis-ci.org/andresg8/Container-Orchestration.svg?branch=master)](https://travis-ci.org/andresg8/Container-Orchestration)

The script orchestrate.py assumes that a "namelist.txt" file exists in the same directory as well
as the file names defined in the text file. Given that these preconditions are met, orchestrate
has container1 run cmd1 on file1 to produce file2 and then has container2 run cmd2 on file2 to 
produce file3 where all the variables are defined in "namelist.txt".
