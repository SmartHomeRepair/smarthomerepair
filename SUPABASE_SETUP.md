# Supabase setup for admin

1. Create project at supabase.com -> copy URL + anon key to GitHub Secrets SUPABASE_URL / SUPABASE_ANON_KEY and local .env
2. Auth -> Users -> Add user admin@smarthomerepair.in
3. SQL Editor -> run:
```sql
create table blogs (id uuid primary key default gen_random_uuid(), title text not null, slug text unique not null, excerpt text, body text, created_at timestamp default now());
create table site_texts (key text primary key, value text);
insert into site_texts (key,value) values ('hero_h1','Fast, reliable AC repair in Kochi'), ('hero_sub','2-hour response');
alter table blogs enable row level security;
alter table site_texts enable row level security;
create policy "public read" on blogs for select using (true);
create policy "auth write" on blogs for insert with check (auth.role()='authenticated');
create policy "public read" on site_texts for select using (true);
create policy "auth write" on site_texts for all using (auth.role()='authenticated');
```
4. GitHub -> Settings -> Secrets -> New: SUPABASE_URL, SUPABASE_ANON_KEY, SECRET_KEY
5. Local: cp .env.example .env and fill
6. Visit /admin/login -> login -> /admin dashboard -> post blogs

Login creds stored hashed in Supabase Auth, keys stored encrypted in GitHub Secrets (never in repo).
