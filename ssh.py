# Import required modules/packages/library
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Create the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session expecting password, enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering enable mode')
    exit()

# Send enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering enable mode after sending password')
    exit()

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering config mode')
    exit()

# Print the IP address, username, and password
print('--------------------------------------------------')
print('Connection Details:')
print(f'--- Success! Connecting to: {ip_address}')
print(f'---                        Username: {username}')
print(f'---                          Password: {password}')
print(f'---              Enable Password: {password_enable}')
print('--------------------------------------------------')

# Change the hostname to Router1
session.sendline('hostname Router1')
result = session.expect([r'Router1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists the display error and exit
if result != 0:
    print('--- Failure! setting hostname')


print('--------------------------') #This entire menu is for the user to decide which option they want to choose after establishing connection
print('Please select an option:')
print('1. No Shutdown interface')
print('2. Shutdown interface')

user_choice = input('Enter your choice: ')# This line is where the user is able to enter their choice and have it registered

if user_choice == '1':                              #This entire script of code runs on an if statement and if the users choice is '1' then it will execute the no shutdown procedure and it will go through all of the commands.
    print('Executing no shutdown interface')
    session.sendline('GigabitEthernet0/0')
    session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline('no shutdown')
    session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('---Interface GigabitEthernet0/0 enabled successfully')


else:
        print('---Failed to enable interface')


if user_choice == '2':      #This entire script of code runs on an if statement and if the users choice is '2' then it will execute the shutdown procedure and it will go through all of the commands.
    print('Executing shutdown interface')
    session.sendline('GigabitEthernet0/0')
    session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])


session.sendline('shutdown')
session.expect([r'GigabitEthernet0/0\(config\#', pexpect.TIMEOUT, pexpect.EOF])

if result == 0:
 print('---Interface GigabitEthernet0/0 shutdown successfully')

else:

 print('---Failed to shutdown interface')


# Exit config mode
session.sendline('exit')

# Exit enable mode
session.sendline('exit')

# Terminate SSH session
session.close()

from netmiko import ConnectHandler
import difflib

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',       
    'username': 'prne',       
    'password': 'cisco123!',     
    'secret': 'class123!' 
}


connection = ConnectHandler(**device)
connection.enable()  

running_config = connection.send_command('show running-config')

startup_config = connection.send_command('show startup-config')


with open('running_config.txt', 'w') as run_file:
    run_file.write(running_config)


with open('startup_config.txt', 'w') as start_file:
    start_file.write(startup_config)


connection.disconnect()


print("Configs retrieved and stored successfully.")


def compare_configs(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        
        running_lines = f1.readlines()
        startup_lines = f2.readlines()
        
       
        diff = difflib.unified_diff(
            running_lines, 
            startup_lines, 
            fromfile='Running Config', 
            tofile='Startup Config', 
            lineterm=''
        )
        
       
        print("\nDifferences between Running and Startup Configurations:\n")
        for line in diff:
            print(line)


compare_configs('running_config.txt', 'startup_config.txt')

from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',       
    'username': 'prne',        
    'password': 'cisco123!',     
    'secret': 'class123!' 
}
syslog_server_ip = "192.168.56.101"  

connection = ConnectHandler(**device)
connection.enable()  


commands = [
    f"logging host {syslog_server_ip}",
    "logging trap informational",     
    "logging on"                     
]
output = connection.send_config_set(commands)


connection.disconnect()


print("Syslog configuration output:\n", output)
print(f"Syslog configured to send logs to {syslog_server_ip}.")

from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'prne',
    'password': 'cisco123!',
    'secret': 'class123!',
}

connection = ConnectHandler(**router)
connection.enable()

commands = [
    'interface Loopback0',
    'ip address 192.168.1.1 255.255.255.255',
    'description Loopback Interface',
    'interface GigabitEthernet2',
    'ip address 1.1.1.1 255.255.255.0',
    'description LAN Interface',
    'no shutdown',
    'ip route 0.0.0.0 0.0.0.0 10.0.0.2',
]

output = connection.send_config_set(commands)
print(output)

connection.disconnect()
from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'prne',
    'password': 'cisco123!',
    'secret': 'class123!',
}

net_connect = ConnectHandler(**router)
net_connect.enable()

rip_config = [
    'router rip',
    'version 2',
    'network 192.168.56.0',
    'network 11.1.1.0',
    'network 192.168.1.0',
]

output = net_connect.send_config_set(rip_config)
print('Configuration Output: ')
print(output)

verification_output = net_connect.send_command('show ip protocols')
print('\nVerification Output: ')
print(verification_output)

net_connect.disconnect()
