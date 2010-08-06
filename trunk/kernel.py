#!/usr/bin/python
# -*- coding: utf -*-
# --------------------------------------------------------------------
#
#                             Osiris Jabber Bot
#                               version 0.02
#
# --------------------------------------------------------------------
#                  (c) 2oo9-2o1o Disabler Production Lab.
# --------------------------------------------------------------------

from __future__ import with_statement
from xmpp import *
from random import *
from time import *

import chardet
import hashlib
import htmlentitydefs
import logging
import os
import re
import simplejson
import sys
import thread
import threading
import time
import urllib
import urllib2
import xmpp

sema = threading.BoundedSemaphore(value=30)

lmass = (('\n','<br>'),('\n','<br />'),('\n','<br/>'),('\n','\n\r'),('','<![CDATA['),('',']]>'),(u'','&nbsp;'),
		(u'','&shy;'),(u'','&ensp;'),(u'','&emsp;'),(u'','&thinsp;'),(u'','&zwnj;'),(u'','&zwj;'))
		
rmass = ((u'\"','&quot;'),(u'\'','&apos;'),(u'˜\'','&tilde;'),
		(u'&','&amp;'),(u'<','&lt;'),(u'>','&gt;'),(u'¡','&iexcl;'),(u'¢','&cent;'),(u'£','&pound;'),
		(u'¤','&curren;'),(u'¥','&yen;'),(u'¦','&brvbar;'),(u'§','&sect;'),(u'¨','&uml;'),(u'©','&copy;'),(u'ª','&ordf;'),
		(u'«','&laquo;'),(u'¬','&not;'),(u'®','&reg;'),(u'¯','&macr;'),(u'°','&deg;'),(u'±','&plusmn;'),
		(u'²','&sup2;'),(u'³','&sup3;'),(u'´','&acute;'),(u'µ','&micro;'),(u'¶','&para;'),(u'·','&middot;'),(u'¸','&cedil;'),
		(u'¹','&sup1;'),(u'º','&ordm;'),(u'»','&raquo;'),(u'¼','&frac14;'),(u'½','&frac12;'),(u'¾','&frac34;'),(u'¿','&iquest;'),
		(u'×','&times;'),(u'÷','&divide;'),(u'À','&Agrave;'),(u'Á','&Aacute;'),(u'Â','&Acirc;'),(u'Ã','&Atilde;'),(u'Ä','&Auml;'),
		(u'Å','&Aring;'),(u'Æ','&AElig;'),(u'Ç','&Ccedil;'),(u'È','&Egrave;'),(u'É','&Eacute;'),(u'Ê','&Ecirc;'),(u'Ë','&Euml;'),
		(u'Ì','&Igrave;'),(u'Í','&Iacute;'),(u'Î','&Icirc;'),(u'Ï','&Iuml;'),(u'Ð','&ETH;'),(u'Ñ','&Ntilde;'),(u'Ò','&Ograve;'),
		(u'Ó','&Oacute;'),(u'Ô','&Ocirc;'),(u'Õ','&Otilde;'),(u'Ö','&Ouml;'),(u'Ø','&Oslash;'),(u'Ù','&Ugrave;'),(u'Ú','&Uacute;'),
		(u'Û','&Ucirc;'),(u'Ü','&Uuml;'),(u'Ý','&Yacute;'),(u'Þ','&THORN;'),(u'ß','&szlig;'),(u'à','&agrave;'),(u'á','&aacute;'),
		(u'â','&acirc;'),(u'ã','&atilde;'),(u'ä','&auml;'),(u'å','&aring;'),(u'æ','&aelig;'),(u'ç','&ccedil;'),(u'è','&egrave;'),
		(u'é','&eacute;'),(u'ê','&ecirc;'),(u'ë','&euml;'),(u'ì','&igrave;'),(u'í','&iacute;'),(u'î','&icirc;'),(u'ï','&iuml;'),
		(u'ð','&eth;'),(u'ñ','&ntilde;'),(u'ò','&ograve;'),(u'ó','&oacute;'),(u'ô','&ocirc;'),(u'õ','&otilde;'),(u'ö','&ouml;'),
		(u'ø','&oslash;'),(u'ù','&ugrave;'),(u'ú','&uacute;'),(u'û','&ucirc;'),(u'ü','&uuml;'),(u'ý','&yacute;'),(u'þ','&thorn;'),
		(u'ÿ','&yuml;'),(u'∀','&forall;'),(u'∂','&part;'),(u'∃','&exists;'),(u'∅','&empty;'),(u'∇','&nabla;'),(u'∈','&isin;'),
		(u'∉','&notin;'),(u'∋','&ni;'),(u'∏','&prod;'),(u'∑','&sum;'),(u'−','&minus;'),(u'∗','&lowast;'),(u'√','&radic;'),
		(u'∝','&prop;'),(u'∞','&infin;'),(u'∠','&ang;'),(u'∧','&and;'),(u'∨','&or;'),(u'∩','&cap;'),(u'∪','&cup;'),
		(u'∫','&int;'),(u'∴','&there4;'),(u'∼','&sim;'),(u'≅','&cong;'),(u'≈','&asymp;'),(u'≠','&ne;'),(u'≡','&equiv;'),
		(u'≤','&le;'),(u'≥','&ge;'),(u'⊂','&sub;'),(u'⊃','&sup;'),(u'⊄','&nsub;'),(u'⊆','&sube;'),(u'⊇','&supe;'),
		(u'⊕','&oplus;'),(u'⊗','&otimes;'),(u'⊥','&perp;'),(u'⋅','&sdot;'),(u'Α','&Alpha;'),(u'Β','&Beta;'),(u'Γ','&Gamma;'),
		(u'Δ','&Delta;'),(u'Ε','&Epsilon;'),(u'Ζ','&Zeta;'),(u'Η','&Eta;'),(u'Θ','&Theta;'),(u'Ι','&Iota;'),(u'Κ','&Kappa;'),
		(u'Λ','&Lambda;'),(u'Μ','&Mu;'),(u'Ν','&Nu;'),(u'Ξ','&Xi;'),(u'Ο','&Omicron;'),(u'Π','&Pi;'),(u'Ρ','&Rho;'),
		(u'Σ','&Sigma;'),(u'Τ','&Tau;'),(u'Υ','&Upsilon;'),(u'Φ','&Phi;'),(u'Χ','&Chi;'),(u'Ψ','&Psi;'),(u'Ω','&Omega;'),
		(u'α','&alpha;'),(u'β','&beta;'),(u'γ','&gamma;'),(u'δ','&delta;'),(u'ε','&epsilon;'),(u'ζ','&zeta;'),(u'η','&eta;'),
		(u'θ','&theta;'),(u'ι','&iota;'),(u'κ','&kappa;'),(u'λ','&lambda;'),(u'μ','&mu;'),(u'ν','&nu;'),(u'ξ','&xi;'),
		(u'ο','&omicron;'),(u'π','&pi;'),(u'ρ','&rho;'),(u'ς','&sigmaf;'),(u'σ','&sigma;'),(u'τ','&tau;'),(u'υ','&upsilon;'),
		(u'φ','&phi;'),(u'χ','&chi;'),(u'ψ','&psi;'),(u'ω','&omega;'),(u'ϑ','&thetasym;'),(u'ϒ','&upsih;'),(u'ϖ','&piv;'),
		(u'Œ','&OElig;'),(u'œ','&oelig;'),(u'Š','&Scaron;'),(u'š','&scaron;'),(u'Ÿ','&Yuml;'),(u'ƒ','&fnof;'),(u'ˆ','&circ;'),
		(u'‎','&lrm;'),(u'‏','&rlm;'),(u'–','&ndash;'),(u'—','&mdash;'),(u'‘','&lsquo;'),(u'’','&rsquo;'),(u'‚','&sbquo;'),
		(u'“','&ldquo;'),(u'”','&rdquo;'),(u'„','&bdquo;'),(u'†','&dagger;'),(u'‡','&Dagger;'),(u'•','&bull;'),(u'…','&hellip;'),
		(u'‰','&permil;'),(u'′','&prime;'),(u'″','&Prime;'),(u'‹','&lsaquo;'),(u'›','&rsaquo;'),(u'‾','&oline;'),(u'€','&euro;'),
		(u'™','&trade;'),(u'←','&larr;'),(u'↑','&uarr;'),(u'→','&rarr;'),(u'↓','&darr;'),(u'↔','&harr;'),(u'↵','&crarr;'),
		(u'⌈','&lceil;'),(u'⌉','&rceil;'),(u'⌊','&lfloor;'),(u'⌋','&rfloor'),(u'◊','&loz;'),(u'♠','&spades;'),(u'♣','&clubs;'),
		(u'♥','&hearts;'),(u'♦','&diams;'))

