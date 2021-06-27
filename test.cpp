#include <stdio.h>
#include <cstdlib>
namespace std;

int main (){
    //declare and instantiate vars
    int ranNum, guessNum;
    //create guess number 
    ranNum = rand()%10;
    //give input
    cout << "Guess the number between 1 - 10: ";
    cin >> guessNum;
    //check if num is higher or lower and return result
    while(guessNum != ranNum){
        if(guessNum > ranNum){
            cout << "Random Number is lower than" << guessNum << endl;
        }
        else{
            cout << "Random number is higher than" << guessNum << endl;
        }
        cout << "Guess the number between 1 - 10: ";
        cin >> guessNum;
    }
    //if correct give happy text
    cout << "Number is correct!"<< endl;
}