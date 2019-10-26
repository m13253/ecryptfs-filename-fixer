ecryptfs-filename-fixer
=======================

Fix long filenames to satisfy the 143-byte limit of eCryptFS.

## Usage

This tool is designed only for people who know what they are doing, incorrect using of this tool may cause data damage.

1. ```find /path/to/directory | sort > input.txt```
2. ```./ecryptfs-filename-fixer < input.txt > output.sh```
3. Read output.sh to make sure everything is correct.
4. Read output.sh again to make sure no file would be overwritten.
5. ```bash output.sh```
