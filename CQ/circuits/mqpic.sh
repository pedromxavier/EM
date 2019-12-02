#!/bin/bash
FILES=./*.q
for f in $FILES
do
	echo "Making Qpic from $f"
	qpic -f pdf $f
done

chmod 755 *.pdf

mv *.pdf ../figs/

echo "done!"