rss_max_feed_limit = 20
user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
size_overflow = 262144
rss_get_timeout = 15

def replacer(msg):
	msg = rss_replace(msg)
	msg = rss_del_html(msg)
	msg = rss_replace(msg)
	msg = rss_del_nn(msg)
	return msg

def unescape(text):
	def fixup(m):
		text = m.group(0)
		if text[:2] == "&#":
			try:
				if text[:3] == "&#x": return unichr(int(text[3:-1], 16))
				else: return unichr(int(text[2:-1]))
			except ValueError: pass
		else:
			try: text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError: pass
		return text
	return re.sub("&#?\w+;", fixup, text)	

def rss_replace(ms):
	for tmp in lmass: ms = ms.replace(tmp[1],tmp[0])
	for tmp in rmass: ms = ms.replace(tmp[1],tmp[0])
	return unescape(ms)

def rss_repl_del_html(ms,item):
	DS,SP,T = '<%s>','/%s',re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in T:
			if (tmp[:3] == '!--' and tmp[-2:] == '--') or tmp[-1:] == '/':
				pattern = DS % tmp
				pos = ms.find(pattern)
				ms = ms[:pos] + item + ms[pos+len(pattern):]
	T = re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in range(0,len(T)-1):
			pos = None
			TT = T[tmp].split(' ')[0]
			if TT[0] != '/':
				try: pos = T.index(SP % TT,tmp)
				except: pass
				if pos:
					pat1,pat2 = DS % T[tmp],DS % T[pos]
					pos1 = ms.find(pat1)
					pos2 = ms.find(pat2,pos1)
					ms = ms[:pos1] + item + ms[pos1+len(pat1):pos2] + item + ms[pos2+len(pat2):]
	for tmp in ('hr','br','li','ul','img','dt','dd','p'):
		T = re.findall('<%s.*?>' % tmp, ms, re.S)
		for tmp1 in T: ms = ms.replace(tmp1,item,1)
	return ms

