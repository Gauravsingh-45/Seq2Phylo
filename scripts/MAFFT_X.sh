#!/bin/bash

input_dir="translated_gene_sequences"
output_dir="aa_aligned_sequences"
mafft_path="$1"  # Accept MAFFT path as a script argument

export PATH=$PATH:$mafft_path

mkdir -p "$output_dir"

for input_file in "$input_dir"/*.FNA; do
    base_name=$(basename "$input_file" .FNA)
    output_file="$output_dir/${base_name}_aligned.FNA"

    sed 's/N/X/g' "$input_file" > "${input_file}.tmp"

    mafft --auto --preservecase --adjustdirection --anysymbol --nwildcard --amino "${input_file}.tmp" > "$output_file"

    rm "${input_file}.tmp"

    echo "Aligned $input_file to $output_file"
done
