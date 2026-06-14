<!-- desc: Factura, presupuesto o cotización con datos de emisor/cliente, tabla de conceptos, totales e impuestos. -->
# Tipo: Factura / presupuesto

Documento comercial con maquetación precisa. Mejor en **PDF** vía `generar_documento_codigo` (reportlab) si quieres cabecera de marca y totales bien alineados; o vía `generar_documento_markdown` con `estilo_css` propio para un acabado rápido. Para un libro de cálculo editable usa **XLSX**.

## Elementos imprescindibles
- **Encabezado**: nombre/logo del emisor, datos fiscales (NIF/CIF), dirección, contacto.
- **Número de factura/presupuesto** y **fecha** (y fecha de vencimiento o validez).
- **Datos del cliente**: nombre, identificación fiscal, dirección.
- **Tabla de conceptos**: descripción, cantidad, precio unitario, importe.
- **Totales**: base imponible, impuestos (IVA/IGIC u otros con su %), **total a pagar** destacado.
- **Condiciones de pago**: método, cuenta/IBAN, plazo.
- Notas o términos al pie si aplica.

## Buenas prácticas
- Alinea importes a la derecha; usa separador de miles y 2 decimales.
- Calcula y muestra impuestos por separado del subtotal.
- El total final debe resaltar (negrita, tamaño mayor o fondo de color).
- Numeración y fecha siempre visibles arriba.

## Errores a evitar
- Olvidar los datos fiscales o el desglose de impuestos.
- Importes mal alineados o sin formato monetario.
- No incluir número de documento.
- En XLSX, calcular totales en Python en vez de con fórmulas si el usuario los editará.
