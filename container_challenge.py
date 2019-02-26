#!/usr/bin/env python3
import docker
import csv
import os


# parse_namelist generates a dictionary representation of the namelist
# text file. Every key is a str that labels the value which is the str 
# content of the .txt line by line. I don't like how hardcoded it 
# looks/is but I think this was inevitable given the defined nature of
# the problem. 
def parse_namelist(filename: "*.txt") -> {"label" : "content"}:
	try:
		with open(filename) as file:
			lines = file.readlines()
			namelist = dict()
			namelist["in_file"] = lines[0].strip('\n')
			namelist["med_file"] = lines[1].strip('\n')
			namelist["out_file"] = lines[2].strip('\n')
			namelist["cont1"] = lines[3].strip('\n')
			namelist["cont2"] = lines[4].strip('\n')
			namelist["cmd1"] = lines[5].strip('\n')
			namelist["cmd2"] = lines[6].strip('\n')
			return namelist

	except IOError as e:
		print("Unable to find/open file: " + filename)
		raise SystemExit(22)


# Using the already initialized DockerClient and the organized namelist
# dict, run_containers handles the orchestration of sharing data across
# two containers so that commands dependent on the data can be run on 
# either container sequentially. This script's working directory serves as 
# the intermediate space where the containers share data. This was done to
# provide access to the intial .csv file and so that the resulting files
# stick around in an easily accessible manner (on the host machine). 
def run_containers(DClient, namelist: {}):
	# sharedDir acts as the temporary destination end to the volume where
	# containers can read from / write to and access the local shared dir.
	shareDir = "/home/vol"
	settings = {"bind": shareDir, "mode": "rw"}
	vol = {os.getcwd(): settings}

	# container commands need to be formed using the namelist definitions 
	# and with the temp destination in mind.
	cmd1 = namelist["cmd1"] + " " + shareDir + namelist["in_file"] + " " + shareDir +namelist["mid_file"]
	cmd2 = namelist["cmd2"] + " " + shareDir + namelist["med_file"] + " " + shareDir + namelist["out_file"]

	# cont1 runs cmd1 on the input file to produce an intermediate file
	# cont2 runs cmd2 on the intermediate file to produce the output file
	DClient.containers.run(namelist["cont1"], cmd1, volumes = vol, stdin_open = True, remove = True)
	DClient.containers.run(namelist["cont2"], cmd2, volumes = vol, stdin_open = True, remove = True)


if __name__ == "__main__":
	# Currently hardcoded, this could easily be turned into an command
	# line input via sys.argv
	namelistfile = "namelist.txt"

	
	namelist = parse_namelist(namelistfile)

	client = docker.from_env()

	run_containers(client, namelist)
