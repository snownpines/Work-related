# Som indata för detta har jag använt en kolumn med kategori och en med nedlagd tid.
# Ta bort [1] från line för att summera en kolumn med delsummor.



import numpy as np

csv_file = np.genfromtxt('Bok2.csv', 
                          delimiter='\t', dtype=str)
top_row = csv_file[:].tolist()



def catch_unique(list_in):
   # från https://www.tutorialspoint.com/get-unique-values-from-a-list-in-python
   # intilize an empty list
   unq_list = []

   # Check for elements
   for x in list_in:
      # check if exists in unq_list
      y = x.split(";")[0]
      if y not in unq_list:
         unq_list.append(y)
         # print list
   return unq_list


def plocka_ut(original_lista, kategori_lista):
    for kategori in kategori_lista:
        tid_lista = []
        
        for value_pair in original_lista:
            if value_pair.split(";")[0] == kategori:
                tid_lista.append(value_pair.split(";")[1])
            else:
                pass
            
        tid_summa = rakna_ihop(tid_lista)[0]

        print(f"{kategori}: {tid_summa}")

def tid_total(original_lista):
    total = 0
    for line in original_lista:
      try:
        h, m, s = line.split(";")[1].split(":") # line[1] för två kolumner och den första är text
        total += 3600*int(h) + 60*int(m) + int(s)
        antal += 1

      except:
        pass
    
    summerad_tid = "%02d:%02d" % (total / 3600, total / 60 % 60)
    print(f"total tid: {summerad_tid}")

def rakna_ihop(lista):
  antal = 0
  tomma = 0
  total = 0
  summerad_tid = ""
  for line in lista:
    try:
      h, m, s = line.split(":") # line[1] för två kolumner och den första är text
      total += 3600*int(h) + 60*int(m) + int(s)
      antal += 1

    except:
      antal += 1
      tomma += 1

  summerad_tid = "%02d:%02d" % (total / 3600, total / 60 % 60)
  return str(summerad_tid), antal, tomma

   # print(f"totalt antal ärenden i kategorin {top_row[0][0]}: {requests}")
   # print(f"antal av dessa utan tid/korrekt tid: {emp_req}")
   # print("total tid loggad: %02d:%02d" % (total / 3600, total / 60 % 60))

kategorier = catch_unique(top_row)

plocka_ut(top_row, kategorier)

tid_total(top_row)
