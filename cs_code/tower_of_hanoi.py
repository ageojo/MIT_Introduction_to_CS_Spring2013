def movePiece (orig, dest):
   print "move from " + str(orig) + " to " + str(dest)
   x = raw_input()

   tomove = T[orig][len(T[orig])-1]
   T[dest].append(tomove)
   T[orig].remove(tomove)

   print T[0]
   print T[1]
   print T[2]


# need temp place to place third peg w/ all discs?

def getother(orig, dest):
   t = [0, 1, 2]
   t.remove(orig)
   t.remove(dest)
   return t[0]


def moveTower(orig, dest, n):
   if n==1: movePiece(orig, dest)
   else:
       other = getother(orig, dest)
       moveTower(orig, other, n-1)
       movePiece(orig, dest)
       moveTower(other, dest, n-1)


#can call fx within itself (moveTower; n-1 critical, solving smaller problem each time until
#get to smallest problem: n==1; once solve smallest one, can solve harder ones each
       

# move tower from pegs number 0 to 2; have 5 discs (n=5); this fx will give step
# by step directions as algorithm runs
moveTower(0, 2, 5)
       

# Complexity of moveTower: run-time will double each time a piece is added



  
