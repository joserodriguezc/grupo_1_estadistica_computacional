# Protocolo de análisis estadístico
## Evaluación Formativa 1

**Asignatura:** Estadística computacional para la toma de decisiones  
**Equipo:** José Ignacio Rodríguez, Yerko Gallardo y Sebastián Rojas  
**Responsable del protocolo:** José Ignacio Rodríguez  
**Revisor:** Yerko Gallardo  
**Fecha:** 06-10-2026  
**Plazo de entrega:** 08-10-2026 a las 23:59, hora de Chile (`America/Santiago`)  
**Estado:** Propuesta para revisión y aprobación del equipo

### 1. Contexto y problema de decisión

El proyecto utilizará el conjunto de datos **E-Commerce Shipping Data**, publicado en Kaggle por Prachi Gopalani:

https://www.kaggle.com/datasets/prachi13/customer-analytics

El conjunto reúne características de productos, clientes y envíos, junto con una variable que identifica si la entrega se produjo dentro del plazo esperado.

Las entregas atrasadas pueden comprometer la experiencia del cliente y motivar una revisión de las operaciones logísticas. Sin embargo, observar diferencias entre envíos no permite determinar por sí solo sus causas.

El problema de decisión consiste en **identificar características o segmentos que justifiquen una investigación operacional posterior**, considerando la magnitud de las diferencias observadas y su incertidumbre.

El análisis no establecerá modificaciones específicas de transporte, bodegas o políticas comerciales. Tales decisiones requieren información adicional sobre tiempos, costos operacionales y factores de confusión.

### 2. Objetivos

**Objetivo general**

Caracterizar los registros de envíos y analizar asociaciones preliminares entre el atraso, la modalidad de envío, el peso y el costo de los productos, mediante estadística descriptiva, estimación e inferencia básica.

**Objetivos específicos**

1. Identificar y clasificar las variables, documentando sus unidades, dominios y limitaciones.
2. Caracterizar su distribución mediante medidas y gráficos pertinentes.
3. Estimar la proporción de entregas atrasadas y las medias de peso, costo y llamadas de atención al cliente.
4. Evaluar la asociación entre modalidad de envío y atraso.
5. Comparar el peso y el costo medios entre entregas atrasadas y puntuales.
6. Interpretar magnitud, incertidumbre y significancia, vinculándolas con el problema de decisión.

### 3. Diseño y unidad de análisis

Se realizará un **análisis observacional de los registros disponibles**, sin intervención experimental.

La unidad de análisis provisional será **cada registro de envío asociado a un cliente**, pendiente de validación mediante el diccionario Y02.

La columna `ID` se utilizará para verificar identificación y unicidad. Se excluirá de estadísticas sustantivas y correlaciones.

La unicidad de `ID` no demuestra que cada persona aparezca una sola vez ni garantiza independencia entre registros.

**Alcance de la inferencia**

Los resultados descriptivos caracterizarán el archivo analizado. Los intervalos de confianza y las pruebas se interpretarán bajo los supuestos de independencia y de un proceso generador comparable al de los registros.

Mientras no se documente el mecanismo de selección, no se afirmará representatividad del comercio electrónico general. Un tamaño muestral grande no elimina sesgos de selección ni dependencia.

### 4. Variable de resultado y convenciones

La variable original de resultado será `Reached.on.Time_Y.N`.

Se establece la siguiente codificación, que deberá corroborarse en Y02:

| Valor | Interpretación | Etiqueta |
|---|---|---|
| 0 | Entrega dentro del plazo | A tiempo |
| 1 | Entrega fuera del plazo | Atrasada |

Se conservará la columna original y podrá crearse el alias `entrega_atrasada`, manteniendo los mismos valores.

Todas las tablas, gráficos y textos utilizarán esta convención.

Las diferencias de medias se calcularán siempre como:

**Media de entregas atrasadas − media de entregas a tiempo.**

