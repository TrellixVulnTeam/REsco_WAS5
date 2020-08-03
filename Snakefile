#!/bin/bash..

import os
import glob
from os import listdir
from os.path import isfile, join
import toml

print("------------ PREPARING ------------")

CWD = os.getcwd() # working directory
print("Working directory: ", os.getcwd())

CONFIG_PATH = "config_minimal_example.toml"
print("configuration is at:", CONFIG_PATH)

# index names of all fasta input files  {index_name}.fa
GENOME_PATH = os.path.join(CWD, "Test/In")
BASIS = [f for f in listdir(GENOME_PATH) if isfile(join(GENOME_PATH, f))]
BASIS = list(filter(lambda x: x[-3:] == ".fa", BASIS))
BASIS = list(map(lambda x: x[:-3], BASIS))

# SUFFIXERATOR
SUFF_OUTPUT = BASIS
SUFF_OUTPUT = list(map(lambda x: "Test/Suff/" + x + ".suf", BASIS))

# CONFIG 
CONFIG_OUTPUT = {} #"config_p1_p2_.._pn.cfg"

RESCO_CONFIG_FOLDER = "Test/Config"
CONFIG_NAMES_PATH = os.path.join(os.getcwd(), RESCO_CONFIG_FOLDER)

print("Config folder: ", RESCO_CONFIG_FOLDER)

def create_config_output_names(method = 0):
    data = toml.load(CONFIG_PATH)
    default_params = data["tools"]["ltrharvest"]

    # method 1
    if method == 0:
        for params in data["ltr_harvest_parameters"]:
            ltr_params = ""
            unique_file_name = "" # unique based on ltr harvest arguments
            for key, value in default_params.items():
                nvalue = value
                if key in params:
                    nvalue = params[key]
                ltr_params += "-" + str(key) + " " + nvalue + " "
                unique_file_name += str(nvalue).replace(" ", "_-_") + "_"

            unique_file_name_path = os.path.join(CONFIG_NAMES_PATH, unique_file_name + ".cfg")
            CONFIG_OUTPUT[unique_file_name] = ltr_params # fill [] with args
            print("save to", unique_file_name_path)
            
            if not os.path.exists(unique_file_name_path):
                print(f"Creating: {unique_file_name_path}")
                file = open(unique_file_name_path, "w")
                file.write(ltr_params)
                file.close()

    # method 2
    elif method == 1:
        for params in data["ltr_harvest_parameters"]:
            ltr_params = ""
            unique_file_name = "" # unique based on ltr harvest arguments
            for key, value in default_params.items():
                nvalue = value
                if key in params:
                    nvalue = params[key]
                    unique_file_name += str(key) + str(nvalue).replace(" ", "_-_") + "_"
                ltr_params += "-" + str(key) + " " + nvalue + " "

            unique_file_name_path = os.path.join(CONFIG_NAMES_PATH, unique_file_name + ".cfg")
            CONFIG_OUTPUT[unique_file_name] = ltr_params # fill [] with args
            print("save to", unique_file_name_path)
            
            if not os.path.exists(unique_file_name_path):
                print(f"Creating: {unique_file_name_path}")
                file = open(unique_file_name_path, "w")
                file.write(ltr_params)
                file.close()

create_config_output_names(1)

# LTR HARVEST
HARVEST_OUTPUT = ""
HARVEST_OUTPUT_CFG = ""

# DEBUG OUTPUT
#print("LTR harvest should output:\n", HARVEST_OUTPUT, "\nand\n", HARVEST_OUTPUT_CFG)

print("Suffixerator should output:")
for i in SUFF_OUTPUT:
    print(" ", i)
print("Config should output:")
for i in CONFIG_OUTPUT.keys():
    print(" ", i)

print("Basis:")
for i in BASIS:
    print(" ", i)


print("todo log genome tools version")


# def get_genome_tools_version(genometools):
#     genometools += " --version"
#     print(f"called {genometools}")
#     genome_version_output = subprocess.run(genometools.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
#     return genome_version_output




