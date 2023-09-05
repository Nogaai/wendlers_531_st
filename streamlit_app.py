import streamlit as st
import json
import os
from collections import defaultdict

dir = os.listdir()

st.set_page_config(page_title = "Wendler's 5/3/1 calculator")
st.title("Wendler's 5/3/1 workout calculator")
def load_weights():
    if "stored_weight.json" in dir:
        with open('stored_weight.json', 'r') as file:
            lifts = json.loads(file.read())
    else:
        lifts = {'Bench': 100, 'Squat': 100, 'Deadlift': 130, 'Press': 65}
    return lifts

def save_weights():
    with open('stored_weight.json', 'w') as file:
        file.write(json.dumps(lifts))

lifts = load_weights()

def round_weights(weight, round_down):
    return (round_down) * round(weight/round_down)
# Converts max numbers to a working weight dictionary
def max_lifts_to_working_weight(lifts_dict):
    working_weight_dict = defaultdict(lambda: 0)
    percentage_of_max = 0.9
    for exercise in lifts_dict.keys():
        working_weight = round_weights((float(lifts_dict[exercise]) * percentage_of_max), 2.5)
        working_weight_dict[exercise] = working_weight
    return working_weight_dict

# Increases working weight after a deload week
def increase_lifts():
    global lifts
    leg_increase = 5
    upper_increase = 2.5
    leg_exercises = ['Squat', 'Deadlift']
    upper_exercises = ['Bench', 'Press']

    for exercise in lifts.keys():
        if exercise in leg_exercises:
            lifts[exercise] += leg_increase
        elif exercise in upper_exercises:
            lifts[exercise] += upper_increase

    st.session_state.bench = lifts['Bench']
    st.session_state.press = lifts['Press']
    st.session_state.deadlift = lifts['Deadlift']
    st.session_state.squat = lifts['Squat']


def setup_weeks(lifts_dict):
    lifting_weeks = {'Week 1': defaultdict(lambda: 0),
                     'Week 2': defaultdict(lambda: 0),
                     'Week 3': defaultdict(lambda: 0),
                     'Week 4': defaultdict(lambda: 0),}
    for exercise in lifts_dict.keys():
        weight = lifts_dict[exercise]
        weeks_sets = {'Week 1':
                          {'Set 1': f'{round_weights((weight * .65), 2.5)}kg x 5',
                           'Set 2': f'{round_weights((weight * .75), 2.5)}kg x 5',
                           'Set 3': f'{round_weights((weight * .85), 2.5)}kg x 5'},
                      'Week 2':
                          {'Set 1': f'{round_weights((weight * .70), 2.5)}kg x 3',
                           'Set 2': f'{round_weights((weight * .80), 2.5)}kg x 3',
                           'Set 3': f'{round_weights((weight * .90), 2.5)}kg x 3'},
                      'Week 3':
                          {'Set 1': f'{round_weights((weight * .75), 2.5)}kg x 5',
                           'Set 2': f'{round_weights((weight * .85), 2.5)}kg x 3',
                           'Set 3': f'{round_weights((weight * .95), 2.5)}kg x 1'},
                      'Week 4':
                          {'Set 1': f'{round_weights((weight * .40), 2.5)}kg x 5',
                           'Set 2': f'{round_weights((weight * .50), 2.5)}kg x 5',
                           'Set 3': f'{round_weights((weight * .60), 2.5)}kg x 5'}
                      }
        lifting_weeks['Week 1'][exercise] = weeks_sets['Week 1']
        lifting_weeks['Week 2'][exercise] = weeks_sets['Week 2']
        lifting_weeks['Week 3'][exercise] = weeks_sets['Week 3']
        lifting_weeks['Week 4'][exercise] = weeks_sets['Week 4']
    return lifting_weeks

with st.sidebar:
    st.header('Input 1RM for each lift')

    bench = st.number_input('Bench Press', value = lifts['Bench'])
    press = st.number_input('Overhead Press', value = lifts['Press'])
    deadlift = st.number_input('Deadlift', value = lifts['Deadlift'])
    squat = st.number_input('Squat', value = lifts['Squat'])

    lbutton, rbutton = st.columns(2, gap = "small")
    with lbutton:
        submit_lifts = st.button("Calculate Lifts")
    with rbutton:
        update_lifts = st.button("Increase Weights")

    if submit_lifts:
        lifts['Bench'] = bench
        lifts['Squat'] = squat
        lifts['Deadlift'] = deadlift
        lifts['Press'] = press
        save_weights()
        st.experimental_rerun()

    if update_lifts:
        lifts['Bench'] = bench + 2.5
        lifts['Squat'] = squat + 2.5
        lifts['Deadlift'] = deadlift + 5
        lifts['Press'] = press + 5
        save_weights()
        st.experimental_rerun()


work_set = max_lifts_to_working_weight(lifts)
lift_week = setup_weeks(work_set)
with st.container():
    st.subheader('Week 1', divider='orange')
    week_1 = st.dataframe(lift_week['Week 1'], use_container_width = True)
    st.subheader('Week 2', divider='orange')
    week_2 = st.dataframe(lift_week['Week 2'], use_container_width = True)
    st.subheader('Week 3', divider='orange')
    week_3 = st.dataframe(lift_week['Week 3'], use_container_width = True)
    st.subheader('Week 4', divider='orange')
    week_4 = st.dataframe(lift_week['Week 4'], use_container_width = True)
