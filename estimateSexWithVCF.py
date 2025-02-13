#!/usr/bin/env python
import sys
import os
import vcfpy
import matplotlib.pyplot as plt
from pathlib import Path

def traiter_vcf(vcfFile):
    if "/" in vcfFile:
        vcfFile = vcfFile.split("/")[-1]
    vcfName = vcfFile.split(".")[0]
    print(f"####### Counting in Chr X for : {vcfFile}")
    vcf_reader = vcfpy.Reader.from_path(vcfFile)
    homozygous_count = 0
    heterozygous_count = 0
    for record in vcf_reader:
        if record.CHROM == 'chrX':
            for call in record.calls:
                genotype = call.data.get('GT')
                if genotype is not None:
                    if genotype == '1/1' or genotype == '1|1':
                        homozygous_count += 1
                    elif genotype == '0/1' or genotype == '0|1' or genotype == '1|0' or genotype == '1/2' or genotype == '1|2' or genotype == '2|1':
                        heterozygous_count += 1
    print(f'Homozygous variants: {homozygous_count}')
    print(f'Heterozygous variants: {heterozygous_count}')
    #print(f'Ratio Hom/All: {heterozygous_count}')
    #print(f'Ratio Het/All: {heterozygous_count}')
    listPat.append(vcfName)
    listHtz.append(heterozygous_count)

def plotPatients(listPat,listHtz):
    plt.plot(listPat, listHtz, 'r+')
    plt.xlabel('Patients') 
    plt.ylabel('Number of Heterozygous variants')
    #plt.title("Plot of all vcf")
    plt.axis((0, len(listPat), 0, max(listHtz)))
    plt.savefig("VCFs.plot_ChrX_Htz.png")


def listVcfFiles(dir):
    dir = Path(dir)
    vcfFiles = [file for file in dir.glob("*.vcf")] + [file for file in dir.glob("*.vcf.gz")]
    if vcfFiles:
        for fichier in vcfFiles:
            traiter_vcf(str(fichier))
    else:
        for subdir in dir.iterdir():
            if subdir.is_dir():
                listVcfFiles(subdir)
            else:
                exit("No VCF files from this directory")

if __name__ == "__main__":
    listPat = []
    listHtz = []
    listVcfFiles(sys.argv[1])
    plotPatients(listPat,listHtz)