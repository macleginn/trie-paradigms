# /home/macleginn/bible-corpus/corpus/eng-x-bible-basic.txt
# /home/macleginn/bible-corpus/corpus/rus-x-bible-modern2011.txt

from Table import corpus2table

bible_version = "rus-x-bible-modern2011"

in_path = f"/home/macleginn/bible-corpus/corpus/{bible_version}.txt"
out_path = f"/home/macleginn/Analyses/bible-tables/{bible_version}.csv"
corpus2table(in_path, out_path)
