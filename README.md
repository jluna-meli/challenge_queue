<div style="text-align: center;">
<h1>Sprint 3</h1>
Challenge Queue
</div>

<br />

<details open="open">
<summary>Tabla de Contenidos</summary>

- [Requisitos](#Requisitos)
- [Levantar el proyecto](#levantar-el-proyecto)
- [Construido con](#construido-con)
- [Validaciones](#validaciones)
- [Test](#tests)

</details>

---

## Requisitos

- El challenge consta de implementar una cola de mensajes utilizando un Redis y además implementar una API que nos permita abstraernos.

---

## Levantar el proyecto

* En terminal correr la siguiente linea de código.
```
   docker compose up
```

### Repositorio

```
    git clone github.com:jluna-meli/challenge_queue.git
```

---

## Construido con

_Herramientas utilizadas:_

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [Redis](https://redis.io/)
* [Unittest](https://docs.python.org/3/library/unittest.html)

---
## Endpoints

#### Login
| HTTP | URI         | Descripción                                    |
|:-----|:------------|:-----------------------------------------------|
| POST | /login       | Iniciar sesión                         |

##### Request

Para esta versión del Challenge, el username debe llamarse "Admin"
```json
{
  "name": String,
  "password": String
}
```
##### Response
Se retorna el token
```json
ey*******y7b
```

#### Verificación del token
---
| HTTP | URI         | Descripción                                    |
|:-----|:------------|:-----------------------------------------------|
| GET | api/verify/token | Verificación del funcionamiento del token |

##### Request

```
Headers:
Authorization = Bearer ey****y7b
```

#### Response
Status Code 200
```json
{
    "exp": timestamp,
    "password": String,
    "username": String
}

```
---

### PUSH mensaje

| HTTP  | URI             | Descripción             |
|:------|:----------------|:------------------------|
| POST  | /api/queue/push | Dar de alta un  mensaje |

##### Request

```
Headers:
Authorization = Bearer ey****y7b
```

```json
{
    "msg": String
}
```
---

##### Response
```json
{
    "status": "success"
}
```

---
### POP mensaje

| HTTP   | URI            | Descripción                          |
|:-------|:---------------|:-------------------------------------|
| DELETE | /api/queue/pop | Elimina el mensaje de la cola (FIFO) |

##### Request

```
Headers:
Authorization = Bearer ey****y7b
```

---

##### Response

```json
{
    "msg": String,
    "status": "success"
}

```
---
### COUNT

| HTTP | URI            | Descripción                          |
|:-----|:---------------|:-------------------------------------|
| GET  | /api/queue/pop | Elimina el mensaje de la cola (FIFO) |

##### Request

```
Headers:
Authorization = Bearer ey****y7b
```

---

##### Response

```json
{
    "count": Integer,
    "status": "0k"
}

```
---

## Validaciones
```
• Header: 
   Authorization =  Bearer token
• 'msg' debe ser string y no nulo

```


---

## Tests 

---

### Listado de tests

#### Test
```
• test_validate_toke: Verifica que el token sea valido
• test_r_push_successful: Verifica que se genere un mensaje nuevo, status_code 201
• test_r_push_fail_when_msg_is_not_string: Verifica que falle cuando el msg no sea string, status_code 400
• test_r_push_fail_when_msg_is_null: Verifica que falle cuando el msg sea null, status_code 400
• test_r_count: Verifica que cuente el valor de los msg, status_code 200
• test_r_pop: Verifica que elimine satisfactoriamente un mensaje, status_code 200
• test_r_pop_fail: Verifica que falle cuando no haya mensajes por eliminar, status_code 400
```

---
### Comentarios generales

---


