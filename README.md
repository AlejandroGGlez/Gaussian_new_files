# Gaussian_new_files

The file new_file_generator.py can be used to generate input files for Gaussian 9, based either in crash files (did not finish normally) or normally terminated files. The program extracts the last coordinate and the input parameters used and generates a input file called new_coordinate.gjf. 
 >> python new_file_generator.py gaussian_output_file.out 
        new_coordinate.gjf

When especific basis-sets are specified you can either change the code in the function write_input_file_1() to introduce the desired basis-sets, you can copy-paste then in the new_coordinate.gjf file, or you can use a gjf file with the desired basis-sets (the original Gaussian input file for example) in the following way:
 >> python new_file_generator.py gaussian_output_file.out gaussian_input_file.gjf (.com extension are also supported)
        new_coordinate.gjf
 The new_coordinate.gjf would have the desired basis set.
