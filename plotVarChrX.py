#!/usr/bin/env python
import sys
import os
import vcfpy
import matplotlib.pyplot as plt
from pathlib import Path

# Activation du mode interactif pour eviter l'arret du script quand un plot est affiche
#plt.ion()


def plotVarChrX(vcfFile):
    vcf_reader = vcfpy.Reader.from_path(vcfFile)
    pos = []
    vaf = []
    chrX_len = 156040895
    if "/" in vcfFile:
        vcfFile = vcfFile.split("/")[-1]
    vcfName = vcfFile.split(".")[0]
    for record in vcf_reader:
        if record.CHROM == 'chrX':
            for call in record.calls:
                if call.data.get('DP') > 20:
                    pos.append(record.POS)
                    DP = int(call.data.get('DP'))
                    alt = int(call.data.get('AD')[1])
                    VAF = alt/DP
                    vaf.append(float(VAF))
    plt.plot(pos, vaf, 'r+')
    plt.xlabel('ChrX position') 
    plt.ylabel('VAF')
    plt.title(vcfName)
    plt.axis((0, chrX_len, 0, 1.2))
    plt.savefig(vcfName+".plotChrX.png")
    #plt.show()

def listVcfFiles(dir):
    dir = Path(dir)
    vcfFiles = [file for file in dir.glob("*.vcf")] + [file for file in dir.glob("*.vcf.gz")]
    if vcfFiles:
        for fichier in vcfFiles:
            plotVarChrX(str(fichier))
    else:
        for subdir in dir.iterdir():
            if subdir.is_dir():
                listVcfFiles(subdir)
            else:
                exit("No VCF files from this directory")

listVcfFiles(sys.argv[1])
