asciidoctor -v index.adoc  
pygmentize -O full,style=sstyle  -l sent -P lang=es -o test/outputs/es.html test/inputs/es.sentence 
pygmentize -O full,style=sstyle  -l sent -P lang=en -o test/outputs/en.html test/inputs/en.sentence 