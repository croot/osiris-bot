# -*- coding: utf-8 -*- 

#------------------------------------------------
#             Osiris-bot Config file
#                  v0.1beta
#------------------------------------------------

RSSsettings = {
'whoami'	: u'rss',
'jid'		: u'rss_login@server.tld/osiris rss',
'password'	: u'********',
'status'	: u'online',
'message'	: u'Osiris RSS/ATOM feed bot',
'priority'	: 777,
'msglimit'	: 4096}

ENRUsettings = {
'whoami'	: u'translate en ru',
'jid'		: u'enru_login@server.tld/osiris en-ru translate',
'password'	: u'********',
'status'	: u'online',
'message'	: u'Osiris EN>RU translate bot',
'priority'	: 777,
'msglimit'	: 512}

RUENsettings = {
'whoami'	: u'translate ru en',
'jid'		: u'ruen_login@server.tld/osiris ru-en translate',
'password'	: u'********',
'status'	: u'online',
'message'	: u'Osiris RU>EN translate bot',
'priority'	: 777,
'msglimit'	: 512}

Settings = [RSSsettings,ENRUsettings,RUENsettings]
Owner = ['jid1@server.tld','jid2@server.tld','jid3@server.tld']
Ignore = []

#debugmode = True
#dm = True
#dm2 = True

CommandsLog = True