# Python DNS Resolver

dns-resolver is a simple DNS resolver written in Python3 using only dnspython as an external library.

To run the program, we can first give it executable permission to run it like an executable as opposed to writing python everytime.
```
chmod +x mydig.py
```

## Usage examples:
### Simple - just get address only
```
$ ./mydig.py stonybrook.edu -S
129.49.2.176
```
### Basic usage - defaults to type A
```
$ ./mydig.py stonybrook.edu
QUESTION SECTION:
stonybrook.edu. IN A

ANSWER SECTION:
stonybrook.edu. 900 IN A 129.49.2.176

Query time: 77 msec
WHEN: Tue Feb 13 15:53:35 2018
MSG SIZE rcvd: 48
```
### Specifying type
```
$ ./mydig.py stonybrook.edu MX
QUESTION SECTION:
stonybrook.edu. IN MX

ANSWER SECTION:
stonybrook.edu. 900 IN MX 20 syr-t5220-01.syracuse.stonybrook.edu.
stonybrook.edu. 900 IN MX 1 sbmta2.cc.stonybrook.edu.
stonybrook.edu. 900 IN MX 1 sbmta1.cc.stonybrook.edu.

Query time: 89 msec
WHEN: Tue Feb 13 15:58:08 2018
MSG SIZE rcvd: 119
```
### Tracing the resolver from root downards
```
$ ./mydig.py stonybrook.edu -T
edu. 172800 IN NS f.edu-servers.net.
edu. 172800 IN NS a.edu-servers.net.
edu. 172800 IN NS g.edu-servers.net.
edu. 172800 IN NS l.edu-servers.net.
edu. 172800 IN NS c.edu-servers.net.
edu. 172800 IN NS d.edu-servers.net.
stonybrook.edu. 172800 IN NS nocnoc.stonybrook.edu.
stonybrook.edu. 172800 IN NS whoisthere.stonybrook.edu.
stonybrook.edu. 172800 IN NS mewho.stonybrook.edu.
stonybrook.edu. 900 IN A 129.49.2.176

```
### Example where DNSSEC is not supported (with and without tracing)
```
$ ./mydig.py stonybrook.edu -D
DNSSEC not supported
$ ./mydig.py stonybrook.edu -DT
DNSKEY found at .
DS record at . validated by ZSK
edu. 172800 IN NS f.edu-servers.net.
edu. 172800 IN NS a.edu-servers.net.
edu. 172800 IN NS g.edu-servers.net.
edu. 172800 IN NS l.edu-servers.net.
edu. 172800 IN NS c.edu-servers.net.
edu. 172800 IN NS d.edu-servers.net.
DNSKEY found at edu.
DNSKEY at edu. validated by parent DS record
NSEC3 record found
DNSSEC not supported
```
### Example where DNSSEC validation is successful (shows up as normal)
```
$ ./mydig.py ietf.org -D
QUESTION SECTION:
ietf.org. IN A

ANSWER SECTION:
ietf.org. 1800 IN A 4.31.198.44
ietf.org. 1800 IN RRSIG A 5 2 1800 20190109135858 20180109130036 40452 ietf.org. O8fJkB4ISG/SzpRd0EBvh49pLzR21cXJ EH7ZWUSfpFjXfv7pqIEX9FUMEjP+VHds P7iCQ3Gkd3PQul7PNFqbdMnk4O5NomCy g71J73G4rLlaBYZYTCTVW+8CdgviqrNo IFSzgPcN7kxDdg25YKi5ywjbMqCU9BWh nGw+4kS7TrXtd92c/YUqViYDN0OCTMn5 b05+a6FJd0Fu4iKbYpFQJ1/dDh5F/RAh IGFbOd2/zGK6xCE3IU8ICzRhIJL0ZiNM RtbZOc1uPOeHd3SQ66ZrNRbl0pxwQlzi zRkaeFchCZ9+w71AmrGG0K4BWNNsW1Pw kgJwb/trlWSTroA4X/6oUg==

Query time: 916 msec
WHEN: Tue Feb 13 16:00:48 2018
MSG SIZE rcvd: 994

```
### Example where DNSSEC validation is unsuccessful
```
$ ./mydig.py dnssec-failed.org -D
DNSSEC verification failed
$ ./mydig.py dnssec-failed.org -DT
DNSKEY found at .
DS record at . validated by ZSK
org. 172800 IN NS d0.org.afilias-nst.org.
org. 172800 IN NS a0.org.afilias-nst.info.
org. 172800 IN NS c0.org.afilias-nst.info.
org. 172800 IN NS a2.org.afilias-nst.info.
org. 172800 IN NS b0.org.afilias-nst.org.
org. 172800 IN NS b2.org.afilias-nst.org.
DNSKEY found at org.
DNSKEY at org. validated by parent DS record
DS record at org. validated by ZSK
dnssec-failed.org. 86400 IN NS dns102.comcast.net.
dnssec-failed.org. 86400 IN NS dns105.comcast.net.
dnssec-failed.org. 86400 IN NS dns104.comcast.net.
dnssec-failed.org. 86400 IN NS dns103.comcast.net.
dnssec-failed.org. 86400 IN NS dns101.comcast.net.
DNSKEY found at dnssec-failed.org.
DNSKEY at dnssec-failed.org. NOT validated by parent DS record
DNSSEC verification failed


```

Run `./mydig.py -h` for argument help.
