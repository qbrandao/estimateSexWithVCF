#!/usr/bin/env python
import sys
import os
import vcf
from pathlib import Path

def traiter_vcf(file):
    # Remplacez cette fonction par votre traitement spécifique
    print(f"####### Counting in Chr X and Y for : {file}")
    vcf_reader = vcf.Reader(filename=file)
    homozygous_count = 0
    heterozygous_count = 0
    for record in vcf_reader:
        if record.CHROM in ['X', 'Y']:
            for sample in record.samples:
                genotype = sample['GT']
                if genotype is not None:
                    if genotype == '1/1' or genotype == '1|1':
                        homozygous_count += 1
                    elif genotype == '0/1' or genotype == '0|1' or genotype == '1|0' or genotype == '1/2' or genotype == '1|2' or genotype == '2|1':
                        heterozygous_count += 1
    print(f'Homozygous variants: {homozygous_count}')
    print(f'Heterozygous variants: {heterozygous_count}')
    print(f'Ratio Hom/All: {heterozygous_count}')
    print(f'Ratio Het/All: {heterozygous_count}')

def listVcfFiles(dir):
    dir = Path(dir)
    vcfFiles = [file for file in dir.glob("*.vcf")] + [file for file in dir.glob("*.vcf.gz")]
    if fichiers_vcf:
        for fichier in fichiers_vcf:
            traiter_vcf(fichier)
    else:
        for subdir in dir.iterdir():
            if subdir.is_dir():
                listVcfFiles(subdir)
            else:
                exit("No VCF files from this directory")

lister_fichiers_vcf(".")
