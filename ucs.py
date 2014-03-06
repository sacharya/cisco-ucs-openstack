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

    def getManagedObject(self, something, classId, level):
        if level is not None:
            resp = self.handle.GetManagedObject(something, classId, level)
        else:
            resp = self.handle.GetManagedObject(something, classId)
        for res in resp:
            print vars(res)
        return resp

    def getNodes(self):
        print "\nGet Nodes......"
        computeNodes = {}
        equipmentChassis = self.handle.GetManagedObject(None, EquipmentChassis.ClassId(), None, dumpXml=False)    
        for chassis in equipmentChassis:
            print vars(chassis)
            computeNodes['Chassis-%s' % (chassis.getattr(EquipmentChassis.ID))] = {}
        return computeNodes

    def getComputeBlades(self):
        print "\nGet Compute Blades......"
        computeNodes = {}
        computeBlades = self.handle.GetManagedObject(None, ComputeBlade.ClassId(), None, dumpXml=False)
        for computeBlade in computeBlades:
            computeNode = {}
            print vars(computeBlade)
            computeNode['chassisID'] = computeBlade.getattr(ComputeBlade.CHASSIS_ID)
            computeNode['availableMemory'] = computeBlade.getattr(ComputeBlade.AVAILABLE_MEMORY)
            computeNode['numOfAdaptors'] = computeBlade.getattr(ComputeBlade.NUM_OF_ADAPTORS)
            computeNode['numOfCores'] = computeBlade.getattr(ComputeBlade.NUM_OF_CORES)
            computeNode['numOfCoresEnabled'] = computeBlade.getattr(ComputeBlade.NUM_OF_CORES_ENABLED)
            computeNode['numOfCpus'] = computeBlade.getattr(ComputeBlade.NUM_OF_CPUS)
            computeNode['numOfEthHostIfs'] = computeBlade.getattr(ComputeBlade.NUM_OF_ETH_HOST_IFS)
            computeNode['numOfFcHostIfs'] = computeBlade.getattr(ComputeBlade.NUM_OF_FC_HOST_IFS)
            computeNode['numOfThreads'] = computeBlade.getattr(ComputeBlade.NUM_OF_THREADS)        
            chassis_str = 'Chassis-%s' % (computeBlade.getattr(ComputeBlade.CHASSIS_ID))
            blade_str = 'Blade-%s' % (computeBlade.getattr(ComputeBlade.SLOT_ID))
            computeNodes[chassis_str][blade_str] = computeNode
        return computeNodes

    def getNetworks(self):
        print "\nGet Networks......"
        nets = {}
        networks = self.handle.GetManagedObject(None, NetworkElement.ClassId(), None, dumpXml=False)
        for network in networks:
            print vars(network)
            print "\n"
        return nets

    def getRootOrg(self):
        print "\nGet Root Org......"
        resp = self.handle.GetManagedObject(None, None,{OrgOrg.DN:"org-root"})
        for res in resp:
            print vars(res)
        return resp         

    def getLevelOrg(self, level):
        print "\N Get Level Org......"
        resp = self.handle.GetManagedObject(None,OrgOrg.ClassId(),{OrgOrg.LEVEL:level})
        for res in resp:
            print vars(res)
        return resp

ucs = UCS()    
ucs.getLevelOrg("1")

sp = "sp_name"
orgOrg = ucs.getRootOrg() 
lsServer = ucs.getManagedObject(orgOrg, LsServer.ClassId(), {LsServer.NAME : sp})

ucs.getNodes()
ucs.getComputeBlades()
ucs.getNetworks()

ucs.logout()
