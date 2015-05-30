# Bot commands #

These commands are available for owner from any bot's jid:

<li><code>sh &lt;command&gt; - execute shell command</code>
<li><code>exec &lt;command&gt; - execute python code</code>
<li><code>update - update bot from svn repository</code>
<li><code>quit - shutdown bot</code>
<li><code>restart - restart bot</code>
<li><code>stats - show some statistic</code>

These commands are available for anybody from any bot's jid:<br>
<br>
<li><code>help - short help</code>
<li><code>about - about me</code>

<h1>Translate jid's</h1>

<li><code>[from] [to] text - translate text</code>
<li><code>list - show list of available languages</code>
<li><code>info [lang1] [lang2] [...] - show description of language</code>
<li><code>set [lang] - set default language for translate</code>

<h1>Feeds jid</h1>

<li><code>show - show feeds for current jid</code>
<li><code>clear - remove all feeds</code>
<li><code>add url time mode - add feed where:</code>
<pre><code>url - url of feed with or without "http://"<br>
time - time between feed check. f.e: 20m or 2h<br>
mode - one of three modes:<br>
 - head - only feed title<br>
 - body - obly fedd body<br>
 - full - title and body<br>
allowed two keys:<br>
-url - show url of feed<br>
-headline - send message as headline<br>
f.e: add bash.org.ru/rss 1h full-url-headline<br>
</code></pre>
<li><code>del url - remove feed</code>
<li><code>get url number_of_feeds mode - get feeds</code>
sintax like in "add" command<br>
<li><code>new url number_of_feeds mode - get only new feeds</code>
sintax like in "add" command<br>
<br>
<br>
<br>
<br>
<hr><br>
<br>
<p align='center'><i><font color='#0000aa' size='1'>(c) 2oo9-2o11 Disabler Production Lab</font><font color='#ff0000' size='1'>A</font><font color='#0000aa' size='1'>ratory</font></i></p>

<hr>

