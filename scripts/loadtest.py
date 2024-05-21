import requests

# f = open("/Users/ronakgarg/Downloads/opendns-top-domains.txt", "r")
#
# urls = []
#
# for line in f:
#     x = "https://www." + line
#     urls.append(x)
#     print(x)
#
# f.close()

f = open("/Users/ronakgarg/RonakProjects/UrlShortener/flaskProject/resources/longurls.txt", "r")
shortUrlFile = open("/Users/ronakgarg/RonakProjects/UrlShortener/flaskProject/resources/shorturls.txt", "w")
shortUrlToLongUrlMapFile = open("/Users/ronakgarg/RonakProjects/UrlShortener/flaskProject/resources"
                                "/shorturltoLongUrlMap.txt", "w")


to_hit = "http://127.0.0.1:5000/shorten_url?url="

# for url in f:
#     x = to_hit + url
#     response = requests.get(x)
#     print(response.text)
#     exit()
x = "https:www.google{data}.com"
for i in range(10**9):
    v = x.format(data=i)
    urltoHit = to_hit + v
    # print(v)
    response = requests.get(urltoHit)

# for url in f:
#     x = to_hit + url
#     response = requests.get(x)
#     shortUrlFile.write(response.text)
#     v = url + "_" + response.text
#     shortUrlToLongUrlMapFile.write(v)

shortUrlFile.close()
shortUrlToLongUrlMapFile.close()