Una diferencia positiva indicará que el promedio es mayor entre entregas atrasadas; una diferencia negativa, que es menor.

### 5. Preguntas de análisis

| Código | Pregunta | Variables | Evidencia prevista |
|---|---|---|---|
| P01 | ¿Cómo se distribuyen las características de los registros? | Variables analíticas del dataset | Estadísticas descriptivas y gráficos |
| P02 | ¿Cuál es la proporción de entregas atrasadas? | Resultado del envío | Proporción e IC del 95 % |
| P03 | ¿Cuáles son el peso, el costo y las llamadas medios? | Peso, costo y llamadas | Medias e IC del 95 % |
| P04 | ¿Existe asociación entre modalidad de envío y atraso? | Modalidad y resultado | Tabla de contingencia, χ² y V de Cramér |
| P05 | ¿Difiere el peso medio entre entregas atrasadas y puntuales? | Peso y resultado | Welch bilateral, diferencia e IC |
| P06 | ¿Difiere el costo medio entre entregas atrasadas y puntuales? | Costo y resultado | Welch bilateral, diferencia e IC |
| P07 | ¿Qué segmentos presentan patrones que ameriten investigar posteriormente? | Modalidad, bodega y variables numéricas | Comparaciones descriptivas y síntesis |

P04, P05 y P06 corresponden a los contrastes planificados T01–T03. Se agregan cuatro pruebas complementarias (E1–E4, §8). **Todas las pruebas que se ejecuten (siete) conforman una sola familia** para el ajuste de Holm. El criterio se fijó antes de ejecutar cualquier prueba y no depende de los resultados: así se conserva el control del error familiar. Es un criterio conservador: ninguna prueba queda fuera del ajuste. P07 mantiene su carácter descriptivo; cualquier prueba nueva que se ejecute también entra en la familia.

### 6. Análisis descriptivo

**Variables cuantitativas**

Se reportarán:

- Número de observaciones válidas y faltantes.
- Media y mediana.
- Desviación estándar.
- Primer y tercer cuartil.
- Rango intercuartílico.
- Mínimo y máximo.

Se utilizarán histogramas y diagramas de caja cuando resulten pertinentes. Los conteos podrán representarse mediante barras.

**Variables nominales**

Se presentarán frecuencias absolutas y porcentajes con denominadores explícitos.

Para modalidad y bodega se distinguirán:

- Participación en el total de envíos.
- Proporción de atraso dentro de cada categoría.

Un mayor número de atrasos puede responder a un mayor volumen de envíos; no implica necesariamente una mayor proporción de atraso.

**Variables ordinales**

Se conservará el orden de las categorías.

Para `Customer_rating` se mostrarán frecuencias ordenadas y, cuando corresponda, mediana y cuartiles.

Para `Product_importance` se utilizará el orden **bajo, medio y alto**. No se supondrán distancias iguales entre categorías.

**Relaciones numéricas exploratorias**

Si se calculan correlaciones, se elegirá el método según la escala y la forma de la relación. Se excluirán `ID` y códigos nominales. Una correlación no se interpretará como causalidad.

### 7. Estimación e intervalos de confianza

Se utilizará un nivel de confianza del **95 %**, con la **aproximación normal (Teorema Central del Límite)** que solicita el curso en esta fase:

- Media: x̄ ± z₀,₉₇₅ · s / √n
- Proporción: p̂ ± z₀,₉₇₅ · √[p̂(1 − p̂) / n]

| Parámetro | Estimador | Método del intervalo | Responsable |
|---|---|---|---|
| Proporción de atraso | Atrasos / registros con resultado válido | Normal para una proporción; requiere n·p̂ ≥ 10 y n·(1 − p̂) ≥ 10 | José |
| Peso medio | Media de `Weight_in_gms` | Normal para una media | José |
| Costo medio | Media de `Cost_of_the_Product` | Normal para una media | Sebastián |
| Llamadas medias | Media de `Customer_care_calls` | Normal para una media (variable de conteo), con justificación | Yerko |

