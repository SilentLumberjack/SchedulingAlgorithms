import random, csv
from operator import itemgetter

#implementation of SJF preemptive version (Shortest Job First) scheduling algorithm in Python
#for more information watch these https://www.youtube.com/watch?v=t0g9b3SJECg

def createRandomlyProcessesList(size:int):
    """ Returns a list of dictionaries
        where every dictionary is a single process with all necessary information.
        All values in the dictionary are set randomly """

    #maxBurstTime variable will be used to set an arrival time of the process
    #this value is not specified so you can change it, but I found the value of (20 * size) the most optimal
    
    maxBurstTime = 20 * size
    processesList = []
    processTemplate = {"Process ID": 0,
                      "Arrival Time": 0, 
                      "Burst Time": 0,
                      "Completion Time": 0,
                      "Turnaround Time": 0,
                      "Waiting Time": 0,
                      "Time Of Process Execution": 0}

    #here we fill up our list with randomly created processes and append it as a dictionary
    #I used copy() method because it returns another object with different id, and this is what I needed
    
    for i in range(size):
        processesList.append(processTemplate.copy())
        processesList[i]["Process ID"] = i + 1
        processesList[i]["Arrival Time"] = random.randint(0, maxBurstTime)
        processesList[i]["Burst Time"] =  random.randint(1, 20)
    
    return processesList


def createManuallyProcessesList():
    """ Returns the list of dictionaries
        where every dictionary is a single process with all necessary information.
        Values in the dictionary are set by user's input """
    
    numberOfProcesses = int(input("How many processes you want to create: "))
    processTemplate = {"Process ID": 0,
                      "Arrival Time": 0, 
                      "Burst Time": 0,
                      "Completion Time": 0,
                      "Turnaround Time": 0,
                      "Waiting Time": 0,
                      "Time Of Process Execution": 0}
    
    processesList = [processTemplate.copy() for i in range(numberOfProcesses)]
    
    #I ask only for two parameters because others will be calculated based on these two
    for process in range(numberOfProcesses):
        arrivalTime = int(input("P{proc} Enter arrival time:".format(proc=process + 1)))
        burstTime = int(input("P{proc} Enter burst time:".format(proc=process + 1)))
        
        processesList[process]["Arrival Time"] = arrivalTime
        processesList[process]["Burst Time"] = burstTime
        processesList[process]["Process ID"] = process + 1
    
    return processesList


