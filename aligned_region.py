import argparse
import subprocess
from pathlib import Path


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-q", "--min-BQ", type=int, default=0)
    parser.add_argument("-Q", "--min-MQ", type=int, default=0)
    parser.add_argument("-d", "--min-depth", type=int, default=1)
    parser.add_argument("-l", "--min-length", type=int)

    parser.add_argument("bam", type=Path)
    parser.add_argument("reference", type=Path)

    return parser.parse_args()


def main():

    args = arguments()

    depth_str = depth(args.bam, args.min_BQ, args.min_MQ)
    depth_table = filter_depth_table(parse_depth_str(depth_str), args.min_depth)

    regions = get_contig_indicies(depth_table, args.min_length)
    extract_regions(regions, args.reference)


def depth(bam: Path, min_bq: int, min_mq: int) -> str:

    cmd = ("samtools", "depth", "-q", str(min_bq), "-Q", str(min_mq), bam)
    return subprocess.run(cmd, text=True, capture_output=True).stdout


def parse_depth_str(depth_str: str):
    lines = map(str.split, depth_str.splitlines())
    return [(chrom, int(pos), int(depth)) for (chrom, pos, depth) in lines]


def filter_depth_table(depth_table, min_depth: int):
    return [line[0:2] for line in depth_table if line[2] >= min_depth]


def get_contig_indicies(depth_table, min_length):
    prev_chrom = depth_table[0][0]
    prev_pos = depth_table[0][1]

    region_chrom = prev_chrom
    region_start = prev_pos

    regions = []
    for chrom, pos in depth_table:

        # if we are on a new chromosome,
        # the old region ends immediately
        if chrom != prev_chrom:

            region = [region_chrom, region_start, prev_pos]
            regions.append(region)

            region_chrom = chrom
            region_start = pos

            prev_chrom = chrom
            prev_pos = pos

        # extending the current region
        elif pos == prev_pos + 1 or pos == prev_pos:
            prev_pos = pos

        # ending a region on the same chromosome
        else:
            region = [region_chrom, region_start, prev_pos]
            regions.append(region)
            region_start = pos
            prev_pos = pos

    regions = [[chrom, start, stop] for [chrom, start, stop] in regions if (1+stop-start) >= min_length]
    return regions


def extract_regions(regions, reference) -> str:

    region_strs = [f"{chrom}:{start}-{stop}" for chrom, start, stop in regions]

    cmd = ["samtools", "faidx", reference] + region_strs
    subprocess.run(cmd, text=True)

if __name__ == "__main__":
    main()