#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():

    trafficLightIDlist = []
    laneLists=[]
    edgelists=[]
    averageList=[]

    trafficLightIDlist=traci.trafficlight.getIDList()

    for i in range(len(trafficLightIDlist)):
        laneLists.append([])
        laneLists[i]=traci.trafficlight.getControlledLanes(trafficLightIDlist[i])


    for i in range(len(laneLists)):
        edgelists.append([])
        for j in range(len(laneLists[i])):
            edgelists[i].append(traci.lane.getEdgeID(laneLists[i][j]))

    for i in range(len(edgelists)):
        edgelists[i]=list(set(edgelists[i]))


    #print(edgelists)
    while traci.simulation.getMinExpectedNumber() > 0:
       waitingTimeList =[]
       averageList=[]
       traci.simulationStep()
       for i in range(len(edgelists)):
           waitingTimeList.append([])
           for j in range(len(edgelists[i])):
               waitingTimeList[i].append(traci.edge.getWaitingTime(edgelists[i][j]))
               averageList.append(sum(waitingTimeList[i])/len(waitingTimeList[i]))
       average=sum(averageList)/len(averageList)
       print(average)


    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "new-network.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()