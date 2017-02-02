#!/usr/bin/python

import csv
import subprocess
import plistlib
import sys
import urllib2

CSV_LOCATION = 'http://pluto.edu.ecuad.ca/imaging/reporting/inventory.csv'
CSV = urllib2.urlopen(CSV_LOCATION)

def get_hardware_info():
    '''Uses system profiler to get hardware info for this machine'''
    cmd = ['/usr/sbin/system_profiler', 'SPHardwareDataType', '-xml']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # system_profiler xml is an array
        sp_dict = plist[0]
        items = sp_dict['_items']
        sp_hardware_dict = items[0]
        return sp_hardware_dict
    except Exception:
        return {}

def check(serial_number, local_computername, local_hostname, local_catalog, local_area, local_room, local_asset):
    csv_data = csv.DictReader(CSV, delimiter=',')
    for row in csv_data:
        serial = row['serial']
        csv_computername = row['name']
        csv_hostname = row['name'].replace(' ','')
        csv_catalog = row['catalog']
        csv_area = row['area']
        csv_room = row['room']
        csv_asset = row['asset']
        if serial == serial_number:
            if csv_computername != local_computername:
                sys.exit(0)                      
            elif csv_hostname != local_hostname:
                sys.exit(0)
            elif csv_catalog != local_catalog:
                sys.exit(0)
            elif csv_area != local_area:
                sys.exit(0)
            elif csv_room != local_room:
                sys.exit(0)
            elif csv_asset != local_asset:
                sys.exit(0)
            else:
                sys.exit(1)

def get_serial_number():
    hardware_info = get_hardware_info()
    return hardware_info.get('serial_number', 'UNKNOWN') 

def get_computername():
    cmd = ['/usr/sbin/scutil', '--get', 'ComputerName']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def get_hostname():
    cmd = ['/usr/sbin/scutil', '--get', 'HostName']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def get_catalog():
    cmd = ['/usr/bin/defaults', 'read', '/Library/Preferences/com.apple.RemoteDesktop', 'Text1']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def get_area():
    cmd = ['/usr/bin/defaults', 'read', '/Library/Preferences/com.apple.RemoteDesktop', 'Text2']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')
    
def get_room():
    cmd = ['/usr/bin/defaults', 'read', '/Library/Preferences/com.apple.RemoteDesktop', 'Text3']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')
    
def get_asset():
    cmd = ['/usr/bin/defaults', 'read', '/Library/Preferences/com.apple.RemoteDesktop', 'Text4']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def main():
    serial_number = get_serial_number()
    local_computername = get_computername()
    local_hostname = get_hostname()
    local_catalog = get_catalog()
    local_area = get_area()
    local_room = get_room()
    local_asset = get_asset()
    check(serial_number, local_computername, local_hostname, local_catalog, local_area, local_room, local_asset)

if __name__ == '__main__':
    main()