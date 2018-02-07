#!/usr/bin/env python3
import argparse
import dns.message
import dns.query
from time import localtime, strftime
from timeit import default_timer as timer

# Function to contact root server, then top level domain, then name server
def query_server(domain, typ, trace=False):
    # intial root servers to query
    root_servers = (
    '198.41.0.4', # a.root-servers.net
    '199.9.14.201', # b.root-servers.net
    '192.33.4.12', # c.root-servers.net
    '199.7.91.13', # d.root-servers.net
    '192.203.230.10', # e.root-servers.net
    '192.5.5.241', # f.root-servers.net
    '192.112.36.4', # g.root-servers.net
    '198.97.190.53', # h.root-servers.net
    '192.36.148.17', # i.root-servers.net
    '192.58.128.30' # j.root-servers.net
    '193.0.14.129', # k.root-servers.net
    '199.7.83.42', # l.root-servers.net
    '202.12.27.33' # m.root-servers.net
    )
    query = dns.message.make_query(domain, typ)
    servers = root_servers
    total_time = 0
    output = ""
    if not trace:
        output += "QUESTION SECTION:\n"
        output += query.question[0].to_text()
        output += "\n\nANSWER SECTION:\n"
    while True:
        resp = None
        for server in servers:
            try:
                start_time = timer()
                resp = dns.query.udp(query, server, timeout=2.0)
                end_time = timer()
                total_time += end_time - start_time
                break
            except:
                continue
        if not resp:
            print("Something crazy happened! All servers are down!")
            return
        if resp.answer:
            output += resp.answer[0].to_text() + '\n'
            if resp.answer[0].rdtype == dns.rdatatype.CNAME:
                domain = resp.answer[0][0].target
                query = dns.message.make_query(domain, typ)
                servers = root_servers
                continue
            if not trace:
                output += '\n'
                output += "Query time: {} msec\n".format(int(total_time*1000))
                output += "WHEN: {}\n".format(strftime("%a %b %-d %H:%M:%S %Y"))
                output += "MSG SIZE rcvd: {}".format(len(resp.to_wire()))
            print(output)
            return
        if resp.additional:
            if trace:
                output += resp.authority[0].to_text() + '\n'
            rrset = resp.additional
            ns_servers = []
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.A:
                    ns_servers.append(rr[0].address)
            servers = ns_servers
        else:
            if not trace:
                output += "Query time: {} msec\n".format(total_time)
                output += "WHEN: {}\n".format(strftime("%a %b %-d %H:%M:%S %Y"))
                output += "MSG SIZE rcvd: {}".format(len(resp.to_wire()))
            print(output)
            return

def main():
    parser = argparse.ArgumentParser(description="Get information out of DNS")
    parser.add_argument('name', metavar='name', type=str,
            help='can be any domain name')
    parser.add_argument('type', metavar='type', type=str, nargs='?', default='A',
            help='defaults to A - supports A, MX, NS')
    parser.add_argument('-D', dest='DNSSEC', action='store_true',
            help='enable DNSSEC in query')
    parser.add_argument('-T', dest='trace', action='store_true',
            help='trace name from the root down')
    args = parser.parse_args()
    query_server(args.name,args.type,args.trace)


if __name__ == "__main__":
    main()
