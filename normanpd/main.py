#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import normanpd
from normanpd import normanpd

def main():
			
	#download data
	normanpd.fetchincidents()

	#extract data
	incidents=normanpd.extractincidents()

	#Create Database
	normanpd.createdb()

	#Insert Data
	normanpd.populatedb(incidents)

	#print status
	normanpd.status('normanpd.db')

if __name__=='__main__':
	main()
