"""Publish an A4 assembly book and the OOBB offline page viewer from the same CAD views."""
import base64
import html
from io import BytesIO
import json
from pathlib import Path
from textwrap import wrap

import fitz
from PIL import Image, ImageChops, ImageDraw
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
import yaml

from catalogue import NOTICE, connector_name

REPO = 'https://github.com/oomlout/oomlout_oobb_electronic_version_5'
PAGE_NAMES = ['Cover', 'Project details', 'Steps 1-4', 'Completed assembly', 'Blank page',
              'Blank page', 'Parts list', 'Back cover']


def illustration(path):
    with Image.open(path) as original:
        image = original.convert('RGBA')
    if image.size == (1600, 1080):
        image = image.crop((80, 137, 1520, 949))
        bounds = ImageChops.difference(image.convert('RGB'), Image.new('RGB', image.size, '#f6f4ef')).getbbox()
    else:
        bounds = image.getbbox()
    image = image.crop(bounds) if bounds else image
    paper = Image.new('RGB', image.size, 'white')
    paper.paste(image, mask=image.getchannel('A'))
    paper.thumbnail((1150, 900), Image.Resampling.LANCZOS)
    return paper


def draw_picture(pdf, image, x, y, width, height):
    scale = min(width / image.width, height / image.height)
    w, h = image.width * scale, image.height * scale
    left, bottom = x+(width-w)/2, y+(height-h)/2
    pdf.drawImage(ImageReader(image), left, bottom, w, h)
    return left+w, bottom


