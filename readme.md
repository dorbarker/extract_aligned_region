Given a BAM file of aligned reads and a FASTA-formatted reference, turns an alignment like this:
```
aligned_read_1                              TTTAAAAA
aligned_read_2                                 AAAAACT
aligned_read_3         TTAAAA
aligned_read_4           AAAAAGT
aligned_read_5              AAGTATTT
reference        GATAAATTAAAAAGTATTTATGGATGATTTAAAAACTATTC
```
into this:
```
>reference:7-19
TTAAAAAGTATTT
>reference:28-37
TTTAAAAACT
```
# Install
```sh
python -m pip install git+https://github.com/dorbarker/extract_aligned_region.git
```
## Requires
- samtools

# Help
```sh
$ extract_aligned_region --help --help
usage: aligned_region.py [-h] [-q MIN_BQ] [-Q MIN_MQ] [-d MIN_DEPTH] [-l MIN_LENGTH] bam reference

positional arguments:
  bam
  reference

optional arguments:
  -h, --help            show this help message and exit
  -q MIN_BQ, --min-BQ MIN_BQ
                        Minimum base quality score [0]
  -Q MIN_MQ, --min-MQ MIN_MQ
                        Minimum map quality score [0]
  -d MIN_DEPTH, --min-depth MIN_DEPTH
                        Minimum depth over a reference position to be considered aligned [1]
  -l MIN_LENGTH, --min-length MIN_LENGTH
                        Minimum length for an aligned region [1]
```