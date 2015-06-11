__author__ = 'siavoosh'
from math import ceil
import matplotlib.pyplot as plt
import Config

def FindScheduleMakeSpan(AG):
    MakeSpan=0
    for Node in AG.nodes():
        for Task in AG.node[Node]['MappedTasks']:
            if AG.node[Node]['Scheduling'][Task][1]>MakeSpan:
                MakeSpan=AG.node[Node]['Scheduling'][Task][1]
    return MakeSpan
################################################################
def ClearScheduling(AG,TG):
    for Node in AG.nodes():
        AG.node[Node]['Scheduling']={}
    for Link in AG.edges():
        AG.edge[Link[0]][Link[1]]['Scheduling']={}
    return None

##########################################################################
#
#                       ADDING TASK AND EDGE TO
#                               RESOURCES
#
##########################################################################

def Add_TG_TaskToNode(TG,AG,SHM,Task,Node,Report):
    if Report: "\t\tADDING TASK:",Task," TO NODE:",Node
    CriticalityLevel=TG.node[Task]['Criticality']
    StartTime=max(FindLastAllocatedTimeOnNode(TG,AG,Node,Report),
                  FindTaskPredecessorsFinishTime(TG,AG,Task,CriticalityLevel),
                  TG.node[Task]['Release'])
    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time

    NodeSpeedDown= 1+((100.0-SHM.SHM.node[Node]['NodeSpeed'])/100)
    TaskExecutionOnNode= ceil(TG.node[Task]['WCET']* NodeSpeedDown)
    EndTime=StartTime+TaskExecutionOnNode
    if Report:print "\t\tSTARTING TIME:",StartTime,"ENDING TIME:",EndTime
    AG.node[Node]['Scheduling'][Task]=[StartTime,EndTime]
    TG.node[Task]['Node']=Node
    return True
################################################################
def Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report):
    if Report:print "\t\tADDING EDGE:",Edge," TO LINK:",Link
    StartTime=max(FindLastAllocatedTimeOnLink(TG,AG,Link,Report),FindEdgePredecessorsFinishTime(TG,AG,Edge))
    EndTime=StartTime+(TG.edge[Edge[0]][Edge[1]]['ComWeight'])
    if Report:print "\t\tSTARTING TIME:",StartTime,"ENDING TIME:",EndTime
    AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]=[StartTime,EndTime]
    return True

##########################################################################
#
#                   CALCULATING LATEST STARTING TIME
#                           FOR TASK BASED ON
#                               PREDECESSORS
##########################################################################
def FindTaskPredecessorsFinishTime(TG,AG,Task,CriticalityLevel):
    FinishTime=0
    if len(TG.predecessors(Task))>0:
        for Predecessor in TG.predecessors(Task):
            if TG.node[Predecessor]['Node'] is not None: #predecessor is mapped
                if TG.node[Predecessor]['Criticality']==CriticalityLevel: #this is not quit right...
                    Node = TG.node[Predecessor]['Node']
                    if  Predecessor in AG.node[Node]['Scheduling']:
                        if AG.node[Node]['Scheduling'][Predecessor][1]>FinishTime:
                            FinishTime=AG.node[Node]['Scheduling'][Predecessor][1]
    for Edge in TG.edges():
        if Edge[1]==Task:
            if TG.edge[Edge[0]][Edge[1]]['Criticality']==CriticalityLevel:
                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0: # if the edge is mapped
                    for Link in  TG.edge[Edge[0]][Edge[1]]['Link']: #for each link that this edge goes through
                        if len(AG.edge[Link[0]][Link[1]]['Scheduling'])>0:
                            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']: #if this edge is scheduled
                                if AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]>FinishTime:
                                    FinishTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]
    return FinishTime
################################################################
def FindEdgePredecessorsFinishTime(TG,AG,Edge):
    FinishTime=0
    Node = TG.node[Edge[0]]['Node']
    if Edge[0] in AG.node[Node]['Scheduling']:
        if AG.node[Node]['Scheduling'][Edge[0]][1]>FinishTime:
            FinishTime=AG.node[Node]['Scheduling'][Edge[0]][1]
    for Link in AG.edges():
        if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
            if AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]>FinishTime:
                FinishTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]

    return FinishTime

##########################################################################
#
#                   CALCULATING LAST ALLOCATED TIME
#                           FOR RESOURCES
#
##########################################################################
def FindLastAllocatedTimeOnLink(TG,AG,Link,Report):
    if Report:print "\t\tFINDING LAST ALLOCATED TIME ON LINK", Link
    LastAllocatedTime=0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                if StartTime is not None and EndTime is not None:
                    if Report:print "\t\t\tTASK STARTS AT:",StartTime,"AND ENDS AT:",EndTime
                    if EndTime > LastAllocatedTime:
                        LastAllocatedTime = EndTime
    else:
        if Report:print "\t\t\tNO SCHEDULED TASK FOUND"
        return 0
    if Report:print "\t\t\tLAST ALLOCATED TIME:",LastAllocatedTime
    return LastAllocatedTime
