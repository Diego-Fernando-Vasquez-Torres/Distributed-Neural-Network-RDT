# Distributed Neural Network RDT (UDP | C++ | Pybind11)

Universidad Católica San Pablo  
Curso: Redes y Comunicaciones  
Docente: Dr. Julio Santisteban Pablo  

Integrantes:
- Jorge Chávez
- José Cornejo
- Marela Mendoza
- Diego Vásquez

---

## 1. Descripción del proyecto

Este proyecto implementa el entrenamiento distribuido de una red neuronal
utilizando una arquitectura tipo Parameter Server.

El sistema está basado en comunicación UDP, sobre la cual se implementa un
protocolo propio llamado RDT-UDP, encargado de garantizar comunicación confiable.

El objetivo principal del proyecto es ser capaces de implementar un protocolo de
transporte desde cero, incluyendo control de errores, orden y retransmisión.

---

## 2. Arquitectura del sistema

El sistema está compuesto por:

- 1 nodo maestro
- 3 nodos esclavos

El flujo de trabajo es el siguiente:

El maestro distribuye datos y parámetros, los esclavos entrenan localmente y
envían gradientes de regreso al maestro para agregación.

---

## 3. Capas del sistema

### Capa de aplicación (Python)

Implementada con PyTorch.

Responsable de:
- Entrenamiento del modelo
- Cálculo de pérdida
- Evaluación de métricas
- Visualización de resultados

---

### Capa de comunicación (C++)

Implementada con sockets UDP.

Responsable de:
- Implementación del protocolo RDT-UDP
- Fragmentación de mensajes
- Construcción de datagramas
- Control de errores
- Retransmisión
- Reensamblaje de mensajes

---

### Interfaz Python – C++

Se utiliza Pybind11 para exponer funciones de C++ hacia Python.

Esto permite que el entrenamiento en PyTorch utilice directamente el protocolo
implementado en C++.

---

## 4. Estructura del proyecto


proyecto_ia_distribuida/

├── dataset/
│ └── Diabetes.csv

├── maestro/
│ ├── maestro.py
│ ├── rdt_master.cpp
│ ├── rdt_master.hpp
│ ├── bindings.cpp
│ ├── setup.py

├── esclavo/
│ ├── esclavo.py
│ ├── rdt_slave.cpp
│ ├── rdt_slave.hpp
│ ├── bindings.cpp
│ ├── setup.py

└── Protocolo.txt


---

## 5. Formato del datagrama (parte más importante)

Cada paquete tiene tamaño fijo obligatorio:

500 bytes exactos

Estructura:

- FLAGS (2 bytes)
- SEQ (4 bytes)
- ACK/NACK (4 bytes)
- PAYLOAD (489 bytes)
- CHECKSUM (1 byte)

---

## 6. Tipos de datos en el sistema

El PAYLOAD transporta tres tipos de información:

- DATASET: particiones del archivo de entrenamiento
- WEIGHTS: parámetros del modelo neuronal
- GRADIENT: gradientes calculados por los nodos esclavos

Todos los datos se serializan en texto plano.

---

## 7. Mecanismos del protocolo

El sistema implementa:

- Control de errores mediante checksum
- Control de orden mediante SEQ
- Confirmación de recepción mediante ACK
- Retransmisión mediante NACK
- Timeout con select()
- Algoritmo de Karn para estimación de RTT
- Backoff exponencial para evitar congestión

---

## 8. Flujo del sistema

1. El maestro divide el dataset en partes iguales.
2. Envía datos a los esclavos.
3. Envía parámetros iniciales del modelo.
4. Cada esclavo entrena localmente.
5. Los gradientes son enviados al maestro.
6. El maestro valida y promedia gradientes.
7. Se actualiza el modelo global.

---

## 9. Compilación

Maestro:

cd maestro
python setup.py build_ext --inplace


Esclavos:

cd esclavo
python setup.py build_ext --inplace


---

## 10. Ejecución

Esclavos primero:

python esclavo.py


Maestro después:

python maestro.py


---

## 11. Resultado esperado

- Modelo entrenado distribuido
- Métricas de clasificación
- Matriz de confusión
- Curva de pérdida

---

## 12. Referencia

Kurose & Ross – Computer Networking: A Top-Down Approach
