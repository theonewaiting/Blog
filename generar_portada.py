"""Genera la portada (1200x630, JPG) de una entrada del blog de AutomateDoctor.

Uso:
  python3 generar_portada.py --slug mi-entrada --titulo "Título de la entrada" --categoria-slug podologia

Crea portadas/<slug>.jpg. Después: git add, commit y push a main, y usa como imageUrl
  https://cdn.jsdelivr.net/gh/theonewaiting/blog@<commit>/portadas/<slug>.jpg
con el hash completo del commit (git rev-parse HEAD). Con @main jsDelivr puede tardar horas
en ver un archivo nuevo; con el hash funciona al momento y la dirección no cambia nunca.
"""
import argparse, asyncio, io, json, os, pathlib, urllib.parse
from PIL import Image
from playwright.async_api import async_playwright

RAIZ = pathlib.Path(__file__).resolve().parent
CATEGORIAS = {
    'fisioterapia': 'Fisioterapia',
    'podologia': 'Podología',
    'medicina-estetica': 'Medicina estética',
    'implante-capilar': 'Implante capilar',
    'captacion-de-pacientes': 'Captación de pacientes',
    'ia-y-automatizacion': 'IA y automatización',
    'abrir-clinica': 'Abrir o ampliar una clínica',
    'casos-de-exito': 'Casos de éxito',
    'novedades': 'Novedades de AutomateDoctor',
    'actualidad-del-sector': 'Actualidad del sector',
}

async def generar(slug, titulo, categoria_slug, salida=None):
    datos = {'titulo': titulo, 'slug_categoria': categoria_slug,
             'categoria': CATEGORIAS.get(categoria_slug, 'Blog de AutomateDoctor')}
    url = (RAIZ / 'plantilla' / 'portada.html').as_uri() + '#' + urllib.parse.quote(json.dumps(datos, ensure_ascii=False))
    salida = pathlib.Path(salida) if salida else RAIZ / 'portadas' / f'{slug}.jpg'
    salida.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pag = await nav.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        await pag.goto(url)
        await pag.wait_for_selector('body[data-listo]', timeout=20000)
        png = await pag.screenshot(clip={'x': 0, 'y': 0, 'width': 1200, 'height': 630})
        tam = await pag.evaluate('document.body.dataset.listo')
        await nav.close()
    Image.open(io.BytesIO(png)).convert('RGB').save(salida, 'JPEG', quality=86, optimize=True, progressive=True)
    return salida, int(tam)

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--slug', required=True)
    a.add_argument('--titulo', required=True)
    a.add_argument('--categoria-slug', required=True, choices=sorted(CATEGORIAS))
    a.add_argument('--salida')
    x = a.parse_args()
    ruta, tam = asyncio.run(generar(x.slug, x.titulo, x.categoria_slug, x.salida))
    print(f'{ruta} ({os.path.getsize(ruta)//1024} KB, título a {tam}px)')
    print(f'Tras el push: https://cdn.jsdelivr.net/gh/theonewaiting/blog@<commit>/portadas/{x.slug}.jpg')
