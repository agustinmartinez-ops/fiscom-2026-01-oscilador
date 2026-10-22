# Cuaderno de laboratorio

## Fecha — Oscilador con los dos Euler

### Afirmación

¿Qué pueden afirmar a partir de los tests y de las figuras?

Como era de esperarse, la energía va aumentando en euler explicito y va disminuyendo en euler implicito. Tambien se comparó la convergencia de cada método y se observa que a dt más grandes el error es menor en euler implícito pero luego a dt mas chicos el error en ambos métodos es similar.

### Evidencia

- Comando ejecutado: 

    uv run pytest
    uv run python experiments/muchos_ciclos.py
    uv run python experiments/convergencia.py

- Resultado cuantitativo:

    Euler explícito
       dt       error   orden
  0.25133   1.133e+00       —
  0.12566   4.787e-01   1.243
  0.06283   2.177e-01   1.137
  0.03142   1.037e-01   1.070
  0.01571   5.058e-02   1.035
  0.00785   2.498e-02   1.018

    Euler implícito
       dt       error   orden
  0.25133   5.387e-01       —
  0.12566   3.245e-01   0.732
  0.06283   1.788e-01   0.859
  0.03142   9.394e-02   0.929
  0.01571   4.814e-02   0.964
  0.00785   2.437e-02   0.982

- Figura regenerable:

    fiscom-2026-01-oscilador\results\convergencia.png
    fiscom-2026-01-oscilador\results\muchos_ciclos.png

### Limitaciones

¿Qué no permite concluir este experimento? Consideren tanto el modelo físico
como el método numérico.

Este experimento no permite concluir que un método sea mejor que otro, al menos a pasos pequeños. Lo único que podríamos concluir es que el método implícito no explota en energía mientras que el explícito sí.

### Próximo control

¿Qué prueba adicional harían para confiar más en el resultado?

Probaría simulando una mayor cantidad de ciclos con diferentes valores de dt
