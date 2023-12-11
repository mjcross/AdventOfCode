from tree import Node, Tree

def parse(stream):
    # first line is the path to be taken (repeats)
    turnSeq = stream.readline().strip()

    # next line is blank
    stream.readline()

    # subsequent lines describe a binary tree
    nodeDir = {}
    tree = Tree()
    while True:
        line = stream.readline().strip()
        if not line:
            break
        nodeName, branches = line.split(' = ')

        branches = branches[1:-1]   # discard enclosing brackets
        leftNodeName, rightNodeName = branches.split(', ')

        # create and link the nodes
        leftNode = nodeDir.get(leftNodeName, Node(name=leftNodeName))
        nodeDir[leftNodeName] = leftNode
        rightNode = nodeDir.get(rightNodeName, Node(name=rightNodeName))
        nodeDir[rightNodeName] = rightNode
        node = nodeDir.get(nodeName, Node(name=nodeName))
        node.left = leftNode
        node.right = rightNode
        nodeDir[nodeName] = node

        # nodes ending in 'A' or 'Z' are start/end nodes
        if nodeName[-1] == 'A':
            if nodeName == 'AAA':
                # primary start node
                tree.startNodes.insert(0, node)
            else:
                tree.startNodes.append(node)
        elif nodeName[-1] == 'Z':
            if nodeName == 'ZZZ':
                tree.endNodes.insert(0, node)
            else:
                tree.endNodes.append(node)
            node.isEndNode = True

    return turnSeq, tree