El uso de la aproximación normal requiere revisar independencia, dispersión, tamaño efectivo y observaciones influyentes. Su justificación no dependerá únicamente del tamaño del archivo.

**Buena práctica y recomendación.** Con muestras pequeñas o proporciones cercanas a 0 o 1 se recomienda:

- **t de Student para medias**: al estimar σ con s, el cuantil t₀,₉₇₅,ₙ₋₁ incorpora esa incertidumbre adicional; con n pequeño, z produce intervalos demasiado estrechos.
- **Wilson para proporciones**: el intervalo normal (Wald) puede tener cobertura bastante inferior a la nominal, salir de [0, 1] o tener ancho cero si p̂ = 0 o 1 (Brown, Cai y DasGupta, 2001, *Statistical Science*, 16(2), 101–133). Wilson invierte la prueba *score*, se mantiene dentro de [0, 1] y conserva una cobertura cercana al 95 %.

En este archivo (n = 10.999, p̂ ≈ 0,60) ambos métodos difieren de la aproximación normal recién en la cuarta cifra decimal, por lo que se usa la aproximación normal sin pérdida. Si en análisis posteriores se trabaja con subgrupos pequeños o proporciones extremas, se usarán t y Wilson.

Cada estimación incluirá parámetro, estimador, n efectivo, unidad, método, límites e interpretación.

Los intervalos describirán la incertidumbre del parámetro bajo los supuestos establecidos. No se interpretarán como rangos que contienen el 95 % de las observaciones.

### 8. Pruebas de hipótesis

Se fijará **α = 0,05** antes de ejecutar los contrastes. Las comparaciones de medias serán bilaterales.

#### T01 Asociación entre modalidad y atraso

**Responsable:** Yerko  
**Revisor:** Sebastián  
**Método:** χ² de independencia.

- **H₀:** La modalidad de envío y el resultado de entrega son independientes.
- **H₁:** Existe asociación entre ambas variables.

Se reportarán tabla observada, tabla esperada, χ², grados de libertad, valor p y **V de Cramér**.

Se revisarán independencia y frecuencias esperadas. Si estas no permiten justificar la aproximación χ², se documentará una alternativa válida antes de interpretar el contraste. No se fusionarán modalidades únicamente para obtener significancia.

#### T02 Diferencia de peso medio

**Responsable:** José  
**Revisor:** Yerko  
**Método:** t de Welch para dos grupos independientes.

Sea Δpeso la diferencia entre el peso medio de entregas atrasadas y puntuales:

- **H₀:** Δpeso = 0.
- **H₁:** Δpeso ≠ 0.

Welch permite comparar medias sin asumir igualdad de varianzas.

Se reportarán n, media y desviación estándar por grupo; diferencia en gramos; IC del 95 % de la diferencia; estadístico t; grados de libertad y valor p.

#### T03 Diferencia de costo medio

**Responsable:** Sebastián  
**Revisor:** José  
**Método:** t de Welch para dos grupos independientes.

Sea Δcosto la diferencia entre el costo medio de entregas atrasadas y puntuales:

- **H₀:** Δcosto = 0.
- **H₁:** Δcosto ≠ 0.

Se reportará la misma estructura de T02, expresando la diferencia en USD, sujeto a confirmación de la unidad en Y02.

**Magnitud de las diferencias**

La diferencia en unidades originales será la medida principal de efecto para T02 y T03.

Como complemento, se podrá utilizar una diferencia estandarizada con denominador común:

**dₐᵥ = diferencia de medias / √[(varianza atrasadas + varianza puntuales) / 2].**

Su fórmula y signo se documentarán. No se establecerán umbrales de importancia operacional sin respaldo externo.

#### Pruebas complementarias E1–E4

