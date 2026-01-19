-- Enable extensions
create extension if not exists "pgcrypto";

-- Products table
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  is_active boolean not null default true,
  title text not null,
  category text not null,
  price_usd numeric not null,
  price_band text not null,
  tags text[] not null default '{}',
  risk_flags text[] not null default '{}',
  content_type text not null check (content_type in ('template_script', 'human_driven', 'ad_scalable')),
  lifecycle_hint text not null check (lifecycle_hint in ('short', 'mid', 'long')),
  supply_chain jsonb not null default '{}',
  content_play jsonb not null default '{}'
);

create table if not exists public.product_cards (
  product_id uuid primary key references public.products(id) on delete cascade,
  why_fit text not null,
  first_test text not null,
  stop_loss text not null
);

create table if not exists public.rules (
  id uuid primary key default gen_random_uuid(),
  tier text not null check (tier in ('forbidden', 'not_recommended', 'testable', 'recommended')),
  priority int not null default 100,
  condition jsonb not null default '{}',
  filter jsonb not null default '{}',
  public_reason_title text not null,
  public_reason_detail text not null,
  is_active boolean not null default true
);

-- RLS: public read-only
alter table public.products enable row level security;
alter table public.product_cards enable row level security;
alter table public.rules enable row level security;

create policy "public read products" on public.products
  for select
  using (true);

create policy "public read product_cards" on public.product_cards
  for select
  using (true);

create policy "public read rules" on public.rules
  for select
  using (true);
