#!/usr/bin/python
# -*- coding: utf -*-

import os, sys, time
pid_file = 'osiris.pid'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def tZ(val):
	val = str(val)
	if len(val) == 1: val = '0'+val
	return val

def printlog(text):
	print text
	lt = tuple(time.localtime())
	fname = 'log/crash_'+tZ(lt[0])+tZ(lt[1])+tZ(lt[2])+'.txt'
	fbody = tZ(lt[3])+tZ(lt[4])+tZ(lt[5])+'|'+text+'\n'
	fl = open(fname, 'a')
	fl.write(fbody.encode('utf-8'))
	fl.close()

def crash(text):
	printlog(text)
	sys.exit()

if os.name == 'nt': printlog('Warning! Correct work only on *NIX system!')

try: writefile('settings/starttime',str(int(time.time())))
except:
	printlog('\n'+'*'*50+'\n Osiris is crashed! Incorrent launch!\n'+'*'*50+'\n')
	raise

if os.path.isfile(pid_file):
	try: last_pid = int(readfile(pid_file))
	except: crash('Unable get information from %s' % pid_file)
	try:
		os.getsid(last_pid)
		crash('Multilaunch detected! Kill pid %s before launch bot again!' % last_pid)
	except Exception, SM:
		if not str(SM).lower().count('no such process'): crash('Unknown exception!\n%s' % SM)
	
writefile(pid_file,str(os.getpid()))

while 1:
	try: execfile('kernel.py')
	except KeyboardInterrupt: break
	except Exception, SM:
		printlog('\n'+'*'*50+'\n Osiris is crashed! It\'s imposible, but You do it!\n'+'*'*50+'\n')
		printlog(str(SM)+'\n')
		raise
