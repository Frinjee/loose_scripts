#!/bin/bash

netfilter-persistent save


# Flush rules and delete chains
iptables -t nat -F
iptables -t mangle -F
iptables -F
iptables -X

# accept all policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# allow loopback connection
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# allow ESTABLISHED && RELATED inc connections
# state is aliased to conntrack
#iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Accept internal > external
iptables -A FORWARD -i enp0s3 -o enp0s5 -j ACCEPT

# drop invalid packets
iptables -A INPUT -m state --state INVALID -j DROP 

# accept icmp on gateway && attacker
iptables -A INPUT -s 10.0.2.1/24 -p ICMP --icmp-type 8 -j ACCEPT
iptables -A OUTPUT -s 10.0.2.1/24 -p ICMP --icmp-type 0 -j ACCEPT

iptables -A INPUT -s 10.0.2.7/24 -p ICMP --icmp-type 8 -j ACCEPT
iptables -A OUTPUT -s 10.0.2.7/24 -p ICMP --icmp-type 0 -j ACCEPT

# drop icmp on victim
iptables -A INPUT -s 10.0.2.15/24 -p ICMP --icmp-type 8 -j DROP
iptables -A OUTPUT -s 10.0.2.15/24 -p ICMP --icmp-type 0 -j DROP

# restrict # of connections
iptables -A INPUT -p tcp -m state --state NEW --dport http -m iplimit --iplimit-above 5 -j DROP

# port scanning protection
iptables -N port-scanning
iptables -A port-scanning -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN
iptables -A port-scanning -j DROP

# syn flood protection
iptables -N syn_flood

iptables -A INPUT -p tcp --syn -j syn_flood
iptables -A syn_flood -m limit --limit 1/s --limit-burst 3 -j RETURN
iptables -A syn_flood -j DROP

iptables -A INPUT -p icmp -m limit --limit  1/s --limit-burst 1 -j ACCEPT

iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 1 -j LOG --log-prefix PING-DROP:
iptables -A INPUT -p icmp -j DROP

iptables -A OUTPUT -p icmp -j ACCEPT

# syn flood mitagation
iptables -t raw -A PREROUTING -p tcp -m tcp --syn -j CT --notrack
iptables -A INPUT -p tcp -m tcp -m state --state INVALID,UNTRACKED -j SYNPROXY --sack-perm --timestamp --wscale 7 --mss 1460
iptables -A INPUT -m state --state INVALID -j DROP

# drop null packets
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# allow inc ssh from attacker
iptables -A INPUT -p tcp -s 10.0.2.7/24 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

# drop outgoing ssh
iptables -A OUTPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j DROP
iptables -A INPUT -p tcp --sport 22 -m state --state ESTABLISHED -j DROP
