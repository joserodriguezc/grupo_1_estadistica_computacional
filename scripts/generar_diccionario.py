"""Y02: genera docs/diccionario_variables.csv a partir del CSV original (solo lectura)."""
from pathlib import Path
import pandas as pd

raiz = Path(__file__).resolve().parents[1]
df = pd.read_csv(raiz / "data/raw/ecommerce_shipping.csv", encoding="utf-8-sig")

# (nombre analítico, descripción, tipo estadístico, unidad, rol, observaciones)
meta = {
 "ID": ("id_envio", "Identificador del registro de envío", "Identificador nominal", "sin unidad", "Identificador", "Solo verificar unicidad; excluir de estadísticas y correlaciones. No implica orden cronológico ni un cliente por registro."),
 "Warehouse_block": ("bloque_bodega", "Bloque de bodega desde donde sale el envío", "Cualitativa nominal", "sin unidad", "Explicativa", "Archivo trae A, B, C, D y F; Kaggle describe A-E. No recodificar F como E."),
 "Mode_of_Shipment": ("modalidad_envio", "Modalidad de transporte del envío", "Cualitativa nominal", "sin unidad", "Explicativa (contraste T01)", "Categorías: Flight, Road, Ship."),
 "Customer_care_calls": ("llamadas_atencion", "Número de llamadas de consulta del cliente por el envío", "Cuantitativa discreta (conteo)", "llamadas", "Explicativa / estimación IC", "Momento de registro no documentado; podría ser posterior al atraso."),
 "Customer_rating": ("calificacion_cliente", "Calificación del cliente (1 = peor, 5 = mejor)", "Cualitativa ordinal", "puntos 1-5", "Explicativa", "Orden 1<2<3<4<5; no suponer distancias iguales. Momento de registro no documentado."),
 "Cost_of_the_Product": ("costo_producto", "Costo del producto", "Cuantitativa de razón", "USD (según Kaggle)", "Explicativa (contraste T03)", "Registrado en enteros."),
 "Prior_purchases": ("compras_previas", "Número de compras previas del cliente", "Cuantitativa discreta (conteo)", "compras", "Explicativa", "Observado 2-10; no aparece el valor 9."),
 "Product_importance": ("importancia_producto", "Importancia del producto", "Cualitativa ordinal", "categoría", "Explicativa", "Orden: low < medium < high."),
 "Gender": ("genero", "Género registrado del cliente", "Cualitativa nominal", "sin unidad", "Explicativa", "Categorías F y M tal como se registran."),
 "Discount_offered": ("descuento_ofrecido", "Descuento ofrecido sobre el producto", "Cuantitativa", "NO ESPECIFICADA", "Explicativa", "No asumir % ni moneda. Observado 1-65."),
 "Weight_in_gms": ("peso_gramos", "Peso del producto", "Cuantitativa de razón", "gramos (según Kaggle)", "Explicativa (contraste T02)", "Registrado en enteros."),
 "Reached.on.Time_Y.N": ("entrega_atrasada", "Resultado de la entrega", "Nominal binaria", "0/1", "Resultado", "1 = no llegó a tiempo (atrasada); 0 = llegó a tiempo. Confirmado en descripción de Kaggle."),
}
filas = []
for i, c in enumerate(df.columns, 1):
    s = df[c]
    nombre, desc, tipo, unidad, rol, obs = meta[c]
    if pd.api.types.is_numeric_dtype(s) and s.nunique() > 12:
        dominio = f"enteros {s.min()} a {s.max()}"
    else:
        dominio = "; ".join(str(k) for k in sorted(s.unique()))
    filas.append(dict(posicion=i, nombre_original=c, nombre_analitico=nombre, descripcion=desc,
        tipo_estadistico=tipo, dtype_pandas=str(s.dtype), unidad=unidad, dominio_observado=dominio,
        n_distintos=s.nunique(), n_nulos=int(s.isna().sum()), rol=rol, observaciones=obs))

out = pd.DataFrame(filas)
out.to_csv(raiz / "docs/diccionario_variables.csv", index=False, encoding="utf-8")
print(out[["nombre_original", "tipo_estadistico", "dtype_pandas", "dominio_observado", "n_distintos"]].to_string())
