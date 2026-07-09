#pragma once
struct TreeNode
{
	int data;
	TreeNode* left;
	TreeNode* right;

	TreeNode();
	TreeNode(int val);
};

//add int value in the tree
void addValueInTree(TreeNode*& node, int val);

//find int value in the tree
bool findValueInTree(TreeNode*& node, int val);

// visit tree Root-Left-Right
void visitTree_RootLeftRight(TreeNode*& node);

// visit tree Root-Right-Left
void visitTree_RootRightLeft(TreeNode*& node);

// visit tree Left-Right-Root
void visitTree_LeftRightRoot(TreeNode*& node);

// visit tree Left-Root-Right
void visitTree_LeftRootRight(TreeNode*& node);