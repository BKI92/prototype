-- name: retrieve^
SELECT
    pk,
    tg_id,
    username,
    description,
    created,
    updated
FROM users
WHERE pk = :pk;

-- name: create<!
INSERT INTO users (
    tg_id,
    username,
    description,
    created
) VALUES (
    :tg_id,
    :username,
    :description,
    :created
) RETURNING
    pk,
    tg_id,
    username,
    description,
    created;


-- name: list
SELECT
    pk,
    tg_id,
    username,
    description,
    created
FROM users
WHERE 1=1
ORDER BY created;