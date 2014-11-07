# Query structure for images
SELECT thumbnails
FROM ( SELECT images.subject,
              images.place,
              images.description,
              images.thumbnail as thumbnail,
              images.permitted,
              setweight(to_tsvector(images.subject), A) ||
              setweight(to_tsvector(images.place), B) ||
              setweight(to_tsvector(images.description), C) ||
              to_tsvector(coalesce((string_agg(<ARGUMENT>, ' ')), '')) as document
       FROM images, grouplist
       WHERE  image.permitted = 1 
              OR (image.permitted = 2 AND image.username = '<USER>') 
              OR (image.permitted = grouplist.group_id AND grouplist.friendid = '<USER>') ) img_search 
WHERE img_search.document @@ to_tsquery('<QUERY>')
ORDER BY ts_rank( array[0.0, 0.1, 0.3, 0.6], img_search.document, to_tsquery('<QUERY>') ) DESC;


SELECT images.permitted,
FROM images, grouplist
WHERE  image.permitted = 1 
       OR (image.permitted = 2 AND image.username = '<USER>') 
       OR (image.permitted = grouplist.group_id AND grouplist.friendid = '<USER>') ) img_search 
ORDER BY image.date DESC;


SELECT images.permitted,
FROM images, grouplist
WHERE  image.permitted = 1 
       OR (image.permitted = 2 AND image.username = '<USER>') 
       OR (image.permitted = grouplist.group_id AND grouplist.friendid = '<USER>') ) img_search 
ORDER BY image.date ASC;

# Example Query Worked from Tutorial

SELECT ptitle, content, auth, ts_rank(array[0.6, 0.1, 0.3, 0.0], p_search.document, to_tsquery('starudshdshk | fan | robert')) as rank
FROM (SELECT post.title as ptitle,
                 post.content as content,
                 author.name as auth,
                 setweight(to_tsvector(post.title), 'A') || 
                 setweight(to_tsvector(post.content), 'B') ||
                 setweight(to_tsvector(author.name), 'C') ||
                 to_tsvector(coalesce((string_agg(tag.name, ' ')), ''))  as document
                           
      FROM post
          JOIN author ON author.id = post.author_id
          JOIN posts_tags ON posts_tags.post_id = posts_tags.tag_id
          JOIN tag ON tag.id = posts_tags.tag_id
      GROUP BY post.id, author.id) p_search

WHERE p_search.document @@ to_tsquery('staruzjsudf | fan | robert')
ORDER BY rank DESC;

#
