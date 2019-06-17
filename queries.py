def code_query(addr):
    return '''
        (WITH RECURSIVE results AS (
            SELECT slug, parent_slug
            FROM regions
            WHERE slug = '{}'
            UNION
            SELECT e.slug, e.parent_slug
            FROM regions e INNER JOIN results s ON s.slug = e.parent_slug)
            select res.code from (SELECT DISTINCT code from ports po left outer join regions r on po.parent_slug = r.slug)
             as res)
    '''.format(addr)