**Responsable:** José  
**Método:** según la prueba; todas bilaterales, con α = 0,05, y forman parte de la familia de Holm (§9).

| Código | H₀ | Método | Efecto reportado |
|---|---|---|---|
| E1 | La distribución del peso es la misma en entregas atrasadas y puntuales | Mann-Whitney *U* (robustez de T02) | Correlación biserial de rangos r = 2U/(n₁n₀) − 1 |
| E2 | La proporción de atraso es igual en productos de importancia alta y en el resto | *z* de dos proporciones | Diferencia de proporciones, IC y riesgo relativo |
| E3 | La proporción de atraso es igual con descuento > 10 y ≤ 10 | *z* de dos proporciones | Diferencia de proporciones, IC y riesgo relativo |
| E4 | Δdescuento = 0 (media atrasadas − media puntuales) | *t* de Welch | Diferencia, IC y dₐᵥ |

En E3 se documentará la separación completa (100 % de atraso con descuento > 10). En E4 la diferencia se expresa en las unidades originales, porque la unidad del descuento no está confirmada (§10, regla 7).

### 9. Comparaciones múltiples e interpretación

Sebastián consolidará los **siete** valores p (T01–T03 y E1–E4) y aplicará el procedimiento **Holm**, controlando el error familiar al nivel 0,05. La familia se definió antes de ejecutar las pruebas (§5). Los valores p sin ajustar de T02 y E1–E4 están en `outputs/tablas/contraste_peso.csv` y `outputs/tablas/contrastes_complementarios.csv`, con las columnas `codigo` y `p`.

Se presentarán:

| Contraste | p original | p ajustado por Holm | Decisión con Holm |
|---|---|---|---|
| T01 Modalidad y atraso | Por calcular | Por calcular | Por determinar |
| T02 Peso medio | Por calcular | Por calcular | Por determinar |
| T03 Costo medio | Por calcular | Por calcular | Por determinar |
| E1 Distribución del peso (Mann-Whitney) | Por calcular | Por calcular | Por determinar |
| E2 Atraso según importancia alta | Por calcular | Por calcular | Por determinar |
| E3 Atraso según descuento > 10 | Por calcular | Por calcular | Por determinar |
| E4 Descuento medio | Por calcular | Por calcular | Por determinar |

La decisión principal de cada contraste se basará en el valor p ajustado.

Los IC del 95 % serán **intervalos individuales sin ajuste por multiplicidad**. No se presentarán como intervalos simultáneos ni se exigirá coincidencia entre su exclusión de cero y la decisión ajustada por Holm.

Se aplicarán estas reglas de interpretación:

- Rechazar H₀ aporta evidencia contra la hipótesis nula bajo los supuestos del método.
- No rechazar H₀ no demuestra igualdad ni ausencia de asociación.
- Un valor p no expresa la probabilidad de que H₀ sea verdadera.
- Significancia estadística no implica importancia operacional.
- Las conclusiones considerarán magnitud, incertidumbre y limitaciones.
- No se cambiarán las preguntas por obtener resultados no significativos.

### 10. Calidad de datos y denominadores

Antes de la inferencia, Y03 verificará esquema, tipos, nulos, dominios, duplicados, rangos y observaciones extremas.

**Reglas de tratamiento**

1. Conservar el archivo original sin modificaciones.
2. Documentar transformaciones y exclusiones con sus motivos y conteos.
3. No eliminar extremos válidos automáticamente.
4. No eliminar perfiles repetidos solo porque coincidan sus características.
5. No crear faltantes artificiales.
6. Conservar las categorías observadas de bodega; no reemplazar F por E para ajustarlas a la descripción.
7. Mantener `Discount_offered` como unidad no especificada mientras no exista confirmación. No etiquetarla como porcentaje o moneda.

**Denominadores**

