#!/usr/bin/env python
import sys
import os
import vcfpy
import matplotlib.pyplot as plt
from pathlib import Path

def plotVarChrX(vcfFile):
    vcf_reader = vcfpy.Reader.from_path(vcfFile)
    pos = []
    vaf = []
    chrX_len = 156040895
    for record in vcf_reader:
        if record.CHROM == 'chrX':
            for sample in record.samples:
                for call in record.calls:
                    #FILTER
                    passLesFiltres = 1
                    if passLesFiltres:
                        pos.append(record.POS)
                        DP = int(call.data.get('DP'))
                        alt = int(call.data.get('AD')[1])
                        VAF = alt/DP
                        vaf.append(float(VAF))
    plt.plot(pos, vaf, 'ro')
    plt.axis((0, chrX_len, 0, 1.2))
    plt.show()

def listVcfFiles(dir):
    dir = Path(dir)
    vcfFiles = [file for file in dir.glob("*.vcf")] + [file for file in dir.glob("*.vcf.gz")]
    if vcfFiles:
        for fichier in vcfFiles:
            plotVarChrX(fichier)
    else:
        for subdir in dir.iterdir():
            if subdir.is_dir():
                listVcfFiles(subdir)
            else:
                exit("No VCF files from this directory")

listVcfFiles(".")
