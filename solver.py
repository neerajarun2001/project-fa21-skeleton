from parse import read_input_file, write_output_file
import os
from functools import cmp_to_key

def knap(cap, tasks):
    max_duration = 60
    max_benefit = 100
    #print([t.get_max_benefit() for t in tasks])
    tasks.sort(key=lambda t: (t.get_max_benefit() / max_benefit + (1 - t.get_duration() / max_duration) + (1 - t.get_deadline() / cap)), reverse=True)
    #print([t.get_max_benefit() for t in tasks])


    t_quantity = len(tasks)
    P = [[0 for x in range(cap+1)] for x in range(t_quantity)]
    T = [[[] for x in range(cap+1)] for x in range(t_quantity)]
    t_durations = [t.get_duration() for t in tasks]

    for i in range(t_quantity):
        for d in range(cap+1):
            if i == 0 or d == 0:
                P[i][d] = 0
            elif t_durations[i] <= cap:
                elapsed_time = sum([t.get_duration() for t in T[i-1][d]])
                v_i = tasks[i].calc_benefit_from_now(elapsed_time)
                max_with_t = P[i-1][d-tasks[i].get_duration()]
                max_prev = P[i-1][d]
                if v_i + max_with_t > max_prev and elapsed_time + tasks[i].get_duration() <= cap:
                    P[i][d] = v_i + max_with_t
                    # try:
                    T[i][d] = T[i-1][d]
                    T[i][d].append(tasks[i])
                    #except IndexError:
                    #    print(i, d, len(T), len(T[0]), len(tasks))
                else:
                    P[i][d] = max_prev
                    T[i][d] = T[i-1][d]
            else:
                P[i][d] = P[i-1][d]

    ret = T[t_quantity-1][cap]
    return [t.get_task_id() for t in ret]



def jobcomparator(task1, task2):
    return task1.get_deadline() - task2.get_deadline()

def findLastNonConflictingJob(tasks, n):
    # search space
    (low, high) = (0, n)
 
    # iterate till the search space is exhausted
    while low <= high:
        mid = (low + high) // 2
        if tasks[mid].get_deadline() <= tasks[n].calc_start():
            if tasks[mid + 1].get_deadline() <= tasks[n].calc_start():
                low = mid + 1
            else:
                return mid
        else:
            high = mid - 1
 
    # return the negative index if no non-conflicting job is found
    return -1

def weightedjobsequencing(tasks):
    output = []

    # base case
    if not tasks:
        return 0
 
    # sort tasks in increasing order of their deadlines
    tasks.sort(key=lambda task: task.get_deadline())
 
    # get the number of tasks
    num_tasks = len(tasks)
 
    # `maxProfit[i]` stores the maximum benefit possible for the first `i` tasks, and
    # `tasks[i]` stores the index of tasks involved in the maximum benefit
    maxBenefit = [None] * num_tasks
    maxTasks = [[] for _ in range(num_tasks)]
 
    # initialize `maxBenefit[0]` and `maxTasks[0]` with the first job
    maxBenefit[0] = tasks[0].get_max_benefit()
    maxTasks[0].append(0)
 
    # fill `maxTasks[]` and `maxBenefit[]` in a bottom-up manner
    for i in range(1, num_tasks):
 
        # find the index of the last non-conflicting task with the current task
        index = findLastNonConflictingJob(tasks, i)
 
        # include the current tasks with its non-conflicting task
        currBenefit = tasks[i].get_max_benefit()
        if index != -1:
            currBenefit += maxBenefit[index]
 
        # if including the current task leads to the maximum benefit so far
        if maxBenefit[i - 1] < currBenefit:
            maxBenefit[i] = currBenefit
 
            if index != -1:
                maxTasks[i] = maxTasks[index][:]
            maxTasks[i].append(i)
 
        # excluding the current task leads to the maximum benefit so far
        else:
            maxTasks[i] = maxTasks[i - 1][:]
            maxBenefit[i] = maxBenefit[i - 1]
 
    for i in maxTasks[num_tasks - 1]:
        output.append(tasks[i].get_task_id())

    return output


def final_dp_attempt(tasks):
    output = []

    # sort by deadline
    tasks.sort(key=lambda task: task.get_deadline())
    Matrix = [[None for x in range(1441)] for y in range(len(tasks)+1)]

    for t in range(1441):
        Matrix[0][t] = 0
    
    for i in range(len(tasks)):
        for t in range(1441):
            latestT = min(t, tasks[i].get_deadline()) - tasks[i].get_duration()
            if latestT < 0:
                Matrix[i+1][t] = Matrix[i][t]
            else:
                Matrix[i+1][t] = max(Matrix[i][t], tasks[i].get_max_benefit() + Matrix[i][latestT])

    printOPT(len(tasks)-1, 1440, Matrix, tasks, output)
    return output

def printOPT(i, t, Matrix, tasks, output):
    if i == 0:
        return
    if Matrix[i+1][t] == Matrix[i][t]:
        printOPT(i-1, t, Matrix, tasks, output)
    else:
        latestT = min(t, tasks[i].get_deadline()) - tasks[i].get_duration()
        printOPT(i-1, latestT, Matrix, tasks, output)
        output.append(tasks[i].get_task_id())




def solve_shitty_naive(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    output = []
    time = 0
    best_id = -1
    best_pos = -1
    list_pos = -1
    best_profit = -1
    while time < 1440:
        for task in tasks:
            benefit = task.calc_benefit_from_now(time)
            if benefit > best_profit:
                best_profit = benefit
                best_id = task.get_task_id()
                best_pos = list_pos
            elif benefit == best_profit:
                prev_best_deadline = tasks[best_pos].get_deadline()
                new_best_deadline = task.get_deadline()
                if new_best_deadline < prev_best_deadline:
                    best_profit = benefit
                    best_id = task.get_task_id()
                    best_pos = list_pos
            list_pos += 1
        if len(tasks) == 0:
            break
        output.append(tasks[best_pos].get_task_id())
        time += tasks[best_pos].get_duration()
        tasks.pop(best_pos)
        best_id = 0
        best_pos = 0
        list_pos = 0
        best_profit = 0
    output.pop()
    return output

def sort_by_deadline(tasks):
    return sorted(tasks, key=cmp_to_key(deadline_comparator))

def deadline_comparator(task1, task2):
    return task1.deadline < task2.deadline

if __name__ == '__main__':
    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if size not in input_file:
                continue
            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            print(input_path, output_path)
            tasks = read_input_file(input_path)
            output = final_dp_attempt(tasks)
            # output = solve_shitty_naive(tasks)
            write_output_file(output_path, output)
