from parse import read_input_file, write_output_file
import os
from functools import cmp_to_key

def knap(cap, tasks):
    t_quantity = len(tasks)
    P = [[0 for x in range(cap+1)] for x in range(t_quantity)]
    T = [[[] for x in range(cap+1)] for x in range(t_quantity)]
    t_durations = [t.get_duration() for t in tasks]

    for i in range(t_quantity):
        for d in range(cap+1):
            if i == 0 or d == 0:
                P[i][d] = 0
            elif t_durations[i] <= cap:
                elapsed_time = sum(T[i-1][d], key=lambda t: t.get_duration())
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
            output = knap(1440, tasks)
            # output = solve_shitty_naive(tasks)
            write_output_file(output_path, output)
