from parse import read_input_file, write_output_file
import os

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


# Here's an example of how to run your solver.
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
            output = solve_shitty_naive(tasks)
            write_output_file(output_path, output)