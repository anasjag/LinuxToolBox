<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<?xml-stylesheet href="file:///opt/homebrew/bin/../share/nmap/nmap.xsl" type="text/xsl"?>
<!-- Nmap 7.94 scan initiated Mon Jan  1 19:54:37 2024 as: nmap -&#45;top-ports 10 -oX google.com -->
<nmaprun scanner="nmap" args="nmap -&#45;top-ports 10 -oX google.com" start="1704128077" startstr="Mon Jan  1 19:54:37 2024" version="7.94" xmloutputversion="1.05">
<scaninfo type="syn" protocol="tcp" numservices="10" services="21-23,25,80,110,139,443,445,3389"/>
<verbose level="0"/>
<debugging level="0"/>
<runstats><finished time="1704128077" timestr="Mon Jan  1 19:54:37 2024" summary="Nmap done at Mon Jan  1 19:54:37 2024; 0 IP addresses (0 hosts up) scanned in 0.01 seconds" elapsed="0.01" exit="success"/><hosts up="0" down="0" total="0"/>
</runstats>
</nmaprun>
