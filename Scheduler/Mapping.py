

__author__ = 'siavoosh'
import Scheduler
import Scheduling_Functions
import random
import copy
from Mapping_Functions import AddClusterToNode
from Mapping_Functions import RemoveClusterFromNode
from Mapping_Functions import ClearMapping
from Mapping_Functions import CostFunction

def MakeInitialMapping(TG,CTG,AG,NoCRG):
    print "STARTING INITIAL MAPPING..."
    for Cluster in CTG.nodes():
        DestNode = random.choice(AG.nodes())
        Itteration=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,Cluster,DestNode,True):
            Itteration+=1
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,Cluster,DestNode,True)
            DestNode = random.choice(AG.nodes())        #try another node
            print "\t-------------------------"
            print "\tMAPPING ATTEMPT: #",Itteration+1,"FOR CLUSTER:",Cluster
            if Itteration == 10* len(CTG.nodes()):
                print "\033[31mERROR::\033[0m INITIAL MAPPING FAILED..."
                ClearMapping(TG,CTG,AG)
                return False
    print "INITIAL MAPPING READY..."
    return True

def OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,ItterationNum,Report):
    print "STARTING MAPPING OPTIMIZATION..."
    BestTG=copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost=CostFunction(TG,AG,False)
    for Itteration in range(0,ItterationNum):
        if Report:print "\tITERATION:",Itteration
        ClusterToMove= random.choice(CTG.nodes())
        CurrentNode=CTG.node[ClusterToMove]['Node']
        RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
        DestNode = random.choice(AG.nodes())
        TryCounter=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,Report):
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,Report)
            AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
            ClusterToMove= random.choice(CTG.nodes())
            CurrentNode=CTG.node[ClusterToMove]['Node']
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
            DestNode = random.choice(AG.nodes())
            if TryCounter >= 3*len(AG.nodes()):
                print "CAN NOT FIND ANY SOLUTION... ABORTING MAPPING..."
                TG=copy.deepcopy(BestTG)
                AG=copy.deepcopy(BestAG)
                CTG=copy.deepcopy(BestCTG)
                Scheduling_Functions.ReportMappedTasks(AG)
                CostFunction(TG,AG,True)
                return False
            TryCounter+=1
        Scheduling_Functions.ClearScheduling(AG,TG)
        Scheduler.ScheduleAll(TG,AG,Report)
        CurrentCost=CostFunction(TG,AG,Report)
        if CurrentCost <= BestCost:
            print "\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:",CurrentCost
            BestTG=copy.deepcopy(TG)
            BestAG=copy.deepcopy(AG)
            BestCTG=copy.deepcopy(CTG)
            BestCost=CurrentCost
        else:
            TG=copy.deepcopy(BestTG)
            AG=copy.deepcopy(BestAG)
            CTG=copy.deepcopy(BestCTG)
    Scheduling_Functions.ReportMappedTasks(AG)
    CostFunction(TG,AG,True)
    return True

