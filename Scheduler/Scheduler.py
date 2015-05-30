__author__ = 'siavoosh'

import copy
from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import Add_TG_TaskToNode
from Scheduling_Functions import Add_TG_EdgeTo_link


#Todo: move sub functions out of the file


def ScheduleAll(TG,AG,Report):
    print "\t\tSTARTING SCHEDULING PROCESS..."
    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    #first schedule the high critical tasks and their high critical transactions
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='H':
                    Node = TG.node[Task]['Node']
                    if Report:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,Task,Node,Report)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='H':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1

    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    #schedule the low critical transactions of high critical tasks
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='H':
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='L':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1
    #schedule low critical tasks and their transactions
    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='L':
                    Node = TG.node[Task]['Node']
                    if Report:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,Task,Node,Report)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                    Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1
    print "\t\tDONE SCHEDULING..."
    return None

