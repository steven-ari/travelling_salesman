#include <vector>
#include <bits/stdc++.h>
using namespace std;

// check if input is purely unsigned integer
bool check_integer(const string& user_input){
    while(user_input.find_first_not_of("0123456789") != string::npos) {
        return false;
    }
    return true;
}

// print entire graph matrix
void print_graph(const vector<vector<unsigned int>>& graph_matrix){
    
    cout << "\nCurrent Graph: " << endl;
    for (auto const& graph_vec : graph_matrix){
        for (auto const& node : graph_vec){
            cout << node << ' ';
        }
        cout << endl;
    }
}
 
// travelling salesman optimization
unsigned int tsp(const vector<vector<unsigned int>>& graph_matrix){

    // store all nodes    
    vector<unsigned int> nodes(graph_matrix.size());
    iota(nodes.begin(), nodes.end(), 0);
    
    // store minimum energy
    unsigned int min_energy = INT_MAX;
    unsigned int current_node = nodes[0];
    unsigned int current_energy = 0;

    do {
        // store current path energy
        current_node = nodes[0];
        for (const auto& value: nodes){
            current_energy += graph_matrix[current_node][value];
            current_node = value;
        }
        // back to start
        current_energy += graph_matrix[current_node][nodes[0]];
        // check energy, start next permutation
        min_energy = min(min_energy, current_energy);
        current_energy = 0;
 
    } while (
        next_permutation(nodes.begin(), nodes.end()));

    return min_energy;
}
 
// delete node selected by user
void delete_node(vector<vector<unsigned int>>& graph_matrix){
    
    // query which node to be deleted
    unsigned int node_arg;
    string user_input;
    cin.clear();
    cout << "Insert n-th node to be deleted (starts with one), integer equal less than " << graph_matrix.size() << " please: " ;
    cin >> user_input;
    while(!check_integer(user_input) || stoi(user_input) > graph_matrix.size()){
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Invalid value, check instruction!" << endl;     
        cout << "Insert n-th node to be deleted, integer equal less than " << graph_matrix.size() << " please: " ;
        cin >> user_input; 
    }

    // delete for real, determine node
    node_arg = stoi(user_input) - 1;
    
    // delete row
    graph_matrix.erase(graph_matrix.begin() + node_arg);
    // delete column
    for(auto& value: graph_matrix){
        value.erase(value.begin() + node_arg);
    }

}   

// add new node
void add_node(vector<vector<unsigned int>>& graph_matrix){

    vector<unsigned int> new_path_energy(graph_matrix.size());
    
    // query value
    // unsigned int path_energy;
    string user_input;
    for(int i = 0; i<graph_matrix.size(); i++){
        cin.clear();
        cout << "Insert energy to " << i+1 << "-th node please: " ;
        // cin >> path_energy;
        // check against non-integer
        cin >> user_input;
        while(!check_integer(user_input)){
            cin.clear();
            cin.ignore(256, '\n');
            cout << "Invalid value, check instruction!" << endl;
            cout << "Insert energy to " << i+1 << "-th node please: " ;
            cin >> user_input;
        }
        new_path_energy.at(i) = stoi(user_input);
    }

    // print newly added vector
    cout << "\nNew node: ";
    for (auto const& energy : new_path_energy){
        cout << energy << ", " ; 
    }

    // add new node to graph, column-wise
    unsigned int a = 1;
    for(int i = 0; i<graph_matrix.size(); i++){
        graph_matrix[i].push_back(new_path_energy.at(i));
    }

    // add new node to graph, row-wise
    new_path_energy.push_back(0);
    graph_matrix.push_back(new_path_energy);
}   

// Driver Code
int main(){
    // matrix representation of graph
    vector<vector<unsigned int>> graph_matrix = {{ 0, 10, 15, 20 },
                                                { 10, 0, 35, 25 },
                                                { 15, 35, 0, 30 },
                                                { 20, 25, 30, 0 }
                                                };
    const string input_query = "Insert Number Command ('calc': 0, 'add': 1, 'del': 2, 'exit': 3): ";
    print_graph(graph_matrix);

    // Request input
    int task;
    string user_input;
    cout << input_query;
    cin >> user_input;
    while(!check_integer(user_input) || stoi(user_input) > 3){
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Invalid value, check instruction!" << endl;
        cout << input_query;
        cin >> user_input; 
    }
    task = stoi(user_input);

    // working
    while(task != 3){

        // report user input
        cout << "\nYou wrote: " << task << endl;
        print_graph(graph_matrix);

        switch(task){

            // calculate current graph
            case 0: 
                cout << "Current optimal energy: " << tsp(graph_matrix) << endl;
                break;

            // add new node to graph
            case 1: 
                cout << "Add new node(" << graph_matrix.size() +1 << "-th node): " << endl;
                add_node(graph_matrix);

                // calculate current graph
                print_graph(graph_matrix);
                cout << "Current optimal energy: " << tsp(graph_matrix) << endl;
                break;

            // only delete if sensible
            case 2: 
                if (graph_matrix.size() > 2){
                    // delete a node from graph
                    delete_node(graph_matrix);

                    // calculate current graph
                    print_graph(graph_matrix);
                    cout << "Current optimal energy: " << tsp(graph_matrix) << endl;
                }
                else {
                    cout << "Graph too small!" << endl;
                }
                break;

            // wrong input
            default:
                cout << "Invalid value, check instruction!" << endl;
                cout << input_query;
                break;
        }

        // request user input again
        cout << input_query;
        cin >> user_input;
        while(!check_integer(user_input) || stoi(user_input) > 3){
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid value, check instruction!" << endl;
            cout << input_query;
            cin >> user_input; 
        }
        task = stoi(user_input);
    }

    return 0;
}