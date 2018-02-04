#include <stdio.h>
#include <unistd.h> // contains getopt and optind

static const char* usage =
"Get information out of DNS\n\n"
"Usage: %s [OPTIONS] name type \n"
"	<name> can be any domain name\n"
"	<type> defaults to A - supports A, CNAME, MX, NS\n\n"
"Options:\n"
"	-D	enable DNSSEC\n"	
"	-h	show this message and exit.\n";

enum dns_type {
	A,
	CNAME,
	MX,
	NS
};


int main(int argc, char** argv){
	char c;
	int dnssec_on = 0;
	while ((c = getopt(argc, argv, "Dh")) != -1){
		switch (c) {
			case 'h':
				printf(usage, argv[0]);
				return 0;
			case 'D':
				dnssec_on = 1;
				break;
			case '?':
				printf(usage, argv[0]);
				return 1;
		}
	}
	printf("DNSSEC is %s\n", dnssec_on ? "on" : "off");
	for (int i = optind; i < argc; i++)
		printf("%s\n",argv[i]);
	return 0;
}
