import requests

def Inspection(iprange,port="80",figure="200",page="/"):
    ip = iprange.split('.')
    if not page.startswith('/'):
        page = '/' + page
    res = []
    target = []
    krange = []
    for i in ip[1:]:
        ran = i.split('-')
        if len(ran) == 1:
            krange.append((i,i))
        elif len(ran) == 2:
            krange.append((ran[0],ran[1]))
    for a in xrange(int(krange[0][0]),int(krange[0][1])+1):
        for b in xrange(int(krange[1][0]),int(krange[1][1])+1):
            for c in xrange(int(krange[2][0]),int(krange[2][1])+1):
                target.append(("%s.%d.%d.%d:%s%s"%(ip[0],a,b,c,port,page),"%s.%d.%d.%d:%s"%(ip[0],a,b,c,port)))
    if figure == 'all':
        for t in target:
            res.append(t[1])
        return res
    # print target
    for i in target:
        #filter by figure
        try:
            response = requests.get(i[0],timeout=3)
            cont = response.content
            code = response.status_code
        except:
            cont = ''
            code = 404
        if figure == '200' and code == 200:
            res.append(i[1])
        elif figure in cont:
            res.append(i[1])
    return res

#huasir
def I():
    iprange = 'http://172.16.10-40.13'
    port = "80"
    figure = "200"
    page = "/"
    print Inspection(iprange,port,figure,page)

if __name__ == '__main__':
    I()