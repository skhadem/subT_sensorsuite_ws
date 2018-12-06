# Radar-Marble

This is the top-level catkin ws for the subT sensor suite.  

To initialize the workspace using [wstool](wiki.ros.org/wstool):

```
mkdir src
wstool init src .rosinstall

```
This pulls all the necessary packages that have separate repos into the src/ folder. Then,

```
catkin_make
source devel/setup.bash
```

All of the meta launch files we use can be found in launch/

## Networking with the odroid

### To get into the odriod:
1. If in Access Point mode:
   - Switch network to name: radar-odroid-ap, password: arpg4ever
   - `ssh odroid@10.10.0.1` password:odroid
   - on your own machine `export ROS_MASTER_URI=http://10.10.0.1:11311`
2. If in BARlab mode:  
   - Switch network to BARlab
   - `ssh odroid@radar-odroid0` password: odroid
   - on your own machine `export ROS_MASTER_URI=http://radar-odroid0:11311`

The topics thatare published from the odroid can be viewed on your own machine.



Below is a log of what changes were made to setup the odriod as an access point, for reference

(Using interface wlan0)

### Files changed 
- added a bunch of lines to /etc/hostapd/hostapd.conf
	- network name: radar-odroid-ap
	- password: arpg4ever
	- (Using interface wlan0)
- added the last 4 lines to /etc/network/interfaces

- added last line to /etc/default/isc-dhcp-server
- commented out some lines from /etc/dhcp/dhcp.conf
- added lines under 'subnet 10.10.0.0 ...' in /etc/dhcp/dhcp.conf
- changed hostname in /etc/hostname, for access point has to be odroid, but for BARlab should be radar-odroid0

### Services changed
- services to stop:
	- networking-manager (necessary?)
- services to restart:
	- networking
- services to start
	- isc-dhcp-server	
	- hostapd

### How to switch back and forth
To go back to BARlab, have to comment out last 4 lines of /etc/network/interface and then $ sudo service network-manager restart, change hostname back to radar-odroid0

To go back to Access point mode, uncomment last 4 lines of /etc/network/interface and then reboot

## TODO: 
- [] make internet somehow
- [] easy switching between BARlab and access point mode
- [] hostname when in access point mode