def rss_repl_html(ms): return rss_repl_del_html(ms,' ')

def rss_del_html(ms): return rss_repl_del_html(ms,'')

def rss_del_nn(ms):
	ms = ms.replace('\r',' ').replace('\t',' ')
	while ms.count('\n '): ms = ms.replace('\n ','\n')
	while len(ms) and (ms[0] == '\n' or ms[0] == ' '): ms = ms[1:]
	while ms.count('\n\n'): ms = ms.replace('\n\n','\n')
	while ms.count('  '): ms = ms.replace('  ',' ')
	while ms.count(u'\n\n•'): ms = ms.replace(u'\n\n•',u'\n•')
	while ms.count(u'• \n'): ms = ms.replace(u'• \n',u'• ')
	return ms.strip()

def html_encode(body):
	encidx = body.find('encoding=')
	if encidx >= 0:
		enc = body[encidx+10:encidx+30]
		if enc.count('"'): enc = enc[:enc.find('"')]
		elif enc.count('\''): enc = enc[:enc.find('\'')]
		elif enc.count('&'): enc = enc[:enc.find('&')]
	else:
		encidx = body.find('charset=')
		if encidx >= 0:
			enc = body[encidx+8:encidx+30]
			if enc.count('"'): enc = enc[:enc.find('"')]
			elif enc.count('\''): enc = enc[:enc.find('\'')]
			elif enc.count('&'): enc = enc[:enc.find('&')]
		else: enc = chardet.detect(body)['encoding']
	if body == None: body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while body.count(splitter): splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'): ttext+=tmp2
					else: ttext+='?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try: return smart_encode(body,enc)
		except: return L('Encoding error!')

def rss_flush(jid,link,break_point):
	global feedbase, feeds
	tstop = []
	feedbase = getFile(feeds,[])
	for tmp in feedbase:
		if tmp[4] == jid and tmp[0] == link:
			try: tstop = tmp[5]
			except: pass
			feedbase.remove(tmp)
			if not break_point: break_point = tstop
			feedbase.append([tmp[0], tmp[1], tmp[2], int(time.time()), tmp[4], break_point])
			writefile(feeds,str(feedbase))
			break
	return tstop
	
def reduce_trash(t):
	t = t.replace('\n',' ').replace('\r',' ').replace('\t',' ')
	while t.count('  '): t = t.replace('  ',' ')
	if t[0] == ' ': t = t[1:]
	if t[-1] == ' ': t = t[:-1]
	return t
		
