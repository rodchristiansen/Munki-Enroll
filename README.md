# Munki Enroll

A set of scripts to automatically enroll clients in Munki, allowing for a very flexible manifest structure.

This is a fork from the original: https://github.com/edingc/munki-enroll

## How To Enrol Clients ##

Munki Enroll requires PHP to be working on the webserver hosting your Munki repository.

1. Create a “enroll” folder in the root of your Munki repository (the same directory as pkgs, pkginfo, manifests and catalogs). 
2. Add the `server.php` and the `templates` folder to this new folder.
3. Edit the `SUBMITURL` inside the `server.php` script.
3. Edit the URL location in the `.pkginfo` of the CSV to match your organization and file share.
4. Add the `.pkginfo` to your Munki repository and add it as an install item. Munki will now do all the magic.

## How This Is All Working ##

My variation uses a central CSV file that machines consult to get their keys and automatically be assigned the appropriate munki manifests built on these keys.

For example a machine destined to placed in a lab, in classroom 203a, in seat number one, would, when being newly imaged or updated, consult our central CSV and assign its unique manifest of `/Lab/Classroom/203a-01` based on the values set for that computer in our enrolment CSV hosted on our central deployment repository.

The idea of using hostname and RemoteDesktop identifiers keys as the basis for the machine manifests was the main purpose of creating this tool, basically creating a script that automagically sets the machine’s manifest, then — in turn — installs softwares, scripts, preferences, and profiles based on a centralized database that we can change and modify in a very flexible, replicable, rational manner.

In essence, this process of creating a unique manifest structure for each computer approximates a waterfall effect. Every computer manifest is now composed of a core manifest that offers all the main apps, and this core manifest is modified through the inclusion of additional manifests based on deployment location and user allocation. 

The end result of this granular manifest structure is the ability to perform very targeted installs right down to the level of a single machine and to also be broad and affect all machines in your shop. 

All in all, this adds tremendous flexibility for software deployment. 

## The Munki Enroll Scripts ##

There are four scripts that make up the enrol process:  

1. Inventory Python script (inventory.py)  
2. Munki Enrol Client Shell Script (client.sh)  
3. Munki Enrol Server PHP Script (server.php)  
4. Munki Install Check Script (preflight.py)

## How These Scripts are Being Invoked ##

Currently the enrol scripts are called by Munki by running the nopkg pkginfo file called `InventoryManifestControl` — this single `pkginfo` runs the 

- The `installcheck` script reads the local keys and based on the central CSV, decides if machine has incorrect information
- The `preinstall` script sets the ARD keys, ComputerNames, and HostNames
- Then `postinstall` script runs the enrol, creating manifests and setting the machine client id.

### First script: inventory.py ###

These scripts manipulate values scraped from a CSV exported from our main inventory spreadsheet that lives in: `https://your.domain/some/location/reporting/inventory.csv`

A. Reads the CSV from the servers for:  
		1. Serial  
		2. Catalog  
		3. Area  
		4. Room  
		5. Asset  
		6. Name  

B. Checks to see if serial number is present and which row it matches to.

C. Sets Values:  
		1. ComputerName,  
		2. HostName,  
		3. LocalHostName. If it has spaces (staff, faculty) the HostName and LocalHostName are CamelBacked™.  

D. Sets ARD keys:  
	ARD keys 1 = Catalog (Staff, Lab, Faculty, Testing)  
	ARD keys 2 = Area (Photo, HR, Classroom, HR, Design)  
	ARD keys 3 = Room (221e, 203b, 449, etc)  
	ARD keys 4 = Asset (L001554, P000843, etc)   


### Second script: client.sh ###

The `client.sh` script reads the new data just written to `com.apple.RemoteDesktop.plist` and `ClientIdentifier` and passes the variables to the server script.

And sets the manifest client id from that same information:

	sudo defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "$CATALOG/$AREA/$HOSTNAME"


### Third script: server.php ###

This script works with the keys passed by the shell script and works on the repo folders, creating the nested manifests inside the proper folders and the included manifests inside the pkginfo files as necessary. This enables a waterfall manifest structure from top to bottom that both can target a single machine all the way to every single managed Mac — it's pretty awesome.

The `server.php` script and the `template` folder need to be inside the `/deployment/enroll` repo folder since Munki must be able to access these scripts in order to create manifests as machines get enrolled.

For reference here is the [**original server side enrol script**](https://raw.githubusercontent.com/edingc/munki-enroll/master/munki-enroll/enroll.php). It's been heavily customized for our needs and sets a standard and replicable structure.

The keys in the spreadsheet itself such as hostname, serial numbers and ARD fields are inputted manually when we receive new equipment and can be changed at any time simply by editing the Inventory.numbers spreadsheet that lives in our mactech@ecuad.ca iCloud account in the `/Documents/Inventory/` folder. Once the spreadsheet is saved, it triggers a Hazel action to export the spreadsheet as a CSV which makes our key values accessible to to the enrol scripts via `https`

### Forth script: preflight.py ###

This is a preinstall check script that Munki will decide on each run if it need to correct the local setting on the machines and re-enrol it into a different manifest.

Similar to the other python script, this will compare the local keys with the keys set by the central .csv database file, and if different, tell Munki to run the enrol scripts to keep everything in order.