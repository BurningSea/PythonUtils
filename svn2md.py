#!/usr/bin/python
import os,sys,re;

def checkCommand(cmd):
	result = os.system(cmd);
	if result!=0x100:
			print "Plz add %s to your PATH"%(cmd);
			sys.exit(0);

def getSubversionLog():
	SVN='/usr/bin/svn';
	OUTPUT='./svn.log';

	checkCommand(SVN);
	length=len(sys.argv);
	if (length!=3 and length!=4):
		print "Usage: cmd $svn_url $revision_before [$revision_after]";
		sys.exit(0);

	url=sys.argv[1];
	before=sys.argv[2];
	if length==4:
		after=sys.argv[3];
	else:
		after='HEAD';

	CMD="%s log %s -r%s:%s --xml > %s"%(SVN,url,after,before,OUTPUT);
	print CMD;
	os.system(CMD);

	return OUTPUT;

def function():
	f=open('./svn.log');
	content=f.read();
	for match in re.finditer(r'^[^\|]*\n', content):
		content=re.sub(r"\n"+match.group(), "<\p>"+match.group(), content);
	print content;
  	# msgBreak = re.compile(r'^[^\|]*\n');
  	# match = msgBreak.search(content);
  	# if match:
  	# 	# print match.group();
  	# 	for i in xrange(0, len(match) - 1):
  	# 		print match.group(i);

def processLog(path):
 	log=open(path);
 	content=log.read();
 	# print content;

 	md=open('./log.md', 'w');

 	content=re.sub(r"<\?xml.*", "", content);
 	# remove<log></log>
 	content=re.sub(r".*log>\n", "", content);
 	# remove <logentry...revision="
 	content=re.sub(r"<logentry.*\n.*revision=\"", "", content);
 	content=re.sub(r"\">.*\n.*<author>", "|", content);
  	content=re.sub(r"</au.*\n.*\n<msg>", "|", content);	
  	content=re.sub(r"</msg>.*\n</logentry>", "", content);
  	content=re.sub(r"\n+", "\n", content);
  	content="Revision|Author|Messages\n|"+content;

 	# print "Replaced:%s"%(content);
 	md.write(content);

logPath=getSubversionLog();
processLog(logPath);