def rss(text,jid,type,to):
	global feedbase, feeds
	text = reduce_trash(text).split(' ')
	tl = len(text)
	if tl < 5: text.append('!')
	mode = text[0].lower() # show | add | del | clear | new | get
	if mode == 'add' and tl < 4: return 'add url timeH|M full|body|head[-url][-headline]'
	elif mode == 'del' and tl < 2: return 'del url'
	elif mode == 'new' and tl < 4: return 'new url max_feed_humber full|body|head[-url][-headline]'
	elif mode == 'get' and tl < 4: return 'get url max_feed_humber full|body|head[-url][-headline]'
	if mode == 'clear':
		feedbase = getFile(feeds,[])
		tf = []
		for taa in feedbase:
			if taa[4] != jid: tf.append(taa)
		feedbase = tf
		writefile(feeds,str(feedbase))
		return L('All RSS was cleared!')
	elif mode == 'show':
		if text[1] and text[1] != '!': tx = text[1]
		else: tx = None
		if getRoom(jid) in Owner and tx: sel_jid = tx
		else: sel_jid = jid
		feedbase = getFile(feeds,[])
		if feedbase != []:
			msg,tmp = '',feedbase
			tmp.sort()
			for rs in tmp:
				if sel_jid == 'all' or rs[4] == sel_jid:
					try: rtime = time.ctime(rs[3])
					except: rtime = 'Unknown'
					if sel_jid == jid: msg += '\n%s (%s) %s - %s' % (rs[0],rs[1],rs[2],rtime)
					else: msg += '\n%s \t%s \t%s (%s) %s' % (rtime,rs[4],rs[0],rs[1],rs[2])
			if len(msg): return L('Schedule feeds for %s:%s') % (sel_jid,msg)
			else: return L('Schedule feeds for %s not found!') % sel_jid
		return L('No RSS found!')
	elif mode == 'add':
		mdd = ['full','body','head']
		if text[3].split('-')[0] not in mdd: return L('Mode %s not detected!') % text[3]
		feedbase = getFile(feeds,[])
		link = text[1]
		if not link[:10].count('://'): link = 'http://'+link
		for dd in feedbase:
			if dd[0] == link and dd[4] == jid:
				feedbase.remove(dd)
				break
		timetype = text[2][-1:].lower()
		if not (timetype == 'h' or timetype == 'm'): timetype = 'h'
		try: ofset = int(text[2][:-1])
		except: ofset = 4
		if timetype == 'm' and ofset < 10: timetype = '10m'
		else: timetype = text[2]
		feedbase.append([link, timetype, text[3], int(time.time()), getRoom(jid),[]]) # url time mode
		writefile(feeds,str(feedbase))
		msg = L('Added: %s (%s) %s') % (link,timetype,text[3])
		sender(xmpp.Message(jid, msg, type),getRoom(to))
		return rss('get %s 1 %s' % (link,text[3]),jid,type,to)
	elif mode == 'del':
		feedbase = getFile(feeds,[])
		link = text[1]
		if not link[:10].count('://'): link = 'http://'+link
		msg = L('Can\'t find in schedule: %s') % link
		for rs in feedbase:
			if rs[0] == link and rs[4] == jid:
				feedbase.remove(rs)
				writefile(feeds,str(feedbase))
				return L('Delete feed from schedule: %s') % link
	elif mode == 'new' or mode == 'get':
		link = text[1]
		if not link[:10].count('://'): link = 'http://'+link
		try:
			if int(''.join(re.findall('([0-9])+\.([0-9])+',sys.version)[0])) >= 26: # python 2.6 and higher
				req = urllib2.Request(link.encode('utf-8'))
				req.add_header('User-Agent',user_agent)
				feed = urllib2.urlopen(url=req,timeout=rss_get_timeout).read(size_overflow)
			else: feed = urllib.urlopen(link).read()
		except:
			rss_flush(jid,link,None)
			if text[4] == 'silent': return None
			else: return L('Unable to access server! %s') % link
		is_rss_aton,fc = 0,feed[:256]
		if fc.count('<?xml version='):
			if fc.count('<feed'): is_rss_aton = 2
			elif fc.count('<rss') or fc.count('<rdf'): is_rss_aton = 1
			feed = html_encode(feed)
			feed = re.sub(u'(<span.*?>.*?</span>)','',feed)
			feed = re.sub(u'(<div.*?>)','',feed)
			feed = re.sub(u'(</div>)','',feed)
		if is_rss_aton and feed != L('Encoding error!'):
			if is_rss_aton == 1:
				if feed.count('<item>'): fd = feed.split('<item>')
				else: fd = feed.split('<item ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</item>')[0])
			else: 
				if feed.count('<entry>'): fd = feed.split('<entry>')
				else: fd = feed.split('<entry ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</entry>')[0])				
			if len(text) > 2:
				try: lng = int(text[2])
				except: lng = rss_max_feed_limit
			else: lng = len(feed)-1
			if len(feed)-1 <= lng: lng = len(feed)-1
			if lng > rss_max_feed_limit: lng = rss_max_feed_limit
			elif lng < 1: lng = 1
			if len(text) > 3: submode = text[3]
			else: submode = 'full'
			headline,urlmode = 'headline' in submode.split('-'),'url' in submode.split('-')
			submode = submode.split('-')[0]
			try:
				break_point = []
				for tmp in feed[1:rss_max_feed_limit+1]: break_point.append(hashlib.md5(tmp.encode('utf-8')).hexdigest())
				tstop = rss_flush(jid,link,break_point)
				t_msg,f_count = [],0
				for mmsg in feed[1:rss_max_feed_limit+1]:
					ttitle = get_tag(mmsg,'title').replace('&lt;br&gt;','\n')
					if mode == 'get' or not (hashlib.md5(mmsg.encode('utf-8')).hexdigest() in tstop):
						if is_rss_aton == 1:
							tbody = get_tag(mmsg,'description').replace('&lt;br&gt;','\n')
							turl = get_tag(mmsg,'link')
						else:
							tbody = get_tag(mmsg,'content').replace('&lt;br&gt;','\n')
							tu1 = mmsg.index('<link')
							tu2 = mmsg.find('href=\"',tu1)+6
							tu3 = mmsg.find('\"',tu2)
							turl = mmsg[tu2:tu3].replace('&lt;br&gt;','\n')
						tmsg, tsubj, tmurl = '','',''
						if submode == 'full': tmsg,tsubj = tbody,ttitle
						elif submode == 'body': tmsg = tbody
						elif submode[:4] == 'head': tsubj = ttitle
						else: return None
						if urlmode: tmurl = turl
						t_msg.append((tmsg, tsubj.replace('\n','; '), tmurl))
						f_count += 1
						if f_count >= lng: break
				if mode == 'new' and not f_count:
					if text[4] == 'silent': return None
					else: return L('New feeds not found!')
				if headline: type = 'headline'
				else: type = 'chat'
				t_msg.reverse()
				for tmp in t_msg:
					tmsg = replacer(tmp[0])
					if tmp[2]: i = xmpp.Message(to=jid, body=tmsg, typ=type, subject=replacer(tmp[1]),payload = [Node('x', {'xmlns': NS_X_OOB},[Node('url',{},tmp[2]),Node('desc',{},get_tag(feed[0],'title'))])])
					else: i = xmpp.Message(to=jid, body=tmsg, typ=type, subject=replacer(tmp[1]))
					sender(i,getRoom(to))
				return None
			except:
				rss_flush(jid,link,None)
				if text[4] == 'silent': return None
				else: return L('Error!')
		else:
			rss_flush(jid,link,None)
			if text[4] == 'silent': return None
			else:
				if feed.count('<TITLE>') and feed.count('</TITLE>'): titl = 'TITLE'
				elif feed.count('<title>') and feed.count('</title>'): titl = 'title'
				else: titl = ''
				if feed != L('Encoding error!'): title = get_tag(feed,titl)
				else: title = feed
				return L('Bad url or rss/atom not found at %s - %s') % (link,title)
	else: return 'show|add|del|clear|new|get'

