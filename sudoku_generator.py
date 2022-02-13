# Importing the libraries
from pysat.solvers import Solver
from pysat.card import *
import time
import random
import math
import csv

# This function is for printing the sudoku onto the terminal
def print_sudoku(sudoku, rem):
  index = 0
  c1=1
  c2=1
  for x1, i in enumerate(sudoku):
    c2=1
    for x2, ele in enumerate(i):
      print("{: >3}".format(ele),end="")
      if(c2%k==0 and c2!=k2):
          print("{: >3}".format("|"),end="")
      c2=c2+1
    print()
    if(c1%k==0 and c1!=k2):
      for h in range(k2+k-1):
        print("{: >3}".format("-"),end="")
      print()
    c1=c1+1
  print("\n")


# These 2 functions are used to print the partially filled sudoku-pair onto the terminal
def print_unfilled_sudoku_1(sudoku, rem):
  index = 0
  c1=1
  c2=1
  for x1, i in enumerate(sudoku):
    c2=1
    for x2, ele in enumerate(i):
      if index < len(rem) and cell_id(c1, c2, ele) == rem[index]:
        print("{: >3}".format(ele),end="")
        index += 1
      else:
        print('{: >3}'.format(0), end = '')
      if(c2%k==0 and c2!=k2):
        print("{: >3}".format("|"),end="")
      c2=c2+1
    print()
    if(c1%k==0 and c1!=k2):
      for h in range(k2+k-1):
        print("{: >3}".format("-"),end="")
      print()
    c1=c1+1
  print()

def print_unfilled_sudoku_2(sudoku, rem):
  index = 0
  c1=1
  c2=1
  for x1, i in enumerate(sudoku):
    # if i in [3, 6]:
    #         print '------+-------+------'
    c2=1
    for x2, ele in enumerate(i):
      if index < len(rem) and cell_id2(c1, c2, ele) == rem[index]:
        print("{: >3}".format(ele),end="")
        index += 1
      else:
        print("{: >3}".format(0),end="")
        # index += 1
      if(c2%k==0 and c2!=k2):
        print("{: >3}".format("|"),end="")
      c2=c2+1
    print()
    if(c1%k==0 and c1!=k2):
      for h in range(k2+k-1):
        print("{: >3}".format("-"),end="")
      print()
    c1=c1+1
  print()

# This function is for writing the sudoku-pair to the csv file "sudoku.csv"
def wrcsv(sudoku1,rem1,sudoku2,rem2):
  index = 0
  c1=1
  c2=1
  ansls1=[]
  ansls2=[]
  for x1, i in enumerate(sudoku1):
    c2=1
    temp=[]
    for x2, ele in enumerate(i):
      if index < len(rem1) and cell_id(c1, c2, ele) == rem1[index]:
        temp.append(ele)
        index += 1
      else:
        temp.append(0)
        # index += 1
      c2=c2+1
    ansls1.append(temp)
    c1=c1+1
  c1=1
  index=0
  for x1, i in enumerate(sudoku2):
    c2=1
    temp=[]
    for x2, ele in enumerate(i):
      if index < len(rem2) and cell_id2(c1, c2, ele) == rem2[index]:
        temp.append(ele)
        index += 1
      else:
        temp.append(0)
        # index += 1
      c2=c2+1
    ansls2.append(temp)
    c1=c1+1
  with open ("sudoku.csv","w") as sudoku_csv:
    writer=csv.writer(sudoku_csv)
    writer.writerows(ansls1)
    writer.writerows(ansls2)


# Inputting the value of k
k = int(input('Enter the value of k: '))

k2 = k**2

start = time.time()

'''
Below functions cell_id and cell_id2 are defined in order to get the variable (proposition) which
encodes the cell(p,q) having the number r
'''
def cell_id(p, q, r):
  return (p-1)*(k**4) + (q-1)*(k**2) + r

def cell_id2(p, q, r):
  return k**6 + cell_id(p, q, r)

'''
Now we encode the different constraints - this time we use some built-in functions in PySAT to give
us the encoding.
These functions are CardEnc.equals and CardEnc.atmost. We have used the pysat.card library
We also tried the manual encoding but here we found that the encoding obtained from the above two functions
result in faster execution of the program
'''

