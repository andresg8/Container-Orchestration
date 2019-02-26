#!/usr/bin/env python3
import docker
import csv
import os
import sys


def parse_namelist(filename: "*.txt") -> {"label" : "content"}:
	try:
		with open(filename) as file:
			lines = file.readlines()
			namelist = dict()
			namelist["in_file"] = lines[0].strip('\n')
			namelist["mid_file"] = lines[1].strip('\n')
			namelist["out_file"] = lines[2].strip('\n')
			namelist["cont1"] = lines[3].strip('\n')
			namelist["cont2"] = lines[4].strip('\n')
			namelist["cmd1"] = lines[5].strip('\n')
			namelist["cmd2"] = lines[6].strip('\n')
			return namelist

	except IOError as e:
		print("Unable to find/open file: " + filename)
		raise SystemExit(22)


def run_containers(DClient, namelist: {}):
	shareDir = "/home/vol"

	settings = {"bind": shareDir, "mode": "rw"}
	
	vol = {os.getcwd(): settings}

	cmd1 = namelist["cmd1"] + " " + shareDir + namelist["in_file"] + " " + shareDir +namelist["mid_file"]
	cmd2 = namelist["cmd2"] + " " + shareDir + namelist["mid_file"] + " " + shareDir + namelist["out_file"]

	DClient.containers.run(namelist["cont1"], cmd1, volumes = vol, stdin_open = True, remove = True)
	DClient.containers.run(namelist["cont2"], cmd2, volumes = vol, stdin_open = True, remove = True)


if __name__ == "__main__":
	namelistfile = "namelist.txt"

	namelist = parse_namelist(namelistfile)

	client = docker.from_env()

	run_containers(client, namelist)
