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

### Lookup next pass

Returns timestamps for the start and end of the next pass.

**Definition**

`GET /satellites/<id>/passes`

**Response**

- `404 Not Found` if the satellite does not exist
- `200 OK` on success

```json
{
  "date": "2021-12-09T17:11:30.321Z"
}
```

### Get position data

Samples the satellite position every second over the next hour.

**Definition**

`GET /satellites/<id>/position`

**Response**

- `404 Not Found` if the satellite does not exist
- `200 OK` on success

```json
[
  ["22/01/06-11:45:13", -30.830016, -164.891788],
  ["22/01/06-11:45:14", -30.771716, -164.908093],
  ["22/01/06-11:45:15", -30.713413, -164.924384],
  ["22/01/06-11:45:16", -30.655109, -164.94066],
  ["22/01/06-11:45:17", -30.596803, -164.956922]
]
```
