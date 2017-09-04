# Copyright (C) 2015 Siavoosh Payandeh Azad  and Thilo Kogge

import copy
import itertools
from random import shuffle, sample
from functools import partial
from multiprocessing import Pool
from statistics import stdev
from scipy.misc import comb
from ConfigAndPackages import PackageFile, Config, all_2d_turn_model_package
from ArchGraphUtilities import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms.Routing_Functions import extended_degree_of_adaptiveness, degree_of_adaptiveness, \
    check_deadlock_freeness, return_turn_model_name
from RoutingAlgorithms.Calculate_Reachability import reachability_metric
from RoutingAlgorithms.turn_model_evaluation.turn_model_viz import viz_all_turn_models_against_each_other
from RoutingAlgorithms.turn_model_evaluation.turn_model_viz import viz_turn_model_evaluation


def enumerate_all_2d_turn_models_based_on_df(combination):
    """
    Lists all 2D deadlock free turn models in "deadlock_free_turns" in "Generated_Files"
    folder!
    ---------------------
        We have 256 turns in 2D Mesh NoC!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_2D_turn_models_'+str(combination)+'.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'NonMinimalPath'

    ag = copy.deepcopy(AG_Functions.generate_ag())
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_2D)

    deadlock_free_counter = 0
    deadlock_counter = 0
    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        turns_health = copy.deepcopy(turns_health_2d_network)
        for turn in turns:
            turns_health[turn] = True
        counter += 1
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
        if check_deadlock_freeness(noc_rg):
            connectivity_metric = reachability_metric(ag, noc_rg, False)
            doa = degree_of_adaptiveness(ag, noc_rg, False)
            doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)
            deadlock_free_counter += 1
            # print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric) +
                                 "\t\t"+str(doa)+"\t\t"+str(doa_ex)+"\n")
        else:
            deadlock_counter += 1
            # print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
            all_turns_file.write(str(counter)+"\t\tDL\t"+str(list(turns))+"\t\t-----"+"\t\t-----"+"\t\t-----"+"\n")
        del shmu
        del noc_rg
    all_turns_file.write("---------------------------"+"\n")
    all_turns_file.write("Number of turn models with deadlock: "+str(deadlock_counter)+"\n")
    all_turns_file.write("Number of turn models without deadlock: "+str(deadlock_free_counter)+"\n")
    all_turns_file.write("=========================================="+"\n")
    all_turns_file.close()
    return None


def enumerate_all_3d_turn_models_based_on_df(combination):
    """
    Lists all 3D deadlock free turn models in "deadlock_free_turns" in "Generated_Files"
    folder!
    ---------------------
        We have 16,777,216 turns in 3D Mesh NoC! if it takes one second to calculate
        deadlock freeness Then it takes almost 194.2 Days (almost 6.4 Months) to
        check all of them. that is the reason we need to make this parallel!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_3D_turn_models_'+str(combination)+'.txt', 'w')
    turns_health_3d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False,
                               "N2U": False, "N2D": False, "S2U": False, "S2D": False,
                               "W2U": False, "W2D": False, "E2U": False, "E2D": False,
                               "U2W": False, "U2E": False, "U2N": False, "U2S": False,
                               "D2W": False, "D2E": False, "D2N": False, "D2S": False}
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 3

    ag = copy.deepcopy(AG_Functions.generate_ag())
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    deadlock_free_counter = 0
    deadlock_counter = 0
    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        turns_health = copy.deepcopy(turns_health_3d_network)
        for turn in turns:
            turns_health[turn] = True
        counter += 1
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
        if check_deadlock_freeness(noc_rg):
            connectivity_metric = reachability_metric(ag, noc_rg, False)
            doa = degree_of_adaptiveness(ag, noc_rg, False)
            deadlock_free_counter += 1
            # print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric) +
                                 "\t\t"+str(doa)+"\n")
        else:
            deadlock_counter += 1
            # print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
            all_turns_file.write(str(counter)+"\t\tDL\t"+str(list(turns))+"\t\t-----""\n")
        del shmu
        del noc_rg
    all_turns_file.write("---------------------------"+"\n")
    all_turns_file.write("Number of turn models with deadlock: "+str(deadlock_counter)+"\n")
    all_turns_file.write("Number of turn models without deadlock: "+str(deadlock_free_counter)+"\n")
    all_turns_file.write("=========================================="+"\n")
    all_turns_file.close()
    return None


