# Seq2Phylo
Here we describe Seq2Phylo, a pipeline that is designed to construct phylogenetic tree directly by Whole Genome Sequencing reads. Seq2Phylo works by skipping the genome assembly and annotation step, and directly generating high-accuracy species-level trees using reference gene assemblies from across the genome.

# Description of the Seq2Phylo workflow
The pipeline involves pre-processing sequencing reads to ensure high-quality data for analysis. Raw sequencing reads are analyzed using FastQC and poor quality bases are trimmed using Trimmomatic v0.36 to ensure only high-quality reads are utilized. Hybpiper performs reference-based assembly of pre-processed reads, using specific aligners for nucleotide or amino acid sequences. The most suitable reference sequence for each gene and sample is identified based on alignment scores. Reads are sorted into directories corresponding to each gene in the reference set, and SPAdes reconstructs the reference gene sequence from the sorted reads. Extracted coding sequences are translated into amino acids using biopython, amino acid sequences are aligned using mafft v7.505 and then converted back to nucleotide sequences. The aligned nucleotide sequences are partitioned by genes and concatenated into a phylogenetic supermatrix using the catsequences tool. IQ-TREE v1.6.12 constructs a phylogenetic tree from the concatenated alignment, using the ModelFinder feature to identify the optimal substitution model for the data. The tree is then bootstrapped using UFBoot2 to determine the support for the tree's branches. Tree files can be then visualized in ETE toolkit or iTOL.

# Dependencies
1. Snakemake :
https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

2. FastQC :
https://github.com/s-andrews/FastQC

3. Trimmomatic :  
http://www.usadellab.org/cms/?page=trimmomatic  

4. Hybpiper :  
https://github.com/mossmatters/HybPiper/wiki/Installation  
(**Refer to the setup section of the above link and install HybPiper using conda**)

6. Biopython :
https://biopython.org/wiki/Download

7. MAFFT :
https://mafft.cbrc.jp/alignment/software/

8. Catsequences :
https://github.com/ChrisCreevey/catsequences

9. IQ-TREE :
http://www.iqtree.org/

# Seq2Phylo Inputs
1. High Throughput DNA sequencing reads:  
Raw sequencing reads in FASTQ format. The cleaning and removal of contaminant sequences will be carried out by Seq2Phylo pipeline.

2. Reference genes:  
Along with the reads, users also require a set of reference genes that cab be either nucleotide or amino acid sequences in FASTA format. These reference sequences can be obtained from OrthoDB, OMA browser or custom set of genes expected to be present across all the samples used for constructing phylogenetic tree. The reference sequence file can contain multiple sequences for each locus using sequence IDs. Each sequence ID should include the organism name and the gene identifier, separated by a hyphen. The name of this fasta file needs to be specified in the config file.

example of a reference genes file :
```plaintext
>Arabidopsis-atpB
MATNRAIRLSSMIFILGAFLGAGAVVGSAQGKFVEKIARQPELQGKIRGTLTNSLAFLMG
>Zea-atpB
MASTKAIRLSAIVFLGAFLGAGAVVGAAQGKFVEKIARQPELQGKIRGTLTNSLAFLMG
>Arabidopsis-rbcS
MASTKEILKAYPETMRRFLVGYQGCTEEYSSLRDGRDLIGNDTGAASTERVLAKYGPRPL
>Zea-rbcS
MASTKEVLKAYPETMRRFLVGYQGCTEEYSSLRDGRDLVGNDTGAASTERVLAKYGPRPL
```

3. Samplename File:  
A text file with the prefixes of the fastq files one per line (eg: T2 will be the prefix for a file named T2_R1.fq.gz). The prefixes will also be required in config file. The name of this file needs to be specified in the config file.

example of samplefile:
```plaintext
T2
T3
T4
```

5. Config File:  
The config file is provided. Provide the number of threads to be used by the pipeline. Fill in appropriate sample names, Specify the Trimmomatic parameters and assembler to be used. Provide paths of the tools.

# Seq2Phylo Outputs
1. Assenbly statistics files:  
Two tsv files, named `hybpiper_stats.tsv` and `seq_lengths.tsv`, containing information about assembly completeness and the lengths of the extracted exon sequences, respectively.

2. Gene recovery heatmap:  
Gene recovery heatmap showing length of the recovered exon sequences, where the colour intensity of each cell represents the recovered sequence length as a percentage of the target gene length.

3. Tree files:  
The tree_files directory contains allseqs.fas.treefile, this file is in newick format and can be visualised using ETE toolkit or iTOl visualiser. The same file can be obtained from the bootstrapped_tree directory with bootstrap support values. Bootstrapped tree files are obtained only if boostrap is set to "yes" in the config file.

After the seq2phylo run completes, it generates multiple directories containing intermediate files:

- **fastqc_output**: Contains quality metrics plots provided as both a ZIP file and an HTML file.
  
- **Trimmomatic_output**: Includes high-quality sequencing reads, which are used as input for HybPiper.

- **Hybpiper_output**: This directory has a subdirectory for each sample, with further subdirectories for each gene.  
  For more details on HybPiper output, visit: [HybPiper Wiki](https://github.com/mossmatters/HybPiper/wiki/Results-and-output-files).

- **extracted_sequences**: Contains FASTA files with exon sequences extracted from each gene.

- **translated_gene_sequences**: Includes exon sequences translated into amino acid sequences.

- **nt_aligned_sequences**: Contains aligned exon sequences.

- **logs**: This directory holds stdout and stderr files for each step, which are useful for debugging.

# Seq2Phylo Usage

1. Ensure the scripts directory, catsequences, Snakefile_1, Snakefile_2, Snakefile.smk and config.yaml are present in a directory.  

2. Edit and fill in the config file completely.  

3. activate the snakemake environment:  
```plaintext
conda activate snakemake
```  

4. Making separate conda environments from snakemake wrappers (fastqc and trimmomatic)  
```plaintext
snakemake --snakefile Snakefile_1 --use-conda --conda-create-envs-only
```  

5. Perform a dry run first to ensure everything is working properly and no errors are seen.  
```plaintext
snakemake --snakefile Snakefile_1 -n
snakemake --snakefile Snakefile_2 -n
```  

6. Run the first snakefile to perform pre-processing and assembly of data 
```plaintext
snakemake --snakefile Snakefile_1 --use-conda
```

7. Run the second snakefile to perform post-assembly steps for generation of phylogenetic tree 
```plaintext
snakemake --snakefile Snakefile_2 --use-conda
```
