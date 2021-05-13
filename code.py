actions_dict = {
        "L": 0, 
        "R": 1,
        "S": 2,
        "U": 3,
        "D": 4}

reverse_action_map = {
      0 :  "l", 
      1 :  "r",
      2 :  "s",
      3 :  "u",
      4 :  "d"
}
positions_dict = {
#     (0,0)	(0,1)	(0,2)	(0,3)
# (1,0)	(1,1)	(1,2)	(1,3)
    "A":0,
    "B":1,
    "C":2,
    "D":3,
    "E":4,
    "F":5,
    "G":6,
    "H":7
}

reverse_positions_dict = {
#     (0,0)	(0,1)	(0,2)	(0,3)
# (1,0)	(1,1)	(1,2)	(1,3)
    0:"00",
    1:"01",
    2:"02",
    3:"03",
    4:"10",
    5:"11",
    6:"12",
    7:"13"
}

import csv

num_pos = 8
num_call = 2
num_actions = 5

states = [(agent_pos, target_pos, call) for agent_pos in range(num_pos)
          for target_pos in range(num_pos)
          for call in range(num_call)]

agent_probability = [[[0
                         for initial_pos in range(num_pos)]
                         for final_pos in range(num_pos)]
                         for action in range(num_actions)]
target_probability = [[0 for initial_pos in range(num_pos)]
                         for final_pos in range(num_pos)]
transition_prob = [[[0 for initial_state in range(len(states))]
                         for final_state in range(len(states))]
                         for action in range(num_actions)]

# transition_prob = {}
# for target_pos, agent_pos, call in states:
#     for target_pos2, agent_pos2, call2 in states:
#         for action in range(num_actions):
#             transition_prob[str(tuple([target_pos, agent_pos, call]))][str(tuple([target_pos2, agent_pos2, call2]))][action] = 0

