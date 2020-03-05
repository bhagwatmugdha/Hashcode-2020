#include<bits/stdc++.h>
using namespace std;

vector<string> get_vector_from_string(string str) {
	istringstream iss(str);
	vector<string> inputs{istream_iterator<string>{iss}, istream_iterator<string>{}};
	return inputs;
}

vector<int> str_to_int(vector<string> s) {
	vector<int> v(s.size());

	for(int i=0; i<s.size(); i++) {
		v[i] = stoi(s[i]);	
	}

	return v;
}

int main() {
	ifstream input_file("a_example.in");
	string line;

	getline (input_file, line);

	vector<int> inputs = str_to_int(get_vector_from_string(line));

	int m, n;
	m = inputs[0];
	n = inputs[1];		
	
	cout<<m<<endl;
	cout<<n<<endl;

	input_file.close();

	ofstream sol_file("sol.txt");

	sol_file<<m<<" "<<n;

	sol_file.close();


	return 0;
}
