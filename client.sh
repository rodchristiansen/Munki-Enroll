#!/bin/sh 

# Gather computer information
IDENTIFIER=$(   defaults read /Library/Preferences/ManagedInstalls ClientIdentifier );
CATALOG=$( 		defaults read /Library/Preferences/com.apple.RemoteDesktop.plist Text1 );
AREA=$( 		defaults read /Library/Preferences/com.apple.RemoteDesktop.plist Text2 );
ROOM=$( 		defaults read /Library/Preferences/com.apple.RemoteDesktop.plist Text3 );
ASSET=$( 		defaults read /Library/Preferences/com.apple.RemoteDesktop.plist Text4 );
HOSTNAMETEMP=$( scutil --get ComputerName );

# Removes spaces if exists in hostname
HOSTNAME=${HOSTNAMETEMP// /}

# Change this URL to the location fo your Munki Enroll install
SUBMITURL="http://pluto.edu.ecuad.ca/deployment/enroll/server.php"

# Test the connection to the server
SHORTURL=$(echo "$SUBMITURL" | awk -F/ '{print $3}')
PINGTEST=$(ping -o "$SHORTURL" | grep "64 bytes")

if [ ! -z "$PINGTEST" ]; then

    # Application paths
    CURL="/usr/bin/curl"

    $CURL --max-time 5 --silent --get \
        -d catalog="$CATALOG" \
        -d area="$AREA" \
        -d room="$ROOM" \
        -d asset="$ASSET" \
        -d hostname="$HOSTNAME" \
        "$SUBMITURL"

     sudo defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "$CATALOG/$AREA/$HOSTNAME"
 
    exit 0

else
    # No good connection to the server
    exit 1

fi