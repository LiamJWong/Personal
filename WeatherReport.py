import socket
import http.client as httplib
import random
import json
import requests
import time

API_PORT = "16021"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#The following functions were used in the exemplar to help talk to the nanoleaf display
def send(verb, endpoint, body, ip):
    '''
    Sends an API command to the Nanoleaf device at a given IP address
    '''
    LISTENER = ip + ":" + API_PORT
    try:
        conn = httplib.HTTPConnection(LISTENER)
        if len(body) != 0:
            conn.request(verb, endpoint, body, {"Content-Type": "application/json"})
        else :
            conn.request(verb, endpoint)
        response = conn.getresponse()
        body = response.read()
        return response.status, response.reason, body
    except (httplib.HTTPException, socket.error) as ex:
        print("Error: %s" % ex)

def getAuth(ip):
    '''
    Gets the authentication token from the Nanoleaf device

    Section 5.1 "Authorization"
    '''
    end_point = "/api/v1/new"
    status, __, body = send("POST", end_point, {}, ip)
    if not (status == 200 or status == 204):
        print("could not connect: " + str(status))
    return body

def getDeviceData(ip, auth):
    '''
    Gets all panel info from the Nanoleaf device

    Section 4.1 "API JSON Structure > Light Panels"
    '''
    endpoint = "/api/v1/" + auth
    status, __, body = send("GET", endpoint, {}, ip)
    if not status == 200:
        print("could not connect: " + str(status))
        #exit(1)
    return body

def setStreamControlMode(ip, auth, version):
    '''
    Enables stream control mode on the Nanoleaf device

    Section 3.2.6.2 "External Control (extControl)" && Section 5.7 "External Control (Streaming)"
    '''
    end_point = "/api/v1/" + auth + "/effects"
    ext_control_version = "v" + str(version)
    ext_control_command = {'write': {'command': 'display', 'animType': 'extControl', 'extControlVersion': ext_control_version}}
    status, __, __ = send("PUT", end_point, json.dumps(ext_control_command), ip)
    if not (status == 200 or status == 204):
        print("could not connect: " + str(status))

def sendStreamControlFrames(frames, ip):
    '''
    frames: An array of frames, with each frame consisting of a dictionary with the panelId and the color
    the panel must go to in the specified time. Color is specified as R, G, B and transTime (T) in multiples of 100ms.

    Section 3.2.6.2 "External Control (extControl)" && Section 5.7 "External Control (Streaming)"
    '''
    stream = bytearray()
    stream.append(len(frames) & 0xFF)
    # Port is 60221 for v1 (original Light Panels), v2 for our newer products (Shapes, Elements, Canvas)
    port = 60221
    for frame in frames:
        stream.append(frame['panelId'] & 0xFF)
        stream.append(1 & 0xFF)
        stream.append(frame['R'] & 0xFF)
        stream.append(frame['G'] & 0xFF)
        stream.append(frame['B'] & 0xFF)
        stream.append(0 & 0xFF) # White channel is automatically controlled, no need to set it
        stream.append(frame['T'] & 0xFF)
    sock.sendto(stream, (ip, port))

