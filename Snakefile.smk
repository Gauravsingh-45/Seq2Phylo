configfile: "config.yaml"

rule all:
    input:
        expand("fastqc_output/zip/{sample}_{read_num}.fastqc.zip", sample=config["samples"], read_num=["1", "2"]),
        expand("trimmomatic_output/{sample}_1.paired.fastq.gz", sample=config["samples"]),
        expand("post_trim_fastqc/html/{sample}_{read_num}.html", sample=config["samples"], read_num=["1", "2"]),
        expand("Hybpiper_output/{sample}/genes_with_seqs.txt", sample=config["samples"]),
        "extracted_sequences/",
        "seq_lengths.tsv",
        expand("gene_recovery_heatmap.{file_ext}", file_ext=config['heatmap_filetype']),
        "translated_gene_sequences/",
        "aa_aligned_sequences/",
        "nt_aligned_sequences/",
        "allseqs.fas",
        "tree_files/allseqs.fas.iqtree",
        "model.txt",
        "bootstrapped_tree/"

include:
    "Snakefile_final_1"

include:
    "Snakefile_final_2"
