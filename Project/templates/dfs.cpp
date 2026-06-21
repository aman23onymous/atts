#include<bits/stdc++.h>
using namespace std;

// DFS (Depth-First Search) is a graph traversal algorithm.
// It explores as far as possible along each branch before backtracking.
// It is commonly used to find connected components, cycles, and topological ordering.

vector<vector<int>> graph;
int v;
vector<int> dis;
bool bi_dir;
unordered_set<int> vis;
void add_edge(int s,int e){
    graph[s].push_back(e);
    if(bi_dir) graph[e].push_back(s);
}
void display(){
    for(int i=0;i<v;i++){
        cout<<i<<" -> ";
        for(auto &ele:graph[i]){
            cout<<ele<<" , ";
        }
        cout<<"\n";
    }
}

void dfs(int s){
    vis.insert(s);
    cout<<s<<" ";
    for(auto x:graph[s]){
        if(vis.find(x)==vis.end()){
            dfs(x);
        }
    }
}

int main(){
    cout<<"NO. of Vertices  and edges and 1 if bidirectional else 0:";
    cin>>v;
    graph.resize(v);
    dis.resize(v);
    int e;
    cin>>e>>bi_dir;
    vis.clear();
    cout<<bi_dir<<"\n";
    while(e--){
        int src,dst;
        cin>>src>>dst;
        add_edge(src,dst);
    }
    display();
    cout<<"\ndfs: ";
    dfs(0);
    cout<<"\nshortest distance: ";
    for(int x:dis) cout<<x<<" ";
}