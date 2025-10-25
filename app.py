from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from pathlib import Path

import argparse
import logging

logger = logging.getLogger(__name__)


def build_parser():
    p = argparse.ArgumentParser(
        description='Document converter CLI for this project (uses docling when available)'
    )
    p.add_argument('-i', '--input', type=Path, required=True,
                   help='Input file or directory')
    p.add_argument('-o', '--output', type=Path,
                   default=Path.cwd(), help='Output directory')
    pdf_group = p.add_argument_group('PDF Processing Options')
    pdf_group.add_argument('--start-page', type=int, default=1,
                           help='Starting page number')
    pdf_group.add_argument('--end-page', type=int,
                           help='Ending page number')
    p.add_argument('-v', '--verbose', action='store_true',
                   help='Verbose logging')
    return p


def parse_document(input_doc_path, output_path, start_page, end_page):
    output_dir = Path(output_path).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    options = PdfPipelineOptions()

    options.images_scale = 2.0
    options.generate_page_images = False
    options.generate_picture_images = True
    options.do_picture_description = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=options)
        }
    )

    conv_res = converter.convert(
        input_doc_path, page_range=(start_page, end_page))

    doc_filename = conv_res.input.file.stem

    md_path = output_dir / f"{doc_filename}.md"

    conv_res.document.save_as_markdown(
        str(md_path), image_mode=ImageRefMode.REFERENCED)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        print('Parsed arguments:')
        print('  input :', args.input)
        print('  output:', args.output)
        print('  start:', args.start_page)
        print('  end:', args.end_page)

    parse_document(args.input, args.output, args.start_page, args.end_page)


if __name__ == '__main__':
    main()
