#! /usr/bin/python
import os

# constants
iteration_count = 10
max_senders = 100
resultfolder = "ns2resultssendersweep"
topofolder = "ns2toposenders"

# protocols
rationalstr="-tcp TCP/Rational -sink TCPSink/Sack1 -gw DropTail"
cubicstr="-tcp TCP/Linux/cubic -sink TCPSink/Sack1 -gw DropTail"
cubicsfqCoDelstr="-tcp TCP/Linux/cubic -sink TCPSink/Sack1 -gw sfqCoDel"

# traffic pattern
traffic_workload="-ontype time -onrand Exponential -onavg 1.0 -offrand Exponential"

# Clean up the results and topologies folder
os.system("rm -rf " + resultfolder)
os.system("mkdir " + resultfolder)
os.system("rm -rf " + topofolder)
os.system("mkdir " + topofolder)

# Vary number of senders in topology
for num_senders in range(1, max_senders + 1, 1):
  fh=open(topofolder + "/senders"+ str(num_senders) + ".txt", "w");
  fh.write("0 1 15 75\n");
  fh.close();

  # Make sd file
  fh=open(topofolder + "/sd" + str(num_senders) + ".txt", 'w');
  for sender_index in range(1, num_senders + 1, 1):
    fh.write("0 1" + " \n");
  fh.close();

# Synthesize command line
def synthesize( whiskertree, topology, sdpairs, tcp_agents, traffic_cfg, off_time, sim_time, run, tag ):
  global topofolder
  global resultfolder
  cmdline="WHISKERS=" + whiskertree + " ./decompose.tcl " + topology + " " + sdpairs + " " + tcp_agents + " " +  traffic_cfg + " -offavg "+ str( off_time ) + " -simtime " + str( sim_time ) + " -run " + str( run )
  fileio=" >" + resultfolder + "/" + tag + "run" + str( run ) + ".out " + "2>" + resultfolder + "/" + tag + "run" + str( run ) +  ".err"
  cmdline += fileio
  target = resultfolder + "/" + tag + "run" + str( run ) + ".out"
  synthesize.targets += " " + target
  synthesize.cmdlines += "\n" + target + ":\n\t" + cmdline
synthesize.targets=""
synthesize.cmdlines=""

# Cross-agility on num_senders
for num_senders in range(1, max_senders + 1, 1):
  senders_topology = topofolder + "/senders" + str(num_senders) + ".txt"
  sdpairs = topofolder + "/sd" + str(num_senders) + ".txt"
  for run in range(1, iteration_count + 1):
    synthesize(os.getcwd() + "/muxing2.dna.2",          senders_topology, sdpairs, rationalstr,      traffic_workload, 1.0, 100, run, "1--2senders" + str(num_senders));
    synthesize(os.getcwd() + "/muxing10-resume.dna.3",  senders_topology, sdpairs, rationalstr,      traffic_workload, 1.0, 100, run, "1--10senders"  + str(num_senders));
    synthesize(os.getcwd() + "/muxing20-resume.dna.5",  senders_topology, sdpairs, rationalstr,      traffic_workload, 1.0, 100, run, "1--20senders"  + str(num_senders));
    synthesize(os.getcwd() + "/muxing50-resume.dna.1",  senders_topology, sdpairs, rationalstr,      traffic_workload, 1.0, 100, run, "1--50senders"  + str(num_senders));
    synthesize(os.getcwd() + "/muxing100-resume.dna.0", senders_topology, sdpairs, rationalstr,      traffic_workload, 1.0, 100, run, "1--100senders"   + str(num_senders));
    synthesize( "NULL",                                   senders_topology, sdpairs, cubicsfqCoDelstr, traffic_workload, 1.0, 100, run, "cubicsfqCoDel-num_senders"+str(num_senders));
    synthesize( "NULL",                                   senders_topology, sdpairs, cubicstr,         traffic_workload, 1.0, 100, run, "cubic-num_senders"+str(num_senders));

print "all: " + synthesize.targets, synthesize.cmdlines
