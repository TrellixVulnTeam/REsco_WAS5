#!/home/cobrapitz/Desktop/Dev/REsco/venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from genometools.ensembl.cli.extract_protein_coding_genes import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