def enumerate_all_3d_turn_models(combination):
    """
    Lists all 3D deadlock free turn models in "deadlock_free_turns"
    ---------------------
        We have 16,777,216 turns in 3D Mesh NoC!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 3
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_3D_turn_models_'+str(combination)+'.txt', 'w')

    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        # print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
    return None


def enumerate_all_odd_even_turn_models():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/all_odd_evens.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_list = []
    #todo: we can change this to exhaustive list! (this is currently 2D deadlock free turn models!)
    for length in range(0, len(turns_health_2d_network.keys())):
        for item in list(itertools.combinations(turns_health_2d_network.keys(), length)):
            if len(item)>0:
                turn_model_list.append(list(item))

    counter = 0
    for turn_model_odd in turn_model_list:
        for turn_model_even in turn_model_list:
            if turn_model_even != turn_model_odd:   # taking out the uniform cases!

                turns_health = copy.deepcopy(turns_health_2d_network)
                shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
                shmu.setup_noc_shm(ag, turns_health, False)
                noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

                for node in ag.nodes():
                    node_x, node_y, node_z = AG_Functions.return_node_location(node)
                    if node_x % 2 == 1:
                        for turn in turn_model_odd:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                    else:
                        for turn in turn_model_even:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                if check_deadlock_freeness(noc_rg):
                    if reachability_metric(ag, noc_rg, False) == number_of_pairs:
                        print "deadlock free, fully connected routing found:", turn_model_odd, turn_model_even
                        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
                        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)

                        all_odd_evens_file.write('%5s' % str(counter)+"  | even turn model:"+'%51s' % str(turn_model_even)+"\t|\n")
                        all_odd_evens_file.write("       | odd turn model: "+'%51s' % str(turn_model_odd)+" \t|")

                        all_odd_evens_file.write(" DoA:" + str("%.2f" %doa)+"\tDoAx:" + str("%.2f" %doa_ex)+"\n")
                        all_odd_evens_file.write("-----------------------------------"*3+"\n")
                        #SHMU_Reports.draw_shm(shmu.SHM)
                        #draw_rg(noc_rg)
                        counter += 1

    all_odd_evens_file.close()
    return None


def enumerate_all_2d_turn_models(combination):
    """
    Lists all 2D deadlock free turn models in "deadlock_free_turns"
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_2D_turn_models_'+str(combination)+'.txt', 'w')
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_2D)

    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        # print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
    return None


def check_fault_tolerance_of_routing_algs(dimension, number_of_multi_threads, viz):
    """
    runs appropriate functions for checking fault tolerance of the network according to the topology,
    on number_of_multi_threads parallel threads
    :param dimension: defines the topology of the network, either "2D" or "3D"
    :param number_of_multi_threads: number of threads for running the program
    :param viz: boolean, if True, generates visualization of convergence of the connectivity metirc
    :return: False if the Dimension is wrong, other wise True
    """
    if dimension == '2D':
        Config.ag.topology = '2DMesh'
        Config.ag.z_size = 1
        args = list(range(0, 25))
        turn_model_list = all_2d_turn_model_package.all_2d_turn_models
    elif dimension == '3D':
        Config.ag.topology = '3DMesh'
        Config.ag.z_size = 3
        args = list(range(0, 108, 4))
        turn_model_list = PackageFile.routing_alg_list_3d
    else:
        print "Please choose a valid dimension!"
        return False
    for turn_model in turn_model_list:
        if dimension == '2D':
            p = Pool(number_of_multi_threads)
            function = partial(report_2d_turn_model_fault_tolerance, turn_model, viz)
            p.map(function, args)
            p.terminate()
        elif dimension == '3D':
            p = Pool(number_of_multi_threads)
            function = partial(report_3d_turn_model_fault_tolerance, turn_model, viz)
            p.map(function, args)
            p.terminate()
    if viz:
        for turn_model in turn_model_list:
            for arg in args:
                turn_model_name = return_turn_model_name(turn_model)
                file_name = None
                if dimension == '2D':
                    file_name = str(turn_model_name) + "_eval_" + str(24-arg)
                elif dimension == '3D':
                    file_name = str(turn_model_name) + "_eval_" + str(108-arg)
                viz_turn_model_evaluation(file_name)
    if dimension == '2D':
        viz_all_turn_models_against_each_other()
    return True


