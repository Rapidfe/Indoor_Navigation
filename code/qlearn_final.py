#import libraries
import numpy as np
import random
import get_coord as coo
import serial
import time
import threading
from PIL import Image

sending = 1
fileName1 = "map1"
fileName2 = "map2"
fileName3 = "map3"
grid_size = [18, 18]     #[row, column]
start_info = [3, 4, 1]   #[floor, row, column] index:start from 0
end_info = [1, 17, 5]

def get_starting_location(MAP, environment_rows, environment_columns):
    for i in range(0, environment_rows):
        for j in range(0, environment_columns):
            if MAP[i,j] == 3:
                row_x = i
                row_y = j
            if MAP[i,j] == 4:
                goal_x = i
                goal_y = j
    return row_x, row_y, goal_x, goal_y

def do_action(MAP, row_index, column_index, action, environment_rows, environment_columns, goal_x, goal_y) :
    # 0 = up, 1 = right, 2 = down, 3 = left
    environment_columns -= 1
    environment_rows -= 1
    if action == 0 :
        if row_index == 0:
            reward = -100
        elif MAP[row_index - 1, column_index] == 1:
            reward = - 100
        else :
            row_index -= 1
            reward = -1
    elif action == 1:
        if column_index == environment_columns:
            reward = -100
        elif MAP[row_index, column_index + 1] == 1:
            reward = -100
        else:
            column_index += 1
            reward = -1
    elif action == 2:
        if row_index == environment_rows:
            reward = - 100
        elif MAP[row_index + 1, column_index] == 1:
            reward = -100
        else :
            row_index += 1
            reward = -1
    elif action == 3:
        if column_index == 0:
            reward = -100
        elif MAP[row_index, column_index -1 ] == 1:
            reward = - 100
        else :
            column_index -= 1
            reward = -1
    if row_index == goal_x and column_index == goal_y:
        done = True
        reward = 100
    else :
        done = False
    return row_index, column_index, reward, done

def savePath(name1, name2, path):
    img1 = Image.open(name1)
    img2 = Image.open(name2)
    img = Image.new('RGB', (img1.size[0]+img2.size[0],img1.size[1]), (250,250,250))
    img.paste(img1, (0,0))
    img.paste(img2.transpose(Image.FLIP_LEFT_RIGHT), (img1.size[0],0))
    (onegaro, onesero) = img.size
    onegaro /= grid_size[1]*2
    onesero /= grid_size[0]
    print(path)
    for ii in range(len(path)):
        ssize = 5
        i = path[ii]
        if ii==0:
            color = (0,0,255)
            ssize = 9
        elif ii==len(path)-1:
            color = (0,255,0)
            ssize = 9
        else:
            color = (255,0,0)
        for gg in range(ssize):
            for cc in range(ssize):
                img.putpixel((int(i[1] * onegaro + onegaro / 2)+gg-int(ssize/2), int(i[0] * onesero + onesero / 2)+cc-int(ssize/2)), color)
    img.save('path.PNG')

planning_send_arduino = []
plann = [[],[],[]]
floor = [0,0]
mapName = []
aisles = []
cntt = 0
cnt = [0,0,0]
ran = [10, 20, 30, 60, 80, 100, 250, 450, 750, 1000]
ranc = 0
# lim = [800, 800, 800, 600, 400, 400, 200, 200, 100, 100]
limit = len(ran)

def divArr():
    global planning_send_arduino
    global plann
    global cntt
    global limit
    global floor
    tmp = [[],[],[]]
    while cntt!=-1:
        if len(planning_send_arduino) > cntt:
            tmp[floor[0]] = [[0 for _ in range(18)] for _ in range(18)]
            tmp[floor[1]] = [[0 for _ in range(18)] for _ in range(18)]
            for i in planning_send_arduino[cntt]:
                if i[1]<18:
                    tmp[floor[0]][i[0]][i[1]] = 1
                else:
                    tmp[floor[1]][i[0]][35-i[1]] = 1
            plann[floor[0]].append(tmp[floor[0]])
            # for j in tmp[floor[1]]:
            #     print(j)
            # print()
            plann[floor[1]].append(tmp[floor[1]])
            cntt += 1
        else:
            time.sleep(0.1)
        if cntt==limit:
            cntt = -1
            planning_send_arduino = []

