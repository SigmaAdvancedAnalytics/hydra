/* Create genres hierarchy table */
IF OBJECT_ID('dbo._genres') IS NOT NULL DROP TABLE dbo._genres;
CREATE TABLE dbo._genres (
    ID int IDENTITY(1,1) PRIMARY KEY,
    name char(255) NOT NULL,
    parent_id INT REFERENCES _genres(ID)
); 

/* Insert values */
INSERT INTO _genres (name, parent_id) VALUES ('Arts & Photography',NULL);
INSERT INTO _genres (name, parent_id) VALUES ('Architecture',1);
INSERT INTO _genres (name, parent_id) VALUES ('Graphic Design',1);
INSERT INTO _genres (name, parent_id) VALUES ('Music',1); -- 4
INSERT INTO _genres (name, parent_id) VALUES ('Songbooks',4);
INSERT INTO _genres (name, parent_id) VALUES ('Instruments & Performers',4); -- 6
INSERT INTO _genres (name, parent_id) VALUES ('Brass',6);
INSERT INTO _genres (name, parent_id) VALUES ('Woodwinds',6);

INSERT INTO _genres (name, parent_id) VALUES ('Comics & Graphic Novels', NULL); -- 9
INSERT INTO _genres (name, parent_id) VALUES ('Comic Strips',9);
INSERT INTO _genres (name, parent_id) VALUES ('Graphic Novels',9);
INSERT INTO _genres (name, parent_id) VALUES ('Manga',9);

INSERT INTO _genres (name, parent_id) VALUES ('Comic Strips',NULL); -- 13
INSERT INTO _genres (name, parent_id) VALUES ('Mystery, Thriller and Suspense', NULL); -- 14
INSERT INTO _genres (name, parent_id) VALUES ('Mystery',14); -- 15
INSERT INTO _genres (name, parent_id) VALUES ('Hard Boiled',15);
INSERT INTO _genres (name, parent_id) VALUES ('Police Procedurals',15); -- 17
INSERT INTO _genres (name, parent_id) VALUES ('British Detectives',17);
INSERT INTO _genres (name, parent_id) VALUES ('FBI Agents',17);
INSERT INTO _genres (name, parent_id) VALUES ('Police Officers',17);

INSERT INTO _genres (name, parent_id) VALUES ('Nonfiction', NULL); -- 21
INSERT INTO _genres (name, parent_id) VALUES ('Biographies and Memoirs',21);
INSERT INTO _genres (name, parent_id) VALUES ('Business & Investing',21);
INSERT INTO _genres (name, parent_id) VALUES ('Computers & Technology',21); -- 24
INSERT INTO _genres (name, parent_id) VALUES ('Databases',24);
INSERT INTO _genres (name, parent_id) VALUES ('Hardware',24);
INSERT INTO _genres (name, parent_id) VALUES ('Software',24);

Select * from _genres
/* Recursively fetch records */
WITH genres_materialized_path AS (
  SELECT id, name, PATH = CAST('' as varchar(255))                      
  FROM _genres WHERE parent_id IS NULL

  UNION ALL

  SELECT _genres.id, _genres.name, CAST(genres_materialized_path.path+'/'+CAST(_genres.parent_id AS VARCHAR)as varchar(255))
  FROM _genres, genres_materialized_path
  WHERE _genres.parent_id = genres_materialized_path.id
) SELECT * FROM genres_materialized_path;