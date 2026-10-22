"""Oscilador con Euler explícito, Euler implícito y Newton–Raphson.

El estado se representa como ``[x, v]``. El tiempo se mide en unidades de
``1/ω``, con ``ω = sqrt(k/m)``: así la masa con resorte cumple ``x'' = -x`` y
un período dura ``2π``.

Los integradores reciben la aceleración como una función de la posición,
``a(x)``. Euler implícito recibe además su derivada ``da/dx``, que usa
Newton–Raphson.
"""

import numpy as np


def aceleracion_resorte(x: float) -> float:
    """Aceleración de la masa con resorte ideal, ``a(x) = -x``."""

    return -x


def derivada_aceleracion_resorte(x: float) -> float:
    """Derivada ``da/dx`` del resorte ideal."""

    return -1.0


def newton_raphson(G, derivada_G, z0: float, tolerancia: float = 1e-12, max_iter: int = 50) -> float:
    """Busca una raíz de ``G`` partiendo de ``z0``.

    Cada iteración reemplaza ``G`` por su recta tangente y toma el cero de esa
    recta: ``z ← z - G(z) / G'(z)``. Se detiene cuando el residuo ``|G(z)|`` es
    menor que ``tolerancia``: una corrección pequeña no alcanza si el residuo
    sigue siendo grande. Si la derivada se anula o no converge en ``max_iter``
    iteraciones, lanza ``ArithmeticError``: nunca devuelve en silencio un valor
    que no convergió.
    """

    iter = 0
    while iter < max_iter:
        Gz = G(z0)
        if abs(Gz) < tolerancia:
            return z0
        dGz = derivada_G(z0)
        if dGz == 0:
            raise ArithmeticError("derivada nula")
        z0 -= Gz / dGz
        iter += 1

    if abs(G(z0)) < tolerancia:
        return z0
    raise ArithmeticError("Newton-Raphson no convergió")


def integrar_euler_explicito(
    estado_inicial: np.ndarray,
    dt: float,
    pasos: int,
    aceleracion=aceleracion_resorte,
) -> tuple[np.ndarray, np.ndarray]:
    """Integra ``x' = v``, ``v' = a(x)`` con Euler explícito.

    Cada paso usa la pendiente al **comienzo** del intervalo:

        x[n+1] = x[n] + dt v[n]
        v[n+1] = v[n] + dt a(x[n])

    Devuelve un arreglo de tiempos y otro de estados. Ambos incluyen la
    condición inicial, por lo que tienen ``pasos + 1`` elementos.
    """

    tiempos = np.linspace(0, dt * pasos, pasos + 1)
    estados = np.empty((pasos + 1, 2))
    estados[0] = estado_inicial

    for i in range(pasos):
        estados[i + 1] = estados[i] + dt * np.array(
            [estados[i, 1], aceleracion(estados[i, 0])]
        )

    return tiempos, estados


def integrar_euler_implicito(
    estado_inicial: np.ndarray,
    dt: float,
    pasos: int,
    aceleracion=aceleracion_resorte,
    derivada_aceleracion=derivada_aceleracion_resorte,
) -> tuple[np.ndarray, np.ndarray]:
    """Integra ``x' = v``, ``v' = a(x)`` con Euler implícito.

    Cada paso usa la pendiente al **final** del intervalo:

        x[n+1] = x[n] + dt v[n+1]
        v[n+1] = v[n] + dt a(x[n+1])

    Reemplazando la segunda ecuación en la primera queda una sola ecuación
    para ``z = x[n+1]``:

        G(z) = z - x[n] - dt v[n] - dt² a(z) = 0,

    que se resuelve con ``newton_raphson`` partiendo de ``z = x[n]``. Después,
    ``v[n+1]`` sale de la segunda ecuación.

    Devuelve tiempos y estados, con ``pasos + 1`` elementos cada uno.
    """

    tiempos = np.linspace(0, dt * pasos, pasos + 1)
    estados = np.empty((pasos + 1, 2))
    estados[0] = estado_inicial

    for i in range(pasos):
        x_n, v_n = estados[i]
        a_n = aceleracion(x_n)

        # Definir G(z) = z - x_n - dt * v_n - dt^2 * a(z)
        def G(z):
            return z - x_n - dt * v_n - dt**2 * aceleracion(z)

        # Definir G'(z) = 1 - dt^2 * a'(z)
        def derivada_G(z):
            return 1 - dt**2 * derivada_aceleracion(z)

        # Resolver G(z) = 0 con Newton-Raphson
        z0 = x_n
        x_np1 = newton_raphson(G, derivada_G, z0, tolerancia=1e-10, max_iter=100)
        v_np1 = v_n + dt * aceleracion(x_np1)

        estados[i + 1] = x_np1, v_np1

    return tiempos, estados


def solucion_exacta(tiempos: np.ndarray, estado_inicial: np.ndarray) -> np.ndarray:
    """Solución del resorte ideal, ``x(t) = x0 cos t + v0 sin t``."""

    x0, v0 = np.asarray(estado_inicial, dtype=float)
    t = np.asarray(tiempos, dtype=float)
    return np.column_stack(
        (
            x0 * np.cos(t) + v0 * np.sin(t),
            -x0 * np.sin(t) + v0 * np.cos(t),
        )
    )


def energia(estados: np.ndarray) -> np.ndarray:
    """Energía del resorte por unidad de masa, ``(v² + x²) / 2``.

    Acepta un estado ``[x, v]`` o una tabla de estados de forma ``(n, 2)``.
    """

    estados = np.asarray(estados, dtype=float)
    return 0.5 * (estados[..., 0] ** 2 + estados[..., 1] ** 2)