def sendToArduino(thisc):
    global plann
    global cnt
    global limit
    por = '/dev/ttyACM' + str(thisc)
    try:
        ser = serial.Serial(port=por, baudrate=9600)
    except:
        print('fail to open arduino port')
        cnt[thisc] = limit
    print(por)
    time.sleep(3)
    # ser = serial.Serial(port='COM3', baudrate=9600)
    while cnt[thisc]!=-1:       # cntt = -2:대기  -1:종료  0이상:전송
        if len(plann[thisc]) > cnt[thisc]:
            planning = plann[thisc][cnt[thisc]]
            if cnt[thisc]==0:
                print('port' + str(thisc) + '...')
                ser.write('a'.encode())
            for i in planning:
                for j in i:
                    string = str(j) + '\n'
                    ser.write(string.encode())
                ss = ser.readline().decode()
            #         print(j, end='')
            cnt[thisc] += 1
            print(cnt[thisc])
            # print('port' + str(thisc) + ': ' + str(cnt[thisc]))
        else:
            time.sleep(0.1)
        if cnt[thisc]==limit:
            # ss = ser.readline().decode()
            print('port'+str(thisc)+' success')
            plann[thisc] = []
            while cnt[thisc]!=-1:
                time.sleep(0.1)
            ser.write('c'.encode())
            time.sleep(4)

if sending:
    thread_0 = threading.Thread(target=divArr)
    thread_0.start()
    thread_1 = threading.Thread(target=sendToArduino, args=(0,))
    thread_1.start()
    thread_2 = threading.Thread(target=sendToArduino, args=(1,))
    thread_2.start()
    thread_3 = threading.Thread(target=sendToArduino, args=(2,))
    thread_3.start()

# define training parameters
epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.99  # discount factor for future rewards
learning_rate = 0.9  # the rate at which the AI agent should learn

environment_rows = grid_size[0]
environment_columns = grid_size[1]*2
MAP = np.ones((environment_rows, environment_columns))
q_values = np.zeros((environment_rows, environment_columns, 4))
actions = ['up', 'right', 'down', 'left']

while 1:
    floor[0] = start_info[0]-1
    floor[1] = end_info[0]-1
    mapName.append(fileName1 + '.PNG')
    mapName.append(fileName2 + '.PNG')
    mapName.append(fileName3 + '.PNG')
    try:
        for i in mapName:
            aisles.append(coo.makeCoord(i))
    except:
        print('\n!!Wrong name!!')
        break
    cntt = 0
    print(grid_size[0])

    for i in range(environment_rows):
        for j in aisles[start_info[0]-1][i]:
            MAP[i, j] = 0
    for i in range(environment_rows):
        for j in aisles[end_info[0]-1][i]:
            MAP[i, 35-j] = 0
    MAP[start_info[1], start_info[2]] = 3
    MAP[end_info[1], environment_columns-1-end_info[2]] = 4
    # print(MAP)

    eps = 0.1
    mincost = -1
    mypath = []
    # run through 1000 training episodes
    for episode in range(1, 1001):
        # get the starting location for this episode
        row_index, column_index, goal_x, goal_y = get_starting_location(MAP, environment_rows, environment_columns)
        #0 = up, 1 = right, 2 = down, 3 = left
        cost = 0
        done = False
        my_planning = []
        my_planning.append([row_index, column_index])
        while not(done) :
            if random.random() < (0.7 / episode) :
                action = random.randint(0, 3)
            else:
                action = np.argmax(q_values[row_index, column_index])
            next_row_index, next_column_index, reward, done = do_action(MAP, row_index, column_index, action, environment_rows, environment_columns, goal_x, goal_y)

            old_q_value = q_values[row_index, column_index, action]
            temporal_difference = reward + (discount_factor * np.max(q_values[next_row_index, next_column_index])) - old_q_value
            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[row_index, column_index, action] = new_q_value
            row_index = next_row_index
            column_index = next_column_index
            cost += 1
            my_planning.append([row_index, column_index])
            if done == True:
                if episode==ran[ranc]:
                    # print(my_planning)
                    # print(cost)
                    planning_send_arduino.append(my_planning)
                    ranc += 1
                break
        if mincost == -1 or mincost>cost:
            mincost = cost
            mypath = my_planning
    savePath(mapName[start_info[0]-1], mapName[end_info[0]-1], mypath)
    print('\noptimal is...')
    print(mypath)
    print(len(mypath)-1)
    if sending:
        print('\nSending to Arduino...')
        while cnt[floor[0]]!=limit or cnt[floor[1]]!=limit:
            time.sleep(0.2)
        cnt[0] = -1
        cnt[1] = -1
        cnt[2] = -1
    break