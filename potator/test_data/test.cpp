#include<iostream>
#include<string>
using namespace std;

void test_function(string message) {
    cout << message << endl;
}


int main(int argc, char** argv) {
    test_function("test");
    return 0;
}