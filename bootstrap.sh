# rdkit dep
sudo apt-get install -y libxrender-dev

conda create -y -n cs510-env
source activate cs510-env
conda install -y -c rdkit rdkit=2017.03.3
conda install -y -c glemaitre imbalanced-learn
conda install -y -c conda-forge keras
conda install -y -c anaconda tensorflow-gpu
conda install -y nb_conda
conda install -y -q -c conda-forge keras

ipython kernel install --prefix=~/anaconda3
