import os
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

# Fixed directories
INPUT_DIR = "extracted_sequences"
OUTPUT_DIR = "translated_gene_sequences"

def custom_translate(nucleotide_seq):
    amino_acid_seq = []
    for i in range(0, len(nucleotide_seq), 3):
        codon = nucleotide_seq[i:i+3]
        if len(codon) == 3:
            if 'N' in codon:
                amino_acid_seq.append('N')
            else:
                amino_acid_seq.append(str(Seq(codon).translate(to_stop=True)))
        else:
            print(f"Incomplete codon found: {codon}")
    return ''.join(amino_acid_seq)

def translate_and_save(input_fasta, output_fasta):
    translated_records = []
    print(f"Translating file: {input_fasta}")

    try:
        with open(input_fasta, "r") as infile:
            for record in SeqIO.parse(infile, "fasta"):
                nucleotide_seq = str(record.seq)

                # Translate the gene sequence using custom translation
                amino_acid_seq = custom_translate(nucleotide_seq)
                # Remove '*' from the amino acid sequence
                amino_acid_seq = amino_acid_seq.replace('*', '')

                # Create a new SeqRecord for the translated sequence
                translated_record = SeqRecord(
                    Seq(amino_acid_seq),
                    id=record.id,
                    description="Translated sequence"
                )

                translated_records.append(translated_record)

        # Write all translated sequences to the output FASTA file
        with open(output_fasta, "w") as outfile:
            SeqIO.write(translated_records, outfile, "fasta")

        print(f"Translated {len(translated_records)} sequences from {input_fasta} to {output_fasta}")
    except Exception as e:
        print(f"Failed to process {input_fasta}: {e}")

def process_directory():
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".FNA"):
            input_fasta = os.path.join(INPUT_DIR, filename)
            output_fasta = os.path.join(OUTPUT_DIR, filename)

            translate_and_save(input_fasta, output_fasta)

if __name__ == "__main__":
    process_directory()
    print(f"All sequences translated and saved to {OUTPUT_DIR}")

