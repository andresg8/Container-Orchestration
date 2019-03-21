# Container-Orchestration

[![Build Status](https://travis-ci.org/andresg8/Container-Orchestration.svg?branch=master)](https://travis-ci.org/andresg8/Container-Orchestration)

The script orchestrate.py assumes all relevant information on how to execute commands will be 
in a namelist text file. This namelist must be in the format of “label#=content” where label 
is one of “file”, “img”, or “cmd” and # increases linearly with repeat labels. Another assumption 
crucial to orchestration is that there will only be one cmd per img and there will be one more 
file than there are cmds. Given that these preconditions are met, orchestrate runs "imgX's"
command "cmdX" with "fileX" and "file(X+1)" as arguments for as many commands as there are in the 
namelist. 