class KThread(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, why, arg):
		if why == 'call': return self.localtrace
		else: return None

	def localtrace(self, frame, why, arg):
		if self.killed:
			if why == 'line': raise SystemExit()
		return self.localtrace

	def kill(self): self.killed = True

def thr(func,param,name):
	global th_cnt, thread_error_count
	th_cnt += 1
	try:
		if thread_type:
			with sema:
				tmp_th = KThread(group=None,target=func,name=str(th_cnt)+'_'+name,args=param)
				tmp_th.start()
		else: thread.start_new_thread(log_execute,(func,param))
	except Exception, SM:
		if str(SM).lower().count('thread'): thread_error_count += 1
		else: logging.exception(' ['+timeadd(tuple(localtime()))+'] '+str(proc))
		if thread_type:
			try: tmp_th.kill()
			except: pass

def log_execute(proc, params):
	try: proc(*params)
	except: logging.exception(' ['+timeadd(tuple(localtime()))+'] '+str(proc))

def send_count(item,ident):
	global message_out, presence_out, iq_out
	cl[ident].send(item)
	itm = unicode(item)[:2]
	if itm == '<m': message_out += 1
	elif itm == '<p': presence_out += 1
	elif itm == '<i': iq_out += 1
	
def sender(item,ident):
	global last_stream
	sleep(0.1)
	send_count(item,ident)

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def getFile(filename,default):
	if os.path.isfile(filename):
		try: filebody = eval(readfile(filename))
		except:
			if os.path.isfile(filename+'.back'):
				while True:
					try:
						filebody = eval(readfile(filename+'.back'))
						break
					except: pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(filename+'.back',str(filebody))
	return filebody

def get_subtag(body,tag):
	beg = body.find('\"',body.find(tag))+1
	return body[beg:body.find('\"',beg)]

def get_tag(body,tag):
	return body[body.find('>',body.find('<'+tag))+1:body.find('</'+tag+'>')]

def get_tag_full(body,tag):
	tmp_body = body[body.find('<'+tag):body.find(tag+'>',body.find('<'+tag)+2)+len(tag)+1]
	if len(tmp_body): return tmp_body
	return body[body.find('<'+tag):body.find('/>',body.find('<'+tag)+2)+2]

def get_tag_item(body,tag,item):
	body = get_tag_full(body,tag)
	return get_subtag(body,item)
	
def parser(text):
	text,ttext = unicode(text),''
	for tmp in text:
		if (tmp<='~'): ttext+=tmp
		else: ttext+='?'
	return ttext

def remove_sub_space(text):
	tx, es = '', '\t\r\n'
	for tmp in text:
		if ord(tmp) >= 32 or tmp in es : tx += tmp
		else: tx += '?'
	return tx

def smart_encode(text,enc):
	tx,splitter = '','|'
	while text.count(splitter): splitter += '|'
	ttext = text.replace('</','<'+splitter+'/').split(splitter)
	for tmp in ttext:
		try: tx += unicode(tmp,enc)
		except: pass
	return tx

def tZ(val):
	val = str(val)
	if len(val) == 1: val = '0'+val
	return val

def timeadd(lt): return '%s.%s.%s %s:%s:%s' % (tZ(lt[2]),tZ(lt[1]),tZ(lt[0]),tZ(lt[3]),tZ(lt[4]),tZ(lt[5]))

def onlytimeadd(lt): return '%s:%s:%s' % (tZ(lt[3]),tZ(lt[4]),tZ(lt[5]))

def pprint(text):
	lt = tuple(localtime())
	zz = parser('['+timeadd(lt)+'] '+text)
	if dm2: print zz
	if CommandsLog:
		fname = slog_folder+tZ(lt[0])+tZ(lt[1])+tZ(lt[2])+'.txt'
		fbody = tZ(lt[3])+tZ(lt[4])+tZ(lt[5])+'|'+text+'\n'
		fl = open(fname, 'a')
		fl.write(fbody.encode('utf-8'))
		fl.close()

def errorHandler(text):
	pprint('\n*** Error ***')
	pprint(text)
	pprint('more info at http://isida-bot.com/osiris\n')
	sys.exit('exit')

def arr_semi_find(array, string):
	astring = [unicode(string.lower())]
	pos = 0
	for arr in array:
		if re.findall(string, arr.lower()) == astring: break
		pos += 1
	if pos != len(array): return pos
	else: return -1

def arr_del_by_pos(array, position):
	return array[:position] + array[position+1:]

def arr_del_semi_find(array, string):
	pos = arr_semi_find(array, string)
	if pos >= 0: array = arr_del_by_pos(array,pos)
	return array

def os_version():
	iSys = sys.platform
	iOs = os.name
	osirisPyVer = sys.version.split(',')[0]+')'
	if iOs == 'posix':
		osInfo = os.uname()
		osirisOs = osInfo[0]+' ('+osInfo[2]+'-'+osInfo[4]+') / Python v'+osirisPyVer
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key):
			return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = get("ProductName")
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			osirisOs = osInfo+' '+spInfo+' (Build: '+buildInfo+') / Python v'+osirisPyVer
		except: osirisOs = osInfo+' (Build: '+buildInfo+') / Python v'+osirisPyVer
	else: osirisOs = 'unknown'
	return osirisOs

