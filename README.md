# phylomap
Python wrapper to run phylogenetic placement of reads

## Purpose

Sequencing data can be used to assemble genomes, detect the presence of, quantify, and describe intra-population diversity within microbial communities. Read alignment provides one method of assigning genomic fragments to a genome of origin via sequence similarity between a read and a reference sequence. While this provides a means of assessing the features describred above and much, much more, alignment approaches do not always take full advantage of information present in the specific loci of differences in sequences.

Phylogenetic read placement approaches seek to more sensitively reflect the information within genomic fragments. By creating a reference phylogenetic tree, the specific locations at which the genomic sequences of related species begin to diverge can be identified. By subsequently mapping a read onto a phylogeny, a read can be assigned to a particular location within the tree, thus (hopefully) identifying the read as belonging to a specific genome or as being more distantly related to several reference genomes (i.e. coming from a common ancestor).

In brief, phylomap exists because the current best-in-class phylogenetic mapping approaches (pplacer, RAxML) are either relatively slow (in the case of RAxML's accurate approach), relatively inaccurate (in the case of RAxML's faster approach) or prohibitively clunky (in the case of pplacer). Phylomap opts for speed and accuracy by employing pplacer - albeit at the cost of RAM efficiency - and seeks to turn the many quite involved steps of running a pplacer workflow into 2 or 3 very simple ones involving only a set of sequences and some reads.

## Requires

### conda

* pplacer
* magicblast
* muscle
* fasttree
* mafft

### pip

* taxtastic
* python-circos==0.3.0

## Usage

python3 phylomap_main.py [build, af, place, viz] [options]

* build creates a reference multiple alignment from a series of nucleotide sequences
* af (short for 'align and filter') aligns a set of nt reads to the reference seqences using magicblast, filters the reads for percent ID to the reference and percent alignment, and creates a multiple alignment to the original reference sequences for passing reads.
* place feeds the multiply aligned reads to pplacer, which places the reads on a phylogenetic tree; the key output here is the jplace files for each set of reads
* viz is under development and doesn't currently work. For now, the best thing to do is to go to ItoL (https://itol.embl.de/upload.cgi) and upload the jplace file there to visualize results.

Currently nucleotide only. Protein support likely to be added at later point.

## Notes on jplace format

https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0031009
