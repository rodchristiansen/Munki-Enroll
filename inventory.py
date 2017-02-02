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

def check_compname(serial_number):
    csv_data = csv.DictReader(CSV, delimiter=',')
    for row in csv_data:
        serial = row['serial']
        computername = row['name']
        hostname = row['name'].replace(' ','')
        catalog_tag = row['catalog']
        area_tag = row['area']
        room_tag = row['room']
        asset_tag = row['asset']
        if serial == serial_number:
            set_sharingname(computername)
            set_hostname(hostname)
            set_localhostname(hostname)
            set_catalog_tag(catalog_tag)
            set_area_tag(area_tag)
            set_room_tag(room_tag)
            set_asset_tag(asset_tag)

def get_serial_number():
    hardware_info = get_hardware_info()
    return hardware_info.get('serial_number', 'UNKNOWN') 

def set_sharingname(computername):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'ComputerName', computername]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_hostname(hostname):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'HostName', hostname]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_localhostname(hostname):
    cmd = ['sudo', '/usr/sbin/scutil', '--set', 'LocalHostName', hostname]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_catalog_tag(catalog_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text1', '-string', catalog_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_area_tag(area_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text2', '-string', area_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_room_tag(room_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text3', '-string', room_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def set_asset_tag(asset_tag):
    cmd = ['sudo', '/usr/bin/defaults', 'write', '/Library/Preferences/com.apple.RemoteDesktop.plist', 'Text4', '-string', asset_tag]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    return output.rstrip('\n')

def main():
    serial_number = get_serial_number()
    check_compname(serial_number)

if __name__ == '__main__':
    main()
    
sys.exit(0)