# Setting up the encoding for the row: each no should be present exactly once in each row
row = []
for p in range(0, k2):
  t = []
  for i in range(0, k**2):
    temp = []
    for j in range(0, k2):
      temp.append(cell_id(p+1, j+1, i+1))
    t.append(temp)
  row.append(t)
for p in range(0, k2):
  t = []
  for i in range(0, k**2):
    temp = []
    for j in range(0, k2):
      temp.append(cell_id2(p+1, j+1, i+1))
    t.append(temp)
  row.append(t)

# Setting up the encoding for the column: each no should be present exactly once in each column
col = []
for p in range(0, k2):
  t = []
  for i in range(0, k2):
    temp = []
    for j in range(0, k2):
      temp.append(cell_id(j+1, p+1, i + 1))
    t.append(temp)
  col.append(t)
for p in range(0, k2):
  t = []
  for i in range(0, k2):
    temp = []
    for j in range(0, k2):
      temp.append(cell_id2(j+1, p+1, i + 1))
    t.append(temp)
  col.append(t)

# Setting up the encoding for the subgrid of size k * k, each no should be present exactly once in each subgrid
box = []
for s in range(k):
  for t in range(k):
    r = s*k
    c = t*k
    for p in range(1, k2 + 1):
      temp = []
      for i in range(k):
        for j in range(k):
          temp.append(cell_id(i + r + 1, j + c + 1, p))
      box.append(temp)
for s in range(k):
  for t in range(k):
    r = s*k
    c = t*k
    for p in range(1, k2 + 1):
      temp = []
      for i in range(k):
        for j in range(k):
          temp.append(cell_id2(i + r + 1, j + c + 1, p))
      box.append(temp)

# Setting up the encoding for the cell: each cell should contain exactly one element
cell = []
for i in range(0, k2**2):
  temp = []
  for j in range(0, k2):
    temp.append(i*k2 + 1 + j)
  cell.append(temp)
for i in range(0, k2**2):
  temp = []
  for j in range(0, k2):
    temp.append(i*k2 + 1 + j+k**6)
  cell.append(temp)

# Setting up the encoding for the sudoku- pair, corresponding cells should have different values
pr=[]
for i in range(1,k2+1):
  for j in range(1,k2+1):
    for r in range(1,k2+1):
      pr.append([cell_id(i,j,r),cell_id2(i,j,r)])

# All the above constraints are encoded in the below for loops
cnf_list = []
for ele in cell:
  cnf = CardEnc.equals(lits=ele, bound = 1, encoding= EncType.pairwise)
  cnf_list.append(cnf)

for i in row:
  for ele in i:
    cnf = CardEnc.equals(lits=ele, bound = 1, encoding= EncType.pairwise)
    cnf_list.append(cnf)

for i in col:
  for ele in i:
    cnf = CardEnc.equals(lits=ele, bound = 1, encoding= EncType.pairwise)
    cnf_list.append(cnf)

for ele in box:
  cnf = CardEnc.equals(lits=ele, bound = 1, encoding= EncType.pairwise)
  cnf_list.append(cnf)

for ele in pr:
  cnf = CardEnc.atmost(lits=ele, bound = 1, encoding= EncType.pairwise)
  cnf_list.append(cnf)

# Collect the constraint encoding in all_clauses
all_clauses=[]
for element in cnf_list:
  for y in element.clauses:
    all_clauses.append(y)

# Initialize the solver and add all the constraints
sol1 = Solver()
sol1.append_formula(all_clauses)

# Now we randomly fix the two cells in each of the sudokus (not corresponding cells)
# This ensures that we get a different sudoku-pair each time
ass=[]
q1=random.randrange(1,k2,1)
q2=random.randrange(1,k2,1)
q3=random.randrange(1,k2,1)
q4=random.randrange(1,k2,1)
ass.append(cell_id(1,1,q1))
ass.append(cell_id(k2,k2,q2))
ass.append(cell_id2(1,k2,q3))
ass.append(cell_id2(k2,1,q4))
sol1.solve(assumptions=ass)

# We get the model and store it in a variable
sol1_model = sol1.get_model()
sol1.delete()
# Collecting the positive elements of the model in order to build the sudoku
sol1_pos=[]
for ele in sol1_model:
  if ele > 0:
    sol1_pos.append(ele)

