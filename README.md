# Portadas del blog de AutomateDoctor

Portadas de 1200x630 para las entradas de automatedoctor.com/blog. Se generan con código para que todas tengan el mismo estilo.

- plantilla/portada.html: diseño de la portada (título, categoría, icono por categoría, logo y degradado de marca).
- plantilla/fuentes: Montserrat, Roboto y Noto Sans JP en local, para que el resultado sea siempre igual.
- generar_portada.py: crea portadas/<slug>.jpg con Playwright.
- portadas/: una imagen por entrada.

Uso:

    python3 generar_portada.py --slug mi-entrada --titulo "Título de la entrada" --categoria-slug podologia
    git add portadas && git commit -m "Portada: mi-entrada" && git push
    # imageUrl: https://cdn.jsdelivr.net/gh/theonewaiting/blog@<commit>/portadas/mi-entrada.jpg

Títulos de hasta unos 70 caracteres quedan mejor. Más largos, la letra se reduce hasta 40 px.

Las reglas del cuerpo de las entradas están en el proyecto de AutomateDoctor, en claude/blog-contrato-cuerpo.md.
