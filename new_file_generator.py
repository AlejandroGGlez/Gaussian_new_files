#!/usr/bin/env python
"""This program generates a Gaussian input file (gjf) from the last Standard Orientation
in a Gaussian out put file

This prgram can work either with the input file (gjf or com) or without it

Whithot input file:
Run the programm:
    >> python new_file_generator gaussian_output_file.out
    
    In this case the program would look for the Last Standar Orientation in the file as 
    well as for the parameters such as the input options, charge and multiplicity and 
    ModRedundant. 
    By the moment the program does not recognize which basis-set are been used for the different elements
    
With input file:
Run the program
    >> python new_file_generator gaussian_output_file.out gaussian_input_file.gjf

 """
__author__ ='Alejandro Gutierrez'
__license__ ='CC' 
__version__ ='1.0'
__email__ = 'alejandro.g.glez@gmail.com'
 
 
import sys
import os
import re

# Receive the Gaussian input file
try:
    
    input_qfi_path = sys.argv[1]
    input_qfi_path_2 = sys.argv[2]
    with open(input_qfi_path, "r") as qfi:
        qfi_lines = qfi.readlines()
    with open(input_qfi_path_2, "r") as qfi:
        qfi_lines_2 = qfi.readlines()
except IndexError:
    print('The new_file_generator program is working without the original input file')

# Read the entire original file


with open(input_qfi_path, "r") as qfi:
        qfi_lines = qfi.readlines()
        
#The following values will be assign to the corresponding indexes in the Gaussian output and input files 
end_document=None #this parameter is used when input file is given an determines the final index for the coordinates in the original filecoordinate_start = None
input_options = None # this element records the input keyworks for gaussian
charge_multiplicity= None # this element record the cahrge and multiplicity
modredundant=None #in case of ModRedundat values it records the index in the gaussian file
#Dictionary with the elements and their corresponding atomic number
periodic_table = { 1 : "H", 2 : "He", 3 : "Li", 4 : "Be", 5 : "B", 6 : "C", 7 : "N", 8 : "O", 9 : "F", 10 : "Ne", 11 : "Na", 12 : "Mg", 13 : "Al", 14 : "Si", 15 : "P", 16 : "S", 17 : "Cl", 18 : "Ar", 19 : "K", 20 : "Ca", 21 : "Sc", 22 : "Ti", 23 : "V", 24 : "Cr", 25 : "Mn", 26 : "Fe", 27 : "Co", 28 : "Ni", 29 : "Cu", 30 : "Zn", 31 : "Ga", 32 : "Ge", 33 : "As", 34 : "Se", 35 : "Br", 36 : "Kr", 37 : "Rb", 38 : "Sr", 39 : "Y", 40 : "Zr", 41 : "Nb", 42 : "Mo", 43 : "Tc", 44 : "Ru", 45 : "Rh", 46 : "Pd", 47 : "Ag", 48 : "Cd", 49 : "In", 50 : "Sn", 51 : "Sb", 52 : "Te", 53 : "I", 54 : "Xe", 55 : "Cs", 56 : "Ba", 57 : "La", 58 : "Ce", 59 : "Pr", 60 : "Nd", 61 : "Pm", 62 : "Sm", 63 : "Eu", 64 : "Gd", 65 : "Tb", 66 : "Dy", 67 : "Ho", 68 : "Er", 69 : "Tm", 70 : "Yb", 71 : "Lu", 72 : "Hf", 73 : "Ta", 74 : "W", 75 : "Re", 76 : "Os", 77 : "Ir", 78 : "Pt", 79 : "Au", 80 : "Hg", 81 : "Tl", 82 : "Pb", 83 : "Bi", 84 : "Po", 85 : "At", 86 : "Rn", 87 : "Fe", 88 : "Ra", 89 : "Ac", 90 : "Th", 91 : "Pa", 92 : "U", 93 : "Np", 94 : "Pu", 95 : "Am", 96 : "Cm", 97 : "Bk", 98 : "Cf", 99 : "Es", 100 : "Fm", 101 : "Md", 102 : "No", 103 : "Lr", 104 : "Rf", 105 : "Db", 106 : "Sg", 107 : "Bh", 108 : "Hs", 109 : "Mt", 110 : "Ds", 111 : "Rg", 112 : "Cn", 113 : "Uut", 114 : "Fl", 115 : "Uup", 116 : "Lv", 117 : "Uus"}

