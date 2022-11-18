# strokeEEG

You need to download the data folders from google drive and unzip them into a folder called data/ that gets made in the instructions below in the main directory of strokeEEG once you clone the repo


to run on mac


First time:

```
cd ~
git clone https://github.com/kylemath/strokeEEG
cd strokeEEG
mkdir data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Future times:
```
cd ~/strokeEEG
source venv/bin/activate
git pull
python main.py
```
