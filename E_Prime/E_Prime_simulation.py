import random

# Parameters (independent variables)
session_duration = 5 * 60 * 1000  # Session duration in milliseconds (5 minutes)
min_ipi = 50  # Minimum Inter-Press Interval in milliseconds
min_iprovi = 3 * 1000  # Minimum Inter-Provocation Interval in milliseconds
max_iprovi = 60 * 1000  # Maximum Inter-Provocation Interval in milliseconds
init_prov_time = 22 * 1000  # Initial Provocation Time in milliseconds
force_prov_interval = 2.5 * 60 * 1000  # Forced Provocation Interval in milliseconds
pfi_duration = 31250  # PFI Duration in milliseconds
click_rate = random.uniform(3.2, 3.3)  # Clicks per second
time_step = 10  # Time step in milliseconds
button_ratio = [0.4, 0.3, 0.3]  # Ratio of pressing buttons 1, 2, 3

# Function to generate button sequence
def generate_button_sequence(duration, rate, ratio):
    presses = int(duration / 1000 * rate)
    return [random.choices([1, 2, 3], ratio)[0] for _ in range(presses)]

# Initialize variables for simulation
def initialize_variables():
    return {
        'total_points': 0,
        'nprov': 0,
        'resume_time': 0,
        'resume_proc': 0,
        'current_opt': 0,
        'press_disp': 0,
        'opt_disp': [0, 0, 0],
        'npress_opt': [0, 0, 0],
        'completed': "",
        'provocation_time': init_prov_time,
        'provocation_proc': 0,
        'nsession_provocation': 0,
        'npress_total': 0,
        'current_time': 0,
        'button_sequence': generate_button_sequence(session_duration, click_rate, button_ratio)
    }

# Simulate session
def simulate_session(buttons_only):
    state = initialize_variables()
    if buttons_only:
        state['button_sequence'] = [buttons_only] * int(session_duration / 1000 * click_rate)

    while state['current_time'] < session_duration:
        if state['button_sequence']:
            next_button = state['button_sequence'].pop(0)
            state['npress_total'] += 1
            current_press_time = state['current_time']
            ipi = current_press_time - (state.get('previous_press_time', 0))
            state['previous_press_time'] = current_press_time

            if ipi > min_ipi and state['resume_proc'] == 0:
                state['current_opt'] = next_button
                state['npress_opt'][next_button - 1] += 1
                state['press_disp'] = state['npress_opt'][next_button - 1]
                if state['npress_opt'][next_button - 1] > 1:
                    pass

                if next_button == 1 and state['npress_opt'][0] == 100:
                    state['completed'] = "Opt1"
                    state['total_points'] += 1
                    state['resume_time'] = current_press_time
                    state['resume_proc'] = 1
                    state['current_opt'] = 0
                    state['current_time'] += 1000  # 1 second pause

                elif next_button == 2 and state['npress_opt'][1] == 10:
                    if current_press_time > state.get('pfi_end_time', 0) and state.get('post_provocation_period', 0) == 1:
                        state['pfi_end_time'] = current_press_time + pfi_duration
                        if (current_press_time / 60000) / force_prov_interval > state['nprov']:
                            state['provocation_time'] = state['pfi_end_time']
                    state['completed'] = "Opt2"
                    state['npress_opt'][1] = 0
                    state['resume_time'] = current_press_time + 1000
                    state['resume_proc'] = 1
                    state['post_provocation_period'] = 0

                elif next_button == 3 and state['npress_opt'][2] == 10:
                    if state['current_time'] > state.get('pfi_end_time', 0) and state.get('post_provocation_period', 0) == 1:
                        state['pfi_end_time'] = current_press_time + pfi_duration
                        if (state['current_time'] / 60000) / force_prov_interval < state['nprov']:
                            state['provocation_time'] = state['pfi_end_time']
                    state['completed'] = "Opt3"
                    state['npress_opt'][2] = 0
                    state['resume_time'] = current_press_time + 1000
                    state['resume_proc'] = 1
                    state['post_provocation_period'] = 0
                    state['current_time'] += 1000  # 1 second pause

        # Check for provocations
        if state['current_time'] > state['provocation_time'] and state['provocation_proc'] == 0:
            state['current_provocation_time'] = state['provocation_time']
            if state['current_time'] < state.get('pfi_end_time', 0):
                state['provocation_time'] += random.randint(min_iprovi, max_iprovi)
            else:
                state['nprov'] += 1
                state['nsession_provocation'] += 1
                state['provocation_proc'] += 1
                state['total_points'] -= 1
                state['provocation_time'] += random.randint(min_iprovi, max_iprovi)

        # Update display logic
        if state['resume_proc'] > 0:
            if state['current_time'] > state['resume_time'] + state['resume_proc'] * 200:
                state['resume_proc'] += 1
                if state['resume_proc'] == 6:
                    state['resume_proc'] = 0

        if state['provocation_proc'] > 0:
            if state['current_time'] > state['current_provocation_time'] + state['provocation_proc'] * 200:
                state['provocation_proc'] += 1
                if state['provocation_proc'] == 6:
                    state['provocation_proc'] = 0

        # Increment time
        state['current_time'] += time_step

    return state['total_points'], state['nprov']

# Run simulation for button 3 only
points_3, prov_3 = simulate_session(3)
print("Total Points (Button 3 Only):", points_3)
print("Number of Provocations (Button 3 Only):", prov_3)

# Run simulation for button 1 only
points_1, prov_1 = simulate_session(1)
print("Total Points (Button 1 Only):", points_1)
print("Number of Provocations (Button 1 Only):", prov_1)

# Run simulation for mixed button presses
points_mixed, prov_mixed = simulate_session(None)
print("Total Points (Mixed Buttons):", points_mixed)
print("Number of Provocations (Mixed Buttons):", prov_mixed)