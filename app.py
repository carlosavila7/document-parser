from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from pathlib import Path
from PIL import Image

import argparse
import logging
import imagehash
import re

logger = logging.getLogger(__name__)


def remove_repeated_images(input_file_path, output_path):
    artifacts_folder_path = Path(
        f"{output_path}/{Path(input_file_path).stem}_artifacts")

    repeated_images = get_repeated_images(artifacts_folder_path)

    output_file_path = Path(f"{output_path}/{Path(input_file_path).stem}.md")

    with open(output_file_path, 'r') as f:
        content = f.read()

    repeated_filenames = [str(path).split('/')[-1] for path in repeated_images]

    image_pattern = r'!\[.*?\]\((.*?)\)'

    def replace_images(match):
        image_path = match.group(1)
        filename = image_path.split('/')[-1]
        if filename in repeated_filenames:
            return ''
        return match.group(0)

    new_content = re.sub(image_pattern, replace_images, content)

    logger.info(f'References to repeated images removed from .md file.')

    with open(output_file_path, 'w') as f:
        f.write(new_content)

    for repeated_image in repeated_images:
        Path(repeated_image).unlink()
        logger.info(f'Deleted {repeated_image}.')


def get_repeated_images(target_path):
    similarity_threshold = 10

    if not target_path.exists():
        raise FileNotFoundError(f"Folder not found: {target_path}")

    images = sorted(target_path.rglob("*.png"))
    unique_images = []

    for i, image in enumerate(images):
        if (len(unique_images) == 0):
            unique_images.append([image])
            continue

        has_similar = False

        for j, unique_image in enumerate(unique_images):
            img_a = unique_image[0]
            img_b = image

            hash_a = imagehash.phash(Image.open(img_a))
            hash_b = imagehash.phash(Image.open(img_b))

            hamming_distance = hash_a - hash_b

            are_images_similar = hamming_distance < similarity_threshold

            if (are_images_similar):
                unique_image.append(img_b)
                has_similar = True
                break

        if (not has_similar):
            unique_images.append([image])

    repeated_images = [r for r in unique_images if len(r) > 1]
    repeated_images = [s for sub in repeated_images for s in sub]  # flat list

    unique_images = [u for u in unique_images if len(u) == 1]

    logger.info(
        f'{len(repeated_images)} repeated images have been found ({len(unique_images)} unique image(s) to keep).')

    return repeated_images


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
    p.add_argument('-x', '--remove-repeated-images', action='store_true',
                   help='Remove repeated images', default=True)
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
        print('  remove images:', args.remove_repeated_images)

    parse_document(args.input, args.output, args.start_page, args.end_page)

    if args.remove_repeated_images:
        remove_repeated_images(args.input, args.output)


if __name__ == '__main__':
    main()
