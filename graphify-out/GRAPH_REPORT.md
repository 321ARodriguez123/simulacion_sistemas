# Graph Report - Simulacion de sistemas  (2026-06-19)

## Corpus Check
- 7 files · ~1,442 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 29 nodes · 28 edges · 8 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ef59df37`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `reporte_simulacion()` - 5 edges
2. `generar()` - 4 edges
3. `configurar_tabla()` - 3 edges
4. `crear_input()` - 3 edges
5. `actualizar_inputs()` - 3 edges
6. `ejecutar_script_externo()` - 3 edges
7. `evaluar_media()` - 3 edges
8. `evaluar_varianza()` - 3 edges
9. `evaluar_uniformidad()` - 3 edges
10. `Configura dinámicamente las columnas del Treeview.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (8 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.31
Nodes (8): evaluar_media(), evaluar_uniformidad(), evaluar_varianza(), Verifica si la varianza de los datos tiende a 1/12 (aprox 0.0833)., Aplica la prueba de Chi-cuadrado para comprobar si los números se     distribuy, Ejecuta las tres pruebas y genera un reporte completo de la simulación., Verifica si la media de los datos tiende a 0.5 usando un intervalo de confianza., reporte_simulacion()

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (6): configurar_tabla(), ejecutar_script_externo(), generar(), Ejecuta un archivo .py externo, le envía los inputs y captura los prints., Configura dinámicamente las columnas del Treeview., Recopila los datos y llama a ejecutar_script_externo.

### Community 2 - "Community 2"
Cohesion: 0.50
Nodes (4): actualizar_inputs(), crear_input(), Crea una fila con un Label y un Entry dinámicamente., Actualiza los campos de texto según el método seleccionado.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generar()` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `configurar_tabla()` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `Configura dinámicamente las columnas del Treeview.`, `Crea una fila con un Label y un Entry dinámicamente.`, `Actualiza los campos de texto según el método seleccionado.` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._