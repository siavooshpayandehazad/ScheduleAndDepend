__author__ = 'siavoosh'

################################################
#          Debug  Config
################################################
DebugInfo = True
DebugDetails = False

################################################
#          TG  Config
################################################
NumberOfTasks= 10
NumberOfEdges= 15
WCET_Range= 30
EdgeWeightRange= 7

################################################
#          Network  Config
################################################
MaXBandWidth = 10
VirtualChannelNum = 0
# in case of automatic generation of AG
# available topologies: --
# Todo: automatic generation of AG
NetworkTopology='Mesh'
Network_X_Size=2
Network_Y_Size=2

################################################
#          Routing  Config
################################################
# Todo: introduce more turn models
FULL_TurnModel=['E2N','E2S','W2N','W2S','S2W','S2E','N2W','N2E']
XY_TurnModel=['E2N','E2S','W2N','W2S']
WestFirst_TurnModel=[]
EastFirst_TurnModel=[]

