CREATE TABLE IF NOT EXISTS public.users
(
 user_id uuid PRIMARY KEY,
 first_name text NOT NULL DEFAULT 'N/A',
 last_name text NOT NULL DEFAULT 'N/A',
 birthday DATE NOT NULL CHECK (birthday <= date_created) DEFAULT '1970-01-01',
 role text NOT NULL DEFAULT 'N/A',
 date_modified TIMESTAMP WITH TIME ZONE NOT NULL CHECK (date_modified >= date_created) DEFAULT clock_timestamp(),
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
 active boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS public.locations
(
 location_id uuid PRIMARY KEY,
 user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
 latitude DOUBLE PRECISION NOT NULL,
 longitude DOUBLE PRECISION NOT NULL,
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS public.help_log
(
 entry_id uuid PRIMARY KEY,
 user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
 description text NOT NULL DEFAULT 'N/A',
 watson_context json NOT NULL DEFAULT '{}',
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS public.distress_log
(
 entry_id uuid PRIMARY KEY,
 user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
 help_log_id uuid NOT NULL REFERENCES public.help_log(entry_id),
 distress_status boolean NOT NULL,
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS public.disasters
(
 disaster_id uuid PRIMARY KEY,
 disaster_type text NOT NULL DEFAULT 'N/A',
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS public.disaster_log
(
 entry_id uuid PRIMARY KEY,
 disaster_id uuid NOT NULL REFERENCES public.disasters(disaster_id) ON DELETE CASCADE,
 center_latitude DOUBLE PRECISION NOT NULL,
 center_longitude DOUBLE PRECISION NOT NULL,
 radius DOUBLE PRECISION NOT NULL,
 severity DOUBLE PRECISION NOT NULL,
 date_created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp()
);

INSERT INTO public.users (user_id, active) VALUES ('00000000-0000-0000-0000-000000000000', FALSE);

INSERT INTO public.help_log (entry_id, user_id) VALUES ('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000');