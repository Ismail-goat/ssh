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