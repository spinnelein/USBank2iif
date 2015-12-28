# Script to convert CSV to IIF output.

import os
import sys, traceback, re

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

account = "USBank Checking"
default = "Uncleared Transactions"

def error(trans):
	sys.stderr.write("%s\n" % trans)
	traceback.print_exc(None, sys.stderr)


def main(input_file_name):
	input_file = open(os.path.join(PROJECT_ROOT, input_file_name), 'r')
	output_file = open(os.path.join(PROJECT_ROOT, input_file_name + '.iif'), 'w')
	head='''!ACCNT,NAME,ACCNTTYPE,DESC
ACCNT,"%s",EXP,"%s"

!TRNS,TRNSID,TRNSTYPE,DATE,ACCNT,NAME,AMOUNT,DOCNUM,CLEAR
!SPL,SPLID,TRNSTYPE,DATE,ACCNT,NAME,AMOUNT,DOCNUM,CLEAR
!ENDTRNS
'''
	template = '''
TRNS,,%s,%s,"%s","%s","%s",,N
SPL,,%s,%s,"Unsorted Transactions",,"%s",,N
ENDTRNS''' #transtype,date,account,name,amount,trsanstype,date,negativeamount

	output_file.write(head % (default, default))
	for trans in input_file:
		trans = trans.strip()
		if trans == "":
			continue
			
		try:
			list = trans.split(',')
			print len(list)
			print list
			assert (len(list) == 5 )
		except:
			error(trans)
			continue

		try:
			(date, transtype, name, memo, amount) = list
		#			 date = date.replace('/', '-')
		except:
			error(trans)
			continue	
		amount = amount.strip('"')
		try:
			amount = float(amount)
		except:
			error(trans)
			continue

		name = name.strip('"')
		name = name.strip("\n")
		name = name.strip("\r")
		if "DEBIT" in transtype:
			transtype = 'CHECK'
		elif "CREDIT" in transtype:
			transtype = 'DEPOSIT'
		else:
			name = 'Check ' + transtype
			transtype = 'CHECK'
		transact = template % (transtype,date,account,name,amount,transtype,date,-amount)
		print transact
		output_file.write(transact)

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print "usage:	python convert.py input.csv"

	main(sys.argv[1])