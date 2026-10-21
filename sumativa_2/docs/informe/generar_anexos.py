"""Genera anexos.tex (Anexos A-C del informe) desde las tablas exportadas por los notebooks de S2.

Uso, desde la carpeta sumativa_2:
    python docs/informe/generar_anexos.py . docs/informe/anexos.tex
"""
import math
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(sys.argv[1])            # carpeta sumativa_2
SALIDA = Path(sys.argv[2])
VC = RAIZ / 'outputs/validacion_completa/tablas'
ENT = RAIZ / 'outputs'
FIG_VC = '../../outputs/validacion_completa/figuras'


def leer(p):
    return pd.read_csv(p, float_precision='round_trip')


VAR = {'costo_producto': 'Costo', 'llamadas_atencion': 'Llamadas', 'peso_gramos': 'Peso',
       'entrega_atrasada': 'Atraso', 'compras_previas': 'Compras previas',
       'descuento_ofrecido': 'Descuento', 'importancia_producto': 'Importancia',
       'bloque_bodega': 'Bodega', 'calificacion_cliente': 'Calificación', 'genero': 'Género',
       'modalidad_envio': 'Modalidad'}
EST = {'media': 'Media', 'proporcion': 'Proporción', 'd_av': '$d_{av}$',
       'diferencia_medias': 'Dif. de medias', 'diferencia_proporciones': 'Dif. de proporciones',
       'r_biserial_rangos': 'Biserial de rangos', 'riesgo_relativo': 'Riesgo relativo',
       'asimetria': 'Asimetría', 'curtosis_exceso': 'Curtosis (exceso)', 'de': 'DE', 'iqr': 'IQR',
       'maximo': 'Máximo', 'mediana': 'Mediana', 'minimo': 'Mínimo',
       'n_extremos_iqr': 'Extremos IQR (\\%)', 'pct_suma_top1': '\\% suma top 1\\%', 'q25': 'Q1',
       'q75': 'Q3', 'tasa_atraso': 'Tasa de atraso', 'estadistico': 'Estadístico', 'p': '$p$',
       'p_holm': '$p$ Holm', 'p_correlacion': '$p$ correlación', 'r_punto_biserial': '$r_{pb}$',
       'rho_spearman': '$\\rho$', 'v_cramer': 'V de Cramér'}
CAT = {'Flight': 'Avión', 'Road': 'Carretera', 'Ship': 'Barco', 'high': 'alta', 'low': 'baja',
       'medium': 'media', 'F': 'Fem.', 'M': 'Masc.'}
ESC = {'completos': 'Completos', 'winsor_01_99': 'Winsor. 1/99', 'exclusion_iqr': 'Excl. IQR',
       'descuento_le10': 'Desc. $\\le$ 10'}
ESCENARIOS = list(ESC)


def tex(s):
    s = str(s)
    for a, b in [('\\', '\\textbackslash{}'), ('&', '\\&'), ('%', '\\%'), ('#', '\\#'),
                 ('_', '\\_'), ('{', '\\{'), ('}', '\\}'), ('<=', '$\\le$'), ('>', '$>$'),
                 ('<', '$<$'), ('−', '$-$'), ('χ²', '$\\chi^2$'), ('χ', '$\\chi$'),
                 ('ρ', '$\\rho$'), ('×', '$\\times$'), ('–', '--')]:
        s = s.replace(a, b)
    return s