#inside main contains predefined ips and auth tokens for each controller 
if __name__ == "__main__":
    ip1="192.168.1.14"
    ip2="192.168.1.13"
    ip3="192.168.1.12"
    ip4="192.168.1.10"
    ip5="192.168.1.11"
    ip6="192.168.1.9"
    ip7="192.168.1.4"
    ip8="192.168.1.5"
    ip9="192.168.1.28" 
    ip10="192.168.1.2"
    ips=[ip1,ip2,ip3,ip4,ip5,ip6,ip7,ip8,ip9,ip10]                       
    auth1="LKI439ILyLPOZ73i0fOodP3rgxObe2eO"
    auth2="Vu9ggkGI9RNQ2SDaFPNfUIa7kX9r86nq"
    auth3="Q6hNMymIYPtuJmc8c3Ok4roVjFlFO3F7"
    auth4="Vu9ggkGI9RNQ2SDaFPNfUIa7kX9r86nq"
    auth5="LKI439ILyLPOZ73i0fOodP3rgxObe2eO"
    auth6="RBjc55LQniYPHOTsTgQW5Yoh792AINRl"
    auth7="ALf4TvPrNiK4hxEVdjtbc5Gl0X2l0NCl"
    auth8="eRTQpXfNZh4KLdvnJXsdQMsSzspSerPu"
    auth9="8Wd6krYZG8bpcOkN8zvfbsFG69b2G4QL" 
    auth10="5lzrK08d5urKlI7pXeIKkWt2H4XtyGoe"
    auth = [auth1, auth2, auth3, auth4, auth5, auth6, auth7, auth8, auth9, auth10]


    data1 = json.loads(getDeviceData(ip1, auth1))
    data2 = json.loads(getDeviceData(ip2, auth2))
    data3 = json.loads(getDeviceData(ip3, auth3))
    data4 = json.loads(getDeviceData(ip4, auth4))
    data5 = json.loads(getDeviceData(ip5, auth5))
    data6 = json.loads(getDeviceData(ip6, auth6))
    data7 = json.loads(getDeviceData(ip7, auth7))
    data8 = json.loads(getDeviceData(ip8, auth8))
    data9 = json.loads(getDeviceData(ip9, auth9))
    data10 = json.loads(getDeviceData(ip10, auth10))

    positionData1 = data1['panelLayout']['layout']['positionData']
    positionData2 = data2['panelLayout']['layout']['positionData']
    positionData3 = data3['panelLayout']['layout']['positionData']
    positionData4 = data4['panelLayout']['layout']['positionData']
    positionData5 = data5['panelLayout']['layout']['positionData']
    positionData6 = data6['panelLayout']['layout']['positionData']
    positionData7 = data7['panelLayout']['layout']['positionData']
    positionData8 = data8['panelLayout']['layout']['positionData']
    positionData9 = data9['panelLayout']['layout']['positionData']
    positionData10 = data10['panelLayout']['layout']['positionData']
    
    setStreamControlMode(ip1, auth1, 1)
    setStreamControlMode(ip2, auth2, 1)
    setStreamControlMode(ip3, auth3, 1)
    setStreamControlMode(ip4, auth4, 1)
    setStreamControlMode(ip5, auth5, 1)
    setStreamControlMode(ip6, auth6, 1)
    setStreamControlMode(ip7, auth7, 1)
    setStreamControlMode(ip8, auth8, 1)
    setStreamControlMode(ip9, auth9, 1)
    setStreamControlMode(ip10, auth10, 1)
    
    positionD=[positionData1,positionData2,positionData3,positionData4,positionData5,positionData6,positionData7,positionData8,positionData9,positionData10]
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color=[r,g,b]

    frames1 = []
    frames2 = []
    frames3 = []
    frames4 = []
    frames5 = []
    frames6 = []
    frames7 = []
    frames8 = []
    frames9 = []
    frames10 = []

    T=5

