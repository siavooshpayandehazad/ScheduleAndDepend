__author__ = 'siavoosh'
import os,sys
import copy
import logging
import time
from Mapper import Mapping
from Scheduler import Scheduling_Functions
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports,TG_Functions
from RoutingAlgorithms import Routing
from ArchGraphUtilities import Arch_Graph_Reports,AG_Functions
import misc
import Logger
import Config

####################################################################
#
#                       Logging Material
#
####################################################################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()
##############################
# preparing to setup Logging
LoGDirectory = "LOGS"
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir,LoGDirectory),
                                          'Logging_Log_'+str(time.time())+'.log'),level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
GraphDirectory = "GraphDrawings"
if not os.path.isdir(GraphDirectory):
   os.makedirs(GraphDirectory)
####################################################################
misc.DrawLogo()
####################################################################
# TODO: can we get TG specifications automatically from some benchmark alg??
TG = copy.deepcopy(TG_Functions.GenerateTG())
Task_Graph_Reports.ReportTaskGraph(TG,logging)
Task_Graph_Reports.DrawTaskGraph(TG)
TG_Functions.CheckAcyclic(TG,logging)
####################################################################
AG = copy.deepcopy(AG_Functions.GenerateAG(logging))
Arch_Graph_Reports.DrawArchGraph(AG)
####################################################################
SHM = SystemHealthMonitor.SystemHealthMonitor()
SHM.SetUp_NoC_SystemHealthMap(AG,Config.TurnsHealth)
SHM.Report_NoC_SystemHealthMap()
print "==========================================="
print "SYSTEM IS UP..."
# Here we are injecting initial faults of the system
SHM.ApplyInitialFaults()
NoCRG = Routing.GenerateNoCRouteGraph(AG,SHM,Config.XY_TurnModel,Config.DebugInfo,Config.DebugDetails)
# NoCRG = Routing.GenerateNoCRouteGraphFromFile(AG,SHM,Config.RoutingFilePath,Config.DebugInfo,Config.DebugDetails)
# print Routing.FindRouteInRouteGraph(NoCRG,0,3,True,True)
####################################################################

BestTG,BestAG = Mapping.Mapping(TG,AG,NoCRG,SHM,logging)
if BestAG is not None and BestTG is not None:
    TG = copy.deepcopy(BestTG)
    AG = copy.deepcopy(BestAG)
    del BestTG, BestAG
    SHM.AddCurrentMappingToMPM(TG)
# SHM.RandomFaultInjection()
# SHM.ReportMPM()
Scheduling_Functions.GenerateGantCharts(TG,AG)
logging.info('Logging finished...')