def timeZero(val):
	rval = []
	for iv in range(0,len(val)):
		if val[iv]<10: rval.append('0'+str(val[iv]))
		else: rval.append(str(val[iv]))
	return rval

def is_ignored(jid):
	jid = getRoom(jid)
	for tmp in Ignore:
		if tmp.count('@') and tmp == jid: return True
		elif tmp.count(jid): return True
	return False
	
def iqCB(sess,iq):
	global iq_in
	iq_in += 1
	id = iq.getID()
	if id == None: return None
	nick = unicode(iq.getFrom())
	query = iq.getTag('query')

	if iq.getType()=='get':
		to = unicode(iq.getTo().getStripped())
		if is_ignored(to): return None
		if iq.getTag(name='query', namespace=xmpp.NS_VERSION):
			pprint('*** iq:version from '+unicode(nick))
			i=xmpp.Iq(to=nick, typ='result')
			i.setAttr(key='id', val=id)
			i.setQueryNS(namespace=xmpp.NS_VERSION)
			i.getTag('query').setTagData(tag='name', val=botName)
			i.getTag('query').setTagData(tag='version', val=botVersion)
			i.getTag('query').setTagData(tag='os', val=botOs)
			sender(i,getRoom(to))
			raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_TIME):
			pprint('*** iq:time from '+unicode(nick))
			gt=timeZero(gmtime())
			t_utc=gt[0]+gt[1]+gt[2]+'T'+gt[3]+':'+gt[4]+':'+gt[5]
			lt=tuple(localtime())
			ltt=timeZero(lt)
			wday = [L('Mon'),L('Tue'),L('Wed'),L('Thu'),L('Fri'),L('Sat'),L('Sun')]
			wlight = [L('Winter time'),L('Summer time')]
			wmonth = [L('Jan'),L('Fed'),L('Mar'),L('Apr'),L('May'),L('Jun'),L('Jul'),L('Aug'),L('Sep'),L('Oct'),L('Nov'),L('Dec')]
			t_display = ltt[3]+':'+ltt[4]+':'+ltt[5]+', '+ltt[2]+'.'+wmonth[lt[1]-1]+'\''+ltt[0]+', '+wday[lt[6]]+', '
			if timeofset < 0: t_tz = 'GMT'+str(timeofset)
			else: t_tz = 'GMT+'+str(timeofset)
			t_display += t_tz + ', ' +wlight[lt[8]]
			i=xmpp.Iq(to=nick, typ='result')
			i.setAttr(key='id', val=id)
			i.setQueryNS(namespace=xmpp.NS_TIME)
			i.getTag('query').setTagData(tag='utc', val=t_utc)
			i.getTag('query').setTagData(tag='tz', val=t_tz)
			i.getTag('query').setTagData(tag='display', val=t_display)
			sender(i,getRoom(to))
			raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_LAST):
			pprint('*** iq:uptime from '+unicode(nick))
			i=xmpp.Iq(to=nick, typ='result')
			i.setAttr(key='id', val=id)
			i.setTag('query',namespace=xmpp.NS_LAST,attrs={'seconds':str(int(time.time())-starttime)})
			sender(i,getRoom(to))
			raise xmpp.NodeProcessed

def translate(from_lang,to_lang,text):
	query = urllib.urlencode({'q' : text.encode("utf-8"),'langpair':from_lang.lower()+'|'+to_lang.lower()})
	url = 'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&%s'.encode("utf-8") % (query)
	search_results = urllib.urlopen(url)
	try: 
		json = simplejson.loads(search_results.read())
		return rss_replace(json['responseData']['translatedText'])
	except: return L('Error!')

def messageCB(sess,mess):
	global message_in
	message_in += 1
	type=unicode(mess.getType())
	jid=unicode(mess.getFrom().getStripped()).lower()
	if is_ignored(jid): return
	text=unicode(mess.getBody())
	if text == 'None' or text == '': return
	if mess.getTimestamp() != None: return
	nick=mess.getFrom().getResource()
	if nick == None: nick = ''
	else: nick = unicode(nick)
	to=unicode(mess.getTo().getStripped())
	whoami = None
	for tmp in Settings:
		if getRoom(tmp['jid']) == to:
			whoami,limit = tmp['whoami'].split(),tmp['msglimit']
			break
	if not whoami: return
	if text: text = text[:limit]
	pprint('ID%s|%s|%s' % (whoami,text,jid))
	skip = None
	if getRoom(jid) in Owner:
		for tmp in OwnerCommands:
			if text.split(' ',1)[0].lower() == tmp[0]:
				skip = True
				try: param = text.split(' ',1)[1]
				except: param = ''
				pprint('Owner:%s|%s' % (jid,text))
				if tmp[2]:
					if len(param): text = tmp[1](param)
					else: text = 'What?'
				else: text = tmp[1]()
	if not skip:
		if text.lower() == 'help': text = u'... oSiris Jabber Bot ...\n© 2oo9-2o1o Disabler Production Lab.\nhttp://isida-bot.com/osiris\nSend donation to:\nYandexMoney: 41001384336826\nWMZ: Z392970180590\nWMR: R378494692310\nWME: E164241657651\nBest regards Disabler'
		elif whoami[0] == 'rss': text = rss(text,jid,type,to)
		elif whoami[0] == 'translate': text = translate(whoami[1],whoami[2],text)
		else: text == 'Not configured now!'
	if text: sender(xmpp.Message(jid, text[:limit], type),getRoom(to))

