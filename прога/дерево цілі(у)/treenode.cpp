#include "treenode.h"
#include <iostream>
using std::cout;


TreeNode::TreeNode()
    : data(0), left(nullptr), right(nullptr)
{}



TreeNode::TreeNode(int val)
    : data(val), left(nullptr), right(nullptr)
{}

void addValueInTree(TreeNode*& node, int val)
{
    if (node == nullptr)
    {
        node = new TreeNode(val);
    }
    else if (val <= node->data)
    {
        addValueInTree(node->left, val);
    }
    else
    {
        addValueInTree(node->right, val);
    }
}


bool findValueInTree(TreeNode*& node, int val)
{
    if (node == nullptr)
        return false;


    if (val == node->data)
        return true;


    else if (val < node->data)
        return findValueInTree(node->left, val);


    else
        return findValueInTree(node->right, val);
}

void visitTree_RootLeftRight(TreeNode*& node)
{
    if (node == nullptr)
        return;

    cout << node->data << "  ";
    visitTree_RootLeftRight(node->left);
    visitTree_RootLeftRight(node->right);
}

void visitTree_RootRightLeft(TreeNode*& node)
{
    if (node == nullptr)
        return;



    cout << node->data << "  ";
    visitTree_RootRightLeft(node->right);
    visitTree_RootRightLeft(node->left);
}


void visitTree_LeftRightRoot(TreeNode*& node)
{
    if (node == nullptr)
        return;


    visitTree_LeftRightRoot(node->left);
    visitTree_LeftRightRoot(node->right);
    cout << node->data << "  ";
}


void visitTree_LeftRootRight(TreeNode*& node)
{
    if(node==nullptr)
        return;


    visitTree_LeftRootRight(node->left);
    cout << node->data << "  ";
    visitTree_LeftRootRight(node->right);
}