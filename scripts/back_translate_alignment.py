import os
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def back_translate():
    
    aligned_dir = "aa_aligned_sequences"
    nucleotide_dir = "extracted_sequences"
    output_dir = "nt_aligned_sequences"

    
    os.makedirs(output_dir, exist_ok=True)

    
    aligned_files = [f for f in os.listdir(aligned_dir) if f.endswith('_aligned.FNA')]

    for aligned_file in aligned_files:
        
        basename = aligned_file.replace('_aligned.FNA', '')

        
        amino_acid_alignment_file = os.path.join(aligned_dir, aligned_file)
        nucleotide_sequences_file = os.path.join(nucleotide_dir, f"{basename}.FNA")
        output_file = os.path.join(output_dir, f"{basename}_back_translated.FNA")

        
        if not os.path.exists(nucleotide_sequences_file):
            print(f"Warning: Nucleotide sequence file {nucleotide_sequences_file} not found. Skipping...")
            continue

        
        amino_acid_alignment = AlignIO.read(amino_acid_alignment_file, "fasta")

        
        nucleotide_sequences = SeqIO.to_dict(SeqIO.parse(nucleotide_sequences_file, "fasta"))

        
        back_translated_sequences = {}

        
        for record in amino_acid_alignment:
            aa_seq = str(record.seq)
            nucleotide_seq = nucleotide_sequences[record.id].seq
            nt_seq = ""
            nt_index = 0

            for aa in aa_seq:
                if aa == "-":
                    nt_seq += "---"
                else:
                    nt_seq += str(nucleotide_seq[nt_index:nt_index+3])
                    nt_index += 3

            back_translated_sequences[record.id] = SeqRecord(Seq(nt_seq), id=record.id, description="")

        
        with open(output_file, "w") as output_handle:
            SeqIO.write(back_translated_sequences.values(), output_handle, "fasta")
        print(f"Back-translated file written to {output_file}")

back_translate()

