#!bin/bash
eval "$(conda shell.bash hook)"
conda activate base 
python ~/Desktop/NKofod.github.io/update_data.py
cd ~/Desktop/NKofod.github.io/
git init 
git add .
git commit -m "Data update"
git push 
echo "Ran the script\n" >> log.txt