from container_challenge.py import *

def test_parse_namelist():
  assert type(parse_namelist("namelist.txt")) == dict
  
