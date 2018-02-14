# Explanation of results

Below, I have the actual numbers of the queries used to generate the CDF
starting from the top website and going to the 25th ranked website. The order is
as described below.

My resolver, Local resolver, Google's resolver
1      2     3     4      5     6     7     8      9      10     11    12    13     14     15    16    17     18     19     20     21     22     23     24     25
[65.8, 65.4, 58.4, 307.9, 84.4, 86.7, 50.8, 155.9, 300.9, 125.7, 62.6, 50.0, 152.4, 518.4, 92.2, 71.5, 433.1, 300.4, 715.4, 538.1, 298.8, 825.0, 215.2, 135.0, 278.3]
[2.9,  4.1,  2.7,  25.2,  10.5, 2.9,  2.3,  4.8,   35.2,  25.7,  3.3,  2.8,  25.6,  4.5,   2.8,  4.6,  2.7,   26.0,  25.9,  26.1,  29.1,  34.4,  4.8,   4.3,   4.0]
[4.0,  21.0, 4.4,  6.5,   25.9, 3.9,  3.7,  19.0,  5.1,   5.3,   4.0,  3.5,  102.4, 18.7,  3.6,  3.7,  3.3,   183.3, 62.0,  155.6, 11.8,  100.1, 19.0,  18.3,  18.4]

From this, I can see that my resolver is clearly slower, and this is most likely
due to fact that DNS resolvers employ caching to return results much faster.
Particularly for commonly visited websites, we would expect their queries to be
cached and would thus would not have to actually query servers for their
response. The local resolver has the lowest query times, which is probably due
to the fact that it is closest to us. The websites that took longer to resolve
such as number 22 - 360.cn - was due to the fact that additional resolutions
were required. However, with proper caching, this could also be greatly speeded
up.