def bot_update():
	global game_over, bot_exit_type
	game_over, bot_exit_type = True, 'update'
	return 'Update!'

def bot_exit():
	global game_over, bot_exit_type
	game_over, bot_exit_type = True, 'exit'
	return 'Quit!'

def bot_restart():
	global game_over, bot_exit_type
	game_over, bot_exit_type = True, 'restart'
	return 'Restart!'

def bot_sh(cmd):
	tmp_file = 'tmp'
	try: os.remove(tmp_file)
	except: pass
	try:
		os.system(cmd+' >> '+tmp_file)
		try: body = readfile(tmp_file)
		except: body = L('Command execution error.')
		if len(body):
			enc = chardet.detect(body)['encoding']
			return unicode(body,enc)
		else: return L('ok')
	except Exception, SM: return L('I can\'t execute it! Error: %s') % str(SM)

def bot_exec(text):
	try: text = unicode(eval(text))
	except Exception, SM: text = L('I can\'t execute it! Error: %s') % unicode(SM)[:msg_limit/2]
	return text

def bot_stats():
	msg  = 'Executed threads: %s | Error(s): %s\n' % (th_cnt,thread_error_count)
	msg += 'Message in %s | out %s\n' % (message_in,message_out)
	msg += 'Presence in %s | out %s\n' % (presence_in,presence_out)
	msg += 'Iq in %s | out %s\n' % (iq_in,iq_out)
	return msg

OwnerCommands = [('update',bot_update,None),
				 ('quit',bot_exit,None),
				 ('restart',bot_restart,None),
				 ('sh',bot_sh,True),
				 ('exec',bot_exec,True),
				 ('stats',bot_stats,None)]
	
def presenceCB(sess,mess):
	global presence_in, online
	presence_in += 1
	type=unicode(mess.getType())
	jid=getRoom(unicode(mess.getFrom().getStripped())).lower()
	if is_ignored(jid): return
	to=getRoom(unicode(mess.getTo()))
	if jid == to: return

	if type == 'subscribe': 
		j = Presence(jid, 'subscribed')
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		sender(j,to)
		j = Presence(jid, 'subscribe')
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		sender(j,to)
		pprint('Subscribe %s for %s' % (jid,getName(to)))
	elif type == 'unsubscribed': 
		j = Presence(jid, 'unsubscribe')
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		sender(j,to)
		j = Presence(jid, 'unsubscribed')
		j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
		sender(j,to)
		pprint('Unsubscribe %s for %s' % (jid,getName(to)))
		feedbase = getFile(feeds,[])
		tf = []
		for taa in feedbase:
			if taa[4] != jid: tf.append(taa)
		feedbase = tf
		writefile(feeds,str(feedbase))
	if type == 'unavailable' and jid in online: online.remove(jid)
	elif not jid in online: online.append(jid)

def getName(jid):
	jid = unicode(jid).lower()
	if jid == 'None': return jid
	return jid[:jid.find('@')].lower()

def getServer(jid):
	jid = unicode(jid).lower()
	if not jid.count('/'): jid += '/'
	if jid == 'None': return jid
	return jid[jid.find('@')+1:jid.find('/')].lower()

def getResourse(jid):
	jid = unicode(jid).lower()
	if jid == 'None': return jid
	return jid[jid.find('/')+1:]

def getRoom(jid):
	jid = unicode(jid).lower()
	if jid == 'None': return jid
	return getName(jid)+'@'+getServer(jid)

def now_schedule():
	while not game_over:
		sleep(schedule_time)
		if not game_over:
			for tmp in gtimer: log_execute(tmp,())

def check_rss():
	to = None
	for tmp in Settings:
		if tmp['whoami'] == 'rss':
			to, limit = getRoom(tmp['jid']),tmp['msglimit']
			break
	if not to: return
	l_hl = int(time.time())
	feedbase = getFile(feeds,[])
	for fd in feedbase:
		ltime = fd[1]
		timetype = ltime[-1:].lower()
		if not (timetype == 'h' or timetype == 'm'): timetype = 'h'
		try: ofset = int(ltime[:-1])
		except: ofset = 4
		if timetype == 'h': ofset *= 3600
		elif timetype == 'm': ofset *= 60
		try: ll_hl = int(fd[3])
		except: ll_hl = 0
		if not is_ignored(fd[4]) and (ll_hl + ofset <= l_hl and (fd[4] in online or not 'headline' in fd[2].split('-'))):
			pprint('check rss: '+fd[0]+' for '+fd[4])
			text = rss('new %s %s %s silent' % (fd[0],rss_max_feed_limit,fd[2]) ,fd[4],'chat',to)
			if text: sender(xmpp.Message(fd[4], text[:limit], 'chat'),to)
			break

