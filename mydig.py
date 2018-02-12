#!/usr/bin/env python3
import argparse # parsing arguments
import dns.message # construct single iterative query
import dns.query # sending query using UDP
import dns.dnssec # validating DNSSEC signatures
import dns.resolver # resolving DNSKEY
from time import localtime, strftime
from timeit import default_timer as timer

def compute_ds_hash(owner, rdata, digest_type):
    """ Compute the hash of a DNSKEY
    Used for checking against parent DS record
    digest = digest_algorithm( DNSKEY owner name | DNSKEY RDATA);
    
    owner: domain such as mewho.stonybrook.edu
    rdata: key signing key DNSKEY object
    digest_type: 1 - SHA1, 2 - SHA256 (found in DS record)
    Full details in RFC4034
    """
    digest_type = int(digest_type)
    s = b''
    for name in owner.split('.'):
        s += bytes([len(name)]) + str.encode(name,encoding='ascii')
    s += rdata.to_digestable()
    hash_func = None
    if digest_type == 1:
        hash_func = dns.hash.get('sha1')
    elif digest_type == 2:
        hash_func = dns.hash.get('sha256')
    else:
        return None
    return hash_func(s)


def find_rdtype(rrset_arr, rdtype):
    """Returns the index of the rdtype in the rrset array, -1 if doesn't exist"""
    for idx, rrset in enumerate(rrset_arr):
        if rrset.rdtype == rdtype:
            return idx
    return -1

def query_server(domain, typ, dnssec=False, trace=False, simple=False):
    """Contacts root server, then top level domain, then name server
    May take more than one pass if address is not given in additional response
    """
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

    query = dns.message.make_query(domain, typ, want_dnssec=dnssec)
    resp = None
    if dnssec:
        dnskey_resp = dns.resolver.query('.','DNSKEY').response
        keys = {}
        parent_ds = None
    servers = root_servers
    curr_domain = '.'
    total_time = 0
    output = ""
    if not trace and not simple:
        output += "QUESTION SECTION:\n"
        output += query.question[0].to_text()
        output += "\n\nANSWER SECTION:\n"
    while True:
        for server in servers:
            try:
                resp = dns.query.udp(query, server, timeout=2.0)
                break
            except:
                continue
        if not resp:
            return "Something crazy happened! All servers are down!"
        if dnssec:
            if dnskey_resp and dnskey_resp.answer:
                dnskey = dnskey_resp.answer[0]
                keys[dnskey.name] = dnskey
                if trace:
                    print("DNSKEY found at {}".format(curr_domain))
                if parent_ds:
                    valid = False
                    for key in dnskey:
                        dnskey_hash = compute_ds_hash(dnskey.name.to_text(), key, parent_ds.digest_type)
                        if parent_ds.digest.hex() == dnskey_hash.hexdigest():
                            if trace:
                                print("DNSKEY at {} validated by parent DS record".format(curr_domain))
                            valid = True
                            break
                    if not valid:
                        if trace:
                            print("DNSKEY at {} NOT validated by parent DS record".format(curr_domain))
                        return "DNSSEC verification failed"
            else:
                print("DNSKEY NOT found at {}".format(curr_domain))
                dnssec = False
        if resp.answer:
            if not simple:
                for rans in resp.answer:
                    output += rans.to_text() + '\n'
            cname_idx = find_rdtype(resp.answer, dns.rdatatype.CNAME)
            if cname_idx != -1:
                if typ == "CNAME":
                    break
                domain = resp.answer[cname_idx][0].target
                query = dns.message.make_query(domain, typ, want_dnssec=dnssec)
                servers = root_servers
                continue
            typ_idx = find_rdtype(resp.answer, dns.rdatatype.from_text(typ))
            rrsig_idx = find_rdtype(resp.answer, dns.rdatatype.RRSIG)
            if typ_idx != -1 and simple:
                output += resp.answer[typ_idx][0].address
                return output
            if dnssec:
                rrset = resp.answer[typ_idx]
                rrsetsig = resp.answer[rrsig_idx]
                try:
                    dns.dnssec.validate(rrset,rrsetsig,keys)
                    if trace:
                        print("{} record validated with RRSIG at {}".format(typ,curr_domain))
                except:
                    if trace:
                        print("{} record INVALID at {}".format(typ,curr_domain))
                    return "DNSSEC verification failed"
            break
        if resp.authority:
            ns_servers = []
            ns_idx = find_rdtype(resp.authority, dns.rdatatype.NS)
            if dnssec:
                ds_idx = find_rdtype(resp.authority, dns.rdatatype.DS)
                nsec3_idx = find_rdtype(resp.authority, dns.rdatatype.NSEC3)
                rrsig_idx = find_rdtype(resp.authority, dns.rdatatype.RRSIG)
                if nsec3_idx != -1:
                    return "DNSSEC not supported"
                else:
                    ds = resp.authority[ds_idx]
                    dssig = resp.authority[rrsig_idx]
                    try:
                        dns.dnssec.validate(ds, dssig, keys)
                        parent_ds = ds[0]
                        if trace:
                            print("DS record at {} validated by ZSK".format(curr_domain))
                    except:
                        if trace:
                            print("DS record at {} NOT validated by ZSK".format(curr_domain))
                        return "DNSSEC verification failed"

            if ns_idx != -1:
                ns = resp.authority[ns_idx]
                curr_domain = ns.name
                try:
                    dnskey_resp = dns.resolver.query(ns.name,'DNSKEY').response
                except:
                    dnskey_resp = None
                if trace:
                    output += ns.to_text() + '\n'
                if resp.additional:
                    for radd in resp.additional:
                        if radd.rdtype == dns.rdatatype.A:
                            ns_servers.append(radd[0].address)
                else:
                    for server in ns:
                        ns_servers.append(query_server(server.to_text(),'A',simple=True))
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
    parser.add_argument('-D', dest='dnssec', action='store_true',
            help='enable DNSSEC in query')
    parser.add_argument('-T', dest='trace', action='store_true',
            help='trace name from the root down')
    args = parser.parse_args()
    info = query_server(args.name,args.type,args.dnssec,args.trace)
    print(info)

if __name__ == "__main__":
    main()