with open('pomdp - Sheet2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        target_probability[positions_dict[row[0]]][positions_dict[row[1]]] = float(row[2])

with open('pomdp - Sheet3.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # count = 0
    for row in csv_reader:
        # print(str(count) + " " + str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        # print(str(count) + " " + str(actions_dict[row[0]]) + " " + str(positions_dict[row[1]]) + " " + str(positions_dict[row[2]]))
        agent_probability[actions_dict[row[0]]][positions_dict[row[1]]][positions_dict[row[2]]] = float(row[3])
        # count += 1

with open('transition_probabilities.txt', 'w+') as f:
    for action in range(num_actions):
        for initial_state in range(len(states)):
            for final_state in range(len(states)):
                initial_agent_pos = states[initial_state][0]
                initial_target_pos = states[initial_state][1]
                initial_call = states[initial_state][2]

                final_agent_pos = states[final_state][0]
                final_target_pos = states[final_state][1]
                final_call = states[final_state][2]

                if(initial_target_pos==initial_agent_pos):
                    if(initial_call==0 and final_call==0):
                        call_probability = 0.5
                    elif(initial_call==0 and final_call==1):
                        call_probability = 0.5
                    elif(initial_call==1 and final_call==0):
                        call_probability = 1
                    elif(initial_call==1 and final_call==1):
                        call_probability = 0

                if(initial_target_pos!=initial_agent_pos):
                    if(initial_call==0 and final_call==0):
                        call_probability = 0.5
                    elif(initial_call==0 and final_call==1):
                        call_probability = 0.5
                    elif(initial_call==1 and final_call==0):
                        call_probability = 0.1
                    elif(initial_call==1 and final_call==1):
                        call_probability = 0.9

                transition_prob[action][initial_state][final_state] = agent_probability[action][initial_agent_pos][final_agent_pos]*target_probability[initial_target_pos][final_target_pos]*call_probability

                if(transition_prob[action][initial_state][final_state]!=0):
                    f.write("T: " + str(reverse_action_map[action]) + " : S" + str(reverse_positions_dict[initial_agent_pos]) + str(reverse_positions_dict[initial_target_pos]) + str(initial_call) + " : S" + str(reverse_positions_dict[final_agent_pos]) + str(reverse_positions_dict[final_target_pos]) + str(final_call) + " " + str(transition_prob[action][initial_state][final_state]) + '\n')

with open('observations.txt', 'w+') as f:
    for final_state in range(len(states)):

        final_agent_pos = states[final_state][0]
        final_target_pos = states[final_state][1]        
        final_call = states[final_state][2]
        
        if(final_target_pos==final_agent_pos):
            num = 1
        elif((final_target_pos==0 and final_agent_pos==1 )
        or (final_target_pos==1 and final_agent_pos==2 )
        or (final_target_pos==2 and final_agent_pos==3 )
        or (final_target_pos==4 and final_agent_pos==5 )
        or (final_target_pos==5 and final_agent_pos==6 )
        or (final_target_pos==6 and final_agent_pos==7 )):
            num = 4
        elif((final_target_pos==1 and final_agent_pos==0 )
        or (final_target_pos==2 and final_agent_pos==1 )
        or (final_target_pos==3 and final_agent_pos==2 )
        or (final_target_pos==5 and final_agent_pos==4 )
        or (final_target_pos==6 and final_agent_pos==5 )
        or (final_target_pos==7 and final_agent_pos==6 )):
            num = 2
        elif((final_target_pos==0 and final_agent_pos==4 )
        or (final_target_pos==1 and final_agent_pos==5 )
        or (final_target_pos==2 and final_agent_pos==6 )
        or (final_target_pos==3 and final_agent_pos==7 )):
            num = 5
        elif((final_target_pos==4 and final_agent_pos==0 )
        or (final_target_pos==5 and final_agent_pos==1 )
        or (final_target_pos==6 and final_agent_pos==2 )
        or (final_target_pos==7 and final_agent_pos==3 )):
            num = 3
        else:
            num = 6
         
        f.write("O :" + " * : "+ "S" + str(reverse_positions_dict[final_agent_pos]) + str(reverse_positions_dict[final_target_pos]) + str(final_call) + " : " + "o" + str(num) + " 1.0" + '\n')

with open('rewards.txt', 'w+') as f:
    for action in range(num_actions):
        for final_state in range(len(states)):

            final_agent_pos = states[final_state][0]
            final_target_pos = states[final_state][1]
            final_call = states[final_state][2]
            if(action==2):
                rew = 0
            else:
                rew = -1

            if((final_target_pos==final_agent_pos) and (final_call==1)):
                num = 1
                rew = 73 + rew
            elif(final_target_pos==final_agent_pos) and (final_call==0):
                num = 1
            elif((final_target_pos==0 and final_agent_pos==1 )
            or (final_target_pos==1 and final_agent_pos==2 )
            or (final_target_pos==2 and final_agent_pos==3 )
            or (final_target_pos==4 and final_agent_pos==5 )
            or (final_target_pos==5 and final_agent_pos==6 )
            or (final_target_pos==6 and final_agent_pos==7 )):
                num = 4
            elif((final_target_pos==1 and final_agent_pos==0 )
            or (final_target_pos==2 and final_agent_pos==1 )
            or (final_target_pos==3 and final_agent_pos==2 )
            or (final_target_pos==5 and final_agent_pos==4 )
            or (final_target_pos==6 and final_agent_pos==5 )
            or (final_target_pos==7 and final_agent_pos==6 )):
                num = 2
            elif((final_target_pos==0 and final_agent_pos==4 )
            or (final_target_pos==1 and final_agent_pos==5 )
            or (final_target_pos==2 and final_agent_pos==6 )
            or (final_target_pos==3 and final_agent_pos==7 )):
                num = 5
            elif((final_target_pos==4 and final_agent_pos==0 )
            or (final_target_pos==5 and final_agent_pos==1 )
            or (final_target_pos==6 and final_agent_pos==2 )
            or (final_target_pos==7 and final_agent_pos==3 )):
                num = 3
            else:
                num = 6
            
            # for i in range(1,7):
            #     if(i==1):
            #         if(final_target_pos==final_agent_pos):
            #             rew = 72
            #         else:
            #             rew = -1
            #     else:
            #         rew = -1
            f.write("R: " + str(reverse_action_map[action]) + " : * : S" + str(reverse_positions_dict[final_agent_pos]) + str(reverse_positions_dict[final_target_pos]) + str(final_call) + " : o" + str(num) + " " + str(rew) + '\n')

def q1_initial_belief_state():
    with open('q1_initial_belief_state.txt', 'w+') as f:
        for state in range(len(states)):

            agent_pos = states[state][0]
            target_pos = states[state][1]

            if(target_pos==4):
                if(agent_pos in (1,2,3,6,7)):
                    f.write("0.1 ")
                else:
                    f.write("0.0 ")
            else:
                f.write("0.0 ")

    with open('q1_initial_belief_state.txt', 'a') as f:
        f.write('\n')
        for state in range(len(states)):

            agent_pos = states[state][0]
            target_pos = states[state][1]

            if(target_pos==4):
                if(agent_pos in (1,2,3,6,7)):
                    f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(states[state][2])+" 0.1" + '\n')
                else:
                    f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(states[state][2])+" 0.0" + '\n')
            else:
                f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(states[state][2])+" 0.0" + '\n')

def q2_initial_belief_state():
    with open('q2_initial_belief_state.txt', 'w+') as f:
        for state in range(len(states)):

            agent_pos = states[state][0]
            target_pos = states[state][1]
            call = states[state][2]

            if(call==0):
                if(agent_pos==5):
                    if(target_pos in (1,4,5,6)):
                        f.write("0.25 ")
                    else:
                        f.write("0.0 ")
                else:
                    f.write("0.0 ")
            else:
                f.write("0.0 ")

    with open('q2_initial_belief_state.txt', 'a') as f:
        f.write('\n')
        for state in range(len(states)):

            agent_pos = states[state][0]
            target_pos = states[state][1]
            call = states[state][2]

            if(call==0):
                if(agent_pos==5):
                    if(target_pos in (1,4,5,6)):
                        f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(call)+" 0.25" + '\n')
                    else:
                        f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(call)+" 0.0" + '\n')
                else:
                    f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(call)+" 0.0" + '\n')
            else:
                f.write("S"+str(reverse_positions_dict[agent_pos])+str(reverse_positions_dict[target_pos])+str(call)+" 0.0" + '\n')

def state_mapping():
    with open('state_map.txt', 'w+') as f:
        i = 0
        for state in range(len(states)):
            agent_pos = states[state][0]
            target_pos = states[state][1]
            call = states[state][2]

            f.write("S" + str(reverse_positions_dict[agent_pos]) + str(reverse_positions_dict[target_pos]) + str(call) + " ")
            # f.write(str(i))
            i += 1

q1_initial_belief_state()
q2_initial_belief_state()
state_mapping()