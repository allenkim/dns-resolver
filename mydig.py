#!/usr/bin/env python3
import argparse
import dns.message
import dns.query
from time import localtime, strftime
from timeit import default_timer as timer

# Function to contact root server, then top level domain, then name server
def query_server(domain, typ, trace=False, simple=False):
    start_time = timer()
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
    if not trace and not simple:
        output += "QUESTION SECTION:\n"
        output += query.question[0].to_text()
        output += "\n\nANSWER SECTION:\n"
    while True:
        resp = None
        for server in servers:
            try:
                resp = dns.query.udp(query, server, timeout=2.0)
                break
            except:
                continue
        if not resp:
            return "Something crazy happened! All servers are down!"
        if resp.answer:
            if not simple:
                output += resp.answer[0].to_text() + '\n'
            if resp.answer[0].rdtype == dns.rdatatype.CNAME:
                domain = resp.answer[0][0].target
                query = dns.message.make_query(domain, typ)
                servers = root_servers
                continue
            end_time = timer()
            total_time += end_time - start_time
            if not trace and not simple:
                output += '\n'
                output += "Query time: {} msec\n".format(int(total_time*1000))
                output += "WHEN: {}\n".format(strftime("%a %b %-d %H:%M:%S %Y"))
                output += "MSG SIZE rcvd: {}".format(len(resp.to_wire()))
            if simple:
                output += resp.answer[0][0].address
            return output
        if resp.authority:
            ns_servers = []
            if resp.additional:
                if trace:
                    output += resp.authority[0].to_text() + '\n'
                rrset = resp.additional
                for rr in rrset:
                    if rr.rdtype == dns.rdatatype.A:
                        ns_servers.append(rr[0].address)
            else:
                rauth = resp.authority[0]
                for auth in rauth:
                    if auth.rdtype == dns.rdatatype.NS:
                        ns_servers.append(query_server(auth.to_text(),'A',simple=True))
            if ns_servers:
                servers = ns_servers
                continue
        end_time = timer()
        total_time += end_time - start_time
        if not trace and not simple:
            output += "\n"
            output += "Query time: {} msec\n".format(int(total_time*1000))
            output += "WHEN: {}\n".format(strftime("%a %b %-d %H:%M:%S %Y"))
            output += "MSG SIZE rcvd: {}".format(len(resp.to_wire()))
        return output

def main():
    parser = argparse.ArgumentParser(description="Get information out of DNS")
    parser.add_argument('name', metavar='name', type=str,
            help='can be any domain name')
    parser.add_argument('type', metavar='type', type=str, nargs='?', default='A',
            help='defaults to A')
    parser.add_argument('-D', dest='DNSSEC', action='store_true',
            help='enable DNSSEC in query')
    parser.add_argument('-T', dest='trace', action='store_true',
            help='trace name from the root down')
    args = parser.parse_args()
    info = query_server(args.name,args.type,args.trace)
    print(info)

if __name__ == "__main__":
    main()