def getAverageValuesOfProcesses(processesList:list):
    """ Returns a tuple with average waiting time and average turnaround time of taken processes """

    #Logic of this function is to store all the processes in processesList and to sort this list by process arrival time
    #then, when process arrives (according to currentTimeCPU) we add it to arrivedProcessesList, where we will store all the processes that arrived and are ready for execution
    #we will sort arrivedProcessesList by burst time of process to always execute the shortest one (main idea of SJF algorithm)
    #we will update all the information about single process in arrivedProcessesList and when process with shortest burst time will be executed, we will delete 
    #this process from arrivedProcessesList and update it's data in out main processesList

    currentTimeCPU = 0
    performedProcesses = 0
    arrivedProcessesCounter = 0
    arrivedProcessesList = []
    
    averageWaitingTime = 0
    averageTurnaroundTime = 0
    
    #I used lambda function to sort dictionaries by arrival time for easier processing 
    processesList = sorted(processesList, key = lambda i: i["Arrival Time"])

    #if shortest process that is ready for execution (already stored in arrivedProcessesList) will finish his execution by arrival of the next process 
    #we can execut it and delete from arrivedProcessesList, as it is already done 

    #in other case, if arrival time of next process will be in less time than out currently shortest process will need for it's execution
    #wi will execute only part of it and will stop at the moment when next process will arrive, then we will add new arrived process to arrivedProcessesList and again will find the shortest
    
    while performedProcesses != len(processesList):
        if not arrivedProcessesList:
            currentTimeCPU = processesList[arrivedProcessesCounter]["Arrival Time"]

            nextProcessArrivalTime = processesList[arrivedProcessesCounter]["Arrival Time"]
            arrivedProcessesList.append(processesList[arrivedProcessesCounter].copy())
            arrivedProcessesCounter += 1

            #after adding next by arrival time process we should sheck if there are more processes with same arrival time and add them
            while (arrivedProcessesCounter < len(processesList)) and ((processesList[arrivedProcessesCounter]["Arrival Time"] == nextProcessArrivalTime)):
                arrivedProcessesList.append(processesList[arrivedProcessesCounter].copy())
                arrivedProcessesCounter += 1

        #arrivedProcessesList = sorted(arrivedProcessesList, key=itemgetter('Burst Time', 'Waiting Time'))
        arrivedProcessesList = sorted(arrivedProcessesList, key=lambda k: (k["Burst Time"], -k["Waiting Time"]))

            
        if (arrivedProcessesCounter == len(processesList)) or  (processesList[arrivedProcessesCounter]["Arrival Time"] > (arrivedProcessesList[0]["Burst Time"] + currentTimeCPU)):

            arrivedProcessesList[0]["Waiting Time"] = (
                currentTimeCPU - arrivedProcessesList[0]["Arrival Time"] - arrivedProcessesList[0]["Time Of Process Execution"])

            currentTimeCPU += arrivedProcessesList[0]["Burst Time"]

            arrivedProcessesList[0]["Completion Time"] = currentTimeCPU

            arrivedProcessesList[0]["Turnaround Time"] = (
                arrivedProcessesList[0]["Completion Time"] - arrivedProcessesList[0]["Arrival Time"])

            averageWaitingTime += arrivedProcessesList[0]["Waiting Time"]
            averageTurnaroundTime += arrivedProcessesList[0]["Turnaround Time"]

            for process in range(len(processesList)):
                if processesList[process]["Process ID"] == arrivedProcessesList[0]["Process ID"]:
                    processesList[process] = arrivedProcessesList[0].copy()
                    break

            for process in range(1, len(arrivedProcessesList)):
                arrivedProcessesList[process]["Waiting Time"] += arrivedProcessesList[0]["Burst Time"]
                
            del arrivedProcessesList[0]
            performedProcesses += 1
        else:
            for process in range(1, len(arrivedProcessesList)):
                arrivedProcessesList[process]["Waiting Time"] += (processesList[arrivedProcessesCounter]["Arrival Time"] - currentTimeCPU)

            arrivedProcessesList[0]["Time Of Process Execution"] += (processesList[arrivedProcessesCounter]["Arrival Time"] - currentTimeCPU)
            arrivedProcessesList[0]["Burst Time"] -= (processesList[arrivedProcessesCounter]["Arrival Time"] - currentTimeCPU)

            currentTimeCPU = processesList[arrivedProcessesCounter]["Arrival Time"]

            arrivedProcessesList.append(processesList[arrivedProcessesCounter])
            arrivedProcessesCounter += 1


    averageWaitingTime /= len(processesList)
    averageTurnaroundTime /= len(processesList)

    return (averageWaitingTime, averageTurnaroundTime)

def writeProcessesDataToCSVfile(processesList:list, fileName:str="processesDataSJF.csv"):
    """ Writes down all the information about single process to a CSV file given as argument, if file wasn't given as argument - 
    creates new CSV file named 'processesDataSJF.scv' and writes down information to it """

    CSVcolumns = ["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time", "Time Of Process Execution"]

    try:
        with open(fileName, "w+") as f:
            writer = csv.DictWriter(f, fieldnames=CSVcolumns)
            writer.writeheader()
            for process in processesList:
                writer.writerow(process)
                
        print("Successfully written to", fileName)
    except IOError:
        print("Input/Output error!") 

def readProcessesDataFromCSVfile(fileName:str):
    """ Reads information about processes from CSV file. Returns a list where every single process is a dictionary. """ 

    try:
        with open(fileName, "r") as f:
            processesList = [{key: int(value) if value.isdigit() else float(value) for key, value in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
            print("Successfully read from", fileName)

            return processesList
    except IOError:
        print("Input/Output error!")

if __name__ == "__main__":

    #here I test SJF algorithm on 100 different lists of processes, then I write all processes data to CSV file named 'processesDataSJF.scv'
    #you can read this file and get list of processes thet are stored in this file using function readProcessesDaraFtromCSVfile (you need to pass file name as argument)

    averageWaitingTime = 0
    averageTurnaroundTime = 0
    timesToRepeat = 100
    operationsInOneList = 100
    allTestedProcessesList = []

    for i in range(timesToRepeat):
        processesList = createRandomlyProcessesList(operationsInOneList)
        allTestedProcessesList += processesList
        result = getAverageValuesOfProcesses(processesList)

        averageWaitingTime += result[0]
        averageTurnaroundTime += result[1]
        

    writeProcessesDataToCSVfile(allTestedProcessesList)

    averageWaitingTime /= timesToRepeat
    averageTurnaroundTime /= timesToRepeat
    print("from 100 different lists of 100 operations in every we get: ")
    print("Average Waiting Time =", averageWaitingTime)
    print("Average Turnaround Time =", averageTurnaroundTime)


    




