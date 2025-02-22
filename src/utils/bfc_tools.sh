# script to verify start and end positions for chromosome

root='/Users/mspriggs/Library/CloudStorage/OneDrive-Illumina,Inc./Documents/Applied_Bioinformatics/modules/data_integration_and_interaction_networks/ASSIGNMENT/data/raw'

vcf=${root}'/RF_090_subset.vcf'
gz=${root}/RF_090_subset.vcf.gz

# zip file
bgzip -c ${vcf} > ${gz}



# make index
tabix -p vcf ${gz}

bcftools query -f '%CHROM\t%POS\n' ${gz} | \
awk 'NR==1{chrom=$1; start=$2} $1!=chrom{print "Chromosome:", chrom, "Start:", start, "End:", end; chrom=$1; start=$2} {end=$2} END{print "Chromosome:", chrom, "Start:", start, "End:", end}'