#the following functions are hard coded scenes for each weather type
def overcast_clouds():
    print('overcast clouds on nano')
    #Controllers 1, 2, 3
    for x in range(len(positionData1)):
        R = 104
        G = 103 #Dark Grey
        B = 103
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)
    
    for x in range(len(positionData2)):
        R = 104
        G = 103 #Dark Grey
        B = 103
        frame2 = {'panelId': positionData2[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames2.append(frame2)
    
    for x in range(len(positionData3)):
        R = 104
        G = 103 #Dark Grey
        B = 103
        frame3 = {'panelId': positionData3[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}

        frames3.append(frame3)

    #Controller 4
    for i,panel in enumerate(positionData4):
        if i<5:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)

    #Controller 5
    for i,panel in enumerate(positionData5):
        if i == 0:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i > 4 and i < 7:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i > 9 and i < 13:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i > 0 and i < 5:
            R = 255
            G = 255 #White
            B = 255
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        else:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
    
    #Controller 6
    for i,panel in enumerate(positionData6):
        if i > 1 and i < 7:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i == 9 or i == 14:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i > 9 and i < 14:
            R = 255
            G = 255 #White
            B = 255
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        else:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
    
    #Controller 7
    for i,panel in enumerate(positionData7):
        if i == 0:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i > 2 and i < 6:
            R = 255
            G = 255 #White
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i > 7 and i < 10:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i > 12:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        else:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
    
    #Controller 8
    for i,panel in enumerate(positionData8):
        if i > 1 and i < 4:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        elif i == 6:
            R = 230
            G = 230 #Lighter Grey
            B = 230
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        else:
            R = 104
            G = 103 #Dark Grey
            B = 103
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
    
    #Controllers 9, 10
        for x in range(len(positionData9)):
            R = 76
            G = 140 #Gloomy Green
            B = 0
            frame9 = {'panelId': positionData9[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)

        for x in range(len(positionData10)):
            R = 76
            G = 140 #Gloomy Green
            B = 0
            frame10 = {'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames10.append(frame10)

    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def broken_clouds():
    print('broken clouds on nano')
    #Controller 1
    for x in range(len(positionData1)):
        R = 0
        G = 244 #Light Blue
        B = 255
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)
    
    #Controller 2
    for i,panel in enumerate(positionData2):
        if i > 7 and i < 13:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        else:
            R = 0
            G = 244 #Light Blue
            B = 255
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)

    #Controller 3
    for i,panel in enumerate(positionData3):
        if i < 5:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        elif i > 7 and i < 14:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        else:
            R = 0
            G = 244 #Light Blue
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3) 

    #Controller 4
    for i,panel in enumerate(positionData4):
        if i > 0 and i < 6:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        elif i > 8 and i < 14:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else:
            R = 0
            G = 244 #Light Blue
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)

    #Controller 5
    for x in range(len(positionData5)):
        R = 0
        G = 244 #Light Blue
        B = 255
        frame5 = {'panelId': positionData5[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames5.append(frame5)

    #Controller 6
    for i,panel in enumerate(positionData6):
        if i > 3 and i < 11:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        else: 
            R = 0
            G = 244 #Light Blue
            B = 255
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)

    #Controller 7
    for i,panel in enumerate(positionData7):
        if i > 3 and i < 9:
            R = 255
            G = 255 #Cloud White
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        else: 
            R = 0
            G = 244 #Light Blue
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)

    #Controller 8
    for i,panel in enumerate(positionData8):
        if i < 11:
            R = 0
            G = 244 #Light Blue
            B = 255
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        else: 
            R = 0
            G = 230 #Green Grass
            B = 0
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)

    #Controller 9
    for i,panel in enumerate(positionData9):
        if i < 9:
            R = 0
            G = 244 #Light Blue
            B = 255
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
        else: 
            R = 0
            G = 230 #Green Grass
            B = 0
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)

    #Controller 10
    for x in range(len(positionData10)):
        R = 0
        G = 230 #Green Grass
        B = 0
        frame10 = {'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)

    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def clear_sky():
    print('clear sky on nano')
    for x in range(len(positionData1)): 
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)

    #Controller 2
    for i,panel in enumerate(positionData2):
        if i < 14: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        else:
            R = 255
            G = 255 #yellow sun
            B = 51
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
            
    #Controller 3   
    for i,panel in enumerate(positionData3):
        if i < 14: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        else:
            R = 255
            G = 255 #yellow sun
            B = 51
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
       
    #Controller 4
    for i,panel in enumerate(positionData4):
        if i < 15: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else: 
            R = 255
            G = 255 #yellow sun
            B = 51
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)

    #Controller 5 
    for i,panel in enumerate(positionData5):
        if i < 17: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        else: 
            R = 255
            G = 255 #yellow sun
            B = 51
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)

    #Controllers 6, 7, 8
    for x in range(len(positionData6)):
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame6 = {'panelId': positionData6[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames6.append(frame6)

    for x in range(len(positionData7)):
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame7 = {'panelId': positionData7[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames7.append(frame7)

    for x in range(len(positionData8)):
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame8 = {'panelId': positionData8[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames8.append(frame8)

    #Controllers 9, 10
    for x in range(len(positionData9)):
        R = 0
        G = 204 #green grass
        B = 0
        frame9 = {'panelId': positionData9[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames9.append(frame9)
    
    for x in range(len(positionData10)):
        R = 0
        G = 204 #green grass
        B = 0
        frame10 = {'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)

    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def light_rain(): 
    print('light rain on nano')
    #Controller 1:   
    for x in range(len(positionData1)): 
        R = 179
        G = 200 #dark blue
        B = 240
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)
    #Controller 2: 
    for i,panel in enumerate(positionData2):
        if i<4:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        elif i>=9:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        else:
            R = 179
            G = 200 #dark blue
            B = 240 
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
            
    #Controller 3:     
    for i,panel in enumerate(positionData3):
        if i == 0 or i == 3 or i == 4:
            R = 179
            G = 200 #dark blue
            B = 240
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        elif i > 6 and i < 10: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames1.append(frame1)
        else: 
            R = 163
            G = 209 #lighter blue 
            B = 255 
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
       
    #Controller 4: 
    for i,panel in enumerate(positionData4):
        if i ==3:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        elif i> 10  and i < 13:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        elif i== 17:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        elif i>= 4 and i <= 6:
            R = 179
            G = 200 #dark blue
            B = 240
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else: 
            R = 163
            G = 209 #lighter blue 
            B = 255 
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
      

    #Controller5 
    for i,panel in enumerate(positionData5):
        if i > 4 and i < 7: 
            R = 179
            G = 200 #dark blue
            B = 240
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i <= 2: 
            R = 163
            G = 209 #lighter blue 
            B = 255 
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i> 13 and i < 16:
            R = 163
            G = 209 #lighter blue 
            B = 255 
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        else : 
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)

    #Controller 6: 
    for i,panel in enumerate(positionData6):
        if i == 3 or i== 4:
            R = 179
            G = 200 #dark blue
            B = 240
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i > 12:
            R = 163
            G = 209 #lighter blue 
            B = 255
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        else: 
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        

    #Controller 7: 
    for i,panel in enumerate(positionData7):
        if i == 3:
            R = 179
            G = 200 #dark blue
            B = 220
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i> 7 and i<11 :
            R = 163
            G = 209 #lighter blue 
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i > 12:
            R = 163
            G = 209 #lighter blue 
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        else: 
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        

    #Controller8: 
    for i,panel in enumerate(positionData8):
        if i > 12 :
            R = 163
            G = 209 #lighter blue 
            B = 255
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8) 
        else:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
   
    #Controller 9: 
    for i,panel in enumerate(positionData9):
        if i > 12 :
            R = 163
            G = 209 #lighter blue 
            B = 255
            frame9= {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
        else:
            R = 231
            G = 236 #white/clear sky
            B = 242
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
    #Controller 10: 
    for x in range(len(positionData10)):
        R = 231
        G = 236 #white/clear sky
        B = 242
        frame10={'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)
    
    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def light_snow():
    print('light snow on nano')
    for x in range(len(positionData1)): 
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)

    #Controller 2
    for i,panel in enumerate(positionData2):
        if i == 4 or i == 8 or i == 10: 
            R = 187
            G = 213 #light snow
            B = 239
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        
        elif i == 16: 
            R = 255
            G = 255 #yellow sun
            B = 51
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
            
    #Controller 3   
    for i,panel in enumerate(positionData3):
        if i == 4 or i== 9 or i== 12: 
            R = 187
            G = 213 #light snow
            B = 239
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        elif i < 16 and i != 4 and i != 9 and i!= 12: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        else:
            R = 255
            G = 255 #yellow sun
            B = 51
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
       
    #Controller 4
    for i,panel in enumerate(positionData4):
        if i== 3 or i==7 or i==12: 
            R = 187
            G = 213 #light snow
            B = 239
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        elif i < 17 and i !=3 and i!=7 and i!=12: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else:
            R = 255
            G = 255 #yellow sun
            B = 51
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
       

    #Controller 5 
    for i,panel in enumerate(positionData5):
        if i == 10: 
            R = 95
            G = 210 #green tree
            B = 77
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i < 19: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        else: 
            R = 255
            G = 255 #yellow sun
            B = 51
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)

    #Controllers 6, 7, 8
    for i,panel in enumerate(positionData6):
        if i == 3 :
            R = 95
            G = 210 #green tree
            B = 77
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i==19:
            R = 95
            G = 210 #green tree
            B = 77
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i>=9 and i<=11:
            R = 95
            G = 210 #green tree
            B = 77
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)

    for i,panel in enumerate(positionData7):
        if i== 0 or i==20: 
            R = 225
            G = 244 #snow near sky
            B = 250
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i>=1 and i<=3  : 
            R = 95
            G = 210 #green tree
            B = 77
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i>=7 and i<=11:
            R = 95
            G = 210 #green tree
            B = 77
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i>=17 and i<=19:
            R = 95
            G = 210 #green tree
            B = 77
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
    

    for i,panel in enumerate(positionData8):
        if i==1  or i==8 or i==9 or i==17: 
            R = 95
            G = 210 #green tree
            B = 77
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        elif i < 3 and i != 1: 
            R = 225
            G = 244 #snow near sky
            B = 250
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        elif i==18:
            R = 225
            G = 244 #snow near sky
            B = 250
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
    
    for x in range(len(positionData9)):
        R = 232
        G = 241 #snow ground
        B = 242
        frame9 = {'panelId': positionData9[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames9.append(frame9)
    for x in range(len(positionData9)):
        R = 232
        G = 241 #snow ground
        B = 242
        frame10 = {'panelId': positionData9[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)
    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def snow():
    for x in range(len(positionData1)): 
        R = 51
        G = 180 #blue clear sky
        B = 255
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)

    #Controller 2
    for i,panel in enumerate(positionData2):
        if i <=1: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
        else:
            R = 158
            G = 223 #green tree snow
            B = 188
            frame2 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames2.append(frame2)
            
    #Controller 3   
    for i,panel in enumerate(positionData3):
        if i <=3: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
        else:
            R = 158
            G = 223 #green tree snow
            B = 188
            frame3 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames3.append(frame3)
       
    #Controller 4
    for i,panel in enumerate(positionData4):
        if i <= 7: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        elif i== 10: 
            R = 243
            G = 53 #hat of snowman
            B = 53
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
        else:
            R = 158
            G = 223 #green tree snow
            B = 188
            frame4 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames4.append(frame4)
       

    #Controller 5 
    for i,panel in enumerate(positionData5):
        if i<6: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        elif i >= 10 and i<=12: 
            R = 224
            G = 224 #Snowman
            B = 224
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)
        else: 
            R = 158
            G = 223 #green tree snow
            B = 188
            frame5 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames5.append(frame5)

    #Controller 6
    for i,panel in enumerate(positionData6):    
        if i >= 10 and i<=12: 
            R = 224
            G = 224 #Snowman
            B = 224
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        elif i>15: 
            R = 158
            G = 223 #green tree snow
            B = 188
            frame6 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame6= {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames6.append(frame6)

    #Controller 7
    for i,panel in enumerate(positionData7):
        if i==5: 
            R = 205
            G = 126 #snowman hand
            B = 47
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i==15:
            R = 205
            G = 126 #snowman hand
            B = 47
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i>=7 and i<= 13:
            R = 224
            G = 224 #Snowman
            B = 224
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        elif i> 17: 
            R = 158
            G = 223 #green tree snow
            B = 188
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame7 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames7.append(frame7)
    
    #Controller 8
    for i,panel in enumerate(positionData8):
        if i>=6 and i<=12: 
            R = 240
            G = 224 #Snowman
            B = 224
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        elif i < 3:  
            R = 206
            G = 206  #snow near sky
            B = 206
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        elif i>16:
            R = 206
            G = 206 #snow near sky
            B = 206
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        else: 
            R = 51
            G = 180 #blue clear sky
            B = 255
            frame8= {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
    #Controller 9: 
    for i,panel in enumerate(positionData9):
        if i>=6 and i<=10: 
            R = 240
            G = 224 #Snowman
            B = 224
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
        else: 
            R = 206
            G = 206 #snow near sky
            B = 206
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
    
    print('snow on nano')
    #Controller 10:
    for x in range(len(positionData10)):
        R = 206
        G = 206 #snow near sky
        B = 206
        frame10 = {'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)
    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)

def mist():
    print('mist on nano')
    #Controller 1
    for x in range(len(positionData1)): 
        R = 224 
        G = 224 #dim grey
        B = 224
        frame1 = {'panelId': positionData1[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames1.append(frame1)
    #Controller 2:
    for x in range(len(positionData2)): 
        R = 214 
        G = 214 #dim grey
        B = 214
        frame2 = {'panelId': positionData2[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames2.append(frame2)
    #Controller 3: 
    for x in range(len(positionData3)): 
        R = 207 
        G = 207 #dim grey
        B = 207
        frame3 = {'panelId': positionData3[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames3.append(frame3)
    #Controller 4
    for x in range(len(positionData4)): 
        R = 200
        G = 200 #dim grey
        B = 200
        frame4 = {'panelId': positionData4[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames4.append(frame4)
    #Controller 5: 
    for x in range(len(positionData5)): 
        R = 200
        G = 200 #dim grey
        B = 200
        frame5 = {'panelId': positionData5[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames5.append(frame5)

    #Controller 6: 
    for x in range(len(positionData6)): 
        R = 195
        G = 195 #dim grey
        B = 195
        frame6 = {'panelId': positionData6[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames6.append(frame6)
    #Controller 7: 

    for x in range(len(positionData7)): 
        R = 195 
        G = 195 #dim grey
        B = 195
        frame7= {'panelId': positionData7[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames7.append(frame7)

    #Controller 8:
    for i,panel in enumerate(positionData8):
        if i<7: 
            R = 12
            G = 118 #Mist ground
            B = 0
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)
        else: 
            R = 195
            G = 195 #snow lower sky
            B = 195
            frame8 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames8.append(frame8)

    #Controller 9: 
    for i,panel in enumerate(positionData9):
        if i<11: 
            R = 12
            G = 118 #Mist ground
            B = 0
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
        else: 
            R = 195
            G = 195 #snow lower sky
            B = 195
            frame9 = {'panelId': panel['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
            frames9.append(frame9)
    
    #Controller 10: 
    for x in range(len(positionData10)): 
        R = 12 
        G = 118 #dim grey
        B = 0
        frame10= {'panelId': positionData10[x]['panelId'], 'R': R, 'G': G, 'B': B, 'T': T}
        frames10.append(frame10)
    for i in range(5):
        sendStreamControlFrames(frames1,ip1)
        sendStreamControlFrames(frames2,ip2)
        sendStreamControlFrames(frames3,ip3)
        sendStreamControlFrames(frames4,ip4)
        sendStreamControlFrames(frames5,ip5)
        sendStreamControlFrames(frames6,ip6)
        sendStreamControlFrames(frames7,ip7)
        sendStreamControlFrames(frames8,ip8)
        sendStreamControlFrames(frames9,ip9)
        sendStreamControlFrames(frames10,ip10)
        time.sleep(5)
    
loop=1

#253682c0bd759acfb4255d4aa08c3dd7 second appid incase ours doesn't work
#While loop for the program to continuously run unless user dictates c
while loop==1:
    userinput = input('Please input the zip code for a city in the US or type c to cancel: ')

    #check for cancel 
    if userinput.lower() == 'c':
        print(userinput)
        break
    
    #else request information requests.get() where zip is defined by user
    else:
        getreq = "http://api.openweathermap.org/data/2.5/weather?zip={},us&appid=16ac93391ed9ff56a249df2499d08d53".format(userinput)
        Place = requests.get(getreq)

        #Here we are printing the response of the web server and converting its information to a readable format
        print(Place.status_code)
        City = Place.json()
        print(City["name"])
        print(City["weather"][0]["description"])
        weath = City["weather"][0]["description"]

        #check response from OpenWeatherAPI, send to respective function
        if weath == "overcast clouds":
            overcast_clouds()
        elif weath == "broken clouds":
           broken_clouds()
        elif weath == "scattered clouds":
            broken_clouds()
        elif weath == "clear sky":
            clear_sky()
        elif weath == "few clouds":
            clear_sky()
        elif weath == "light rain":
            light_rain()
        elif weath == "light snow":
            light_snow()
        elif weath == "snow":
            snow()
        elif weath == "mist":
            mist()
        else:
            print("Invalid Entry")
            break
