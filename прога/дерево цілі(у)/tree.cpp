#include "tree.h"
#include <iostream>
using std::cout;



IntNode::IntNode()
    : data(0), left(nullptr), right(nullptr)
{}



IntNode::IntNode(int val)
    : data(val), left(nullptr), right(nullptr)
{}



IntTree::IntTree()
    : root(nullptr)
{}



IntTree::IntTree(int val)
    : root(new IntNode(val))
{}



IntTree::IntTree(IntNode* node)
    : root(node)
{}



void IntTree::add(IntNode*& node, int val)
{
    if (node == nullptr)
    {
        node = new IntNode(val);
    }
    else if (val <= node->data)
    {
        add(node->left, val);
    }
    else
    {
        add(node->right, val);
    }
}



bool IntTree::find(IntNode*& node, int val)
{
    if (node == nullptr)
        return false;



    if (val == node->data)
        return true;
    else if (val < node->data)
        return find(node->left, val);
    else
        return find(node->right, val);
}



void IntTree::visit_RtLR(IntNode*& node)
{
    if (node == nullptr)
        return;



    cout << node->data << "  ";
    visit_RtLR(node->left);
    visit_RtLR(node->right);
}



void IntTree::addValue(int val)
{
    add(root, val);
}



bool IntTree::findValue(int val)
{
    return find(root, val);
}



void IntTree::visit_RootLeftRight()
{
    visit_RtLR(root);
    cout << "\n";
}



void IntTree::visit_LRRt(IntNode*& node)
{
    if (node == nullptr)
        return;



    visit_LRRt(node->left);
    visit_LRRt(node->right);
    cout << node->data << "  ";
}



void IntTree::visit_LeftRightRoot()
{
    visit_LRRt(root);
    cout << "\n";
}