
# CS510

## Overview

This is the repo for our CS510 project group, focused on applications of AI to the drug discovery process

## Brief Proposal

Our proposal is to look at novel applications of artificial intelligence in the process of drug discovery, looking specifically at repurposing of existing drugs for new indications and at the degree to which the application of novel deep learning and reinforcement learning techniques (such as graph convolutions and meta-learning/multi-task learning). We will use PubChem BioAssay as our primary dataset and MoleculeNet as our primary benchmark

## Relevant articles
0) MoleculeNet: A benchmark for molecular machine learning - https://arxiv.org/abs/1703.00564

Summary is that the PCBA benchmark will be useful for us.

1) Meta-QSAR: a large-scale application of meta-learning to drug design and discovery  - https://arxiv.org/abs/1709.03854

Summary: Meta-learning is the process of building an ML model which, when input a dataset, looks at features of this dataset such as entropy, number of samples, etc. and will then give info as to 'which algo' would perform the best. 

The authors note QSAR learning is one of the most important and established applications of machine  learning.  We  demonstrate  that  meta-learning  can  be  leveraged  to build  QSAR  models  which  are  much  better  than  those  learned  with  any base-level regression algorithm"

They add their dataset under "learning how to learn QSARs"
https://www.openml.org/s/13

2) Learning Graph-Level Representation for Drug Discovery - https://arxiv.org/pdf/1709.03741.pdf

Interesting notes - they "adopt focal  loss(Lin  et  al.  2017)
and  show  that  it  can  effectively  improve  the  classification
performance in unbalanced molecular dataset."

3) Generating Focussed Molecule Libraries for Drug Discovery with Recurrent Neural Networks - https://arxiv.org/pdf/1701.01329
4) Low Data Drug Discovery with One-shot Learning - https://arxiv.org/pdf/1611.03199

## Background Reading

1) Drug discovery: Practices, Processes and Perspectives

at: https://ebookcentral-proquest-com.ezproxy2.library.drexel.edu/lib/drexel-ebooks/detail.action?docID=1166776

2) Semantic breakthrough in drug discovery

at: http://www.morganclaypool.com.ezproxy2.library.drexel.edu/doi/pdf/10.2200/S00600ED1V01Y201409WEB009

Summary: Chem2Bio2RDF is a large RDF based database.

For PubChem there is a specific RDF download

3)  https://pubchem.ncbi.nlm.nih.gov/rdf/



### Other potentially relevant articles

1) Large-scale detection of drug off-targets - https://bmcpharmacoltoxicol-biomedcentral-com.ezproxy2.library.drexel.edu/articles/10.1186/s40360-017-0128-7#CR2

2) ChemTS: An Efficient Python Library for de novo Molecular Generation - https://arxiv.org/pdf/1710.00616.pdf

Uses Monte Carlo Tree Search

3) Learning to Plan Chemical Synthesis - https://arxiv.org/abs/1708.04202

Also uses MCTS, "These deep neural networks were trained on 12 million reactions, which represents essentially all reactions ever published in organic chemistry"
