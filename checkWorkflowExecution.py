import boto.swf.layer2 as swf
import smtplib
import time
import commands
 
def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message,login, password,smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

def freakout():
	sendemail(from_addr    = 'python@RC.net', 
		  to_addr_list = ['hanysalaheldeen@gmail.com'],
		  cc_addr_list = ['hany@cs.odu.edu'], 
		  subject      = 'Super Urgent', 
		  message      = 'Something fucked up and the workflow is not working', 
		  login        = 'longitudinalStudyAWS@gmail.com', 
		  password     = 'HANYHANY')

while(True):
	domain = swf.Domain(name='LongitudinalStudy')

	try:
		status = str(domain.executions()[0].describe()['executionInfo']['executionStatus'])
		if(status!='OPEN'):
			freakout()
	except:		
		freakout()
		commands.getoutput("ruby lib/periodic_workflow_starter.rb workflow-config.json")

	time.sleep(600)
	

