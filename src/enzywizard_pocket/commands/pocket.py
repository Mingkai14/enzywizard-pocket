from __future__ import annotations
from argparse import Namespace, ArgumentParser
from ..services.pocket_service import run_pocket_service


def add_pocket_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-i", "--input_path", required=True,help="Path to the input cleaned protein structure file in CIF or PDB format.")
    parser.add_argument("-o", "--output_dir",required=True,help="Directory to save the JSON report.")
    parser.add_argument("--min_rad",type=float,default=1.8,help="Minimum probe radius used by PyVOL for cavity detection (default: 1.8). Smaller values allow detection of narrower cavities, but excessively small values may lead to PyVOL failure.")
    parser.add_argument("--max_rad",type=float,default=6.2,help="Maximum probe radius used by PyVOL for cavity detection (default: 6.2). Larger values allow detection of broader pockets, but excessively large values may lead to PyVOL failure.")
    parser.add_argument("--min_volume",type=float,default=50,help="Minimum pocket volume threshold (default: 50). Pockets with volume below this value will be discarded.")

    parser.set_defaults(func=run_pocket)


def run_pocket(args: Namespace) -> None:
    run_pocket_service(input_path=args.input_path,output_dir=args.output_dir,min_rad=args.min_rad,max_rad=args.max_rad,min_volume=args.min_volume)

