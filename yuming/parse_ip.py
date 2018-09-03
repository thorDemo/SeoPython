
# domain = open('yuming.txt', 'r+')
# ip = open('r_ip.txt', 'w+')
#
# for line in domain:
#     ip.write('www.' + line)
#     ip.write('*.' + line)
#     ip.write(line)

# for num in range(1, 100):
for num in range(1, 20):
    url = 'https://i.youku.com/i/UMzg2NzA3NDcy/videos?spm=a2hzp.8253869.0.0&order=1&page=%s' \
          '&last_item=&last_pn=1&last_vid=949641746'
    # 化工企业 20
    url2 = 'https://so.youku.com/search_video/q_%E5%8C%96%E5%B7%A5%E4%BC%81%E4%B8%9A?spm=a2h' \
           '0k.11417342.pageturning.dpagenumber&f=1&kb=020200000000000__%E5%8C%96%E5%B7%A5%E4%' \
           'BC%81%E4%B8%9A&aaid=98693ca15f89b3dc3b6b1e90b205eb1f&pg=%s'
    # 钢铁企业 15
    url3 = 'https://so.youku.com/search_video/q_%E9%92%A2%E9%93%81%E4%BC%81%E4%B8%9A?spm=a2h0' \
           'k.11417342.pageturning.dpagenumber&f=1&kb=020200000000000__%E9%92%A2%E9%93%81%E4%' \
           'BC%81%E4%B8%9A&aaid=7e0234fe7c9ae38d45e7733c0126ded0&pg=%s'
    # 机械企业 20
    url4 = 'https://so.youku.com/search_video/q_%E6%9C%BA%E6%A2%B0%E4%BC%81%E4%B8%9A?spm=a2h0k' \
           '.11417342.pageturning.dpagenumber&f=1&kb=020200000000000__%E6%9C%BA%E6%A2%B0%E4%BC' \
           '%81%E4%B8%9A&aaid=061beef42d57d2551c6489a5d5120b43&pg=%s'
    # 电子企业 20
    url5 = 'https://so.youku.com/search_video/q_%E7%94%B5%E5%AD%90%E4%BC%81%E4%B8%9A?spm=a2h0k.' \
           '11417342.pageturning.dpagenumber&f=1&kb=020200000000000__%E7%94%B5%E5%AD%90%E4%BC%' \
           '81%E4%B8%9A&aaid=4f82e8d6cc0cf0b6b07bdff8e0ed3808&pg=%s'
    print(url2 % num)
    print(url4 % num)
    print(url5 % num)

