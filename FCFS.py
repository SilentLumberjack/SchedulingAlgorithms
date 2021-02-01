import random, csv

#implementation of FCFS (First Come First Serve) scheduling algorithm in Python
#for more information watch these https://www.youtube.com/watch?v=VSMAjMfJ6KQ&t=774s

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
                      "Waiting Time": 0}

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
                      "Waiting Time": 0}
    
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

    #logic of this function is to sort all the processes by arrival time and execute them one-by-one
    #we will calculate all necessary data for each process in for loop
    
    currentTimeCPU = 0
    averageWaitingTime = 0
    averageTurnaroundTime = 0
    
    #I used lambda function to sort dictionaries by arrival time for easier processing 
    processesList = sorted(processesList, key = lambda i: i["Arrival Time"])
    
    for process in range(len(processesList)):
        if processesList[process]["Arrival Time"] > currentTimeCPU:
            currentTimeCPU = (processesList[process]["Arrival Time"] + processesList[process]["Burst Time"])
        else:
            currentTimeCPU += processesList[process]["Burst Time"]

        processesList[process]["Completion Time"] = currentTimeCPU
        
        processesList[process]["Turnaround Time"] = (
            processesList[process]["Completion Time"] - processesList[process]["Arrival Time"])

        processesList[process]["Waiting Time"] = (
            processesList[process]["Turnaround Time"] - processesList[process]["Burst Time"])

        averageWaitingTime += processesList[process]["Waiting Time"]
        averageTurnaroundTime += processesList[process]["Turnaround Time"]

    try:
        averageWaitingTime /= len(processesList)
        averageTurnaroundTime /= len(processesList)
    except ZeroDivisionError:
        print("There are no processes to process!")

    return (averageWaitingTime, averageTurnaroundTime)

def writeProcessesDataToCSVfile(processesList:list, fileName:str="processesDataFCFS.csv"):
    """ Writes down all the information about single process to a CSV file given as argument, if file wasn't given as argument - 
    creates new CSV file named 'processesDataFCFS.scv' and writes down information to it """
    CSVcolumns = ["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]
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

    #here I test FCFS algorithm on 100 different lists of processes, then I write all processes data to CSV file named "processesDataFCFS.csv'
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

    
    