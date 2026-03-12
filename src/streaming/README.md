Staging Layer

Este directorio representa la zona de staging del pipeline ETL. El staging se utiliza para almacenar datos temporalmente antes de ser procesados. En este proyecto se simula mediante archivos locales:

batch_input.jsonl
datos introducidos por el usuario

batch_output.jsonl
resultados generados por el batch

Cada línea contiene un JSON independiente.

Ejemplo:

{"value": 5}

Después de procesarse:

{"result": 6}

En sistemas reales, el staging podría ser un S3, HDFS, Data Lake, una base de datos temporal, una cola de mensajes o cualquier otro sistema, pero por no complicar más las cosas lo dejamos aquí.