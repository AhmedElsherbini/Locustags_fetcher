#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Thursday Oct 31 00:42:02 2024

#@author: ahmed

######################
from Bio import Entrez, SeqIO
import argparse
#####################
# Set your email for Entrez
#salut to Nile University
Entrez.email = "hello@nu.edu.eg"

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Retrieve sequences for given locus tags.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file with locus tags.')
    parser.add_argument('-db', '--database', type=str, required=True, help='Database to search in (e.g., "nucleotide").')
    return parser.parse_args()

def read_locus_tags(file_path):
    """
    Read locus tags from a file.
    """
    locus_tags = []
    with open(file_path, 'r') as file:
        for line in file:
            locus_tags.append(line.strip())
    return locus_tags

def fetch_sequence(tag, database):
    """
    Fetch the sequence for a specific locus tag from the Entrez database.
    """
    try:
        search_handle = Entrez.esearch(db=database, term=tag)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if search_results['IdList']:
            nucleotide_id = search_results['IdList'][0]
            fetch_handle = Entrez.efetch(db=database, id=nucleotide_id, rettype="fasta", retmode="text")
            seq_record = SeqIO.read(fetch_handle, "fasta")
            fetch_handle.close()

            # Update sequence record to match the locus tag
            seq_record.id = tag
            seq_record.description = f"Sequence for locus tag {tag}"
            return seq_record
        else:
            print(f"No data found for {tag}")
            return None
    except Exception as e:
        print(f"An error occurred with locus tag {tag}: {e}")
        return None

def save_sequences_to_fasta(sequences, output_file):
    """
    Save a list of sequences to a FASTA file.
    """
    with open(output_file, "w") as fasta_file:
        SeqIO.write(sequences, fasta_file, "fasta")
    print(f"Sequences successfully saved to {output_file}")

def main():
    # Parse arguments
    args = parse_arguments()
    input_file = args.input
    database = args.database
    output_fasta = "locus_tags_sequences.fasta"

    # Read locus tags from the input file
    locus_tags = read_locus_tags(input_file)
    
    # Fetch sequences for each locus tag
    sequences = []
    print("Hello!")
    for tag in locus_tags:
        seq_record = fetch_sequence(tag, database)
        if seq_record:
            sequences.append(seq_record)
            print(f"Successfully retrieved sequence for {tag}")

    # Save all fetched sequences to a FASTA file
    if sequences:
        save_sequences_to_fasta(sequences, output_fasta)

if __name__ == "__main__":
    main()
