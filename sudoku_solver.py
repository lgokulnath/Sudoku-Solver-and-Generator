#Importing libraries
import time
from pysat.solvers import Solver
import csv

#Inputting the value of k
k = int(input('Enter the value of k: '))
k2 = k**2
start = time.time() 

#please change file name below here for each input file
filename = "sudokutestcases/sudoku1.csv"

'''
Below functions cell_id and cell_id2 are defined in order to get the variable (proposition) which
encodes the cell(p,q) having the number r
'''
def cell_id(p, q, r):
  return (p-1)*(k**4) + (q-1)*(k**2) + r

def cell_id2(p, q, r):
  return k**6 + cell_id(p, q, r)

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

#Reading from the csv file
rows=[]
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
#assump list has the cellid for all the filled cells
assump=[]
for i, row in enumerate(rows):
  if i < k2:
    for j, ele in enumerate(row):
      if (j>=k2):
        break
      
      if ele.isalnum():
        ele = int(ele, 10)
      
        if ele != 0:
          assump.append(cell_id(i+1, j+1, ele))
  else:
     for j, ele in enumerate(row):
     
      if ele.isalnum():
        ele = int(ele, 10)
       
        if ele != 0:
          assump.append(cell_id2(i+1-k2, j+1, ele))

'''
Now we do the encoding for the constraints of the sudoku which can be found in the attached report
(we have used the minimal encoding here)

'''

#encoding the constraint that each cell should have at least one element
cell_clauses = []
for i in range(k2):
  for j in range(k2):
    t = []
    for p in range(k2):
      t.append(cell_id(i+1, j+1, p+1))
    cell_clauses.append(t)

for i in range(k2):
  for j in range(k2):
    t = []
    for p in range(k2):
      t.append(cell_id2(i+1, j+1, p+1))
    cell_clauses.append(t)


#encoding the constraint: each no appears at most once in each row
row_clauses = []
for i in range(1, k2+1):
  for j in range(1, k2+1):
    for x in range(1, k2):
      for y in range(x+1, k2+1):
        row_clauses.append([-1*cell_id(x, i, j), -1*cell_id(y, i, j)])


for i in range(1, k2+1):
  for j in range(1, k2+1):
    for x in range(1, k2):
      for y in range(x+1, k2+1):
        row_clauses.append([-1*cell_id2(x, i, j), -1*cell_id2(y, i, j)])

#encoding the constraint: each no appears at most once in each column
col_clauses = []

for x in range(1, k2 + 1):
  for z in range(1, k2 + 1):
    for y in range(1, k2):
      for i in range(y+1, k2+1):
        col_clauses.append([-1*cell_id(x, y, z), -1*cell_id(x, i, z)])

for x in range(1, k2 + 1):
  for z in range(1, k2 + 1):
    for y in range(1, k2):
      for i in range(y+1, k2+1):
        col_clauses.append([-1*cell_id2(x, y, z), -1*cell_id2(x, i, z)])

# encoding the constraint: each no appears at most once in subgrid of k * k
subgrid_clauses = []

for z in range(1, k2 + 1):
  for i in range(0, k):
    for j in range(0, k):
      for x in range(1, k + 1):
        for y in range(1, k+1):
          for k0 in range(y+1, k+1):
            subgrid_clauses.append([-1*cell_id(k*i+x, k*j+y, z), -1*cell_id(k*i+x, k*j+k0, z)])
            subgrid_clauses.append([-1*cell_id2(k*i+x, k*j+y, z), -1*cell_id2(k*i+x, k*j+k, z)])

for z in range(1, k2 + 1):
  for i in range(0, k):
    for j in range(0, k):
      for x in range(1, k + 1):
        for y in range(1, k+1):
          for k0 in range(x+1, k+1):
            for l in range(1, k+1):
              subgrid_clauses.append([-1*cell_id(k*i+x, k*j+y, z), -1*cell_id(k*i+k0, k*j+l, z)])
              subgrid_clauses.append([-1*cell_id2(k*i+x, k*j+y, z), -1*cell_id2(k*i+k0, k*j+l, z)])

# encoding the constraint that each corresponding cell of the two sudokus should have different nos
pr=[]
for i in range(1,k2+1):
  for j in range(1,k2+1):
    for r in range(1,k2+1):
      pr.append([-1*cell_id(i,j,r),-1*cell_id2(i,j,r)])


# Now we collect all the constraints we have till now in the list of lists- all_clauses

all_clauses = []

for ele in row_clauses:
  all_clauses.append(ele)

for ele in col_clauses:
  all_clauses.append(ele)

for ele in cell_clauses:
  all_clauses.append(ele)

for ele in subgrid_clauses:
  all_clauses.append(ele)

for ele in pr:
  all_clauses.append(ele)


#initializing the PySAT solver and adding the clauses to it
sol = Solver(use_timer = True)

sol.append_formula(all_clauses)

# Now we check whether the sudoku-pair have a valid solution or not
if sol.solve(assumptions=assump) == False:
  print("None")

else:
  # collecting the positive elements of the sol_model in order to construct the sudoku
  sol_model = sol.get_model()
  sol_pos=[]
  for ele in sol_model:
    if ele > 0:
      sol_pos.append(ele)
  #ans and ans2 will contain the solution of the two sudokus 
  ans= []
  ans2=[]
  i = 0
  temp = []
  temp2=[]

  # now we decode the cell_ids to get our solution and store it in ans and ans2
  for ele in sol_pos:
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
 
  print("Solution for the 1st sudoku: ")
  print_sudoku(ans, 1)
  print("Solution for the 2nd sudoku: ")
  print_sudoku(ans2, 2)
end = time.time()

# print the time taken for the execution of the entire program
print("{:.4f}".format(end - start), "s")

