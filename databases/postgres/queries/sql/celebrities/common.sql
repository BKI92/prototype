-- name: retrieve^
SELECT
    pk,
    name,
    description,
    created
FROM celebrities
WHERE pk = :pk;

-- name: create<!
INSERT INTO celebrities (
    name,
    description,
    created
) VALUES (
    :name,
    :description,
    :created
) RETURNING
    pk,
    name,
    description,
    created;


-- name: list
SELECT
    pk,
    name,
    description,
    created
FROM celebrities
WHERE 1 = 1
ORDER BY created;