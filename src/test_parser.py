from container_challenge import *

def test_parse_namelist():
  assert type(parse_namelist("namelist.txt")) == dict
  