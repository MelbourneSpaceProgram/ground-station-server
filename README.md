# Ground station backend

The backend for the ACRUX-2 ground station. It maintains a list of tracked satellites and computes the time of their passes.

## Building and running

## API

### List all satellites

**Definition**

`GET /satellites`

**Response**

- `200 OK` on success

```json
[
  {
    "id": "43013",
    "name": "NOAA-20",
    "pipeline": "NOAA"
  },
  {
    "id": "33591",
    "name": "NOAA-19",
    "pipeline": "NOAA"
  }
]
```

### Adding a new satellite

**Definition**

`POST /satellites`

**Arguments**

- `"id":string` the NORAD ID for this satellite
- `"name":string` the name of the satellite
- `"pipeline":string` the decoding pipeline relevant for the satellite

If a satellite with the given `id` already exists, the existing data will be overwritten.

**Response**

- `201 Created` on success

```json
{
  "id": "43013",
  "name": "NOAA-20",
  "pipeline": "NOAA"
}
```

### Lookup satellite details

**Definition**

`GET /satellites/<id>`

**Response**

- `404 Not Found` if the satellite does not exist
- `200 OK` on success

```json
{
  "id": "43013",
  "name": "NOAA-20",
  "pipeline": "NOAA"
}
```

### Delete satellite

**Definition**

`DELETE /satellites/<id>`

**Response**

- `404 Not Found` if the satellite does not exist
- `204 No Content` on success

```json
{
  "id": "43013",
  "name": "NOAA-20",
  "pipeline": "NOAA"
}
```

### Lookup next pass

**Definition**

`GET /passes/<id>`

**Response**

- `404 Not Found` if the satellite does not exist
- `200 OK` on success

```json
{
  "date": "2021-12-09T17:11:30.321Z"
}
```
