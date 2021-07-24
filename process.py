#The two threads can be seen in line 158, threads for getAverageWaitTime() and getAverageTurnaroundTime() were created and also started

import threading
import time

class ProcessSimulation:
    
    def Process(self, NumberOfProcess):
        processList = []
        for i in range(NumberOfProcess):
            initQueue = []
            
            processId = int(input('Pls, input the process ID: '))
            priority = int(input("Pls, Enter the priority for process {}: ".format(processId)))#Priority of the process
            arrivalTime = int(input("Pls, Enter Arrival Time for Process {}: ".format(processId)))#Time it arrives
            processTime = int(input("Pls, Enter process Time for Process {}: ".format(processId)))#Time for the process to be completed
            initQueue.extend([processId, priority, arrivalTime, processTime, 0]) #Add the process and its detail to the end of the list
            
            processList.append(initQueue) #Now add the list of that process to the "processList"
         
        quantumTime = int(input('Enter the Quantum Time: '))

        ProcessSimulation.Scheduler(self, processList, quantumTime)
    def Scheduler(self, processList, quantumTime):
        processList.sort(key = lambda s:s[2]) #Now lets sort the process in the processList according to its arrivaltime
        readyList = [] #Processes that have been admitted but not yet running will wait in this queue
        runningList = [] #Processes that are executing will run in this queue
        arriveInit = 0 #We use this to compare with the arrival time to know which gets in the ready queue
        
        commenceTIme = [] #keeps the time each process starts at each time the process runs
        exitTime = [] #Keeps the time each process ends due to the expiration of its quantum time

        while 1:
            standardList = []
            initList = [] #to hold the process detail before we append to either the runningList or readyList
        
            for i in range(len(processList)):
                if processList[i][2] <= arriveInit and processList[i][4] == 0: #if the process is less than or equal to arriveinit and it
                    #is neww that it means it is not in the readylist, so we set ready to 0
                    ready = 0
                    if len(readyList) != 0: #Now we check if it is already in the ready queue if it is in we set ready to 1
                        for j in range(len(readyList)):
                            if processList[i][0] == readyList[j][0]:
                                ready = 1

                    if ready == 0: #if it is not in the readyList we can add it in
                        initList.extend([processList[i][0], processList[i][1], processList[i][2], processList[i][3], processList[i][4]])
                        readyList.append(initList)
                        initList = []
                        time.sleep(2)
                        
                        print('Process {} is now in the ready state'.format(processList[i][0]))

                    if len(readyList) != 0 and len(runningList) != 0: #if the readyList and runningList are not empty
                        for j in range(len(readyList)): #iterate through the readyList
                            if readyList[j][0] == runningList[len(runningList) - 1]:
                                readyList.insert((len(readyList) - 1), readyList.pop(j))

                elif processList[i][4] == 0: #if the process is new
                    initList.extend([processList[i][0], processList[i][1], processList[i][2], processList[i][3], processList[i][4]])
                    standardList.append(initList)
                    initList = []

            if len(readyList) == 0 and len(standardList) == 0: #That means we have no process left for execution, then we break
                break

            if len(readyList) != 0:
                readyList.sort(key = lambda s:s[1]) #Now we sort according to priority, the higher priority runs first

                if readyList[0][3] > quantumTime: #if the quantum time is less than the process time, the process wint be able to finish in that
                    #quantum time
                    commenceTIme.append(arriveInit) #append to the list the time this process starta
                    arriveInit = arriveInit + quantumTime #Now we add the quantumTime to the arriveInit, this shows the next time after the 
                    #current process quantum time is over
                    exitInit = arriveInit
                    exitTime.append(exitInit)#Now the time the process ends due to the expiration of its quantum number
                    #Now we have done those calculation, we can append to the running queue
                    runningList.append(readyList[0][0])
                    time.sleep(2)
                    print("process {} is now running".format(readyList[0][0]))

                    for j in range(len(processList)):
                        if processList[j][0] == readyList[0][0]:
                            break

                    processList[j][3] = processList[j][3] - quantumTime #Now we update the remaining process time, we minus the process time 
                    #from the quantum time
                    readyList.pop(0)
                    time.sleep(3)
                    
                    print("process {}'s quantum number is expired and now returns to the ready state with a remaining process time of {}".format(processList[j][0], processList[j][3]))

                elif readyList[0][3]<=quantumTime : #if the quantum number is greater or same as the process time then the process can be completed in on execution
                    commenceTIme.append(arriveInit)
                    arriveInit = arriveInit + readyList[0][3] #Since the quantum number is more we just add to the process time
                    exitInit = arriveInit
                    exitTime.append(exitInit) #Now we added the time the process finished to the exitTime list
                    #now the process can be appended to the runningList
                    runningList.append(readyList[0][0])
                    
                    print("process {} is now running".format(readyList[0][0]))

                    for j in range(len(processList)):
                        if processList[j][0] == readyList[0][0]:
                            break

                    #since this process is completed we set the status to Terminated and the remaining process time to 0
                    processList[j][4] = 1
                    processList[j][3] = 0
                    processList[j].append(exitInit) #Now we append the time the process completed to the processList[j]
                    readyList.pop(0)
                    time.sleep(3)
                    
                    print("process {} has finished executing and has been Terminated".format(processList[j][0]))

                elif len(readyList) == 0:
                    if arriveInit < standardList[0][2]:
                        arriveInit = standardList[0][2]

                    if standardList[0][3] > quantumTime:
                        commenceTIme.append(arriveInit) #append to the list the time this process starta
                        arriveInit = arriveInit + quantumTime #Now we add the quantumTime to the arriveInit, this shows the next time after the 
                        #current process quantum time is over
                        exitInit = arriveInit
                        exitTime.append(exitInit)#Now the time the process ends due to the expiration of its quantum number
                        #Now we have done those calculation, we can append to the running queue
                        runningList.append(standardList[0][0])
                        
                        print("process {} is now running".format(standardList[0][0]))

                        for j in range(len(processList)):
                            if processList[j][0] == standardList[0][0]:
                                break

                        processList[j][3] = processList[j][3] - quantumTime #Now we update the remaining process time, we minus the process time 
                        #from the quantum time
                        print("process {}'s quantum number is expired and now returns to the ready state with a remaining process time of {}".format(processList[j][0], processList[j][3]))

                        
                    elif standardList[0][3] <= quantumTime:
                        commenceTIme.append(arriveInit)
                        arriveInit = arriveInit + standardList[0][3] #Since the quantum number is more we just add to the process time
                        exitInit = arriveInit
                        exitTime.append(exitInit) #Now we added the time the process finished to the exitTime list
                        #now the process can be appended to the runningList
                        runningList.append(standardList[0][0])
                        
                        print("process {} is now running".format(standardList[0][0]))

                        for j in range(len(processList)):
                            if processList[j][0] == standardList[0][0]:
                                break
                        #since this process is completed we set the status to Terminated and the remaining process time to 0
                        processList[j][4] = 1
                        processList[j][3] = 0
                        processList[j].append(exitInit) #Now we append the time the process completed to the processList[j]
                        print("process {} has finished executing and has been Terminated".format(processList[j][0]))
        #Create two threads           
        turnAround = threading.Thread(target = ProcessSimulation.GetAverageTurnaroundTime, args = (self, processList,))
        waitingTime = threading.Thread(target = ProcessSimulation.GetAverageWaitingTime, args = (self, processList,))
        #start the two threads
        print("The threads have started")
        turnAround.start()
        time.sleep(2)
        waitingTime.start()

        #To find the total turn around time, we minus the completion time from the arrival time and add to the total turn around time
    def GetAverageTurnaroundTime(self, processList):
        total_tat_time = 0
        for i in range(len(processList)):
            tat_time = processList[i][5] - processList[i][1]
            total_tat_time = total_tat_time + tat_time
            processList[i].append(tat_time)
        average_tat_time = total_tat_time / len(processList)
        print()
        print("Thread 1 has started")
        print (f'The average turnaround time is: {average_tat_time}')
        print("This is just used to showcase the average time between the process getting into the waiting state and its completion.")
        print("Thread 1 has ended")
                        
            
            
    def GetAverageWaitingTime(self, processList):
        total_w_time = 0
        for i in range(len(processList)):
            w_time = processList[i][6] - processList[i][4]
            total_w_time = total_w_time + w_time
            processList[i].append(w_time)
        average_w_time = total_w_time / len(processList)
        print("Thread 2 has started")
        print (f'The average wait time is: {average_w_time}')
        print("This is just used to showcase the average time the process waits in the ready state for CPU.")
        print("Thread 2 has ended")

        
        

        
                        
if __name__ == "__main__":
    NumberOfProcess = int(input("How many processes are you trying to execute: "))
    ps = ProcessSimulation()
    ps.Process(NumberOfProcess)
