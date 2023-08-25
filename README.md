# bioconverter

```
python converter.py braf 'homo sapiens'
```
```
python converter.py braf
```
```
python converter.py 122438725
```
```
python converter.py rs5030858
```
# normalizer

Input file with 3 columns: pmid, gene, HGVS. Returns two files in the specified output directory, one with LitVar normalization and the second one with SynVar normalization.
```
python normalize.py test.tsv '.'
```
