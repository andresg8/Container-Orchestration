#!/usr/bin/env python3
# Author: Andy Gonzalez
import docker
import csv
import os

# parse_namelist generates a dictionary representation of the namelist
# text file. Every key is the label or name for the corresponding content.
# Both label and content are directly derived from the conventions used 
# in the namelist. Then, to facilitate orchestrating many containers at 
# once, the number of commands to be executed is recorded into the dict. 
def parse_namelist(filename: "*.txt") -> {"label" : "content"}:
	namelist = dict()
	cmdCount = 0
	try:
		with open(filename) as file:
			for line in file:
				if line.strip() and line[0] != "!":
					line = line.strip().split("=")
					label, content = line[0], line[1]
					namelist[label] = content
					if "cmd" in label:
						cmdCount += 1
			namelist["cmdCount"] = cmdCount
			return namelist

	except IOError as e:
		print("Unable to find/open file: " + filename)
		raise SystemExit(22)


# Using an already initialized DockerClient and the organized namelist
# dict, run_containers handles the orchestration of sharing data across
# a number of containers equal to the number of commands defined by the
# namelist. This script's working directory serves as the intermediate 
# space where the containers share data. This was done to provide access
# to the intial .csv file and so that the resulting files stick around
# in an easy to access manner (on the host machine). 
def run_containers(DClient, namelist: {"label" : "content"}):
	# sharedDir acts as the temporary destination end in the volume where
	# containers can read from / write to and access the local shared dir.
	shareDir = "/home/vol"
	settings = {"bind": shareDir, "mode": "rw"}
	vol = {os.getcwd(): settings}

	containers = []
	for cmdNum in range(1, namelist["cmdCount"] + 1):
		# container commands need to be formed using the namelist definitions 
		# and with the temp destination in mind.
		cmd = (namelist["cmd" + str(cmdNum)] + " " +
						shareDir + namelist["file" + str(cmdNum)] +
						" " + shareDir +namelist["file" + str(cmdNum + 1)])
		# containers are run in the background so that DClient doesn't try 
		# cleaning volume references once a container falls out of scope.
		# This would happen if "remove" was set to True and a list wasn't
		# used to maintain a reference to each container.  
		containers.append(DClient.containers.run(namelist["img" + str(cmdNum)], cmd, 
								volumes = vol, stdin_open = True, detach = True))
	# closing containers
	for container in containers:
		container.wait()
		container.stop()
		container.remove()


# Given a .csv file, print_data prints the raw content of the file
def print_data(data: ".csv"):
	try:
		with  open(data, "r") as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				print(",".join(row))

	except IOError as e:
		print("Unable to find/open file: " + data)
		raise SystemExit(22)			


if __name__ == "__main__":
	# Currently hardcoded, this could easily be turned into an command
	# line input via sys.argv
	namelistfile = "namelist.txt"

	namelist = parse_namelist(namelistfile)

	client = docker.from_env()

	run_containers(client, namelist)

	# Visual confirmation the script was successful on Travis CI. 
	print_data("angles_Basic_final.csv")
