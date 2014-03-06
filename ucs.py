import os
from UcsSdk import * 

UCSM_HOST = os.environ['UCSM_HOST']
UCSM_USERNAME = os.environ['UCSM_USERNAME']
UCSM_PASSWORD = os.environ['UCSM_PASSWORD']

class UCS(object):
    def __init__(self):
        self.handle = UcsHandle()
        self.login()        

    def login(self):
        self.handle.Login(UCSM_HOST, username=UCSM_USERNAME, password=UCSM_PASSWORD, noSsl=False, port=443, dumpXml=YesOrNo.FALSE)

    def logout(self):
        self.handle.Logout()

    def getObject(self, org=None, classId=None, level=None):
        print "############################################"
        print "org: %s class: %s level: %s" % (org, classId, level)
        response = self.handle.GetManagedObject(org, classId, level, dumpXml=False)  
        for item in response:
            print vars(item)
            print "\n"
        print "\n"
        return response            

    def getObjects(self, classIds):
        for classId in classIds:
            self.getObject(classId=classId)

ucs = UCS()    
ucs.getObject(classId=OrgOrg.ClassId(),level={OrgOrg.LEVEL:"1"})
orgOrg = ucs.getObject(level={OrgOrg.DN:"org-root"})
lsServer = ucs.getObject(org=orgOrg, classId=LsServer.ClassId(), level={LsServer.NAME : 'sp_name'})

classIds = [
    EquipmentChassis.ClassId(),
    ComputeBlade.ClassId(),
    NetworkElement.ClassId()
]
ucs.getObjects(classIds)

ucs.logout()
