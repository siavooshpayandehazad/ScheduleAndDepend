# Copyright (C) 2015 Siavoosh Payandeh Azad


class CounterThreshold():

    def __init__(self, fault_threshold, health_threshold, intermittent_threshold):
        self.fault_counters = {}
        self.intermittent_counters = {}
        self.health_counters = {}

        self.fault_threshold = fault_threshold
        self.intermittent_threshold = intermittent_threshold
        self.health_threshold = health_threshold

        self.dead_components = []
        self.memory_counter = 0

    def increase_health_counter(self, location, logging):
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")

        if location in self.dead_components:
            return None
        if location not in self.fault_counters.keys():
            return None

        if location in self.health_counters.keys():
            self.health_counters[location] += 1
        else:
            self.health_counters[location] = 1
        logging.info("Increasing health counter at location: "+location +
                     " Counter: "+str(self.health_counters[location]))
        if self.health_counters[location] == self.health_threshold:
            logging.info("resetting component: "+location+" counters")
            self.reset_counters(location)

        current_memory_usage = self.return_allocated_memory()
        if current_memory_usage > self.memory_counter:
            self.memory_counter = current_memory_usage
        return None

    def increase_intermittent_counter(self):

        return None

    def increase_fault_counter(self, location, logging):
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")
        if location in self.dead_components:
            return None
        if location in self.fault_counters.keys():
            self.fault_counters[location] += 1
        else:
            self.fault_counters[location] = 1
        logging.info("Increasing counter at location: "+location+" Counter: "+str(self.fault_counters[location]))
        if self.fault_counters[location] == self.fault_threshold:
            logging.info("Declaring component: "+location+" dead!")
            self.dead_components.append(location)
            self.reset_counters(location)

        current_memory_usage = self.return_allocated_memory()
        if current_memory_usage > self.memory_counter:
            self.memory_counter = current_memory_usage
        return None

    def reset_counters(self, location):
        if location in self.fault_counters.keys():
            del self.fault_counters[location]
        else:
            pass
        if location in self.intermittent_counters.keys():
            del self.intermittent_counters[location]
        else:
            pass
        if location in self.health_counters.keys():
            del self.health_counters[location]
        else:
            pass
        return None

    def return_allocated_memory(self):
        return len(self.health_counters) + len(self.fault_counters)

    def report(self, number_of_nodes):
        print "==========================================="
        print "        COUNTER-THRESHOLD REPORT"
        print "==========================================="
        print "DEAD Components:", self.dead_components
        print "MAX MEMORY USAGE:", self.memory_counter
        print "AVERAGE COUNTER PER Node: ", float(self.memory_counter)/number_of_nodes
        return None