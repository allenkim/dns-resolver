# Python DNS Resolver

dns-resolver is a simple DNS resolver written in Python3 using only dnspython as an external library.

To run the program, we can first give it executable permission to run it like an executable as opposed to writing python everytime.
```
chmod +x mydig.py
```

Usage examples:

Basic usage - defaults to type A
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
Tracing the resolver
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

Run `./mydig.py -h` for argument help.
