-- name: retrieve^
SELECT
    user_pk,
    celebrity_pk,
    title,
    created
FROM messages
WHERE pk = :pk;

-- name: create<!
INSERT INTO messages (
    user_pk,
    celebrity_pk,
    title,
    created
) VALUES (
    :user_pk,
    :celebrity_pk,
    :title,
    :created
) RETURNING
    user_pk,
    celebrity_pk,
    title,
    created;


-- name: list
SELECT
    user_pk,
    celebrity_pk,
    title,
    created
FROM messages
WHERE 1=1
ORDER BY created;