- Proporción global: registros con resultado válido.
- Atraso por categoría: registros con resultado y categoría válidos dentro de esa categoría.
- Medias e IC: registros válidos de la variable correspondiente.
- Welch: registros con resultado y variable numérica válidos.
- χ²: registros con modalidad y resultado válidos.

Si aparecen faltantes, cada análisis utilizará los registros válidos de las variables necesarias y reportará su n efectivo. No se aplicará una eliminación global sin justificarla.

### 11. Limitaciones previstas

Se documentará:

- Mecanismo de selección y población de origen, si están disponibles.
- Posible dependencia entre registros de un mismo cliente o proceso logístico.
- Ausencia de fechas suficientes para establecer secuencia temporal.
- Incertidumbre sobre el momento de registro de llamadas y calificaciones.
- Unidad del descuento pendiente de confirmación.
- Posibles factores de confusión no observados.

Las llamadas o calificaciones podrían haberse registrado después del atraso. Su asociación no demuestra utilidad para anticiparlo.

El análisis no permitirá atribuir el atraso a la modalidad, el peso o el costo.

### 12. Trazabilidad y presentación

Cada resultado deberá identificar:

- Pregunta y responsable.
- Variables y muestra efectiva.
- Procedimiento y supuestos.
- Estadísticos, estimadores y unidades.
- Valor p original y ajustado, cuando corresponda.
- Intervalo de confianza y medida de efecto.
- Interpretación y limitación.
- Archivo o sección donde puede reproducirse.

Las cifras se conservarán con precisión completa en las exportaciones. El redondeo se aplicará al presentar tablas y texto.

Los valores p pequeños se expresarán, por ejemplo, como **p < 0,001**; no como **p = 0,000**.

Los cambios de método se registrarán con motivo, fecha, responsable y revisión. Si ocurren después de observar resultados, se declarará ese hecho.

### 13. Calendario y condiciones para avanzar

**Fecha límite confirmada por el equipo: 08-10-2026.**  
**Hora oficial de cierre confirmada: 23:59.**  
**Zona horaria de referencia: America/Santiago.**

Los bloques representan secuencia de trabajo y pueden ejecutarse dentro de una misma jornada.

| Orden | Bloque | Trabajo | Responsables | Condición para avanzar |
|---|---|---|---|---|
| 1 | B1 | Fuente, diccionario, protocolo y entorno | Yerko, José y Sebastián | Resultado, variables y métodos revisados |
| 2 | B2 | Calidad, carga y descriptiva | Yerko y Sebastián | Base analítica validada |
| 3 | B3 | Estimaciones y tres contrastes | José, Yerko y Sebastián | Resultados propios documentados |
| 4 | B4 | Holm, figuras, síntesis e informe | Sebastián, José y Yerko | Resultados y textos integrados |
| 5 | B5 | Revisión y ejecución completa | José, Yerko y Sebastián | Correcciones cerradas y PDF verificado |
| 6 | B6 | Entrega y publicación inicial | Sebastián y José | Comprobante y publicación disponibles |
| 7 | Foro | Dos comentarios y registro de evidencia | José, Yerko y Sebastián | Dos grupos distintos comentados dentro del plazo |

Se trabajará con el 08-10-2026 a las 23:59 como límite para entrega y foro, salvo que Canvas establezca explícitamente otro plazo para este último.

### 14. Cierre de J01

J01 podrá marcarse como completada cuando:

- [ ] Y02 confirme significado, unidades y dominios relevantes.
- [ ] Se corrobore la codificación 1 = atraso y 0 = a tiempo.
- [ ] Yerko revise el protocolo.
- [ ] El equipo valide las preguntas y los métodos.
- [x] Se registre la hora oficial de cierre: 08-10-2026 a las 23:59, hora de Chile.
- [ ] El protocolo quede disponible antes de ejecutar los contrastes.

**Estado actual:** protocolo desarrollado; plazo confirmado por José. Pendiente de validación de Y02 y revisión del equipo.
