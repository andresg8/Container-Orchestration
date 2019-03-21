
#!/usr/bin/env python3
# Author: Andy Gonzalez
from orchestrate import *

def test_parse_namelist():
  assert type(parse_namelist("namelist.txt")) == dict
  
