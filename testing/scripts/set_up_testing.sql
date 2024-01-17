TRUNCATE chapters, league_tables, match_audit, matches, pitches, players, sports, teams, timetable, users;
-- Insert into chapters table and store the ID in the temporary table
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('ddbcea96-ae5e-45c1-9b30-d47179d30dfd', 'Imperial', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('a1d2b0ed-81bb-473a-b436-dcd12eb4ccc7', 'City', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('5ac46b7b-4dae-4955-9992-bbb0e4a4352e', 'Bristol', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('bcc90c9b-2d4b-4110-9f1b-f65bb33bfaff', 'Cardiff', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('7fea5add-82ee-4532-8ced-07626724eb0f', 'Reading', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('65ab1692-0689-4ed0-afdd-62870972a026', 'Kent', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('e4f0bd48-cfe9-4bb5-8ab0-11f0c1defc9b', 'Hertfordshire', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('8e3aad93-9515-40ce-9bef-79e14e52ac8c', 'Sussex', '2023-11-16 00:52:35.065331 +00:00', false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('f061f80e-22ee-4a37-87ef-aa295c2de70a', 'Bath', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('c84c9d23-4e0f-4fc7-af31-f63bd46a842e', 'Portsmouth', '2023-11-16 00:52:27.311398 +00:00', false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('f984b473-3e12-47b8-9785-aee9f6dab839', 'Brunel', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('6b64811e-4ab2-4a3a-8a5a-7141013088e5', 'SOAS', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('ea75267d-6f80-4e7a-ad00-5fe27fb0a371', 'LSE', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('5f129d0c-e62d-4dbc-8c35-4ad0143d6436', 'KCL', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('7ade937d-e8c2-49d6-b258-29ff4bf602ba', 'Westminster', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('26560d53-4125-4e35-8eab-b9ce6d5d7289', 'QM', now(), false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('7a26b441-6fba-40ac-a33d-5a3d97183794', 'Sheffield', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('78998228-4785-405f-83fa-69afe87a5c7d', 'Liverpool', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('ee1fff7d-32ab-49fb-a2a1-d3790fe3c78d', 'York', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('c2494814-9e27-4886-8651-50d6f4ab1768', 'Trafford', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('7ce3f19d-238f-45b6-9912-c90bec52064b', 'Nottingham', now(),
        false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('aa3ec885-bedf-4dcc-bc68-dc86ec4684aa', 'Manchester', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('c3097974-9377-44c5-8fc1-2d00e1df5e57', 'UoB', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('b4c98efb-ed9a-44c0-9b01-00bb2433e6e9', 'Coventry', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('69517b83-68eb-41dd-a2c7-211bfd8984a6', 'Leicester', now(),
        false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('33da0973-f082-4dcf-aefd-1de17d519fd5', 'Warwick', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('3d89e2a3-b331-4cbe-a590-5c52653750ea', 'Loughborough', now(),
        false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('671f9b5d-55ce-4606-93c5-bb8d63de1886', 'NTU', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('f4083b0f-6d98-45c7-bfb8-014e06201f82', 'DMU', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('f020435e-4ae5-4645-bc9b-d4483b1afd03', 'Leeds', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('f2de1e8b-a324-4955-9e8f-9a5eb1324ef4', 'UCLAN', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('27c80561-6b50-4919-a718-67840a6c8ee0', 'Cambridge', now(),
        false, null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('1677413d-4830-431d-b5e3-e697512e3d9f', 'Aston', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('8382fd49-0ced-4b28-820b-3309c0fde1cb', 'Lancaster', now(), false,
        null);
INSERT INTO public.chapters (id, name, created_date, is_deleted, last_modified_date)
VALUES ('3c62673b-f2c3-4cef-8dbd-c578f33f99b2', 'KCL', now(), false,
        null);


INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('7e90575b-5b04-4a12-9279-f7124a5f737c', 'Netball', now(), false, null, false,
        true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('189772ac-8d6d-4662-b5aa-000fa4271138', 'Badminton', now(), false, null, false,
        true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('5d231a25-d15a-4881-a004-9b9ddfa4b988', 'Kho', now(), false, null, false, true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('7dac42d7-e397-4efa-b70a-0232cacd4c4f', 'Football', '2023-09-13 00:09:50.564341 +00:00', false, null, false,
        true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('29fc8489-95ee-4dd5-bf21-0703f4df41c6', 'KabaddiM', now(), false, null, false,
        true);
INSERT INTO public.sports (id, name, created_date, is_deleted, last_modified_date, quarter_finals, semi_finals)
VALUES ('3429e138-0e55-4096-b30d-6b2f789365b4', 'KabaddiW', now(), false, null, false,
        false);


-- Insert into pitches table and store the ID in the temporary table
INSERT INTO public.pitches (id, name, created_date, is_deleted, last_modified_date, sport_id)
VALUES ('b6faa095-b64f-4bca-a9e3-d9795b530f21', 'Football Pitch 1', '2023-09-14 23:26:38.610667 +00:00', false, null,
        '7dac42d7-e397-4efa-b70a-0232cacd4c4f');


INSERT INTO public.users (id, username, email, hashed_password, created_date, is_deleted, last_modified_date,
                          chapter_id, user_type_id, full_name)
VALUES ('22e49def-7eb1-452a-aea5-723b886434aa', 'admin', 'user@example.com',
        '$2b$12$w46.KJhlC5nnKq6UR7LO4OkWksNJOZQ7.vsE8cGLE13Ou39KB0FFa', '2023-11-05 12:15:01.397891 +00:00', false,
        null, null, '87545bbb-9750-4e4f-bdfa-790f3994cd19', 'admin');
INSERT INTO public.users (id, username, email, hashed_password, created_date, is_deleted, last_modified_date,
                          chapter_id, user_type_id, full_name)
VALUES ('d0faac9e-d791-4c89-b4b3-da07d448445d', 'chapter', 'chapter@example.com',
        '$2b$12$w46.KJhlC5nnKq6UR7LO4OkWksNJOZQ7.vsE8cGLE13Ou39KB0FFa', '2023-11-05 12:15:01.397891 +00:00', false,
        null, 'ddbcea96-ae5e-45c1-9b30-d47179d30dfd', '6b7815b7-5563-445e-b400-48e81d1dbce6', 'chapter');
INSERT INTO public.users (id, username, email, hashed_password, created_date, is_deleted, last_modified_date,
                          chapter_id, user_type_id, full_name)
VALUES ('6b9e0b40-221a-4f30-a9ed-28a283436e97', 'super_admin', 'user@example.com',
        '$2b$12$w46.KJhlC5nnKq6UR7LO4OkWksNJOZQ7.vsE8cGLE13Ou39KB0FFa', '2024-01-08 02:06:18.724737 +00:00', false,
        null, null, '975ca347-4467-4d68-b2ef-f5a81c090959', 'super_admin');


INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (2, '8:30 AM', 'Registration', '');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (3, '9:00 AM', 'Opening Ceremony', 'Sports Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (4, '9:30-11:25', 'Netball', 'Sports Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (5, '9:30-12:30', 'Football', '3G Pitch Outside');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (6, '11:30-12:45', 'Women''s Kabaddi', 'Main Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (7, '12:00-13:50', 'Badminton', 'Sports Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (8, '13:15-16:05', 'Men''s Kabaddi', 'Main Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (9, '13:15-16:30', 'Kho-Kho', 'Sports Hall');
INSERT INTO public.timetable (id, time_activity, activity_name, location)
VALUES (10, '16:30-17:00', 'Closing Ceremony', 'Sports Hall');
