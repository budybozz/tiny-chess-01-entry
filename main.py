import json,os,sys,urllib.error,urllib.request as u
U=os.getenv("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL")
V=[0,100,320,330,500,900,2e4]
def P(p,b):
    r=u.Request(U+p,data=json.dumps(b).encode(),headers={"c":"application/json"})
    try:return json.load(u.urlopen(r))
    except u.HTTPError as e:sys.exit(f"{p}:{e.code}{e.read().decode()}")
def F(s):
    b=[0]*128
    for ri,ro in enumerate(s.split()[0].split("/")):
        x=0
        for c in ro:
            if c.isdigit():x+=int(c)
            else:
                q=(7-ri)*16+x
                v="pnbrqk".find(c.lower())+1
                if c.islower():v=-v
                b[q]=v;x+=1
    st=s.split()
    return b,1 if st[1]=="w"else -1,st[2],st[3]if len(st)>3else"-"
def E(b,s):
    t=0
    for i in b:
        if i:
            v=V[abs(i)]
            t+=v if i>0 else -v
    return t*s
def G(b,s,c,e):
    m=[];D=(-16,-15,-17,1,16,15,17,-1);N=(-33,-31,-18,-14,14,18,31,33)
    for i in range(128):
        p=b[i]
        if p*s<=0:continue
        a=abs(p)
        if a==1:
            d=16*s
            if 0<=i+d<128 and not b[i+d]:m+=(i,i+d,0),
            for o in(15,17):
                t=i+s*o
                if 0<=t<128 and b[t]*s<0:m+=(i,t,0),
        elif a==2:
            for o in N:
                t=i+o
                if 0<=t<128 and b[t]*s<=0 and(i&8)==(t&8):m+=(i,t,0),
        elif a in(3,5):
            for o in D:
                t=i+o
                while 0<=t<128:
                    if b[t]*s>0:break
                    m+=(i,t,0),
                    if b[t]:break
                    t+=o
        elif a==4:
            for o in(1,-1,16,-16):
                t=i+o
                while 0<=t<128 and(t&8)==(i&8)+o//8*8:
                    if b[t]*s>0:break
                    m+=(i,t,0),
                    if b[t]:break
                    t+=o
        elif a==6:
            for o in D:
                t=i+o
                if 0<=t<128 and b[t]*s<=0:m+=(i,t,0),
    return m
def M(b,s,c,e,o):
    nb=b[:];f,t,pr=o;p=nb[f];nb[f]=0
    if pr:p=pr*s
    nb[t]=p
    return nb,-s,c,e
def I(b,s):
    k=next(i for i in range(128)if b[i]==6*s)
    for i in range(128):
        p=b[i]
        if p*s>=0:continue
        a=abs(p)
        if a==1:
            if s==1and(i-15==k or i-17==k):return 1
            if s==-1and(i+15==k or i+17==k):return 1
        elif a==2:
            for o in(-33,-31,-18,-14,14,18,31,33):
                if i+o==k and(i&8)==(k&8):return 1
        elif a in(3,5):
            for o in(-16,-15,-17,1,16,15,17,-1):
                t=i+o
                while 0<=t<128:
                    if t==k:return 1
                    if b[t]:break
                    t+=o
        elif a==4:
            for o in(1,-1,16,-16):
                t=i+o
                while 0<=t<128 and(t&8)==(i&8)+o//8*8:
                    if t==k:return 1
                    if b[t]:break
                    t+=o
        elif a==6:
            for o in(-16,-15,-17,1,16,15,17,-1):
                if i+o==k:return 1
    return 0
def U(f,t,pr):
    return chr(97+f%16)+str(8-f//16)+chr(97+t%16)+str(8-t//16)+("q"if pr else"")
def A(b,s,c,e,d,a,B,n):
    if d==0 or n[0]<=0:return E(b,s),None
    n[0]-=1
    bst=-3e4;bm=None
    for o in G(b,s,c,e):
        nb,ns,nc,ne=M(b,s,c,e,o)
        if I(nb,-s):continue
        v=-A(nb,ns,nc,ne,d-1,-B,-a,n)[0]
        if v>bst:bst=v;bm=o
        if v>a:a=v
        if a>=B:break
    return(bst,bm)if bm else(E(b,s),None)
while 1:
    g=P("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        b,s,c,e=F(g["fen"])
        C=sum(x for x,v in zip((1,2,4,8),("K","Q","k","q"))if v in g["fen"].split()[2])
        n=[2e5]
        _,bm=A(b,s,C,e,4,-3e4,3e4,n)
        g=P("/move",{"game":g["game"],"move":U(*bm)if bm else g["legal_moves"][0]})
    print(g["outcome"],file=sys.stderr)
print(g.get("wins",0),g.get("draws",0),g.get("losses",0),file=sys.stderr)