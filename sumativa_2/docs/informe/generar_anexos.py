"""Genera anexos.tex (Anexos A-F del informe) desde las tablas exportadas por los notebooks de S2.

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

# ---------------------------------------------------------------- Anexo A
inv = leer(VC / 'inventario_resultados_s1.csv')
bi = leer(VC / 'bootstrap_intervalos.csv')
A('\\section{Anexo A. Bootstrap de todos los parámetros, descriptivas y efectos}\\label{anx:A}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{A-\\arabic{table}}\\renewcommand{\\thefigure}{A-\\arabic{figure}}')
A('La tabla \\ref{tab:A1} contiene los 128 estimandos de S1 de las familias parámetros (4), efectos (13) '
  'y descriptivas (111), con $B = 10.000$ remuestras cada uno (flujo \\texttt{bootstrap\\_parametros}). '
  'Para los estimandos globales se remuestrean filas completas; para diferencias y tasas por grupo, '
  'dentro de cada grupo. El IC clásico es el publicado en S1 (Wilson, $t$ o Welch) y solo existe para '
  'los parámetros y algunos efectos. Las notas (a)--(c) registran los casos en que el BCa no se estima o '
  'en que el bootstrap no tiene cobertura poblacional. Fuente: '
  '\\texttt{outputs/validacion\\_completa/tablas/bootstrap\\_intervalos.csv}.')
cod = {'Réplicas constantes: distribución degenerada; BCa no estimable': 'a',
       'Jackknife sin variación: aceleración y BCa no estimables': 'b',
       'Extremo muestral: solo diagnóstico, sin cobertura poblacional': 'c'}
filas = []
for _, r in bi.iterrows():
    nota = ''
    if isinstance(r.advertencia, str):
        nota = ','.join(sorted(v for k, v in cod.items() if k in r.advertencia))
    filas.append([r.id, EST.get(r.estimando, tex(r.estimando)) + ', ' + variable(r.variable).lower(),
                  grupo(r.grupo), num(r.n, 0), num(r.estimacion_s1), ic(r.ic_clasico_inf, r.ic_clasico_sup),
                  ic(r.ic_percentil_inf, r.ic_percentil_sup), ic(r.ic_bca_inf, r.ic_bca_sup), nota])
A(longtable('@{}l >{\\raggedright\\arraybackslash}p{2.3cm} >{\\raggedright\\arraybackslash}p{2.0cm} r r l l l c@{}',
            ['ID', 'Estimando', 'Grupo', '$n$', 'S1', 'IC clásico S1', 'IC percentil',
             'IC BCa', 'Nota'], filas,
            'Bootstrap de los 128 estimandos de S1 ($B = 10.000$, IC al 95\\,\\%).', 'tab:A1',
            nota='(a) Réplicas constantes: distribución degenerada, BCa no estimable (por ejemplo, la tasa '
                 'de atraso con descuento $> 10$, siempre 1). (b) \\emph{Jackknife} sin variación: '
                 'aceleración no estimable. (c) Extremo muestral: solo diagnóstico descriptivo, sin '
                 'cobertura poblacional. Montos en USD, pesos en gramos, proporciones entre 0 y 1.',
            tam='\\tiny'))
A('Las figuras \\ref{fig:A1}--\\ref{fig:A11} muestran la distribución \\emph{bootstrap} de cada '
  'estimando con sus intervalos (atlas completo).')
for k in range(1, 12):
    A(figura(f'{FIG_VC}/fig_boot_A{k:02d}_atlas.pdf',
             f'Atlas de distribuciones \\emph{{bootstrap}}, parte {k} de 11.', f'fig:A{k}',
             alto='0.40\\textheight'))

# ---------------------------------------------------------------- Anexo B
pt = leer(VC / 'permutaciones_todas.csv')
A('\\clearpage\\section{Anexo B. Permutación de las siete pruebas de S1}\\label{anx:B}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{B-\\arabic{table}}\\renewcommand{\\thefigure}{B-\\arabic{figure}}')
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
            'tab:B1',
            nota='Efecto: diferencia atrasada $-$ puntual (T02, T03, E4), V de Cramér (T01), '
                 'biserial de rangos (E1) y diferencia de proporciones (E2, E3). Conc.: la decisión '
                 'al 5\\,\\% coincide con S1 en la familia cruda y en la ajustada por Holm. E2: importancia '
                 'alta frente al resto; E3: descuento $>$ 10 frente a $\\le$ 10. \\textsuperscript{s} '
                 'Subdesbordamiento numérico en S1, no una probabilidad nula.'))
A('Las distribuciones nulas de T01, T02 y T03 se muestran en la figura \\ref{fig:perm} del cuerpo; '
  'las de E1 a E4, en las figuras \\ref{fig:B1}--\\ref{fig:B4}.')
for k, (f, c) in enumerate([('fig_perm_4_e1', 'E1, $U$ de Mann--Whitney del peso'),
                            ('fig_perm_5_e2', 'E2, $z$ de dos proporciones (importancia alta / resto)'),
                            ('fig_perm_6_e3', 'E3, $z$ de dos proporciones (descuento $>$ 10 / $\\le$ 10)'),
                            ('fig_perm_7_e4', 'E4, $t$ de Welch del costo')], 1):
    A(figura(f'{FIG_VC}/{f}.pdf', f'Distribución nula por permutación: {c}.', f'fig:B{k}',
             ancho='0.85\\linewidth'))

# ---------------------------------------------------------------- Anexo C
cb = leer(VC / 'correlaciones_bootstrap.csv')
ab = leer(VC / 'asociaciones_bootstrap.csv')
A('\\clearpage\\section{Anexo C. Las 20 correlaciones y las 15 asociaciones de S1}\\label{anx:C}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{C-\\arabic{table}}\\renewcommand{\\thefigure}{C-\\arabic{figure}}')
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
            'Las 20 correlaciones de S1 con IC \\emph{bootstrap} percentil.', 'tab:C1'))
filas = [[r.id, variable(r.variable), num(r.estimacion_s1), num(r.media_bootstrap), num(r.sesgo),
          num(r.ee), ic(r.ic_inf, r.ic_sup, 3), num(r.ancho_ic, 3)] for _, r in ab.iterrows()]
A(longtable('@{}l l r r r r l r@{}',
            ['ID', 'Par', 'V S1', 'Media boot.', 'Sesgo', 'EE', 'IC 95\\,\\%', 'Ancho'], filas,
            'Las 15 asociaciones V de Cramér de S1 con IC \\emph{bootstrap} percentil.', 'tab:C2',
            nota='El sesgo positivo en las V cercanas a cero es esperable: la V remuestreada nunca es '
                 'negativa. Las asociaciones con el atraso (T01 incluida) se validan una vez y se '
                 'referencian desde el Anexo B.'))
A(figura(f'{FIG_VC}/fig_cor_correlaciones_intervalos.pdf',
         'IC \\emph{bootstrap} de las 20 correlaciones de S1.', 'fig:C1'))
A(figura(f'{FIG_VC}/fig_cor_asociaciones_intervalos.pdf',
         'IC \\emph{bootstrap} de las 15 asociaciones V de Cramér.', 'fig:C2'))

# ---------------------------------------------------------------- Anexo D
me = leer(VC / 'montecarlo_escenarios.csv')
mc = leer(VC / 'montecarlo_convergencia.csv')
ms = leer(VC / 'montecarlo_segmentos.csv')
sm = leer(VC / 'sensibilidad_montecarlo.csv')
emp = leer(VC / 'montecarlo_empirico.csv')
A('\\clearpage\\section{Anexo D. Simulación Monte Carlo ampliada}\\label{anx:D}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{D-\\arabic{table}}\\renewcommand{\\thefigure}{D-\\arabic{figure}}')
A('Las tablas D-1 a D-4 provienen del notebook de validación completa, cuyo flujo aleatorio se consume '
  'en otro orden que en el de entrega; por eso algunas cifras difieren en el último decimal respecto del '
  'cuerpo. Todas usan $p = 6.563/10.999$ o valores del IC de Wilson de S1 y $B = 10.000$ lotes.')
filas = [[num(r.N, 0), num(r.media), num(r.de), num(r.de_teorica), ic(r.q025, r.q975, 3),
          num(r.q99, 3), num(r.q99_exacto, 3), num(r.prob_sobre_umbral, 4), num(r.prob_exacta, 4),
          num(r.mcse_media, 5), num(r.mcse_prob, 4), 'Sí' if r.cumple_tolerancia else 'No']
         for _, r in me.iterrows()]
A(longtable('@{}r r r r l r r r r r r c@{}',
            ['$N$', 'Media', 'DE', 'DE exacta', 'Rango 95\\,\\%', 'P99', 'P99 exacto', 'P($>$0,6)',
             'Exacta', 'MCSE med.', 'MCSE prob.', 'Tol.'], filas,
            'Lotes binomiales por tamaño: estadísticos simulados frente a los exactos.', 'tab:D1',
            nota='Tolerancias fijadas antes de ejecutar: MCSE de la media $\\le 0{,}001$ y de la '
                 'probabilidad $\\le 0{,}005$.'))
filas = [[num(r.N, 0), num(r.B_parcial, 0), num(r.media), num(r.mcse_media, 5),
          num(r.prob_sobre_umbral, 4), num(r.mcse_prob, 4), num(r.dif_media, 5), num(r.dif_prob, 4)]
         for _, r in mc.iterrows()]
A(longtable('@{}r r r r r r r r@{}',
            ['$N$', '$B$ parcial', 'Media', 'MCSE media', 'P($>$0,6)', 'MCSE prob.',
             'Dif. media', 'Dif. prob.'], filas,
            'Convergencia de la media y de P(tasa $> 60$\\,\\%) según el número de lotes simulados.',
            'tab:D2', nota='Dif.: valor simulado menos valor binomial exacto.'))
filas = [[num(r.N, 0), num(r.n_alto, 0), num(r.media), num(r.de), num(r.de_global),
          num(r.razon_de_segmentos_global, 3), num(r.q99, 3), num(r.prob_sobre_umbral, 4),
          num(r.prob_exacta, 4), num(r.prob_global, 4)] for _, r in ms.iterrows()]
A(longtable('@{}r r r r r r r r r r@{}',
            ['$N$', '$N_{alto}$', 'Media', 'DE', 'DE homog.', 'Razón DE', 'P99', 'P($>$0,6)',
             'Exacta', 'Homog.'], filas,
            'Modelo de dos segmentos (descuento $> 10$ con tasa 1; resto con tasa $3.916/8.352$) frente '
            'al modelo homogéneo.', 'tab:D3',
            nota='$N_{alto} = \\mathrm{redondeo}(N \\cdot 2.647/10.999)$. La tasa 1 del segmento alto '
                 'es una frontera muestral, no una certeza poblacional.'))
filas = [[tex(r.entrada), tex(r.escenario), num(r.valor_entrada), num(r.N, 0), num(r.media),
          num(r.q99, 3), num(r.prob_sobre_umbral, 4),
          num(r.prob_exacta, 4) if not pd.isna(r.prob_exacta) else '---', num(r.mcse_prob, 4)]
         for _, r in sm.iterrows()]
A(longtable('@{}l l r r r r r r r@{}',
            ['Entrada', 'Escenario', 'Valor', '$N$', 'Media', 'P99', 'P($>$0,6)', 'Exacta',
             'MCSE prob.'], filas,
            'Sensibilidad del Monte Carlo a las entradas con IC en S1 (extremos y centro del IC).',
            'tab:D4'))
A('\\textbf{Extensión Monte Carlo a todos los estimandos.} Según la planificación, cada estimando del '
  'inventario se evalúa con remuestras conjuntas de la distribución empírica de S1. Se reutilizan las '
  'réplicas \\emph{bootstrap} (Anexos A y C) y las distribuciones de permutación (Anexo B), identificadas '
  'como experimento Monte Carlo y no como evidencia independiente. La tabla \\ref{tab:D5} resume el sesgo '
  'relativo y el MCSE por familia; el detalle de los 194 resultados está en '
  '\\texttt{montecarlo\\_empirico.csv} y en la figura \\ref{fig:D1}.')
emp['abs_sr'] = emp.sesgo_relativo.abs()
res = emp.groupby('familia').agg(n=('id', 'size'), evaluados=('sesgo_relativo', 'count'),
                                 mediana=('abs_sr', 'median'), maximo=('abs_sr', 'max'),
                                 mcse=('mcse_media', 'max'))
filas = [[tex(f), num(r.n, 0), num(r.evaluados, 0), num(r.mediana * 100, 3) if r.evaluados else '---',
          num(r.maximo * 100, 3) if r.evaluados else '---', num(r.mcse) if r.evaluados else '---']
         for f, r in res.iterrows()]
A(longtable('@{}l r r r r r@{}',
            ['Familia', 'Resultados', 'Con sesgo definido', '|Sesgo rel.| mediano (\\%)',
             '|Sesgo rel.| máx. (\\%)', 'MCSE máx. de la media'], filas,
            'Monte Carlo sobre la distribución empírica: sesgo relativo respecto del valor de S1, por familia.',
            'tab:D5',
            nota='Sin sesgo definido: distribuciones nulas de permutación, $p$ ajustados por Holm, '
                 '$p$ de correlación (evaluados con su coeficiente) y extremos muestrales.'))
A(figura(f'{FIG_VC}/fig_mc_D01_sesgo_relativo.pdf',
         'Sesgo relativo Monte Carlo de cada estimando respecto de su valor empírico.', 'fig:D1'))

# ---------------------------------------------------------------- Anexo E
jk = leer(VC / 'jackknife_resumen.csv')
se = leer(VC / 'sensibilidad_escenarios.csv')
su = leer(VC / 'sensibilidad_umbrales.csv')
sp = leer(VC / 'sensibilidad_pruebas.csv')
sc = leer(VC / 'sensibilidad_coeficientes.csv')
spa = leer(VC / 'sensibilidad_parametros.csv')
A('\\clearpage\\section{Anexo E. Robustez: \\emph{jackknife}, influencia y escenarios}\\label{anx:E}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{E-\\arabic{table}}\\renewcommand{\\thefigure}{E-\\arabic{figure}}')
A('\\textbf{\\emph{Jackknife}.} Se recalcula cada uno de los 194 resultados del inventario retirando, uno '
  'a la vez, cada envío; en los efectos por grupo se conserva la pertenencia y se actualizan los tamaños. '
  'Los 24 resultados ``no aplica\'\' son valores $p$: los de las pruebas se evalúan como cambio de decisión '
  '(cruda y Holm) y los de correlación, a través de su coeficiente. Los diez envíos más influyentes de cada '
  'resultado, con su valor original y el cambio absoluto y relativo, están en '
  '\\texttt{jackknife\\_influyentes.csv} (1.700 filas; los empates se resuelven por \\texttt{id\\_envio}).')
filas = []
for _, r in jk.iterrows():
    if r.estado == 'evaluado':
        cambio = num(r.cambio_max_rel * 100, 4) if not pd.isna(r.cambio_max_rel) else '---'
        dec = '' if pd.isna(r.envios_cambian_decision_cruda) else \
            f'{int(r.envios_cambian_decision_cruda)} / {int(r.envios_cambian_decision_holm)}'
        filas.append([r.id, EST.get(r.estimando, tex(r.estimando)) + ', ' + variable(r.variable).lower(),
                      grupo(r.grupo), num(r.estimacion), num(r.ee_jackknife), num(r.cambio_max_abs),
                      cambio, num(r.id_envio_max, 0) if not pd.isna(r.id_envio_max) else '---', dec])
    else:
        filas.append([r.id, EST.get(r.estimando, tex(r.estimando)) + ', ' + variable(r.variable).lower(),
                      grupo(r.grupo), num(r.estimacion), '\\multicolumn{5}{l}{\\emph{No aplica: '
                      + tex(r.motivo) + '}}', '', '', '', ''][:5])
A(longtable('@{}l >{\\raggedright\\arraybackslash}p{2.6cm} >{\\raggedright\\arraybackslash}p{2.2cm} r r r r r c@{}',
            ['ID', 'Estimando', 'Grupo', 'Estimación', 'EE \\emph{jk}', 'Cambio máx.',
             'Cambio rel. (\\%)', 'Envío', 'Cambian dec.'], filas,
            '\\emph{Jackknife} de los 194 resultados de S1: EE y mayor cambio al retirar un envío.',
            'tab:E1',
            nota='Envío: \\texttt{id\\_envio} que produce el mayor cambio. Cambian dec.: número de envíos '
                 'cuya eliminación cambia la decisión de la prueba, sin ajuste / con Holm. El cambio '
                 'relativo no se define cuando la estimación es 0 o cuando el estimando es un conteo.',
            tam='\\tiny'))
A(figura(f'{FIG_VC}/fig_jk_1_influencia.pdf',
         'Influencia de cada envío en los resultados principales (\\emph{jackknife}).', 'fig:E1'))
A('\\textbf{Escenarios.} Las reglas se fijaron antes de calcular, con umbrales obtenidos de los datos '
  'completos (tabla \\ref{tab:E2}). El CSV original no se modifica: cada escenario es una vista. Los '
  'escenarios restringidos describen subpoblaciones y no estiman el mismo parámetro.')
filas = [[ESC[r.tratamiento], VAR.get(r.variable, tex(r.variable)),
          num(r.inferior) if not pd.isna(r.inferior) else '---', num(r.superior), tex(r.regla)]
         for _, r in su.iterrows()]
filas += [['\\midrule\\multicolumn{5}{@{}l}{\\emph{Tamaño de cada escenario}}', '', '', '', ''][:1]]
filas += [[ESC[r.escenario], f'retenidos {num(r.n_retenido, 0)}', f'excluidos {num(r.n_excluido, 0)}',
           f'modificados {num(r.n_modificado, 0)}', f'tasa de atraso {num(r.tasa_atraso, 4)}']
          for _, r in se.iterrows()]
A(longtable('@{}l l r r l@{}', ['Escenario', 'Variable', 'Inferior', 'Superior', 'Regla'], filas,
            'Reglas, umbrales y tamaños de los escenarios de sensibilidad.', 'tab:E2'))
filas = []
for cod_ in ['T01', 'T02', 'T03', 'E1', 'E2', 'E3', 'E4']:
    fila = [cod_, NOMBRE[cod_]]
    for e in ESCENARIOS:
        r = sp[(sp.codigo == cod_) & (sp.escenario == e)].iloc[0]
        if r.estado != 'evaluable':
            fila.append('no evaluable')
        else:
            marca = '*' if r.rechaza_p_perm_holm in (True, 'True') else ''
            fila.append(f'{num(r.efecto)} ({num(r.p_perm_holm, 4)}){marca}')
    filas.append(fila)
A(longtable('@{}l l r r r r@{}', ['ID', 'Contraste'] + [ESC[e] for e in ESCENARIOS], filas,
            'Efecto y $p$ de permutación ajustado por Holm de las siete pruebas en cada escenario.',
            'tab:E3',
            nota='* Se rechaza $H_0$ al 5\\,\\% con Holm sobre la familia completa del escenario. E3 no es '
                 'evaluable con descuento $\\le 10$: el escenario suprime uno de sus grupos.'))
filas = []
for cid in sc.id.unique():
    d = sc[sc.id == cid].set_index('escenario')
    r0 = d.loc['completos']
    fila = [cid, variable(r0.variable)]
    for e in ESCENARIOS:
        r = d.loc[e]
        txt = f'{num(r.estimacion, 3)} {ic(r.ic_inf, r.ic_sup, 3)}'
        if e != 'completos' and (r.cambia_signo in (True, 'True') or
                                 r.cambia_inclusion_cero in (True, 'True')):
            txt += '\\,\\dag'
        fila.append(txt)
    filas.append(fila)
A(longtable('@{}l l l l l l@{}', ['ID', 'Par'] + [ESC[e] for e in ESCENARIOS], filas,
            'Correlaciones y asociaciones de S1 por escenario: estimación e IC \\emph{bootstrap} 95\\,\\%.',
            'tab:E4', nota='\\dag\\ Cambia el signo o la inclusión del cero respecto de los datos completos.',
            tam='\\tiny'))
filas = []
for pid in spa.id.unique():
    d = spa[spa.id == pid].set_index('escenario')
    r0 = d.loc['completos']
    fila = [pid, EST.get(r0.estimando, tex(r0.estimando)) + ', ' + variable(r0.variable).lower(), grupo(r0.grupo)]
    for e in ESCENARIOS:
        r = d.loc[e] if e in d.index else None
        if r is None or r.estado != 'evaluable':
            fila.append('no evaluable')
        else:
            fila.append(num(r.estimacion))
    filas.append(fila)
A(longtable('@{}l >{\\raggedright\\arraybackslash}p{3.0cm} >{\\raggedright\\arraybackslash}p{3.2cm} r r r r@{}',
            ['ID', 'Estimando', 'Grupo'] + [ESC[e] for e in ESCENARIOS], filas,
            'Los 128 estimandos de la tabla A-1 en cada escenario.', 'tab:E5',
            nota='Los IC percentil y BCa por escenario están en \\texttt{sensibilidad\\_parametros.csv}. '
                 '``No evaluable\'\': el escenario elimina el grupo o deja la variable sin variación.',
            tam='\\tiny'))
for k, (f, c) in enumerate([('fig_sens_parametros', 'Cambio relativo de los parámetros y efectos por escenario'),
                            ('fig_sens_efectos_pruebas', 'Efectos de las siete pruebas por escenario'),
                            ('fig_sens_holm_escenarios', 'Decisiones con Holm por escenario'),
                            ('fig_sens_correlaciones_intervalos', 'IC de las 20 correlaciones por escenario'),
                            ('fig_sens_asociaciones_intervalos', 'IC de las 15 asociaciones por escenario')], 2):
    A(figura(f'{FIG_VC}/{f}.pdf', f'{c}.', f'fig:E{k}', alto='0.55\\textheight'))

# ---------------------------------------------------------------- Anexo F
rv = leer(ENT / 'resultados_validados.csv')
A('\\clearpage\\section{Anexo F. Matriz de resultados validados para S3}\\label{anx:F}')
A('\\setcounter{table}{0}\\setcounter{figure}{0}'
  '\\renewcommand{\\thetable}{F-\\arabic{table}}\\renewcommand{\\thefigure}{F-\\arabic{figure}}')
A('La tabla \\ref{tab:F1} reproduce \\texttt{outputs/resultados\\_validados.csv}, archivo de entrada a S3, '
  'con el estado y la recomendación de cada resultado discutido en el cuerpo. La tabla \\ref{tab:F2} '
  'comprueba la cobertura del 100\\,\\% del inventario: cada uno de los 194 resultados de S1 tiene una '
  'validación o una excepción metodológica explícita.')
filas = [[r.id, tex(r.resultado), tex(r.estado), tex(r.recomendacion_s3)] for _, r in rv.iterrows()]
A(longtable('@{}l >{\\raggedright\\arraybackslash}p{4.2cm} >{\\raggedright\\arraybackslash}p{2.3cm} '
            '>{\\raggedright\\arraybackslash}p{6.4cm}@{}',
            ['ID', 'Resultado', 'Estado', 'Recomendación para S3'], filas,
            'Resultados validados, estado y recomendación para S3.', 'tab:F1'))
cob = inv.groupby('familia').size()
jk_ev = jk.groupby(jk.id.map(inv.set_index('id').familia)).estado.value_counts().unstack(fill_value=0)
anx = {'parametros': 'A, D, E', 'efectos': 'A, D, E', 'descriptivas': 'A, D, E',
       'pruebas': 'B, D, E', 'correlaciones': 'C, D, E', 'asociaciones': 'C, D, E'}
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
             'Anexos'], filas, 'Cobertura del inventario de S1 por familia.', 'tab:F2',
            nota='Inventario: \\texttt{inventario\\_resultados\\_s1.csv} (194 resultados únicos tras '
                 'deduplicar las tablas de S1). Todos los resultados entran además en el Monte Carlo '
                 'empírico (Anexo D) y en los escenarios (Anexo E).'))

SALIDA.write_text('\n\n'.join(partes) + '\n', encoding='utf-8')
print('Anexos escritos en', SALIDA)
