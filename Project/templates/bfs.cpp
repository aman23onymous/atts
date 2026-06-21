#include<bits/stdc++.h>
using namespace std;

// BFS (Breadth-First Search) is a graph traversal algorithm.
// It explores all nodes at the current level before moving to the next level.
// It is commonly used to find shortest paths in an unweighted graph.
// LIST ARE INBUILT LINKED LIST

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

void bfs(int s){
    queue<int> q;
    q.push(s);
    dis[s]=0;
    vis.insert(s);
    while(q.size()){
        int node=q.front();
        q.pop();
        for(auto x:graph[node]){
            if(vis.find(x)==vis.end()){
                q.push(x);
                vis.insert(x);
                dis[x]=dis[node]+1;
            }
        }
        cout<<node<<" ";
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
    cout<<"\nbfs: ";
    bfs(0);
    cout<<"\nshortest distance: ";
    for(int x:dis) cout<<x<<" ";
}