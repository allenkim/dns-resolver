import subprocess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mydig import query_server

def extract_query_time(response):
    query_line = [l for l in response.split('\n') if "Query" in l][0]
    t = [int(i) for i in query_line.split() if i.isdigit()]
    return t

def test_url_time(url, status=False):
    mydig_str = query_server(url,"A")
    if status:
        print(url + ": mydig done")

    proc = subprocess.Popen(["drill", "@209.222.18.222", url], stdout=subprocess.PIPE)
    output, error = proc.communicate()
    local_str = output.decode('utf-8')
    if status:
        print(url + ": localdig done")

    proc = subprocess.Popen(["drill","@8.8.8.8", url], stdout=subprocess.PIPE)
    output, error = proc.communicate()
    google_str = output.decode('utf-8')
    if status:
        print(url + ": googledig done")

    mydig_time = extract_query_time(mydig_str)[0]
    local_time = extract_query_time(local_str)[0]
    google_time = extract_query_time(google_str)[0]
    return (mydig_time, local_time, google_time)

def main():
    top_sites = [
        "google.com",
        "youtube.com",
        "facebook.com",
        "baidu.com",
        "wikipedia.org",
        "reddit.com",
        "yahoo.com",
        "google.co.in",
        "qq.com",
        "taobao.com",
        "amazon.com",
        "twitter.com",
        "tmall.com",
        "google.co.jp",
        "live.com",
        "instagram.com",
        "vk.com",
        "sohu.com",
        "sina.com.cn",
        "jd.com",
        "weibo.com",
        "360.cn",
        "google.de",
        "google.co.uk",
        "google.com.br"
    ]
    # Results hard coded after running the tests
    mydig_times = [65.8, 65.4, 58.4, 307.9, 84.4, 86.7, 50.8, 155.9, 300.9, 125.7, 62.6, 50.0, 152.4, 518.4, 92.2, 71.5, 433.1, 300.4, 715.4, 538.1, 298.8, 825.0, 215.2, 135.0, 278.3]
    local_times = [2.9,  4.1,  2.7,  25.2,  10.5, 2.9,  2.3,  4.8,   35.2,  25.7,  3.3,  2.8,  25.6,  4.5,   2.8,  4.6,  2.7,   26.0,  25.9,  26.1,  29.1,  34.4,  4.8,   4.3,   4.0]
    google_times = [4.0,  21.0, 4.4,  6.5,   25.9, 3.9,  3.7,  19.0,  5.1,   5.3,   4.0,  3.5,  102.4, 18.7,  3.6,  3.7,  3.3,   183.3, 62.0,  155.6, 11.8,  100.1, 19.0,  18.3,  18.4]
    """
    NUM_AVG = 10
    for i,url in enumerate(top_sites):
        a_sum = b_sum = c_sum = 0
        for _ in range(NUM_AVG):
            a, b, c = test_url_time(url,status=False)
            a_sum += a
            b_sum += b
            c_sum += c
        mydig_times.append(a_sum/NUM_AVG)
        local_times.append(b_sum/NUM_AVG)
        google_times.append(c_sum/NUM_AVG)
        print("Finished website #{}".format(i+1))
    print(mydig_times)
    print(local_times)
    print(google_times)
    """
    A,B,C = mydig_times,local_times,google_times
    n = np.arange(1,len(A)+1) / np.float(len(A))
    As = np.sort(A)
    Bs = np.sort(B)
    Cs = np.sort(C)
    fig, ax = plt.subplots()
    ax.step(As,n,label="My DNS resolver")
    ax.step(Bs,n,label="Local DNS resolver")
    ax.step(Cs,n,label="Google's DNS resolver")
    ax.set(xlabel='Query time (ms)', ylabel='Cumulative Probability')
    ax.set_title("CDF of Query time of DNS Resolvers for the Top 25 Websites")
    ax.legend()
    plt.show()

if __name__=="__main__":
    main()