rule all_harvest:
    input:
        #"Test/Out/{index_name}?{config}.fasta"
        mehl=expand("Test/Out/{index_name}?{config}.fasta", index_name=BASIS, config=list(CONFIG_OUTPUT.keys()))
    

rule harvest:
    input:
        cfg_file="Test/Config/{config}.cfg",
        suff="Test/Suff/{index_name}.suf"
    output:
        o_fasta="Test/Out/{index_name}?{config}.fasta",
        o_inner="Test/Out/{index_name}?{config}_inner.fasta",
        o_gff3="Test/Out/{index_name}?{config}.csv"#,
#        "Test/Out/{}"
    shell:
#        "python3 ltrharvest_call.py gt ltrharvest Test/Suff/{wildcards.index_name} {output.o_fasta} {output.o_inner} {output.o_gff3}"
        "gt ltrharvest -index Test/Suff/{wildcards.index_name} -out {output.o_fasta} -outinner {output.o_inner} -gff3 {output.o_gff3} -tabout yes  -seqids no  -md5 no  -overlaps best  -seed 30  -minlenltr 100  -maxlenltr 2000  -mindistltr 3000  -maxdistltr 25000 -similar 85  -mintsd 4  -maxtsd 20  -motif tgca  -motifmis 1  -vic 60  -xdrop 5  -mat 2  -mis -2  -ins -3  -del -3  -longoutput  -v >HARV_stout_16.csv 2>HARV_stout_16.ERR.txt"

#        "python3 ltrharvest_call.py gt ltrharvest -index Test/Suff/{wildcards.index_name} -out {output.o_fasta} -outinner {output.o_inner} -gff3 {output.o_gff3} -tabout yes  -seqids no  -md5 no  -overlaps best  -seed 30  -minlenltr 100  -maxlenltr 2000  -mindistltr 3000  -maxdistltr 25000 -similar 85  -mintsd 4  -maxtsd 20  -motif tgca  -motifmis 1  -vic 60  -xdrop 5  -mat 2  -mis -2  -ins -3  -del -3  -longoutput  -v >HARV_stout_16.csv 2>HARV_stout_16.ERR.txt"

        # "python3 ltrharvest_call.py gt ltrharvest -index Test/Suff/{wildcards.index_name} {output.o_fasta} {output.o_inner} {output.o_gff3}"

    # run:
    #     print("ADSALKSD:AJSDL:KASJD:ASJDLK:ASJD:LJSAD")
    #     print(f'Test/Suff/{wildcards.index_name}')
    #     print(f'{output.o_fasta}')
    #     print(f'{output.o_inner}')
    #     print(f'{output.o_gff3}')


#        "print('Test/Suff/{wildcards.index_name} {output.o_fasta} {output.o_inner} {output.o_gff3}')"
#        "python3 ltrharvest_call.py Test/Suff/{wildcards.index_name} {output.o_fasta} {output.o_inner} {output.o_gff3}"



rule all_suff:
    input:
        expand("Test/Suff/{base}.suf", base=BASIS)
        


# 1 fasta input
# x
# 1 suff output
rule suff:
    resources:
        mem_mb=1500
    threads: 1
    input:
        fasta="Test/In/{index_name}.fa"
    output:
        "Test/Suff/{index_name}.des",
        "Test/Suff/{index_name}.esq",
        "Test/Suff/{index_name}.lcp",
        "Test/Suff/{index_name}.llv",
        "Test/Suff/{index_name}.md5",
        "Test/Suff/{index_name}.ois",
        "Test/Suff/{index_name}.prj",
        "Test/Suff/{index_name}.sds",
        "Test/Suff/{index_name}.ssp",
        "Test/Suff/{index_name}.suf"
    shell:
        "gt suffixerator -dna -tis -suf -lcp -des -sds -lossless  -v -db {input.fasta} -indexname Test/Suff/{wildcards.index_name}"
        #%(LOC.genometools_bin, spec_d['LTRharvest_input_fasta_fp'], spec_d['LTRharvest_input_fasta_suffixerator_index']) 
#        "{PYTHON_PATH} {SUFFIX_SCRIPT_PATH} {SUFF_CMD} {input.fasta} suffixerator_output/{wildcards.suff}"

