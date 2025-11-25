# Specyfikacja API: {{api_name}}

**Wersja:** 1.0.0  
**Data:** {{date}}  
**Autor:** {{author}}

## Przegląd

{{overview}}

## Informacje Podstawowe

- **Base URL:** `https://api.example.com`
- **Wersja API:** {{api_version}}
- **Format:** JSON
- **Autoryzacja:** {{auth_type}}

## Endpointy

### {{endpoint_name}}

**Metoda:** `{{method}}`  
**URL:** `{{endpoint_url}}`

#### Opis

{{endpoint_description}}

#### Parametry

| Nazwa         | Typ     | Wymagany | Opis         |
|---------------|---------|----------|--------------|
{{parameters}}

#### Request Body

```json
{{request_body}}
```

#### Response

**Status Code:** `{{status_code}}`

```json
{{response_body}}
```

#### Przykład

```bash
curl -X {{method}} \
  https://api.example.com{{endpoint_url}} \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{{request_example}}'
```

## Kody Błędów

| Kod | Znaczenie              | Opis                      |
|-----|------------------------|---------------------------|
| 400 | Bad Request            | Nieprawidłowe żądanie     |
| 401 | Unauthorized           | Brak autoryzacji          |
| 403 | Forbidden              | Brak uprawnień            |
| 404 | Not Found              | Zasób nie znaleziony      |
| 500 | Internal Server Error  | Błąd serwera              |

## Modele Danych

### {{model_name}}

```json
{{model_schema}}
```

## Autoryzacja

{{authorization_details}}

## Rate Limiting

{{rate_limiting}}

## Wersjonowanie

{{versioning}}

## Changelog

### Wersja 1.0.0

{{changelog}}

