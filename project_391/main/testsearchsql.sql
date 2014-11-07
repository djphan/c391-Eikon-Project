# Initial Test Data
###################

CREATE TABLE author(
   id SERIAL PRIMARY KEY,
   name TEXT NOT NULL
);

CREATE TABLE post(
   id SERIAL PRIMARY KEY,
   title TEXT NOT NULL,
   content TEXT NOT NULL,
   author_id INT NOT NULL references author(id) 
);

CREATE TABLE tag(
   id SERIAL PRIMARY KEY,
   name TEXT NOT NULL 
);

CREATE TABLE posts_tags(
   post_id INT NOT NULL references post(id),
   tag_id INT NOT NULL references tag(id)
 );

INSERT INTO author (id, name) 
VALUES (1, 'Pete Graham'), 
       (2, 'Rachid Belaid'), 
       (3, 'Robert Berry');

INSERT INTO tag (id, name) 
VALUES (1, 'scifi'), 
       (2, 'politics'), 
       (3, 'science');

INSERT INTO post (id, title, content, author_id) 
VALUES (1, 'Endangered species', 'Pandas are an endangered species', 1 ), 
       (2, 'Freedom of Speech', 'Freedom of speech is a necessary right missing in many countries', 2), 
       (3, 'Star Wars vs Star Trek', 'Few words from a big fan', 3);

INSERT INTO post(id, title, content, author_id)
VALUES (4, 'Fans of Fans, a monolouge of Fanny Fans and the Fandoms Fan', 'Fanny Fan is the best Fan of the world', 3),
       (5, 'Freedom of the Fan', 'Starwars epic style sage of the fan wars between the free handfans and the oppressed electric fans', 3),
       (6, 'Freeing Star Lords', 'Star lawds are free and freedom is a lie', 3);


INSERT INTO posts_tags (post_id, tag_id) 
VALUES (1, 3), 
       (2, 2), 
       (3, 1); 

###################


 SELECT post.title, 
        post.content, 
        author.name, 
        coalesce((string_agg(tag.name, ' ')), '') as document
 FROM post
 JOIN author ON author.id = post.author_id
 JOIN posts_tags ON posts_tags.post_id = posts_tags.tag_id
 JOIN tag ON tag.id = posts_tags.tag_id
 GROUP BY post.id, author.id;

SELECT post.title || ' ' || 
        post.content || ' ' ||
        author.name || ' ' ||
        coalesce((string_agg(tag.name, ' ')), '') as document
 FROM post
 JOIN author ON author.id = post.author_id
 JOIN posts_tags ON posts_tags.post_id = posts_tags.tag_id
 JOIN tag ON tag.id = posts_tags.tag_id
 GROUP BY post.id, author.id;

# Example of using to_tsvector
SELECT to_tsvector(post.title) || 
       to_tsvector(post.content) ||
       to_tsvector(author.name) ||
       to_tsvector(coalesce((string_agg(tag.name, ' ')), '')) as document
FROM post
JOIN author ON author.id = post.author_id
JOIN posts_tags ON posts_tags.post_id = posts_tags.tag_id
JOIN tag ON tag.id = posts_tags.tag_id
GROUP BY post.id, author.id;


SELECT post.title
       post.content
       author.name, ts_rank([0., 0.3, 0.1],  ) AS rank
FROM post
WHERE
ORDER BY rank DESC 

####
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


####


SELECT post.title,
       post.content, 
       author.name, 
       ts_rank(array[0.6, 0.3, 0.2, 0.0],, 'vs') AS rank
FROM post
JOIN author ON author.id = post.author_id
JOIN posts_tags ON posts_tags.post_id = posts_tags.tag_id
JOIN tag ON tag.id = posts_tags.tag_id
ORDER BY rank DESC;


SELECT to_tsvector(Images.subject) ||
       to_tsvector(Images.place) ||
       to_tsvector(Images.description) ||
       to_tsvector(coalesce((string_agg(tag.name, ' ')), '')) as document


FROM Images
WHERE
ORDER BY