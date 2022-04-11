

import subprocess
import sys
import time


try:
    from paramiko import SSHClient, AutoAddPolicy
except:
    print('''
    ****************************************
    * You Need To install Some Requirments *
    ****************************************''')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments.txt"])
    print("\033[93m**********Please Restart The program!!!**********\033[0m")         
    time.sleep(4)
    quit()
FIRST_IP =  input('Add Your first IP in the range: ')  #add your first IP in the range   
LAST_IP =   input('Add your last IP: ')  #add your last IP in the range      


editableIP =   FIRST_IP


hosts = []
ask = input('Do you want to add unique IPs out of the range? (y/n): ')
if ask.casefold() == 'y':
    n = input("Enter the IPs separated by space: ") 
      
    hosts = n.split()

print('_____________________________________')

username = input('Enter Username: ')
passWord = input('Enter Password: ')

def SliceIP(fullIP:str):
    octetsList = ['-1','-1','-1','-1']
    tempIP = fullIP
    n = 0
    #======================================Fourth Octet
    if fullIP[-2] == '.':
       octetsList[3] = fullIP[-1:]
    else: 
        if fullIP[-3] == '.':
            octetsList[3] = fullIP[-2:]
        else:
            if fullIP[-4] == '.':
                octetsList[3] = fullIP[-3:]
    #======================================First Octet
    while tempIP[n] != '.':
        n = n + 1
    # print(tempIP[0:n])
    octetsList[0] = tempIP[0:n] # 192.168.100.1
    tempIP = tempIP[n+1:]
    # print(tempIP)
    #======================================Second Octet
    while tempIP[n] != '.':
        n = n + 1
    # print(tempIP[0:n])
    octetsList[1] = tempIP[0:n]
    tempIP = tempIP[n+1:]
    # print(tempIP) 
    #======================================third octet
    while tempIP[n] != '.':
        n = n + 1
    # print(tempIP[0:n])
    octetsList[2] = tempIP[0:n]
    tempIP = tempIP[n+1:]
    # print(tempIP)
    
    return octetsList

def increaseAndRepet(ip1:str):
    o1 = SliceIP(ip1)[0]
    o2 = SliceIP(ip1)[1]
    o3 = SliceIP(ip1)[2]
    o4 = SliceIP(ip1)[3]
    o1int = int(o1)
    o2int = int(o2)
    o3int = int(o3)
    o4int = int(o4)
    if o4int == 255 and o3int != 255 and o2int != 255:
        o4int = 0
        o3int = o3int + 1
        return f"{o1int}.{o2int}.{o3int}.{o4int}"
    else:
        if o4int == 255 and o3int == 255 and o2int != 255:
            o4int = 0 
            o3int = 0 
            o2int = o2int + 1 
            return f"{o1int}.{o2int}.{o3int}.{o4int}"
        else:
            if o4int == 255 and o3int ==255 and o2int == 255:
                o4int = 0
                o3int = 0 
                o2int = 0
                o1int = o1int + 1
                return f"{o1int}.{o2int}.{o3int}.{o4int}"
            else: 
                return f"{o1int}.{o2int}.{o3int}.{o4int}"
# ====================Go To the next IP==================== #
def nextIP(oldIP:str):
    o1 = int(SliceIP(oldIP)[0])
    o2 = int(SliceIP(oldIP)[1])
    o3 = int(SliceIP(oldIP)[2])
    o4 = int(SliceIP(oldIP)[3])
    o4 = o4 + 1 
    newIP = f"{o1}.{o2}.{o3}.{o4}"
    newIP = increaseAndRepet(newIP)
    return newIP

# ====================Add IPs Into the list==================== #
while editableIP != LAST_IP:
    hosts.append(editableIP)
    x = nextIP(editableIP)
    editableIP = x
hosts.append(editableIP)    
#==============================read commandes from file============================
with open('commands.txt') as f:
    lines = f.readlines()


# ====================Enter the hosts one by one==================== #
for host in hosts:
    client = SSHClient()
    client.load_host_keys('./key')
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host,22, username , passWord)
    
    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    # read from the the lines 
    print('')
    print('*************************************')
    print(f'Connect To {host}')
    print('*************************************')
    print('')
    print('=====================================')
    n = len(lines) 
    for command1 in range(n):
        stdin.write(lines[command1] + '\n')
        print(f'configuring: {lines[command1]} ')
    
    print('=====================================')
    time.sleep(  (n * 0.07 )+ 0.05)
    
    
    stdin.close()
    stdout.close()
    client.close()

input("--- Your Configuration Is Done, Press Enter to close the Terminal ^,^ ---")