ans= []
ans2=[]
i = 0
temp = []
temp2=[]
for ele in sol1_pos:
  i = i + 1
  if(ele<=k**6):
    if ((i > 1) and (i % k2 == 0)):
      if ele % k2 != 0:
        temp.append(ele % k2)
      else:
        temp.append(k2)
      ans.append(temp)
      temp = []
    else:
      if ele % k2 != 0:
        temp.append(ele % k2)
      else:
        temp.append(k2)
  if(ele>k**6):
    if ((i > 1) and (i % k2 == 0)):
      if ele % k2 != 0:
        temp2.append(ele % k2)
      else:
        temp2.append(k2)
      ans2.append(temp2)
      temp2 = []
    else:
      if ele % k2 != 0:
        temp2.append(ele % k2)
      else:
        temp2.append(k2)

'''
- Now we have the solution of the sudoku-pair. We now make a list of the cell nos (1 . . . .k^2 . . . .2k^2)
  and randomly shuffle them
- Now we take an empty sudoku.
- We take elements from this list and insert the values corresponding to these cell nos into the sudoku
  and check if they have a unique solution
- Once they have a unique solution, we break from that loop and consider all the elements which we have already 
  inserted into the sudoku. We check that if we get a unique solution on removing them. If yes, we can safely remove
  that element from the sudoku. Else, we insert that element back into the sudoku.
- Finally, we have our sudoku-pair which is maximal and has a unique solution
'''
l = []
for i in range(1, k2**2 + 1):
  l.append(i)
  l.append(i + k2**2)

random.shuffle(l)

# This function returns the cell id of the cell
def get_coordinate(cell_no):
  i = math.ceil(cell_no/k2)
  if cell_no % k2 == 0:
    j = k2
  else:
    j = cell_no % k2
  return i, j

for ele in l:
  if ele <= k2**2:
    i, j = get_coordinate(ele)
 


inserted_elements = []
new_assump = []
rem_cell_no = []
s = Solver()
s.append_formula(all_clauses)
inserted_cell_id = 0
new_sol_pos= []
new_sol_pos_copy = []
not_filled = sol1_pos.copy()
cell_no_rem = []
for v, ele in enumerate(l):
  if ele <= k2**2:
    i, j = get_coordinate(ele)
    new_sol_pos.append(cell_id(i,j,ans[i-1][j-1]))
    inserted_cell_id = cell_id(i,j,ans[i-1][j-1])
    # rem_cell_no.append(ele)
  else:
    i, j = get_coordinate(ele-k2**2)
    new_sol_pos.append(cell_id2(i,j,ans2[i-1][j-1]))
    inserted_cell_id = cell_id2(i,j,ans2[i-1][j-1])
    # rem_cell_no.append(ele)
  not_filled.remove(inserted_cell_id)

  if (s.solve(assumptions = new_assump + [-1*inserted_cell_id]) == False):
    f=1
    new_assump.append(inserted_cell_id)
   
    for element in not_filled:
      
      if(s.solve(assumptions = new_sol_pos+ [-1*element]) == True):
        f=0
        break
      
    if(f==1):
      s.delete()
      s1 = Solver()
      s1.append_formula(all_clauses)
      new_sol_pos_copy = new_sol_pos.copy()
      last_index = len(new_sol_pos) - 1
     
      for element in new_sol_pos:
       
        new_sol_pos_copy.remove(element)  # la = 
        if s1.solve(assumptions= new_sol_pos_copy + [-1*element]) == False:
          continue
        else:
          new_sol_pos_copy.append(element)

      s1.delete()
      break
    else:
        None
  else:
    new_assump.append(inserted_cell_id)
 
inserted_elements = new_sol_pos_copy.copy()

s.delete()



inserted_elements.sort()
inserted_ele_1 = []
inserted_ele_2 = []
for element in inserted_elements:
  if element <= k2**3:
    inserted_ele_1.append(element)
  else:
    inserted_ele_2.append(element)


print_unfilled_sudoku_1(ans, inserted_ele_1)

print_unfilled_sudoku_2(ans2, inserted_ele_2)

wrcsv(ans, inserted_ele_1, ans2, inserted_ele_2)

end = time.time()

print("Time taken = {:.4f}s".format(end-start))