#!/usr/bin/env python

if __name__ == '__main__':

    import newick3, phylo3, numpy, sys

    if len(sys.argv) < 3:
        print "usage: remove_badtips.py <treefile> <maxdevfactor> [keep=\"<tax1, tax2, ...>\"]"
        sys.exit()

    treefname = sys.argv[1]
    treefile = open(treefname, "r")
    tree = newick3.parse(treefile.readline())
    maxdevfactor = int(sys.argv[2])

    if len(sys.argv) > 3:
        keepnames_str = sys.argv[3].split("keep=",1)[1]
        keepnames = [n.strip() for n in keepnames_str.split(",")]
    else:
        keepnames = []

    lengths = [t.length for t in tree.leaves()]

    avg = numpy.mean(lengths)

    for tip in tree.leaves():
    
        if tip.parent == tree:
            continue

        if tip.length > avg * maxdevfactor:
            if tip.label not in keepnames:
                print "pruning " + tip.label
                tip.prune()

            # compress knuckle if there is one
    #        if len(parent.children) == 1:
    #            child = parent.children[0]
    #            if child.label != None:
    #                rightlabel = child.label
    #            else:
    #                rightlabel = ", ".join([leaf.label for leaf in child.leaves()])
    #            print "compressing a knuckle in the tree: " + leftlabel + " | " + rightlabel
    #            pp = parent.parent
    #            pp.remove_child(parent)
    #            pp.add_child(child)

    #nodes_to_remove = []
    for n in tree.descendants():

        nc = n
        while (not nc.istip) and len(nc.children) == 0:
            print "pruning an empty tip"
            np = nc.parent
            nc.prune()
            if np:
                nc = np
            else:
                break

    outfile = open(treefname.rsplit(".tre",1)[0] + ".pruned.tre","w")
    outfile.write(newick3.tostring(tree) + ";")
    outfile.close()
