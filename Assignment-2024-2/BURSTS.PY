import sys
import math
import argparse

# Function to read time points from a file
def read_time_points(filepath):
    with open(filepath, 'r') as file:
        return list(map(float, file.readline().strip().split()))

# Helper function to calculate lambda values
def calculate_lambdas(total_time, num_intervals, scale, min_gap):
    k = int(1 + math.log(total_time, scale) + math.log(1 / min_gap, scale))
    avg_time = total_time / num_intervals
    return [scale ** i / avg_time for i in range(k)], k

# Viterbi algorithm implementation
def run_viterbi(time_points, scale=3, penalty=0.5):
    num_intervals = len(time_points) - 1
    total_time = time_points[-1]
    gaps = [time_points[i + 1] - time_points[i] for i in range(num_intervals)]
    lambdas, num_states = calculate_lambdas(total_time, num_intervals, scale, min(gaps))

    costs = [[float('inf')] * num_states for _ in range(num_intervals + 1)]
    paths = [[0] * (num_intervals + 1) for _ in range(num_states)]
    costs[0][0] = 0

    for t in range(1, num_intervals + 1):
        for j in range(num_states):
            min_cost, best_state = min(
                (costs[t - 1][l] + (penalty * (j - l) * math.log(num_intervals) if j > l else 0), l)
                for l in range(num_states)
            )
            costs[t][j] = min_cost - math.log(lambdas[j]) + lambdas[j] * gaps[t - 1]
            paths[j][t] = best_state

    final_states = [0] * (num_intervals + 1)
    final_states[-1] = min(range(num_states), key=lambda j: costs[num_intervals][j])
    for t in range(num_intervals, 0, -1):
        final_states[t - 1] = paths[final_states[t]][t]

    return final_states, lambdas, costs


# Function to print state transitions
def print_state_transitions(time_points, states):
    num_intervals = len(time_points) - 1
    current_state = states[0]
    start_time = time_points[0]
    for t in range(1, num_intervals + 1):
        if states[t] != current_state:
            print(f"State {current_state}: [{start_time} - {time_points[t - 1]})")
            current_state = states[t]
            start_time = time_points[t - 1]
    print(f"State {current_state}: [{start_time} - {time_points[-1]})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", choices=["viterbi", "trellis"])
    parser.add_argument("file_path")
    parser.add_argument("-s", "--scale", type=float, default=3)
    parser.add_argument("-g", "--penalty", type=float, default=0.5)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    time_points = read_time_points(args.file_path)

    if args.algorithm == "viterbi":
        states, lambdas, cost_matrix = run_viterbi(time_points, args.scale, args.penalty)
        print("Final cost matrix (Viterbi):")
        print_state_transitions(time_points, states)
    elif args.algorithm == "trellis":
        print("Not implemented yet")

if __name__ == "__main__":
    main()
