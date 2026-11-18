import json,os,sys,urllib.error,urllib.request
U=os.getenv("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL")
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
S={}
for i in range(64):
    r=i//8;f=i%8
    S[i]={'p':[0,5,10,20,35,60,100,0][r],
          'n':[-50,-40,-30,-30,-30,-30,-40,-50][r]+[-50,-30,-20,-10,-10,-20,-30,-50][f],
          'b':[-20,-10,-10,-10,-10,-10,-10,-20][r]+[-20,-10,-10,-10,-10,-10,-10,-20][f],
          'r':[0,5,10,20,35,60,100,0][r],
          'q':[0,5,10,20,35,60,100,0][r],
          'k':[0,0,0,0,0,0,0,0][r]}

def F(fen):
    b={}
    for ri,row in enumerate(fen.split()[0].split("/")):
        x=0
        for c in row:
            if c.isdigit():x+=int(c)
            else:b["abcdefgh"[x]+str(8-ri)]=c;x+=1
    return b

def Eval(fen,side):
    b=F(fen);s=0
    for sq,pc in b.items():
        v=V[pc.lower()];i=(8-int(sq[1]))*8+ord(sq[0])-97
        if pc.islower():v=-v
        s+=v+S[i][pc.lower()]
    return s if side=="w" else -s

def Make(fen,move):
    b=F(fen);fr,to=move[:2],move[2:4];pc=b.pop(fr);b[to]=pc
    if len(move)>4:b[to]=move[4].upper() if pc.isupper() else move[4]
    return " ".join(["".join(b.get("abcdefgh"[x]+str(r),"") for x in range(8) for r in range(8,0,-1)),"b" if fen.split()[1]=="w" else "w","-","-","0","1"])

def Nega(fen,side,depth,nodes):
    if depth==0 or nodes<=0:return Eval(fen,side)
    best=-30000
    for m in F(fen).keys():
        if nodes<=0:break
        v=-Nega(Make(fen,m),"b" if side=="w" else "w",depth-1,nodes-1)
        if v>best:best=v
    return best if best>-30000 else Eval(fen,side)

def P(path,body):
    req=urllib.request.Request(U+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(req)as r:return json.load(r)
    except urllib.error.HTTPError as e:sys.exit(f"{path}:{e.code}{e.read().decode()}")

while 1:
    g=P("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        bm=max(g["legal_moves"],key=lambda m:Nega(Make(g["fen"],m),"b" if g["fen"].split()[1]=="w" else "w",4,1000))
        g=P("/move",{"game":g["game"],"move":bm})
    print(g["outcome"],file=sys.stderr)
print(g.get("wins",0),g.get("draws",0),g.get("losses",0),file=sys.stderr)