def flush_stats():
	pprint('Executed threads: %s | Error(s): %s' % (th_cnt,thread_error_count))
	pprint('Message in %s | out %s' % (message_in,message_out))
	pprint('Presence in %s | out %s' % (presence_in,presence_out))
	pprint('Iq in %s | out %s' % (iq_in,iq_out))
	
def disconnecter():
	global bot_exit_type, game_over
	pprint('--- Restart by disconnect handler! ---')
	game_over, bot_exit_type = True, 'restart'
	sleep(2)

def L(text):
	if not len(text): return text
	try: return locales[text]
	except: return text

def kill_all_threads():
	if thread_type:
		for tmp in threading.enumerate():
			try: tmp.kill()
			except: pass

# --------------------- Иницилизация переменных ----------------------
slog_folder = 'log/'					# папка системных логов
LOG_FILENAME = slog_folder+'error.txt'	# логи ошибок
set_folder = 'settings/'				# папка настроек
configname = set_folder+'config.py'		# конфиг бота
feeds = set_folder+'feed'				# список rss каналов
loc_file = set_folder+'locale'			# файл локализации
loc_folder = 'locales/'					# папка локализаций

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)		# включение логгирования

nmbrs = ['0','1','2','3','4','5','6','7','8','9','.']
debugmode = None						# остановка на ошибках
dm = None								# отладка xmpppy
dm2 = None								# отладка действий бота
CommandsLog = None						# логгирование команд
botName = 'Osiris-Bot'					# название бота
botVersion = 'v0.02'					# версия бота
capsVersion = botVersion[1:]			# версия для капса
capsNode = 'Osiris-Bot'					# капс бота
th_cnt = 0								# счётчик тредов
schedule_time = 10						# время проверки расписания
thread_error_count = 0					# счётчик ошибок тредов
reboot_time = 180						# таймаут рестарта бота при ошибке не стадии подключения (нет инета, ошибка авторизации)
bot_exit_type = None					# причина завершения бота
thread_type = True						# тип тредов
message_in = 0
message_out = 0
iq_in = 0
iq_out = 0
presence_in = 0
presence_out = 0
online = []

gt=gmtime()
lt=tuple(localtime())
if lt[0:3] == gt[0:3]: timeofset = int(lt[3])-int(gt[3])
elif lt[0:3] > gt[0:3]: timeofset = int(lt[3])-int(gt[3]) + 24
else: timeofset = int(gt[3])-int(lt[3]) + 24

botOs = os_version()
pprint('*** Loading config')
if os.path.isfile(configname): execfile(configname)
else: errorHandler(configname+' is missed.')
pprint('*** Settings count %s' % len(Settings))

locales = {}

gtimer = [check_rss]

if os.path.isfile('settings/starttime'):
	try: starttime = eval(readfile('settings/starttime'))
	except: starttime = readfile('settings/starttime')
else: starttime = int(time.time())
sesstime = int(time.time())

if os.path.isfile('version'): botVersion += '.' + str(readfile('version')).replace('\n','')

pprint('*'*50)
pprint('*** Bot Name: '+botName)
pprint('*** Version '+botVersion)
pprint('*** OS '+botOs)
pprint('*'*50)
pprint('*** (c) 2oo9-2o1o Disabler Production Lab.')

cl = {}

for st in Settings:
	jid = xmpp.JID(st['jid'])
	pprint('>>> bot jid: %s' % st['jid'])
	jr = getRoom(jid).lower()
	
	try:
		if dm: cl[jr] = Client(jid.getDomain())
		else: cl[jr] = Client(jid.getDomain(), debug=[])
		cl[jr].connect()
		pprint('> Connected')
		cl[jr].auth(jid.getNode(), st['password'], jid.getResource())
		pprint('> Autheticated')
	except:
		pprint('Auth error or no connection. Restart in '+str(reboot_time)+' sec.')
		sleep(reboot_time)
		sys.exit('restart')
	pprint('> Registration Handlers')
	cl[jr].RegisterHandler('message',messageCB)
	cl[jr].RegisterHandler('iq',iqCB)
	cl[jr].RegisterHandler('presence',presenceCB)
	cl[jr].RegisterDisconnectHandler(disconnecter)
	cl[jr].UnregisterDisconnectHandler(cl[jr].DisconnectHandler)
	show,status,priority = 'online','Ready!',777
	for tmp in Settings:
		if getRoom(tmp['jid']) == jr:
			show,status,priority = tmp['status'],tmp['message'],tmp['priority']
			break
	j = Presence(show=show, status=status, priority=priority)
	j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
	sender(j,jr)

game_over = None
thr(now_schedule,(),'schedule')

pprint('Ready to work!')

while 1:
	try:
		while not game_over:
			for cli in cl: cl[cli].Process(1)
		kill_all_threads()
		flush_stats()
		sys.exit(bot_exit_type)

	except KeyboardInterrupt:
		StatusMessage = L('Shutdown by CTRL+C...')
		pprint(StatusMessage)
		sleep(0.1)
		kill_all_threads()
		flush_stats()
		sys.exit('exit')

	except Exception, SM:
		pprint('*** Error *** '+str(SM)+' ***')
		logging.exception(' ['+timeadd(tuple(localtime()))+'] ')
		if str(SM).lower().count('parsing finished'):
			kill_all_threads()
			flush_stats()
			sleep(300)
			sys.exit('restart')
		if debugmode: raise

# The end is near!
