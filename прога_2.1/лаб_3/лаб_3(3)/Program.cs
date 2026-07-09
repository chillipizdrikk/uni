using System;

public class Node
{
    public int Id { get; set; }
    public int Value { get; set; }
    public Node Left { get; set; }
    public Node Right { get; set; }

    public Node(int id, int value)
    {
        Id = id;
        Value = value;
        Left = null;
        Right = null;
    }
}

public class BinaryTree
{
    private Node root;

    public BinaryTree()
    {
        root = null;
    }

    public void Insert(int id, int value)
    {
        root = InsertRec(root, id, value);
    }

    private Node InsertRec(Node root, int id, int value)
    {
        if (root == null)
        {
            return new Node(id, value);
        }

        if (value < root.Value)
        {
            root.Left = InsertRec(root.Left, id, value);
        }
        else
        {
            root.Right = InsertRec(root.Right, id, value);
        }

        return root;
    }

    public void PrintMaxValuePath()
    {
        var maxSum = int.MinValue;
        Node maxSumLeaf = null;
        FindMaxSumLeaf(root, 0, ref maxSum, ref maxSumLeaf);

        Console.WriteLine("Path from leaf to root with maximum value sum:");
        PrintPath(root, maxSumLeaf);
    }

    private bool FindMaxSumLeaf(Node node, int currentSum, ref int maxSum, ref Node maxSumLeaf)
    {
        if (node == null)
        {
            return false;
        }

        currentSum += node.Value;

        if (node.Left == null && node.Right == null)
        {
            if (currentSum > maxSum)
            {
                maxSum = currentSum;
                maxSumLeaf = node;
            }
            return true;
        }

        bool leftFound = FindMaxSumLeaf(node.Left, currentSum, ref maxSum, ref maxSumLeaf);
        bool rightFound = FindMaxSumLeaf(node.Right, currentSum, ref maxSum, ref maxSumLeaf);

        return leftFound || rightFound;
    }

 
    private bool PrintPath(Node root, Node target)
    {
        if (root == null)
        {
            return false;
        }

        if (root == target)
        {
            Console.Write($"{root.Id} ");
            return true;
        }

        if (PrintPath(root.Right, target) || PrintPath(root.Left, target))
        {
            Console.Write($"{root.Id} ");
            return true;
        }

        return false;
    }

}

class Program
{
    static void Main(string[] args)
    {
        BinaryTree tree = new BinaryTree();

        tree.Insert(1, 10);
        tree.Insert(2, 5);
        tree.Insert(3, 15);
        tree.Insert(4, 3);
        tree.Insert(5, 7);
        tree.Insert(6, 18);

        tree.PrintMaxValuePath();
    }
}