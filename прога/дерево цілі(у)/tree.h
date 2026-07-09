#pragma once

struct IntNode
{
	int data;
	IntNode* left;
	IntNode* right;

	IntNode();
	IntNode(int val);
};

class IntTree
{
private:
    IntNode* root;

    void add(IntNode*& node, int val);
    bool find(IntNode*& node, int val);
    void visit_RtLR(IntNode*& node);
    void visit_LRRt(IntNode*& node);

public:
    IntTree();
    IntTree(int val);
    IntTree(IntNode* node);

    void addValue(int val);
    bool findValue(int val);
    void visit_RootLeftRight();
    void visit_LeftRightRoot();
};

