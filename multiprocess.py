import multiprocessing
import os

def execute(process):
    os.system(f'python -u -W ignore {process}')

# Creating the tuple of all the processes
numberOfThreads = int(os.environ['THREADS_NUMBER']) if int(
    os.environ['THREADS_NUMBER']) >= 1 else 1
processList = ()
listProcess = []
for i in range(0, numberOfThreads):
    listProcess.append("api.py")

processList = tuple(listProcess)

process_pool = multiprocessing.Pool(processes=numberOfThreads)
process_pool.map(execute, processList)