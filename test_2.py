#First Question
"""sequence = input("Enter the sequence: ..")
print(f"Fraction of G base: {sequence.count('G')}/{len(sequence)}\nFraction of C base: {sequence.count('C')}/{len(sequence)}")


#Second question
nucleotide_sequence = input("Enter the nucleotide sequence: ... ").upper()
compliment = ""
for strand in nucleotide_sequence:
    if strand == "A":
        compliment += "T"
    elif strand == "T":
        compliment += "A"
    elif strand == "C":
        compliment += "G"
    elif strand == "G":
        compliment += "C"

if nucleotide_sequence[::-1] == compliment:
    print("Palindromic")
else:
    print("Not Palindromic")

"""






file1 = open('redwood-data.txt', 'r')
Lines = file1.readlines()
tree_list = []
diameter_list = []
height_list = []
for line in Lines:
    tree = {
        "name": line.strip().split("  ")[0].split('\t')[0],
        "location": line.strip().split("  ")[0].split('\t')[1],
        "diameter": line.strip().split("  ")[0].split('\t')[2],
        "height": line.strip().split("  ")[0].split('\t')[3]
    }
    tree_list.append(tree)
    diameter_list.append(float(tree["diameter"]))
    height_list.append(float(tree["height"])) 
max_diameter = max(diameter_list)
max_height = max(height_list)
for tree in tree_list:
    if float(tree.get("diameter")) == max_diameter:
        print(f"Tree with the Maximum Diameter is: {tree['name']} with diameter {max_diameter}\n\n")
    
    if float(tree.get("height")) == max_height:
        print(f"Tree with the Maximum Diameter is: {tree['name']} with diameter {max_height}\n\n")










