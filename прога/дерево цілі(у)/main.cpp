#include <iostream>
#include "treenode.h"
#include "tree.h"
#include"imdbmovie.h"
using namespace std;



int main()
{
    ImdbMovie M1;
    ImdbMovie M2("Superman", 8.2);
    ImdbMovie M3(M2);
    ImdbMovie M4;



    cout << "Enter movie\n";
    cin >> M1;
    M4.read();



    M1.print();
    M2.print();
    M3.print();
    cout << M4 << "\n";
    cout << "\n";

    M1.setName("Harry Potter");
    M1.setRate(9.5);
    M3.modifyRate(0.2);

    M1.print();
    M2.print();
    M3.print();
    cout << "\n\n";

    M3.getName() = "Superman 2";
    M1.getRate() -= 1.0;
    M1.print();
    M2.print();
    M3.print();
    cout << "\n\n";

    cout << "All movies:\n" << M1.getName() << "\n";
    cout << M2.getName() << "\n" << M3.getName() << "\n\n";

    double avgRate = M1.getRate() + M2.getRate() + M3.getRate();
    avgRate /= 3.0;
    cout << "Avg Rate: " << avgRate << "\n\n";

    /*
    IntTree T1(10);
    T1.addValue(5);
    T1.addValue(7);
    T1.addValue(12);
    T1.addValue(15);
    T1.addValue(3);
    T1.addValue(17);
    T1.visit_RootLeftRight();
    T1.visit_LeftRightRoot();
    cout << "\n\n";



    if (T1.findValue(15))
        cout << "Contains 15!\n";
    if (!T1.findValue(1))
        cout << "No value 1..\n";
    cout << "\n";
    */

    /*
    TreeNode* root = new TreeNode(10);
    addValueInTree(root, 5);
    addValueInTree(root, 7);
    addValueInTree(root, 12);
    addValueInTree(root, 15);
    addValueInTree(root, 3);
    addValueInTree(root, 17);



    if (findValueInTree(root, 7))
        cout << "Contains 7!\n";
    if (findValueInTree(root, 15))
        cout << "Contains 15!\n";
    if (!findValueInTree(root, 1))
        cout << "No 1 in tree.\n";
    if (!findValueInTree(root, 16))
        cout << "No 16 in tree.\n";
    cout << "\n\n";

    visitTree_RootLeftRight(root);
    cout << "\n";

    visitTree_RootRightLeft(root); 
    cout << "\n";

    visitTree_LeftRightRoot(root); 
    cout << "\n";

    visitTree_LeftRootRight(root); 
    cout << "\n";
    */

    return 0;
}