################################################################
def FindLastAllocatedTimeOnNode(TG,AG,Node,Report):
    if Report:print "\t\tFINDING LAST ALLOCATED TIME ON NODE", Node
    LastAllocatedTime=0
    if len(AG.node[Node]['MappedTasks'])>0:
        if Report:print "\t\t\tMAPPED TASKS ON THE NODE:",AG.node[Node]['MappedTasks']
        for Task in AG.node[Node]['MappedTasks']:
            if Task in AG.node[Node]['Scheduling']:
                StartTime=AG.node[Node]['Scheduling'][Task][0]
                EndTime=AG.node[Node]['Scheduling'][Task][1]
                if StartTime is not None and EndTime is not None:
                    if Report:print "\t\t\tTASK STARTS AT:",StartTime,"AND ENDS AT:",EndTime
                    if EndTime > LastAllocatedTime:
                        LastAllocatedTime = EndTime
    else:
        if Report:print "\t\t\tNO SCHEDULED TASK FOUND"
        return 0
    if Report:print "\t\t\tLAST ALLOCATED TIME:",LastAllocatedTime
    return LastAllocatedTime

##########################################################################
#
#                                   REPORTS
#
#
##########################################################################
def ReportMappedTasks(AG):
    print "==========================================="
    print "          REPORTING SCHEDULING "
    print "==========================================="
    for Node in AG.nodes():
        print "NODE", Node,"CONTAINS THE FOLLOWING TASKS:",AG.node[Node]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.node[Node]['Scheduling']
    for Link in AG.edges():
        print "LINK", Link,"CONTAINS THE FOLLOWING TG's Edges:",AG.edge[Link[0]][Link[1]]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.edge[Link[0]][Link[1]]['Scheduling']

    return None

def GenerateGantCharts(TG,AG):

    NodeMakeSpanList=[]
    LinkMakeSpanList=[]
    for Node in AG.nodes():
        NodeMakeSpanList.append(FindLastAllocatedTimeOnNode(TG,AG,Node,False))
    for link in AG.edges():
        LinkMakeSpanList.append(FindLastAllocatedTimeOnLink(TG,AG,link,False))
    MAX_Time_Link = max(LinkMakeSpanList)
    MAX_Time_Node = max(NodeMakeSpanList)
    Max_Time = max(MAX_Time_Link,MAX_Time_Node)

    fig = plt.figure()
    NodeCounter = 0
    EdgeCounter = 0
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            NodeCounter += 1
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            EdgeCounter += 1
    Count = 1
    for Node in AG.nodes():
        PE_T = []
        PE_P = []
        PE_P.append(0)
        PE_T.append(0)
        if len(AG.node[Node]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NodeCounter+EdgeCounter + 1 ,1,Count)
            for Task in AG.node[Node]['MappedTasks']:
                    if Task in AG.node[Node]['Scheduling']:
                        StartTime=AG.node[Node]['Scheduling'][Task][0]
                        EndTime=AG.node[Node]['Scheduling'][Task][1]
                        PE_T.append(StartTime)
                        PE_P.append(0)
                        PE_T.append(StartTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0)
            PE_T.append(Max_Time)
            PE_P.append(0)
            ax1.fill_between(PE_T, PE_P, 0 , color='b', edgecolor='k')
            ax1.set_ylabel(r'PE'+str(Node), size=14, rotation=0)
            Count += 1
    # TODO: Fix the Links reports also...

    for Link in AG.edges():
        PE_T = []
        PE_P = []
        PE_P.append(0)
        PE_T.append(0)
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            ax1 = fig.add_subplot(EdgeCounter+EdgeCounter + 1,1,Count)
            for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                if AG.edge[Link[0]][Link[1]]['Scheduling']:
                        StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                        EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                        PE_T.append(StartTime)
                        PE_P.append(0)
                        PE_T.append(StartTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0)
            PE_T.append(Max_Time)
            PE_P.append(0)
            ax1.fill_between(PE_T, PE_P, 0 , color='r', edgecolor='k')
            ax1.set_ylabel(r'L'+str(Link), size=10, rotation=0)
            Count += 1
    # plot 1

    for ax in [ax1]:
        #ax.set_ylim(0,0.1)
        #ax.spines['right'].set_visible(False)
        #ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
    plt.show()
    return None