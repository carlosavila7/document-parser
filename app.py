from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from pathlib import Path
import argparse


def build_parser():
    p = argparse.ArgumentParser(
        description='Document converter CLI for this project (uses docling when available)'
    )
    p.add_argument('-i', '--input', type=Path, required=True,
                   help='Input file or directory')
    p.add_argument('-o', '--output', type=Path,
                   default=Path.cwd(), help='Output directory')
    p.add_argument('-v', '--verbose', action='store_true',
                   help='Verbose logging')
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        print('Parsed arguments:')
        print('  input :', args.input)
        print('  output:', args.output)

if __name__ == '__main__':
    main()
