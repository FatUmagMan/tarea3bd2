# Projecto 3 (frontend)

## Contexto

Este proyecto implementa una interfaz web para un sistema de gestión de biblioteca.
Las tecnologías utilizadas son:

- Lenguaje de programación: Typescript
- Gestor de dependencias: PNPM
- Framework web: Vue 3 (composition API)
- Librería de componentes: Inkline
- Otras librerías: Vue Router, Pinia

## ¿Cómo configurar el entorno para el proyecto?

1. Instala las dependencias del proyecto con PNPM
   ```shell
   pnpm install
   ```
2. Ejecuta el servidor de desarrollo
   ```shell
   pnpm dev
   ```
3. Si no hay errores, la interfaz estará disponible en http://localhost:5173/.

## ¿Cómo trabajar en el proyecto?

Al considerar la implementación de nueva página asociada con alguna interacción con la API, se debe seguir el siguiente
procedimiento:

1. Crear una nueva interfaz en `interfaces.ts` que sea coherente con el modelo de datos asociado en la API.
2. Crear una nueva función para interactuar con la ruta de la API en `api/index.ts`.
3. Crear una nueva vista en `views/` para crear la página que hará uso de la función creada en el paso anterior.
4. Asociar una ruta en `router/index.ts` para la nueva vista creada en el paso anterior.

Es importante considerar que este flujo de trabajo aplicaría sólo para implementar nuevas páginas, pero en caso de
querer añadir nuevas funcionalidades o modificar las existentes, es flujo de trabajo será más específico y dependerá
de la funcionalidad a implementar.

### Si quieres usar nuevos íconos

La librerías de íconos que utiliza el proyecto es Font Awesome 6. Para utilizar nuevos íconos, primero debes
[buscar el ícono que deseas](https://fontawesome.com/search?o=r&m=free) y luego importarlo en el archivo `main.ts` junto
a los íconos ya importados. Por ejemplo, para el ícono "user":

```typescript
// Agrega faUser al import
import { faCircleInfo, faEdit, faMoon, faSun, faUser } from '@fortawesome/free-solid-svg-icons'
// ...
// Agrega faUser al objeto de íconos
library.add(faCircleInfo, faEdit, faMoon, faSun, faUser)
```

Esto permitirá utilizar el ícono en cualquier parte del proyecto a través del componente `FontAwesomeIcon`.

## Recomendaciones

- Utilizar el comando `pnpm format` y `pnpm lint --fix` para formatear el código antes de hacer un commit.

## En caso de errores...

- Recuerda revisar los errores en la consola del navegador.
- Si el error impide que parta el servidor de desarrollo, revisa que no haya errores de sintaxis en el código.
- Si el error es un error desde el servidor, revisa que los datos que estás enviando a la API sean adecuados y que
  la ruta y método que estás utilizando sea la correcta. Esto se puede hacer a través de la pestaña de red en las
  herramientas de desarrollador del navegador.
