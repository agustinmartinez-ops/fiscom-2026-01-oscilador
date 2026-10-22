# Pregunta y predicciones

Completen este archivo **antes** de ejecutar los experimentos.

## Pregunta

¿Qué evidencia necesitamos para confiar en una trayectoria del oscilador
calculada durante muchos ciclos?

La trayectoria obtenida debe converger a la solución analítica que ya conocemos: una solución armónica

## Modelo y supuestos

- Una masa unida a un resorte ideal, sin rozamiento: $m x''=-kx$.
- Medimos el tiempo en unidades de $1/\omega$, con $\omega=\sqrt{k/m}$. Así la
  ecuación queda $x''=-x$ y un período dura $2\pi$.
- La energía por unidad de masa es $E=(x^2+v^2)/2$.

## Predicciones

1. ¿Qué forma tiene la órbita exacta en el plano $(x,v)$? ¿Qué pasa con la
   energía exacta a lo largo del tiempo?

   Con las unidades que estamos usando tenemos $E = (x^2 + v^2)/2$ constante. Entonces, la órbita exacta debe ser una circunferenia de radio igual $\sqrt(2E)$.

2. Escriban a mano un paso de Euler explícito para $x''=-x$. ¿En qué factor
   cambia $x^2+v^2$ en ese paso? ¿Y en un paso de Euler implícito?

   Euler explícito:

      $v_{n+1} = v_n - dt * x_n$
      $x_{n+1} = x_n + dt * v_n$

      $E_{n+1} = 1/2 * (x_n^2 + dt^2 * v_n^2 + 2 * dt * x_n * v_n + v_n^2 + dt^2 * x_n^2 - 2 * dt * v_n * x_n) = (dt^2 + 1) * E_n$

   Euler implicíto:

      $x_{n+1} = x_n + dt * v_{n+1}$
      $v_{n+1} = v_n - dt * x_{n+1}$

      Despejando:

      $x_{n+1} = x_n + dt * v_n - dt^2 * x_{n+1}$ Entonces 
      
      $x_{n+1} = (x_n + dt * v_n)/(1 + dt^2)$

      $v_{n+1} = v_n - dt * (x_n + dt * v_n)/(1 + dt^2) = (1 - dt^2/(1 + dt^2)) * v_n - dt * x_n/(1 + dt^2)$

      $v_{n+1} = (v_n - dt * x_n)/(1 + dt^2)$

      $E_{n+1} = E_n/(1 + dt^2)$

3. Con esa cuenta, ¿qué esperan que pase con la amplitud y con el período de
   la oscilación después de diez períodos con cada método? ¿Qué verían en el
   plano $(x,v)$?

   Con el método de euler implícito, el sistema disipa energía en cada paso. Luego de 10 períodos, el número total de pasos es $N = 20*\pi/dt$:

   $E_{n+10} = E_n/(1 + dt^2)^N$

   Y como la apmlitud del movimiento va como $\sqrt(2E)$, luego de 10 pasos dicha amplitud se achica.

4. Si `dt` se reduce a la mitad, ¿qué esperan que ocurra con el error a tiempo
   final fijo?

   A un tiempo final fijo $T$, el número de pasos a realizar es $N = T/dt ~ O(1/dt)$. El error local de un solo paso es de orden $e_l ~ O(dt^2)$. El error final es $e_f ~ N * O(dt^2) ~ O(dt)$. Entonces si reducimos el paso temporal a la mitad, el error a tiempo final tambien se reduce a la mitad.

5. Para el resorte, ¿cuántas iteraciones de Newton esperan que haga falta en
   cada paso implícito?

   Tenemos un sistema de ecuaciones extrictamente lineales, entonces el método de Newton necesita sólamente 1 iteración por paso.

## Criterio de aceptación

Propongan un criterio para decidir si un valor de `dt` es aceptable para
simular cien períodos. ¿Qué cantidad medirían y qué tolerancia le pedirían?

Mediría la amplitud final del movimiento y pediría que discrepe de la inicial con un error de 10^-5.