__author__ = 'siavoosh'
import Config,Scheduler,Mapping_Functions
from Clusterer import Clustering_Functions,Clustering
from Mapping_Heuristics import MinMin_MaxMin,Local_Search
from Scheduler import Scheduling_Functions,Scheduler
import copy

def Mapping (TG,AG,NoCRG,SHM,logging):
    if Config.Mapping_Function=='MinMin':
        if Config.TG_Type=='RandomIndependent':
            return MinMin_MaxMin.Min_Min_Mapping (TG,AG,NoCRG,SHM,logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='MaxMin':
        if Config.TG_Type=='RandomIndependent':
            return MinMin_MaxMin.Max_Min_Mapping (TG,AG,NoCRG,SHM,logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='LocalSearch' or Config.Mapping_Function=='IterativeLocalSearch':
        if Config.TG_Type!='RandomDependent':
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
    # clustered task graph
        CTG=copy.deepcopy(Clustering.TaskClusterGeneration(len(AG.nodes())))
        if Clustering.InitialClustering(TG, CTG):
            # Clustered Task Graph Optimization
            (BestClustering,BestTaskGraph)= Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000)
            TG= copy.deepcopy(BestTaskGraph)
            CTG= copy.deepcopy(BestClustering)
            del BestClustering, BestTaskGraph
            Clustering_Functions.DoubleCheckCTG(TG,CTG)
            Clustering_Functions.ReportCTG(CTG,"CTG_PostOpt.png")
            # Mapping CTG on AG
            if Mapping_Functions.MakeInitialMapping(TG,CTG,AG,SHM,NoCRG,True,logging):
                Mapping_Functions.ReportMapping(AG)
                # Schedule all tasks
                Scheduler.ScheduleAll(TG,AG,SHM,Config.DebugInfo,Config.DebugDetails)
                Scheduling_Functions.ReportMappedTasks(AG)
                Mapping_Functions.CostFunction(TG,AG,Config.DebugInfo)
                if Config.Mapping_Function=='LocalSearch':
                    (BestTG,BestCTG,BestAG)=Local_Search.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                                Config.LocalSearchIteration,
                                                                                Config.DebugInfo,Config.DebugDetails,
                                                                                logging)
                    TG= copy.deepcopy(BestTG)
                    AG= copy.deepcopy(BestAG)
                    del BestTG,BestCTG,BestAG
                elif Config.Mapping_Function=='IterativeLocalSearch':
                    (BestTG,BestCTG,BestAG)=Local_Search.OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                                        Config.IterativeLocalSearchIterations,
                                                                                        Config.LocalSearchIteration,
                                                                                        Config.DebugInfo,
                                                                                        Config.DebugDetails,
                                                                                        logging)
                    TG= copy.deepcopy(BestTG)
                    AG= copy.deepcopy(BestAG)
                    del BestTG,BestCTG,BestAG
                Scheduling_Functions.ReportMappedTasks(AG)
                Mapping_Functions.CostFunction(TG,AG,True)
                return TG,AG
            else:
                print "Initial Mapping Failed...."
                Mapping_Functions.ReportMapping(AG)
                print "==========================================="
                return None, None
        else :
            print "Initial Clustering Failed...."
            return None, None
    elif Config.Mapping_Function=='SimulatedAnnealing':
        None