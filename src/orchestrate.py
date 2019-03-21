#!/usr/bin/env python3
# Author: Andy Gonzalez
import docker
import csv
import os

# filename is expected to be a txt file that follows the 
# namelist conventions. 
def parse_namelist(filename: "*.txt") -> {"label" : "content"}:
	namelist = dict()
	cmdCount = 0
	try:
		with open(filename) as file:
			for line in file:
				if line.strip() and line[0] != "!":
					line = line.strip().split("=")
					label, content = line[0], line[1]
					if "file" in label:
						namelist[label] = content[1:]
					else:
						namelist[label] = content
					if "cmd" in label:
						cmdCount += 1
			namelist["cmdCount"] = cmdCount
			return namelist

	except IOError as e:
		print("Unable to find/open file: " + filename)
		raise SystemExit(22)


# Uses an already initialized DockerClient to execute the commands
# defined by the namelist. All containers are flagged as removable 
# upon completion so they're cleaned up by the DockerClient automatically
def run_containers(DClient, namelist: {"label" : "content"}):
	# Setup for shared local directory that can be passed as a volume 
	# to each container run
	shareDir = "/home/vol"
	settings = {"bind": shareDir, "mode": "rw"}
	vol = {os.getcwd(): settings}

	# Starts and runs each container as defined by the namelist
	for cmdNum in range(1, namelist["cmdCount"] + 1):
		cmd = (namelist["cmd" + str(cmdNum)] + " " +
						shareDir + namelist["file" + str(cmdNum)] +
						" " + shareDir +namelist["file" + str(cmdNum + 1)])

		DClient.containers.run(namelist["img" + str(cmdNum)], cmd, 
								volumes = vol, stdin_open = True, remove = True)


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
	client = docker.from_env()
	
	print("Running with the provided namelist.txt:")
	namelistfile = "namelist.txt"
	namelist = parse_namelist(namelistfile)
	run_containers(client, namelist)
	print_data("angles_Basic_final.csv")
	
	print("Running with namelistMC.txt to demonstrate multiple containers/commands in one run:")
	namelistfile = "namelistMC.txt"
	namelist = parse_namelist(namelistfile)
	run_containers(client, namelist)
	print_data("angles_Basic_final.csv")
