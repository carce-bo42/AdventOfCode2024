class Node:
   def __init__(self, result):
      self.plus = None
      self.mult = None
      self.conc = None
      self.result = result

def generate_tree(node, nbrs, target):

    if node.result > target:
        return False

    if node.result == target:
        if len(nbrs) == 1:
            return True if nbrs[0] == 1 else False
        elif len(nbrs) == 0:
            return True
        else:
            return False

    if len(nbrs) == 0:
        return False

    ret = set()
    node.plus = Node(node.result+nbrs[0])
    node.mult = Node(node.result*nbrs[0])
    node.conc = Node(int(str(node.result)+str(nbrs[0])))

    ret.add(generate_tree(node.plus, nbrs[1:], target))
    ret.add(generate_tree(node.mult, nbrs[1:], target))
    ret.add(generate_tree(node.conc, nbrs[1:], target))

    return True in ret

results = []
operands = []
fname = "input.txt"
with open(fname) as file:
    for line in file:
        results.append(int(line.strip().split(":")[0]))
        operands.append([ int(n.strip()) for n in line.strip().split(":")[1].strip().split(" ") ])

count = 0
for idx, res in enumerate(results):
    node = Node(operands[idx][0])
    if generate_tree(node, operands[idx][1:], res) == True:
        count += res

print(count)