# Output of mydig program
## Output for A record
```
$ ./mydig.py stonybrook.edu A
QUESTION SECTION:
stonybrook.edu. IN A

ANSWER SECTION:
stonybrook.edu. 900 IN A 129.49.2.176

Query time: 45 msec
WHEN: Tue Feb 13 16:05:58 2018
MSG SIZE rcvd: 48
```
## Output for NS record
```
$ ./mydig.py stonybrook.edu NS
QUESTION SECTION:
stonybrook.edu. IN NS

ANSWER SECTION:
stonybrook.edu. 900 IN NS nocnoc.stonybrook.edu.
stonybrook.edu. 900 IN NS whoisthere.stonybrook.edu.
stonybrook.edu. 900 IN NS mewho.stonybrook.edu.

Query time: 68 msec
WHEN: Tue Feb 13 16:06:04 2018
MSG SIZE rcvd: 98
```
## Output for MX record
```
$ ./mydig.py stonybrook.edu MX
QUESTION SECTION:
stonybrook.edu. IN MX

ANSWER SECTION:
stonybrook.edu. 900 IN MX 1 sbmta2.cc.stonybrook.edu.
stonybrook.edu. 900 IN MX 1 sbmta1.cc.stonybrook.edu.
stonybrook.edu. 900 IN MX 20 syr-t5220-01.syracuse.stonybrook.edu.

Query time: 85 msec
WHEN: Tue Feb 13 16:06:07 2018
MSG SIZE rcvd: 119
```
## Output for CNAME record
```
$ ./mydig.py www.stonybrook.edu CNAME
QUESTION SECTION:
www.stonybrook.edu. IN CNAME

ANSWER SECTION:
www.stonybrook.edu. 900 IN CNAME stonybrook.edu.

Query time: 64 msec
WHEN: Tue Feb 13 16:09:08 2018
MSG SIZE rcvd: 50
```
## Output for A record requiring multiple passes
```
./mydig.py google.co.jp A
QUESTION SECTION:
google.co.jp. IN A

ANSWER SECTION:
google.co.jp. 300 IN A 172.217.9.227

Query time: 724 msec
WHEN: Tue Feb 13 16:09:47 2018
MSG SIZE rcvd: 46
```
Additional resolutions were required for google.co.jp. Usually, there are
additional fields that provide the address for NS records, but in this case,
there were no additional records.  Thus, we needed to resolve the IP address for
the name servers recursively ourselves.
