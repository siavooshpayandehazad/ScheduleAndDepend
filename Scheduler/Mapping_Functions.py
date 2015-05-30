
__author__ = 'siavoosh'
import statistics
from RoutingAlgorithms import Routing
import Scheduling_Functions

def AddClusterToNode(TG,CTG,AG,NoCRG,Cluster,Node,Report):
    print "\tADDING CLUSTER:",Cluster,"TO NODE:",Node
    CTG.node[Cluster]['Node'] = Node
    for Task in CTG.node[Cluster]['TaskList']:
        TG.node[Task]['Node'] = Node
        AG.node[Node]['MappedTasks'].append(Task)
    AG.node[Node]['Utilization']+=CTG.node[Cluster]['Utilization']
    for Edge in CTG.edges():
        if Cluster in Edge: # find all the edges that are connected to Cluster
            if Report:print "\t\tEDGE:",Edge,"CONTAINS CLUSTER:",Cluster
            SourceNode=CTG.node[Edge[0]]['Node']
            DestNode=CTG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None: #check if both ends of this edge is mapped
                if SourceNode != DestNode:
                    ListOfLinks=Routing.FindRouteInRouteGraph(NoCRG,SourceNode,DestNode) #Find the links to be used
                    ListOfEdges=[]
                    for edge in TG.edges(): #find all the edges in TaskGraph that contribute to this edge in CTG
                        if TG.node[edge[0]]['Cluster']== Edge[0] and TG.node[edge[1]]['Cluster']==Edge[1]:
                            ListOfEdges.append(edge)

                    #add edges from list of edges to all links from list of links
                    #Todo what if findRouteInRouteGRaph returns 2 routs??
                    if ListOfLinks is not None and len(ListOfEdges)>0:
                        if Report:print "\t\t\tADDING PATH FROM NODE:",SourceNode,"TO NODE",DestNode
                        if Report:print "\t\t\tLIST OF LINKS:",ListOfLinks
                        if Report:print "\t\t\tLIST OF EDGES:",ListOfEdges
                        for Link in ListOfLinks:
                            for Edge in ListOfEdges:
                                AG.edge[Link[0]][Link[1]]['MappedTasks'].append(Edge)
                                TG.edge[Edge[0]][Edge[1]]['Link'].append(Link)
                    else:
                        if Report:print "\t\033[33mWARNING\033[0m NOTHING TO BE MAPPED..."
                        return False
    return True

def RemoveClusterFromNode(TG,CTG,AG,NoCRG,Cluster,Node,Report):
    print "\tREMOVING CLUSTER:",Cluster,"FROM NODE:",Node
    for Edge in CTG.edges():
        if Cluster in Edge: # find all the edges that are connected to Cluster
            SourceNode=CTG.node[Edge[0]]['Node']
            DestNode=CTG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None: #check if both ends of this edge is mapped
                if SourceNode != DestNode:
                    ListOfLinks=Routing.FindRouteInRouteGraph(NoCRG,SourceNode,DestNode) #Find the links to be used
                    ListOfEdges=[]
                    for edge in TG.edges(): #find all the edges in TaskGraph that contribute to this edge in CTG
                        if TG.node[edge[0]]['Cluster']==Edge[0] and TG.node[edge[1]]['Cluster']==Edge[1]:
                            ListOfEdges.append(edge)
                    #remove edges from list of edges to all links from list of links
                    if ListOfLinks is not None and len(ListOfEdges)>0:
                        if Report:print "\t\t\tREMOVING PATH FROM NODE:",SourceNode,"TO NODE",DestNode
                        if Report:print "\t\t\tLIST OF LINKS:",ListOfLinks
                        if Report:print "\t\t\tLIST OF EDGES:",ListOfEdges
                        for Link in ListOfLinks:
                            for Edge in ListOfEdges:
                                if Edge in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                                    AG.edge[Link[0]][Link[1]]['MappedTasks'].remove(Edge)
                                    TG.edge[Edge[0]][Edge[1]]['Link'].remove(Link)
                    else:
                        print "\t\033[33mWARNING\033[0m NOTHING TO BE REMOVED..."
    CTG.node[Cluster]['Node'] = None
    for Task in CTG.node[Cluster]['TaskList']:
        TG.node[Task]['Node'] = None
        AG.node[Node]['MappedTasks'].remove(Task)
    AG.node[Node]['Utilization']-=CTG.node[Cluster]['Utilization']
    return True

def ReportMapping(AG):
    print "==========================================="
    print "      REPORTING MAPPING RESULT"
    print "==========================================="
    for Node in AG.nodes():
        print "NODE:",Node,"CONTAINS:",AG.node[Node]['MappedTasks']
    for link in AG.edges():
         print "LINK:",link,"CONTAINS:",AG.edge[link[0]][link[1]]['MappedTasks']
    return None

def ClearMapping(TG,CTG,AG):
    for node in TG.nodes():
        TG.node[node]['Node'] = None
    for Edge in TG.edges():
        TG.edge[Edge[0]][Edge[1]]['Link']=None
    for cluster in CTG.nodes():
        CTG.node[cluster]['Node'] = None
    for node in AG.nodes():
        AG.node[node]['MappedTasks'] = []
        AG.node[node]['Utilization'] = 0
        AG.node[node]['Scheduling'] ={}
    for link in AG.edges():
        AG.edge[link[0]][link[1]]['MappedTasks']=[]
        AG.edge[link[0]][link[1]]['Scheduling']={}
    return True

def CostFunction(TG,AG,Report):
    Cost=0
    NodeMakeSpanList=[]
    LinkMakeSpanList=[]
    for Node in AG.nodes():
        NodeMakeSpanList.append(Scheduling_Functions.FindLastAllocatedTimeOnNode(TG,AG,Node,False))
    for link in AG.edges():
        LinkMakeSpanList.append(Scheduling_Functions.FindLastAllocatedTimeOnLink(TG,AG,link,False))

    NodeMakeSpan_Stdev=statistics.stdev(NodeMakeSpanList)
    NodeMakeSpan_Max=max(NodeMakeSpanList)

    LinkMakeSpan_Stdev=statistics.stdev(LinkMakeSpanList)
    LinkMakeSpan_Max=max(LinkMakeSpanList)

    Cost= NodeMakeSpan_Max + NodeMakeSpan_Stdev + LinkMakeSpan_Stdev + LinkMakeSpan_Max
    if Report:
        print "NODES MAKE SPAN MAX:",NodeMakeSpan_Max
        print "NODES MAKE SPAN STANDARD DEVIATION:",NodeMakeSpan_Stdev
        print "LINKS MAKE SPAN MAX:",LinkMakeSpan_Max
        print "LINKS MAKE SPAN STANDARD DEVIATION:",LinkMakeSpan_Stdev
        print "MAPPING SCHEDULING COST:",Cost

    return Cost
