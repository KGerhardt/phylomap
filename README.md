# phylomap
Python wrapper to run phylogenetic placement of reads

## Purpose

phylomap exists because the current best-in-class phylogenetic mapping approaches (pplacer, RAxML) are either relatively slow (in the case of RAxML's accurate approach), relatively inaccurate (in the case of RAxML's faster approach) or prohibitively clunky (in the case of pplacer). Phylomap opts for speed and accuracy by employing pplacer - albeit at the cost of RAM efficiency. Phylomap seeks to turn the process of running a pplacer workflow, with its many tool dependencies, dozens of intermediate files, and finnicky restraints on naming conventions and required options on intermediate tools into 2 or 3 very simple ones involving only a set of sequences, some reads, and simple, highly streamlined commands.

## Requires

### conda

* pplacer
* magicblast
* muscle
* fasttree
* mafft

### pip

* taxtastic

## Usage

python3 phylomap_main.py [build, af, place, viz] [options]

* build creates a reference multiple alignment from a series of nucleotide sequences
* af (short for 'align and filter') aligns a set of nt reads to the reference seqences using magicblast, filters the reads for percent ID to the reference and percent alignment, and creates a multiple alignment to the original reference sequences for passing reads.
* place feeds the multiply aligned reads to pplacer, which places the reads on a phylogenetic tree; the key output here is the jplace files for each set of reads
* viz is under development and doesn't currently work. For now, the best thing to do is to go to ItoL (https://itol.embl.de/upload.cgi) and upload the jplace file there to visualize results.

Currently nucleotide only. Protein support likely to be added at later point.

## Notes on jplace format

https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0031009
