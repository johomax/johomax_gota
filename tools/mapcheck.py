#!/usr/bin/env python3
"""Map utilities from the probe dump: walkability, clearance, BFS route lengths.
usage: tools/mapcheck.py x,y x,y ...   -> per point: kind, walkable, clearance radius; BFS tile distance between consecutive points
"""
import sys, collections
kinds={}; walk={}
for line in open('runs/probe-002/logs/policy_agent_0.log'):
    p=line.split()
    if p and p[0]=='K':
        row=int(p[1]); x=0
        for v in [int(v) for v in p[2:]]:
            for j in range(7):
                if x+j<128:
                    t=(v>>(4*j))&15; kinds[(x+j,row)]=t&7; walk[(x+j,row)]=t>>3
            x+=7
def clearance(x,y):
    r=0
    while r<6:
        ok=all(walk.get((x+dx,y+dy),0) for dx in range(-r-1,r+2) for dy in range(-r-1,r+2))
        if not ok: return r
        r+=1
    return r
def bfs(a,b):
    q=collections.deque([a]); dist={a:0}
    while q:
        c=q.popleft()
        if c==b: return dist[c]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(c[0]+dx,c[1]+dy)
            if n not in dist and walk.get(n,0): dist[n]=dist[c]+1; q.append(n)
    return None
def snap_wide(x,y,minclear=2,rad=6):
    best=None
    for dx in range(-rad,rad+1):
        for dy in range(-rad,rad+1):
            p=(x+dx,y+dy)
            if walk.get(p,0) and clearance(*p)>=minclear:
                d=dx*dx+dy*dy
                if best is None or d<best[0]: best=(d,p)
    return best[1] if best else None
if __name__=='__main__':
    pts=[tuple(int(v) for v in a.split(',')) for a in sys.argv[1:]]
    prev=None; total=0
    for p in pts:
        k=kinds.get(p,0); w=walk.get(p,0); c=clearance(*p); s=snap_wide(*p)
        d=bfs(prev,p) if prev else 0
        total+=d or 0
        print(f"{p}: kind={k} walk={w} clearance={c} snap_wide={s} bfs_from_prev={d} cum={total}")
        prev=p
