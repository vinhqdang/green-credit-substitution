"""Build the Journal of Development Effectiveness upload files in submission_jde/:
figures as 300-dpi LZW-compressed TIFFs numbered in manuscript order, and a zip of
the LaTeX sources (T&F asks for both alongside the two manuscript PDFs)."""
import re
import shutil
import zipfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
FIGDIR = HERE.parent / 'output' / 'figures'
OUT = HERE / 'submission_jde'

SOURCES = ['manuscript.tex', 'manuscript_with_authors.tex', 'chicago_refs.tex',
           'supplementary_material.tex']


def figure_order():
    tex = (HERE / 'manuscript.tex').read_text()
    return re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', tex)


def main():
    OUT.mkdir(exist_ok=True)
    names = figure_order()
    for n, name in enumerate(names, start=1):
        im = Image.open(FIGDIR / name).convert('RGB')
        im.save(OUT / f'Figure{n}.tif', dpi=(300, 300), compression='tiff_lzw')
        print(f'Figure{n}.tif  <- {name}  {im.size}')
    with zipfile.ZipFile(OUT / 'LaTeX_source_files.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for src in SOURCES:
            z.write(HERE / src, src)
        for name in names:
            z.write(FIGDIR / name, f'figures/{name}')
    for pdf in ['manuscript.pdf', 'manuscript_with_authors.pdf', 'supplementary_material.pdf',
                'cover_letter.pdf']:
        shutil.copy(HERE / pdf, OUT / pdf)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
