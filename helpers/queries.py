def code_query(addr):
    return '''
        (WITH RECURSIVE parents AS (
            SELECT slug, parent_slug
            FROM regions WHERE slug = '{}'
            UNION
            SELECT e.slug, e.parent_slug
            FROM regions e INNER JOIN parents s ON s.slug = e.parent_slug)
            SELECT * FROM (SELECT DISTINCT code
                  from ports right outer join parents p on ports.parent_slug = p.slug) as res)
    '''.format(addr)


def code_query_new(addr):
    return '''
        (WITH RECURSIVE parents AS (
            SELECT slug, parent_slug
            FROM locations
            WHERE slug = '{}'
            UNION
            SELECT e.slug, e.parent_slug
            FROM locations e INNER JOIN parents s ON s.slug = e.parent_slug)
            select slug from parents)
    '''.format(addr)


def insert_prices(dest, orig, date_from, date_to, price):
    return '''
        INSERT INTO public.prices(dest_code, orig_code, day, price)
        SELECT '{0}', '{1}', resp.day, {4}
        FROM  (select d as day from generate_series('{2}'::timestamp , '{3}'::timestamp,
         '1 day'::interval) d) resp

    '''.format(dest, orig, date_from, date_to, price)
