#include<bits/stdc++.h>
using namespace std;

// Disjoint Set Union (DSU) / Union-Find keeps track of connected components.
// It supports two main operations: find(x) and union(a, b).
// It is commonly used for detecting cycles and connecting groups efficiently.

int find(vector<int>&par,int x){
    return par[x]=(x==par[x])?x:find(par,par[x]);
}

void Union(vector<int>&par,vector<int>&rank,int a,int b){
    a=find(par,a);
    b=find(par,b);
    if(rank[a]>=rank[b]){
        par[b]=a;
        rank[a]++;
    }
    else{
        par[a]=b;
        rank[b]++;
    }
}

int main(){
    int n,m;
    cin>>n>>m;
    vector<int> par(n+1,1),rank(n+1,1);
    for(int i=1;i<=n;i++) par[i]=i;
    while(m--){
        int c;
        cin>>c;
        if(c==1){
            int x,y;
            cin>>x>>y;
            Union(par,rank,x,y);
        }
        else{
            int x;
            cin>>x;
            cout<<find(par,x);
        }
    }
}