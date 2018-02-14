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
    mydig_times = []
    local_times = []
    google_times = []
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
    sns.distplot(mydig_times,hist=False,kde_kws={'cumulative':True,'label':"My DNS resolver"})
    sns.distplot(local_times,hist=False,kde_kws={'cumulative':True,'label':"Local DNS resolver"})
    ax = sns.distplot(google_times,hist=False,kde_kws={'cumulative':True,'label':"Google's DNS resolver"})
    ax.set(xlabel='Query time (ms)', ylabel='Cumulative Probability')
    ax.set_title("CDF of Query time of DNS Resolvers for the Top 25 Websites")
    plt.show()

if __name__=="__main__":
    main()