def record_input_parameters_1():
    """This function modifies the parameters: coordinate_star, input_options
    charge_multiplicity and modredundant if no Gaussian input file is given"""

    for i, line in enumerate(qfi_lines):
        global coordinate_start, input_options, charge_multiplicity, modredundant
        if "Standard orientation:" in line: #seeks for the Standard orientations and records the last one
            coordinate_start = i
        elif  "Default route: SCF=Direct" in line: #seeks the input parameters
            input_options= i
        elif "Charge = " in line: #seeks for the charge and multiplicity
            charge_multiplicity=i
        elif 'ModRedundant' in line: #seeks fot the ModRedundant parameter
            modredundant=i
        
def new_name():
    """This function asks the user if they want to name the file"""

    input_1=input('Do you want to name the new file): y/n\t')
    if 'y' in input_1.lower(): 
        name=input(f'Please introduce the file name (no extension are required):\t')
        while ' '  in name:
            name=input('Please introduce a valid file name without spaces\t')
        if name[-3:]=='gjf':
            name=name[:-4]
        return name
    elif 'n' in input_1.lower():
        return 'new_coordinate'
    else:
        print('Please introduce a valid command: "y" or "n"')
        new_name()


# Create a new file with writing rights
def write_input_file_1():
    """This functions writes a Gaussian input file(gjf) if no original input file
    is given"""
    name=new_name()
    with open(f"{name}.gjf", "w") as new_coordinate:
        patron='\n'
        input_options_1= re.sub(patron,"",(qfi_lines[input_options+2])) 
        input_options_2= re.sub(patron,"",(qfi_lines[input_options+3]))
           
        charge , multiplicity = [x for x in qfi_lines[charge_multiplicity].split() if x in '0123456789']
        
        new_coordinate.write(f'{input_options_1[1:]}{input_options_2[1:]}\n\nTitle Card Required\n\n{charge} {multiplicity}\n', ) #Write down the 
        
        for i, line in enumerate(qfi_lines[coordinate_start+5:]):
            if '---' in line:
                break
            fields = line.split()
            atomic_number = int(fields[1])
            element = periodic_table[atomic_number]
            x, y, z = map(float, fields[3:])
            new_coordinate.write(f'{element}\t{x}\t{y}\t{z}\n')
        if type(modredundant)==int:
            new_coordinate.write(f'\n{qfi_lines[modredundant+1][1:]}\n')
        #This line must be mudified for every case where the elements and the bases are changed
        new_coordinate.write(f'Pd 0\nLANL2DZ\nF 1 1.0\n1.472 1.0\n ****\nO 0\n6-31g(d,p)\n ****\nC 0\n6-31g(d,p)\n ****\nH 0\n6-31g(d,p)\n ****\nN 0\n6-31g(d,p)\n ****\nS 0\n6-31g(d,p)\n ****\n\nPd\nLANL2DZ\n\n')    



def record_input_parameters_2():
    """This fucntion records the indexes in the input files for coordinate_start,
    input_options, end_document"""
    global coordinate_start, input_options, end_document
    for i, line in enumerate(qfi_lines_2):
        if line=='\n':
            input_options=i-1
            break
    for i, line in enumerate(qfi_lines):
        if "Standard orientation:" in line: #seeks for the Standart orientation and record the last one
            coordinate_start = i
    for i, line in enumerate(qfi_lines_2[input_options+4:]):
        if line=='\n':
            end_document=i+input_options+4 
            break
                        
def write_input_file_2():
    """This functions writes a Gaussian input file(gjf) if an original input file
    is given"""
    name= new_name()
    with open(f"{name}.gjf", "w") as new_coordinate:
        new_coordinate.writelines(qfi_lines_2[:input_options+4])
        for i, line in enumerate(qfi_lines[coordinate_start+5:]):
            if '---' in line:
                break
            fields = line.split()
            atomic_number = int(fields[1])
            element = periodic_table[atomic_number]
            x, y, z = map(float, fields[3:])
            new_coordinate.write(f'{element}\t{x}\t{y}\t{z}\n')
        
        new_coordinate.writelines(qfi_lines_2[end_document:])
    
        
if __name__=='__main__':
    if len(sys.argv)==2:
        record_input_parameters_1()
        write_input_file_1()
    if len(sys.argv)==3:
        record_input_parameters_2()
        print(end_document)
        print(input_options)
        write_input_file_2()
