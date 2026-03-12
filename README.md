# Mini ETL Demo (Batch + Streaming)

Este proyecto es una **demo de un pipeline ETL completo** con dos modos de procesamiento:

- **Batch** → los datos se acumulan y se procesan cada X segundos
- **Streaming** → los datos se procesan inmediatamente al llegar

El objetivo funcional es muy simple, le das un número y te devuelve el siguiente.

Sin embargo, el proyecto está diseñado para **simular una arquitectura de datos real**, separando claramente:

- extracción
- limpieza
- transformación
- envío
- staging
- metadatos
- modelo independiente

Todo el sistema está **dockerizado** para que no sea necesario instalar dependencias manualmente.

---

# 1. Requisitos desde cero

El proyecto está pensado para ejecutarse desde un **terminal de VSCode** incluso en un sistema sin Python.

Solo necesitas instalar:

### 1.1. WSL (Windows Subsystem for Linux)

En el terminal ejecutar:

wsl --install

Esto instalará WSL Ubuntu (distribución Linux por defecto). Puede ser que pida un reinicio del ordenador

Luego entraremos en el subsistema (nos creará un usuario y hay que ponerle una contraseña). Para entrar, en vscode tenemos un símbolo como >< en la esquina inferior izquierda.

### 1.2. Git

Prueba primero si lo tienes ya:

```
git --version
```

Si no te sale, o te da error, ve a https://git-scm.com/downloads, instálalo y vuelve a probar.

### 1.3. Docker Desktop

Lo mismo que antes:

```
docker --version

docker compose version
```

Si no, en el mismo terminal,lanza lo siguiente (os pedirá la password de wsl):
```
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

---

# 2. Descargar el proyecto

Clonar el repositorio:

```
git clone <repo>
```

Aunque es más sencillo abrir en VSCode. En cualquier caso, poned vuestro nombre de usuario y correo con:

```
git config --global user.name "Nombre"
git config --global user.email "user@nebrija.es"
```

---

# 3. Construir el entorno

Desde el terminal de VSCode:

```
docker compose build
```

Esto construirá los contenedores:

- frontend
- model
- batch worker
- streaming worker
- redis (broker)

---

# 4. Arrancar el sistema

```
docker compose up
```

Esto iniciará:

- interfaz web
- cola de streaming
- workers
- modelo

La interfaz estará disponible en:

```
http://localhost:1936
```

---

# 5. Uso del sistema

La interfaz permite introducir un número. Las distintas configuraciones se pueden cambiar desde ```/app/src/common/config.py```

Dependiendo del modo elegido:


## Batch

1. el usuario introduce números
2. se almacenan en staging
3. cada X segundos el batch job se ejecuta
4. procesa todos los datos acumulados

Flujo:

```
Frontend
   ↓
Extract
   ↓
Staging
   ↓
(Batch trigger cada X segundos)
   ↓
Clean
   ↓
Transform
   ↓
Send
```

Esto simula un sistema típico de **procesamiento por lotes**.

---

## Streaming

1. el usuario introduce un número
2. el frontend envía el evento
3. el número entra en el pipeline
4. se procesa inmediatamente
5. se devuelve el resultado

Flujo:

```
Frontend
   ↓
Extract
   ↓
Clean
   ↓
Transform (modelo)
   ↓
Send
```

Resultado mostrado al instante.

---


# 6. Arquitectura del proyecto

El repositorio está organizado para reflejar una arquitectura ETL real.

```
mini-etl
│
├── src
│
│   ├── frontend
│   │
│   │   Interfaz web simple
│   │   - introduce números
│   │   - muestra resultados
│   │
│   ├── model
│   │
│   │   "modelo" aislado
│   │   predict(x) = x + 1
│   │
│   │   Está separado para simular
│   │   un modelo de ML real.
│   │
│   ├── batch
│   │
│   │   Pipeline batch dividido en:
│   │
│   │   ingest.py
│   │       extracción
│   │
│   │   clean.py
│   │       limpieza / validación
│   │
│   │   transform.py
│   │       llamada al modelo
│   │
│   │   send.py
│   │       envío del resultado
│   │
│   ├── streaming
│   │
│   │   pipeline en tiempo real
│   │   consume eventos y procesa
│   │   inmediatamente
│   │
│   ├── staging
│   │
│   │   zona temporal donde se guardan
│   │   datos antes de procesarlos
│   │
│   ├── metadata
│   │
│   │   registra información como:
│   │
│   │   - timestamp
│   │   - duración del job
│   │   - estado
│   │   - inputs y outputs
│   │
│   └── common
│
│       utilidades compartidas
│       logging
│       configuración
│
├── docker-compose.yml
│
│   orquesta todos los servicios
│
├── docs
│
│   documentación adicional
│
└── README.md
```

- **Extracción**: 
  - Batch: lee un archivo, o recibe un número por CLI o API y lo pone en staging.
  - Streaming: procesa cada dato según entra.

- **Limpieza**: `batch/clean.py` y la parte de limpieza en `consumer.py`.
  - Validaciones: que el input sea numérico, límites, valores nulos, etc.

- **Transformación**: `batch/transform.py` y `consumer.py` llamarán a `model/model.py`.
  - La lógica del "modelo" está aislada en `src/model/model.py` y expuesta como función o servicio HTTP según prefieras.

- **Envío / Load**: `batch/send.py` (escribir a output file, DB o respuesta HTTP) y dentro de `consumer.py` (publicar resultado / guardar en staging / retornar al frontend).

- **Staging**: `src/staging/` actúa como zona temporal de persistencia (archivos, sqlite o carpeta) accesible por los servicios.

- **Metadatos**: `src/metadata/collector.py` registra: timestamp de ingestión, tiempo de procesamiento, versiones del modelo, id de job, estado (ok/fail), y esquema de entrada/salida.

- **Front**: `src/frontend/app.py` (Flask) muestra un form con un campo numérico y un botón. Envío via POST a la API del pipeline batch o publica al topic en streaming y muestra el resultado.

- **Modelo**: `src/model/model.py` exporta `predict(x)` y se construye como contenedor Docker independiente. El resto de la aplicación trata al modelo como un servicio separado (o se puede importar directamente para simplificar las pruebas).

---

# 7. Metadatos

Cada ejecución registra:

- id de ejecución
- timestamp de entrada
- timestamp de salida
- duración
- input
- output
- estado

Esto permite simular **lineage y observabilidad de pipelines**.

---

