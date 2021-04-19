# requires 'npm i -g autodidact'
autodidact openshift.adoc 

cat openshift.adoc.didact.adoc | sed -E 's/:sectnums:/:image-prefix:/g' > openshift.didact.adoc

rm openshift.adoc.didact.adoc