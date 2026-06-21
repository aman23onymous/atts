#include<bits/stdc++.h>
using namespace std;

// Dijkstra's algorithm finds the shortest path from a source node
// to all other nodes in a graph with non-negative edge weights.
// It uses a priority queue to always pick the node with the smallest distance.

int n,m;
vector<vector<pair<int,int>>> graph;
void show_path(int d,vector<int>&par){
    if(par[d]==-1){
        cout<<d<<"->";
        return;
    }
    show_path(par[d],par);
    cout<<d<<"->";
}
int dijkstra(int s,int d){
    set<int> vis;
    vector<int> par(n,-1),dis(n,INT_MAX);
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
    dis[s]=0;
    pq.push({0,s});
    while(pq.size()){
        auto x=pq.top();
        pq.pop();
        if(vis.find(x.second)!=vis.end()) continue;
        vis.insert(x.second);
        for(auto&neb:graph[x.second]){
            if(vis.find(neb.first)==vis.end() and dis[neb.first]>dis[x.second]+neb.second){
                pq.push({dis[x.second]+neb.second,neb.first});
                dis[neb.first]=dis[x.second]+neb.second;
                par[neb.first]=x.second;
            }
        }
    }
    show_path(d,par);
    return dis[d];
}

int main(){
    cin>>n>>m;
    graph.resize(n);
    while(m--){
        int a,b,wt;
        cin>>a>>b>>wt;
        graph[a].push_back({b,wt});
        graph[b].push_back({a,wt});
    }
    int s,d;
    cin>>s>>d;
    cout<<prims(s,d);
}
