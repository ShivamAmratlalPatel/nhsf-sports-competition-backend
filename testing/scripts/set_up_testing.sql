DROP TABLE IF EXISTS temp_ids;
-- Create a temporary table to store the IDs
CREATE TEMP TABLE temp_ids
(
    id uuid
);

DELETE
FROM chapters;
-- Insert into chapters table and store the ID in the temporary table
INSERT INTO public.chapters (id, name, zone, email, created_date, is_deleted,
                             last_modified_date)
VALUES ('15ecd3e8-5489-4056-b474-4495a0b1e3ef',
        'Imperial',
        'London',
        'a@ba.com',
        '2023-09-13 00:09:50.564341 +00:00',
        FALSE,
        NULL);

-- Insert the ID into the temporary table
INSERT INTO temp_ids (id)
SELECT '15ecd3e8-5489-4056-b474-4495a0b1e3ef'
WHERE NOT EXISTS (SELECT 1
                  FROM temp_ids
                  WHERE id = '15ecd3e8-5489-4056-b474-4495a0b1e3ef');

DELETE
FROM sports;
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('7e90575b-5b04-4a12-9279-f7124a5f737c', 'Netball', '2023-09-19 19:39:43.167812 +00:00', false, null, false, true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('189772ac-8d6d-4662-b5aa-000fa4271138', 'Badminton', '2023-09-19 19:39:43.167812 +00:00', false, null, false, true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('5d231a25-d15a-4881-a004-9b9ddfa4b988', 'Kho', '2023-09-19 19:39:43.167812 +00:00', false, null, false, true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'Football', '2023-09-13 00:09:50.564341 +00:00', false, null, false, true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('29fc8489-95ee-4dd5-bf21-0703f4df41c6', 'KabaddiM', '2023-09-19 19:39:43.167812 +00:00', false, null, false, false);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals) VALUES ('3429e138-0e55-4096-b30d-6b2f789365b4', 'KabaddiW', '2023-11-07 17:27:37.122753 +00:00', false, null, false, true);


DELETE
FROM teams;
-- Insert into teams table using the ID from the temporary table
INSERT INTO public.teams (id, name, created_date, is_deleted, last_modified_date,
                          chapter_id, sport_id)
VALUES ('7dc264e3-db16-47c7-bd46-ad766c05a42d',
        'Imperial Football Team',
        NOW(),
        FALSE,
        NULL,
        (SELECT id FROM temp_ids WHERE id = '15ecd3e8-5489-4056-b474-4495a0b1e3ef'),
        '7dac42d7-e397-4efa-b70a-0232cacd4c4f');

-- Insert into chapters table and store the ID in the temporary table
INSERT INTO public.chapters (id, name, zone, email, created_date, is_deleted,
                             last_modified_date)
VALUES ('e846aa5a-7a7f-46c1-934d-032140116141',
        'UCLAN',
        'North',
        'a@b.com',
        '2023-09-13 00:09:50.564341 +00:00',
        FALSE,
        NULL);

-- Insert the ID into the temporary table
INSERT INTO temp_ids (id)
SELECT 'e846aa5a-7a7f-46c1-934d-032140116141'
WHERE NOT EXISTS (SELECT 1
                  FROM temp_ids
                  WHERE id = 'e846aa5a-7a7f-46c1-934d-032140116141');

-- Insert into teams table using the ID from the temporary table
INSERT INTO public.teams (id, name, created_date, is_deleted, last_modified_date,
                          chapter_id, sport_id)
VALUES ('35569907-cf47-4fc9-80db-0fc5762e7e5e',
        'UCLAN Football Team',
        '2023-09-13 00:11:24.107033 +00:00',
        FALSE,
        NULL,
        (SELECT id FROM temp_ids WHERE id = 'e846aa5a-7a7f-46c1-934d-032140116141'),
        '7dac42d7-e397-4efa-b70a-0232cacd4c4f');


-- Insert the ID into the temporary table
INSERT INTO temp_ids (id)
SELECT '61dafaac-ad51-4754-944f-f85487666df0'
WHERE NOT EXISTS (SELECT 1
                  FROM temp_ids
                  WHERE id = '61dafaac-ad51-4754-944f-f85487666df0');


DELETE
FROM pitches;
-- Insert into pitches table and store the ID in the temporary table
INSERT INTO public.pitches (id, name, created_date, is_deleted, last_modified_date, sport_id) VALUES ('b6faa095-b64f-4bca-a9e3-d9795b530f21', 'Football Pitch 1', '2023-09-14 23:26:38.610667 +00:00', false, null, '7dac42d7-e397-4efa-b70a-0232cacd4c4f');


-- Insert the ID into the temporary table
INSERT INTO temp_ids (id)
SELECT 'b6faa095-b64f-4bca-a9e3-d9795b530f21'
WHERE NOT EXISTS (SELECT 1
                  FROM temp_ids
                  WHERE id = 'b6faa095-b64f-4bca-a9e3-d9795b530f21');

DELETE
FROM matches;
-- Insert into matches table using the IDs from the temporary table
INSERT INTO public.matches (id, created_date, is_deleted, last_modified_date, home_team_id, away_team_id, sport_id, pitch_id, stage_id, home_score, away_score, home_penalties, away_penalties, time) VALUES ('3a51516c-6df0-47c7-a756-a768a12a0f79', '2023-09-13 02:13:09.945014 +00:00', false, null, '7dc264e3-db16-47c7-bd46-ad766c05a42d', '35569907-cf47-4fc9-80db-0fc5762e7e5e', '7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'b6faa095-b64f-4bca-a9e3-d9795b530f21', 0, null, null, 0.00, 0.00, '2023-09-13 01:13:09.945014 +00:00');
INSERT INTO public.matches (id, created_date, is_deleted, last_modified_date, home_team_id, away_team_id, sport_id, pitch_id, stage_id, home_score, away_score, home_penalties, away_penalties, time) VALUES ('4dd77f40-644f-49ea-8fea-436c5cdb8453', '2023-09-13 00:13:09.945014 +00:00', false, null, '35569907-cf47-4fc9-80db-0fc5762e7e5e', '7dc264e3-db16-47c7-bd46-ad766c05a42d', '7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'b6faa095-b64f-4bca-a9e3-d9795b530f21', 0, null, null, null, null, '2023-09-13 00:13:09.945014 +00:00');
INSERT INTO public.matches (id, created_date, is_deleted, last_modified_date, home_team_id, away_team_id, sport_id, pitch_id, stage_id, home_score, away_score, home_penalties, away_penalties, time) VALUES ('3a51516c-6df0-47c7-a756-a768a12a0f78', '2023-09-13 02:13:09.945014 +00:00', false, null, '7dc264e3-db16-47c7-bd46-ad766c05a42d', '35569907-cf47-4fc9-80db-0fc5762e7e5e', '7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'b6faa095-b64f-4bca-a9e3-d9795b530f21', 1, null, null, 0.00, 0.00, '2023-09-13 01:13:09.945014 +00:00');
INSERT INTO public.matches (id, created_date, is_deleted, last_modified_date, home_team_id, away_team_id, sport_id, pitch_id, stage_id, home_score, away_score, home_penalties, away_penalties, time) VALUES ('4dd77f40-644f-49ea-8fea-436c5cdb8454', '2023-09-13 00:13:09.945014 +00:00', false, null, '35569907-cf47-4fc9-80db-0fc5762e7e5e', '7dc264e3-db16-47c7-bd46-ad766c05a42d', '7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'b6faa095-b64f-4bca-a9e3-d9795b530f21', 2, null, null, null, null, '2023-09-13 00:13:09.945014 +00:00');



DROP TABLE IF EXISTS temp_ids;


DELETE FROM users;

INSERT INTO public.users (id, username, email, hashed_password, created_date, is_deleted, last_modified_date, chapter_id, user_type_id, full_name) VALUES ('22e49def-7eb1-452a-aea5-723b886434aa', 'string', 'user@example.com', '$2b$12$w46.KJhlC5nnKq6UR7LO4OkWksNJOZQ7.vsE8cGLE13Ou39KB0FFa', '2023-11-05 12:15:01.397891 +00:00', false, null, null, '87545bbb-9750-4e4f-bdfa-790f3994cd19', 'string');