def publish(part, scratch, assembly, detail, hardware_root):
    name = connector_name(detail)
    output = part/'assembly'
    output.mkdir(exist_ok=True)
    source_url = REPO+'/tree/main/parts/'+part.name
    diagrams = {key: illustration(scratch/(key+'.png')) for key in assembly['images']}
    entries = {}
    for key, item in zip(('stock', 'prepared', 'housing', 'socket'), assembly['hardware'], strict=True):
        folder = hardware_root/'parts'/item['id']
        code = yaml.safe_load((folder/'working.yaml').read_text(encoding='utf-8'))['md5_6_alpha']
        entries[key] = (item['name'].split(' (')[0].replace('header_long section', 'long header').split(',')[0],
                        item['quantity'], illustration(folder/'data/model_3d_render.png'), code, item['url'])
    entries['print'] = ('Base and top retainer' if detail.get('multiple') else 'Printed base', 1, diagrams['plate'], '', '')
    wire = Image.new('RGB', (240, 90), 'white')
    ImageDraw.Draw(wire).line([(18, 74), (219, 17)], fill='#a83739', width=8)
    entries['wire'] = ('Wire, cut to suit', assembly['wire_count'], wire, '', '')
    path = output/'assembly_instructions.pdf'
    pdf = Canvas(str(path), pagesize=landscape(A4), pageCompression=1, invariant=1)
    pdf.setTitle(name+' | OOBB assembly guide')
    width, height = landscape(A4)

    def words(x, y, value, size=11, face='Helvetica'):
        pdf.setFont(face, size)
        pdf.drawString(x, y, value)

    def border(x, y, w, h, thick=3):
        pdf.setLineWidth(thick)
        pdf.roundRect(x, y, w, h, 3*mm)

    def entry(key, x, top, w, h):
        label, count, image, code, url = entries[key]
        border(x, top-h, w, h, 1.1)
        text_height = 25 if code else 16
        right, bottom = draw_picture(pdf, image, x+4, top-h+text_height, w-24, h-text_height-5)
        if count > 1:
            words(right+mm, bottom, f'x{count}', 8)
        words(x+4, top-h+(14 if code else 5), label, 8, 'Helvetica-Bold')
        if code:
            words(x+4, top-h+4, 'oom.lt/a/', 7, 'Courier')
            words(x+42, top-h+4, str(code), 8, 'Courier-Bold')
            pdf.linkURL('https://oom.lt/a/'+str(code), (x+3, top-h+2, x+w-3, top-h+12), thickness=0)
            pdf.linkURL(url, (x+3, top-h+13, x+w-3, top-2), thickness=0)

    # Covers, parts inventory and blank signature pages follow the base book order.
    words(26, height-55, name, 30, 'Helvetica-Bold')
    words(27, height-79, f"{assembly['wire_count']} contacts  /  2.54 mm pitch  /  {detail['depth']:g} mm base", 13)
    draw_picture(pdf, diagrams['assembled'], 50, 75, width-100, height-180)
    words(26, 43, 'OOBB electronic parts', 12, 'Helvetica-Bold')
    words(26, 27, REPO, 10)
    pdf.linkURL(REPO, (25, 24, 420, 41), thickness=0)
    pdf.showPage()
    words(30, height-50, 'Build notes', 25, 'Helvetica-Bold')
    y = height-84
    for para in [assembly['description'], *[f'{i}. {s}' for i, s in enumerate(assembly['steps'], 1)],
                 'Fit has not been physically tested. Wire colours identify conductors. Check the pinout for your application.', NOTICE]:
        for line in wrap(para.replace('×','x'), 105):
            words(30, y, line, 12)
            y -= 16
        y -= 10
    pdf.showPage()
    margin, gap = 6*mm, 4*mm
    w, h = (width-2*margin-gap)/2, (height-2*margin-gap)/2
    for index, (view, added) in enumerate(zip(assembly['step_views'], [('stock',), ('print','housing','socket','wire'), (), ()], strict=True)):
        x, y = margin+(index%2)*(w+gap), margin+(1-index//2)*(h+gap)
        border(x, y, w, h)
        words(x+9, y+h-31, str(index+1), 27, 'Courier')
        inset = 34*mm if added else 0
        draw_picture(pdf, diagrams[view], x+7, y+8, w-inset-19, h-45)
        for j, key in enumerate(added):
            cell = min(22*mm, (h-14)/len(added))
            entry(key, x+w-inset-6, y+h-6-j*cell, inset, cell)
    pdf.showPage()
    border(margin, margin, width-2*margin, height-2*margin)
    words(margin+12, height-margin-34, '5', 27, 'Courier')
    draw_picture(pdf, diagrams['assembled'], 50, 35, width-100, height-100)
    pdf.showPage()
    pdf.showPage()
    pdf.showPage()
    words(24, height-42, 'Parts for one connector', 24, 'Helvetica-Bold')
    for i, key in enumerate(('print','stock','housing','socket','wire')):
        w, h = 80*mm, 68*mm
        entry(key, 24+(i%3)*(w+14), height-62-(i//3)*(h+18), w, h)
    pdf.showPage()
    words(30, height-60, name, 26, 'Helvetica-Bold')
    words(30, height-90, 'OOBB electronic parts', 14)
    words(30, 45, 'Parts and written instructions on GitHub', 12)
    pdf.linkURL(source_url, (29, 42, 300, 60), thickness=0)
    words(30, 25, NOTICE, 10)
    pdf.save()
    viewer(output, name, source_url)


def viewer(output, name, url):
    slides, images = [], {}
    with fitz.open(output/'assembly_instructions.pdf') as book:
        for index, (label, page) in enumerate(zip(PAGE_NAMES, book, strict=True), 1):
            key = f'page-{index:02d}'
            pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
            images[key] = 'data:image/webp;base64,'
            stream = BytesIO()
            Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(stream, 'WEBP', quality=92)
            images[key] += base64.b64encode(stream.getvalue()).decode()
            links = []
            for link in page.get_links():
                box, bounds = link['from'], page.rect
                links.append(dict(url=link['uri'], rect=[box.x0/bounds.width, box.y0/bounds.height,
                                                         box.width/bounds.width, box.height/bounds.height]))
            slides.append(dict(id=key, image=key, label=label, number=index, steps=[1,2,3,4] if index==3 else [],
                               kind='summary' if index==4 else label, links=links))
    template = (Path(__file__).parent/'presentation/scripts/assembly_viewer.html').read_text(encoding='utf-8')
    data = dict(slides=slides, images=images, start='page-03', step_count=4)
    (output/'assembly_instructions.html').write_text(template.replace('__TITLE__', html.escape(name))
        .replace('__PROJECT_URL__', html.escape(url)).replace('__DATA__', json.dumps(data, separators=(',',':'))), encoding='utf-8')