def num(x, dec=None):
    """Número en formato es-CL; decimales según magnitud si no se indican."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return '---'
    if isinstance(x, str):
        try:
            x = float(x)
        except ValueError:
            return '/'.join(num(float(p), dec) for p in x.split('/'))
    x = float(x)
    if dec is None:
        a = abs(x)
        if a == 0:
            dec = 0 if x == int(x) else 4
        elif a >= 1000:
            dec = 1
        elif a >= 10:
            dec = 2
        elif a >= 0.001:
            dec = 4
        else:
            m, e = f'{x:.2e}'.split('e')
            return f'${m.replace(".", "{,}")}\\cdot 10^{{{int(e)}}}$'
    s = f'{x:,.{dec}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    return s.replace('-', '$-$')


def ic(a, b, dec=None):
    if pd.isna(a) or pd.isna(b):
        return '---'
    return f'[{num(a, dec)}; {num(b, dec)}]'


def variable(v):
    return ' -- '.join(VAR.get(p, tex(p)) for p in str(v).split('|'))


def grupo(g):
    g = str(g)
    if g == 'global':
        return 'global'
    for k, v in VAR.items():
        g = g.replace(k, v)
    for k, v in CAT.items():
        g = g.replace(f'={k}', f'={v}').replace(f'{{{k}', f'{{{v}').replace(f' {k}}}', f' {v}}}')
    g = g.replace('atrasada - puntual', 'atras. $-$ punt.')
    return tex(g).replace('\\$', '$')


def longtable(cols, enc, filas, titulo, etiqueta, nota=None, tam='\\scriptsize'):
    out = [f'{{{tam}\\setlength{{\\tabcolsep}}{{3pt}}',
           f'\\begin{{longtable}}{{{cols}}}',
           f'\\caption{{{titulo}}}\\label{{{etiqueta}}}\\\\\\toprule',
           ' & '.join(enc) + '\\\\\\midrule\\endfirsthead',
           f'\\multicolumn{{{len(enc)}}}{{@{{}}l}}{{\\emph{{Continuación de la tabla \\ref{{{etiqueta}}}}}}}\\\\\\toprule',
           ' & '.join(enc) + '\\\\\\midrule\\endhead',
           '\\bottomrule\\endfoot']
    out += [' & '.join(f) + '\\\\' for f in filas]
    out.append('\\end{longtable}}')
    if nota:
        out.append(f'{{\\footnotesize {nota}\\par}}\\medskip')
    return '\n'.join(out)


def figura(ruta, titulo, etiqueta, ancho='\\linewidth', alto='0.42\\textheight'):
    return (f'\\begin{{figure}}[H]\\centering\\includegraphics[width={ancho},height={alto},'
            f'keepaspectratio]{{{ruta}}}\\caption{{{titulo}}}\\label{{{etiqueta}}}\\end{{figure}}')


partes = []
A = partes.append

inv = leer(VC / 'inventario_resultados_s1.csv')
jk = leer(VC / 'jackknife_resumen.csv')

# ---------------------------------------------------------------- Anexo A
pt = leer(VC / 'permutaciones_todas.csv')
A('\\clearpage\\section{Anexo A. Permutación de las siete pruebas de S1}\\label{anx:A}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{A-\\arabic{table}}\\renewcommand{\\thefigure}{A-\\arabic{figure}}')
A('Cada prueba conserva la hipótesis, los grupos y el estadístico de S1, recalculado en cada una de las '
  '$B = 10.000$ permutaciones (flujo \\texttt{permutaciones}). Se usa '
  '$p_{perm} = (1 + \\text{excedencias})/(B + 1)$, con resolución $1/10.001$; cola superior para '
  '$\\chi^2$, bilateral para $t$ y $z$, y distancia al centro $n_1 n_0/2$ para $U$. Holm se aplica a la '
  'familia de los siete $p$ de permutación y se compara con la familia Holm de S1. Fuente: '
  '\\texttt{permutaciones\\_todas.csv}.')
NOMBRE = {'T01': 'Modalidad', 'T02': 'Peso', 'T03': 'Descuento',
          'E1': 'Peso (rangos)', 'E2': 'Importancia alta',
          'E3': 'Descuento $>$ 10', 'E4': 'Costo'}
ESTAD = {'chi-cuadrado de Pearson': '$\\chi^2$', 't de Welch': '$t$ Welch',
         'U de Mann–Whitney': '$U$', 'z de dos proporciones': '$z$'}
filas = []
for _, r in pt.iterrows():
    filas.append([r.codigo, NOMBRE[r.codigo], ESTAD.get(r.estadistico, tex(r.estadistico)), num(r.estadistico_observado),
                  num(r.efecto), num(r.excedencias, 0), num(r.p_perm), num(r.p_perm_holm),
                  num(r.p_s1) if r.p_s1 > 0 else '0\\textsuperscript{s}',
                  num(r.p_s1_holm) if r.p_s1_holm > 0 else '0\\textsuperscript{s}',
                  'Sí' if r.concordancia_cruda and r.concordancia_holm else 'No'])
A(longtable('@{}l l l r r r r r r r c@{}',
            ['ID', 'Variable', 'Estad.', 'Observado', 'Efecto', 'Exced.', '$p_{perm}$',
             'Holm perm.', '$p$ S1', 'Holm S1', 'Conc.'], filas,
            'Siete pruebas de S1: valor $p$ de permutación frente al paramétrico, crudo y con Holm.',
            'tab:A1',
            nota='Efecto: diferencia atrasada $-$ puntual (T02, T03, E4), V de Cramér (T01), '
                 'biserial de rangos (E1) y diferencia de proporciones (E2, E3). Conc.: la decisión '
                 'al 5\\,\\% coincide con S1 en la familia cruda y en la ajustada por Holm. E2: importancia '
                 'alta frente al resto; E3: descuento $>$ 10 frente a $\\le$ 10. \\textsuperscript{s} '
                 'Subdesbordamiento numérico en S1, no una probabilidad nula.'))
A('Las distribuciones nulas de T01, T02 y T03 se muestran en la figura \\ref{fig:perm} del cuerpo; '
  'las de E1 a E4, en las figuras \\ref{fig:A1}--\\ref{fig:A4}.')
for k, (f, c) in enumerate([('fig_perm_4_e1', 'E1, $U$ de Mann--Whitney del peso'),
                            ('fig_perm_5_e2', 'E2, $z$ de dos proporciones (importancia alta / resto)'),
                            ('fig_perm_6_e3', 'E3, $z$ de dos proporciones (descuento $>$ 10 / $\\le$ 10)'),
                            ('fig_perm_7_e4', 'E4, $t$ de Welch del costo')], 1):
    A(figura(f'{FIG_VC}/{f}.pdf', f'Distribución nula por permutación: {c}.', f'fig:A{k}',
             ancho='0.85\\linewidth'))

# ---------------------------------------------------------------- Anexo B
cb = leer(VC / 'correlaciones_bootstrap.csv')
ab = leer(VC / 'asociaciones_bootstrap.csv')
A('\\clearpage\\section{Anexo B. Las 20 correlaciones y las 15 asociaciones de S1}\\label{anx:B}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{B-\\arabic{table}}\\renewcommand{\\thefigure}{B-\\arabic{figure}}')
A('\\emph{Bootstrap} de filas emparejadas con $B = 10.000$ (flujo \\texttt{bootstrap\\_coeficientes}) e '
  'IC percentil al 95\\,\\%; en Spearman, los rangos se recalculan en cada réplica. Las mismas remuestras '
  'sirven para los 35 coeficientes. Para la V de Cramér, acotada en $[0, 1]$, el IC describe magnitud y '
  'precisión: un IC positivo no prueba dependencia, porque el estimador está sesgado hacia arriba cerca de '
  'cero. Fuentes: \\texttt{correlaciones\\_bootstrap.csv} y \\texttt{asociaciones\\_bootstrap.csv}.')
filas = [[r.id, EST[r.estimando], variable(r.variable), num(r.estimacion_s1), num(r.sesgo),
          num(r.ee), ic(r.ic_inf, r.ic_sup, 3), num(r.ancho_ic, 3),
          'Sí' if r.incluye_cero else 'No'] for _, r in cb.iterrows()]
A(longtable('@{}l l l r r r l r c@{}',
            ['ID', 'Coef.', 'Par', 'S1', 'Sesgo', 'EE', 'IC 95\\,\\%', 'Ancho', 'Incluye 0'], filas,
            'Las 20 correlaciones de S1 con IC \\emph{bootstrap} percentil.', 'tab:B1'))
filas = [[r.id, variable(r.variable), num(r.estimacion_s1), num(r.media_bootstrap), num(r.sesgo),
          num(r.ee), ic(r.ic_inf, r.ic_sup, 3), num(r.ancho_ic, 3)] for _, r in ab.iterrows()]
A(longtable('@{}l l r r r r l r@{}',
            ['ID', 'Par', 'V S1', 'Media boot.', 'Sesgo', 'EE', 'IC 95\\,\\%', 'Ancho'], filas,
            'Las 15 asociaciones V de Cramér de S1 con IC \\emph{bootstrap} percentil.', 'tab:B2',
            nota='El sesgo positivo en las V cercanas a cero es esperable: la V remuestreada nunca es '
                 'negativa. Las asociaciones con el atraso (T01 incluida) se validan una vez y se '
                 'referencian desde el Anexo A.'))
# ---------------------------------------------------------------- Anexo C
rv = leer(ENT / 'resultados_validados.csv')
A('\\clearpage\\section{Anexo C. Matriz de resultados validados para S3}\\label{anx:C}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{C-\\arabic{table}}\\renewcommand{\\thefigure}{C-\\arabic{figure}}')
A('La tabla \\ref{tab:C1} reproduce \\texttt{outputs/resultados\\_validados.csv}, archivo de entrada a S3, '
  'con el estado y la recomendación de cada resultado discutido en el cuerpo. La tabla \\ref{tab:C2} '
  'comprueba la cobertura del 100\\,\\% del inventario: cada uno de los 194 resultados de S1 tiene una '
  'validación o una excepción metodológica explícita.')
filas = [[r.id, tex(r.resultado), tex(r.estado), tex(r.recomendacion_s3)] for _, r in rv.iterrows()]
A(longtable('@{}l >{\\raggedright\\arraybackslash}p{4.2cm} >{\\raggedright\\arraybackslash}p{2.3cm} '
            '>{\\raggedright\\arraybackslash}p{6.4cm}@{}',
            ['ID', 'Resultado', 'Estado', 'Recomendación para S3'], filas,
            'Resultados validados, estado y recomendación para S3.', 'tab:C1'))
cob = inv.groupby('familia').size()
jk_ev = jk.groupby(jk.id.map(inv.set_index('id').familia)).estado.value_counts().unstack(fill_value=0)
anx = {'parametros': '---', 'efectos': '---', 'descriptivas': '---',
       'pruebas': 'A', 'correlaciones': 'B', 'asociaciones': 'B'}
tec = {'parametros': 'Bootstrap percentil y BCa', 'efectos': 'Bootstrap por grupo, percentil y BCa',
       'descriptivas': 'Bootstrap percentil y BCa; extremos solo diagnóstico',
       'pruebas': 'Permutación y Holm', 'correlaciones': 'Bootstrap emparejado percentil',
       'asociaciones': 'Bootstrap emparejado percentil'}
filas = []
for f in ['parametros', 'efectos', 'descriptivas', 'pruebas', 'correlaciones', 'asociaciones']:
    filas.append([tex(f).capitalize(), num(cob[f], 0), tec[f], num(jk_ev.loc[f].get('evaluado', 0), 0),
                  num(jk_ev.loc[f].get('no aplica', 0), 0), anx[f]])
filas.append(['\\midrule Total', num(cob.sum(), 0), '', num((jk.estado == 'evaluado').sum(), 0),
              num((jk.estado != 'evaluado').sum(), 0), ''])
A(longtable('@{}l r >{\\raggedright\\arraybackslash}p{5.2cm} r r l@{}',
            ['Familia', 'Resultados', 'Técnica principal', '\\emph{Jk} evaluado', '\\emph{Jk} no aplica',
             'Anexos'], filas, 'Cobertura del inventario de S1 por familia.', 'tab:C2',
            nota='Inventario: \\texttt{inventario\\_resultados\\_s1.csv} (194 resultados únicos tras '
                 'deduplicar las tablas de S1). ---: detalle no incluido en los anexos. '
                 'Todos los resultados entran además en el Monte Carlo '
                 'empírico y en los escenarios del notebook de validación completa. '))

SALIDA.write_text('\n\n'.join(partes) + '\n', encoding='utf-8')
print('Anexos escritos en', SALIDA)