def report_2d_turn_model_fault_tolerance(turn_model, viz, combination):
    """
    generates 2D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param turn_model: list of allowed turns for generating the routing graph
    :param viz: if true, generates the visualization files
    :param combination: number of links to be present in the network
    :return: None
    """
    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
    else:
        turn_model_eval_viz_file = None
    counter = 0
    metric_sum = 0

    sub_ag_list = list(itertools.combinations(ag.edges(), combination))
    shuffle(sub_ag_list)

    list_of_avg = []
    for sub_ag in sub_ag_list:
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, copy.deepcopy(Config.TurnsHealth), False)
        for link in list(sub_ag):
            shmu.break_link(link, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                False,  False))
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        # std = None
        list_of_avg.append(float(metric_sum)/counter)
        if len(list_of_avg) > 5000:
            list_of_avg.pop(0)
            std = stdev(list_of_avg)
            if std < 0.009:
                # turn_model_eval_file.write("STD of the last 5000 average samples is bellow 0.009\n")
                # turn_model_eval_file.write("Terminating the search!\n")
                del shmu
                del noc_rg
                break
        if viz:
            turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")
        # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
        #     float(metric_sum)/counter, "\t\tstd:", std
        del shmu
        del noc_rg

    if counter > 0:
        avg_connectivity = float(metric_sum)/counter
    else:
        avg_connectivity = 0
    turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
    if viz:
        turn_model_eval_viz_file.close()
    turn_model_eval_file.close()
    return None


def report_3d_turn_model_fault_tolerance(turn_model, viz, combination):
    """
    generates 3D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param turn_model: list of allowed turns for generating the routing graph
    :param combination: number of links to be present in the network
    :param viz: if true, generates the visualization files
    :return: None
    """
    if combination == 108:
        raise ValueError("breaking 108 edges out of 108 edges is not possible your connectivity is 0!")

    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
    else:
        turn_model_eval_viz_file = None
    counter = 0
    metric_sum = 0

    list_of_avg = []
    number_of_combinations = comb(108, combination)
    while True:
        sub_ag = sample(ag.edges(), combination)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, copy.deepcopy(Config.TurnsHealth), False)
        for link in list(sub_ag):
            shmu.break_link(link, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                False,  False))
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        # std = None
        list_of_avg.append(float(metric_sum)/counter)
        if len(list_of_avg) > 5000:
            list_of_avg.pop(0)
            std = stdev(list_of_avg)
            if std < 0.009:
                # turn_model_eval_file.write("STD of the last 5000 average samples is bellow 0.009\n")
                # turn_model_eval_file.write("Terminating the search!\n")
                del shmu
                del noc_rg
                break
        if viz:
            turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")

        if counter >= number_of_combinations:
            del shmu
            del noc_rg
            break

        # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
        #    float(metric_sum)/counter, "\t\tstd:", std
        del shmu
        del noc_rg

    if counter > 0:
        avg_connectivity = float(metric_sum)/counter
    else:
        avg_connectivity = 0
    turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
    turn_model_eval_file.close()
    if viz:
        turn_model_eval_viz_file.close()
    return None
