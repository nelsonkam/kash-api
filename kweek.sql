--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: set_current_timestamp_updated_at(); Type: FUNCTION; Schema: public; Owner: nelson
--

CREATE FUNCTION public.set_current_timestamp_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$;


ALTER FUNCTION public.set_current_timestamp_updated_at() OWNER TO nelson;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: affiliate_agents; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.affiliate_agents (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    code character varying(10) NOT NULL,
    momo_number character varying(255),
    avatar_url character varying(200) NOT NULL,
    user_id bigint NOT NULL,
    commission numeric(6,5) NOT NULL
);


ALTER TABLE public.affiliate_agents OWNER TO nelson;

--
-- Name: affiliate_agents_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.affiliate_agents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.affiliate_agents_id_seq OWNER TO nelson;

--
-- Name: affiliate_agents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.affiliate_agents_id_seq OWNED BY public.affiliate_agents.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO nelson;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO nelson;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO nelson;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO nelson;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO nelson;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO nelson;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO nelson;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: banners; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.banners (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    link text NOT NULL,
    image_url text NOT NULL
);


ALTER TABLE public.banners OWNER TO nelson;

--
-- Name: banner_new_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.banner_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banner_new_id_seq OWNER TO nelson;

--
-- Name: banner_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.banner_new_id_seq OWNED BY public.banners.id;


--
-- Name: banners_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.banners_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banners_id_seq OWNER TO nelson;

--
-- Name: banners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.banners_id_seq OWNED BY public.banners.id;


--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.cart_items (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    cart_id bigint NOT NULL,
    product_id bigint NOT NULL,
    price numeric(14,2) NOT NULL,
    price_currency character varying(3) NOT NULL
);


ALTER TABLE public.cart_items OWNER TO nelson;

--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.cart_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cart_items_id_seq OWNER TO nelson;

--
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- Name: carts; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.carts (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    uid character varying(40) NOT NULL,
    paid boolean NOT NULL,
    shop_id bigint
);


ALTER TABLE public.carts OWNER TO nelson;

--
-- Name: carts_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.carts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.carts_id_seq OWNER TO nelson;

--
-- Name: carts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.carts_id_seq OWNED BY public.carts.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.categories (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name text NOT NULL,
    slug character varying(50) NOT NULL,
    shop_id bigint
);


ALTER TABLE public.categories OWNER TO nelson;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO nelson;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: checkouts; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.checkouts (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    country character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    address text NOT NULL,
    uid character varying(40) NOT NULL,
    cart_id bigint NOT NULL,
    customer_id bigint NOT NULL,
    payment_method character varying(10) NOT NULL,
    ref_id character varying(40) NOT NULL,
    paid boolean NOT NULL,
    shipping_fees numeric(14,2),
    shipping_fees_currency character varying(3) NOT NULL,
    shipping_profile_id bigint,
    zone character varying(255) NOT NULL
);


ALTER TABLE public.checkouts OWNER TO nelson;

--
-- Name: checkouts_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.checkouts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.checkouts_id_seq OWNER TO nelson;

--
-- Name: checkouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.checkouts_id_seq OWNED BY public.checkouts.id;


--
-- Name: core_bankaccount; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_bankaccount (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    external_id character varying(255) NOT NULL,
    account_bank character varying(10) NOT NULL,
    account_number character varying(255) NOT NULL,
    rave_subaccount_id character varying(255) NOT NULL,
    service character varying(15) NOT NULL,
    shop_id bigint NOT NULL
);


ALTER TABLE public.core_bankaccount OWNER TO nelson;

--
-- Name: core_bankaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_bankaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_bankaccount_id_seq OWNER TO nelson;

--
-- Name: core_bankaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_bankaccount_id_seq OWNED BY public.core_bankaccount.id;


--
-- Name: core_billingplan; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_billingplan (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    plan_name character varying(255) NOT NULL,
    status character varying(20) NOT NULL,
    user_id bigint NOT NULL,
    rc_app_user_id character varying(255) NOT NULL
);


ALTER TABLE public.core_billingplan OWNER TO nelson;

--
-- Name: core_billingplan_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_billingplan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_billingplan_id_seq OWNER TO nelson;

--
-- Name: core_billingplan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_billingplan_id_seq OWNED BY public.core_billingplan.id;


--
-- Name: core_shippingmethod; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_shippingmethod (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    price_currency character varying(3) NOT NULL,
    price numeric(14,2) NOT NULL,
    zone_id bigint NOT NULL
);


ALTER TABLE public.core_shippingmethod OWNER TO nelson;

--
-- Name: core_shippingmethod_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_shippingmethod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_shippingmethod_id_seq OWNER TO nelson;

--
-- Name: core_shippingmethod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_shippingmethod_id_seq OWNED BY public.core_shippingmethod.id;


--
-- Name: core_shippingprofile; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_shippingprofile (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    avatar_url character varying(200) NOT NULL,
    backend character varying(255) NOT NULL,
    profile_type character varying(255) NOT NULL
);


ALTER TABLE public.core_shippingprofile OWNER TO nelson;

--
-- Name: core_shippingprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_shippingprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_shippingprofile_id_seq OWNER TO nelson;

--
-- Name: core_shippingprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_shippingprofile_id_seq OWNED BY public.core_shippingprofile.id;


--
-- Name: core_shippingprofile_shops; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_shippingprofile_shops (
    id integer NOT NULL,
    shippingprofile_id bigint NOT NULL,
    shop_id bigint NOT NULL
);


ALTER TABLE public.core_shippingprofile_shops OWNER TO nelson;

--
-- Name: core_shippingprofile_shops_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_shippingprofile_shops_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_shippingprofile_shops_id_seq OWNER TO nelson;

--
-- Name: core_shippingprofile_shops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_shippingprofile_shops_id_seq OWNED BY public.core_shippingprofile_shops.id;


--
-- Name: core_shippingzone; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_shippingzone (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    profile_id bigint NOT NULL
);


ALTER TABLE public.core_shippingzone OWNER TO nelson;

--
-- Name: core_shippingzone_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_shippingzone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_shippingzone_id_seq OWNER TO nelson;

--
-- Name: core_shippingzone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_shippingzone_id_seq OWNED BY public.core_shippingzone.id;


--
-- Name: core_shopdesign; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.core_shopdesign (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    tagline character varying(225) NOT NULL,
    hero_cta character varying(100) NOT NULL,
    instagram_link character varying(200) NOT NULL,
    facebook_link character varying(200) NOT NULL,
    language character varying(10) NOT NULL,
    shop_id bigint NOT NULL,
    whatsapp_link character varying(200) NOT NULL,
    theme character varying(255) NOT NULL,
    color character varying(20) NOT NULL
);


ALTER TABLE public.core_shopdesign OWNER TO nelson;

--
-- Name: core_shopdesign_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.core_shopdesign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_shopdesign_id_seq OWNER TO nelson;

--
-- Name: core_shopdesign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.core_shopdesign_id_seq OWNED BY public.core_shopdesign.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.customers (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255),
    phone_number character varying(255),
    user_id bigint
);


ALTER TABLE public.customers OWNER TO nelson;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.customers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO nelson;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO nelson;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO nelson;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO nelson;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO nelson;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO nelson;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO nelson;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO nelson;

--
-- Name: exchange_exchangebackend; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.exchange_exchangebackend (
    name character varying(255) NOT NULL,
    last_update timestamp with time zone NOT NULL,
    base_currency character varying(3) NOT NULL
);


ALTER TABLE public.exchange_exchangebackend OWNER TO nelson;

--
-- Name: exchange_rate; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.exchange_rate (
    id integer NOT NULL,
    currency character varying(3) NOT NULL,
    value numeric(20,6) NOT NULL,
    backend_id character varying(255) NOT NULL
);


ALTER TABLE public.exchange_rate OWNER TO nelson;

--
-- Name: exchange_rate_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.exchange_rate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exchange_rate_id_seq OWNER TO nelson;

--
-- Name: exchange_rate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.exchange_rate_id_seq OWNED BY public.exchange_rate.id;


--
-- Name: kash_checkoutsession; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_checkoutsession (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    uid character varying(255) NOT NULL,
    paid_at timestamp with time zone,
    cancel_url character varying(200) NOT NULL,
    cart_id bigint NOT NULL,
    shop_id bigint NOT NULL,
    order_id bigint,
    user_id bigint
);


ALTER TABLE public.kash_checkoutsession OWNER TO nelson;

--
-- Name: kash_checkoutsession_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_checkoutsession_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_checkoutsession_id_seq OWNER TO nelson;

--
-- Name: kash_checkoutsession_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_checkoutsession_id_seq OWNED BY public.kash_checkoutsession.id;


--
-- Name: kash_fundinghistory; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_fundinghistory (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    txn_ref character varying(255) NOT NULL,
    card_id bigint NOT NULL,
    amount numeric(17,2) NOT NULL,
    amount_currency character varying(3) NOT NULL,
    status character varying(15) NOT NULL
);


ALTER TABLE public.kash_fundinghistory OWNER TO nelson;

--
-- Name: kash_fundinghistory_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_fundinghistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_fundinghistory_id_seq OWNER TO nelson;

--
-- Name: kash_fundinghistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_fundinghistory_id_seq OWNED BY public.kash_fundinghistory.id;


--
-- Name: kash_invitecode; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_invitecode (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    code character varying(10) NOT NULL,
    used_at timestamp with time zone,
    invited_id bigint,
    inviter_id bigint NOT NULL
);


ALTER TABLE public.kash_invitecode OWNER TO nelson;

--
-- Name: kash_invitecode_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_invitecode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_invitecode_id_seq OWNER TO nelson;

--
-- Name: kash_invitecode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_invitecode_id_seq OWNED BY public.kash_invitecode.id;


--
-- Name: kash_kashrequest; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_kashrequest (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    note text NOT NULL,
    amount_currency character varying(3) NOT NULL,
    amount numeric(17,2) NOT NULL,
    initiator_id bigint NOT NULL,
    accepted_at timestamp with time zone,
    recipient_id bigint NOT NULL,
    rejected_at timestamp with time zone
);


ALTER TABLE public.kash_kashrequest OWNER TO nelson;

--
-- Name: kash_kashrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashrequest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashrequest_id_seq OWNER TO nelson;

--
-- Name: kash_kashrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashrequest_id_seq OWNED BY public.kash_kashrequest.id;


--
-- Name: kash_kashrequest_recipients; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_kashrequest_recipients (
    id integer NOT NULL,
    kashrequest_id bigint NOT NULL,
    userprofile_id bigint NOT NULL
);


ALTER TABLE public.kash_kashrequest_recipients OWNER TO nelson;

--
-- Name: kash_kashrequest_recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashrequest_recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashrequest_recipients_id_seq OWNER TO nelson;

--
-- Name: kash_kashrequest_recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashrequest_recipients_id_seq OWNED BY public.kash_kashrequest_recipients.id;


--
-- Name: kash_kashrequestresponse; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_kashrequestresponse (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    accepted boolean NOT NULL,
    request_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    transaction_id bigint
);


ALTER TABLE public.kash_kashrequestresponse OWNER TO nelson;

--
-- Name: kash_kashrequestresponse_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashrequestresponse_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashrequestresponse_id_seq OWNER TO nelson;

--
-- Name: kash_kashrequestresponse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashrequestresponse_id_seq OWNED BY public.kash_kashrequestresponse.id;


--
-- Name: kash_kashtransaction; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_kashtransaction (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    amount_currency character varying(3) NOT NULL,
    amount numeric(17,2) NOT NULL,
    receiver_id integer,
    txn_ref character varying(20) NOT NULL,
    narration text NOT NULL,
    txn_type character varying(20) NOT NULL,
    "timestamp" timestamp with time zone,
    profile_id bigint NOT NULL,
    receiver_type_id integer,
    sender_id bigint NOT NULL
);


ALTER TABLE public.kash_kashtransaction OWNER TO nelson;

--
-- Name: kash_sendkash; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_sendkash (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    note text NOT NULL,
    group_mode character varying(10) NOT NULL,
    is_incognito boolean NOT NULL,
    amount_currency character varying(3) NOT NULL,
    amount numeric(17,2) NOT NULL,
    initiator_id bigint NOT NULL
);


ALTER TABLE public.kash_sendkash OWNER TO nelson;

--
-- Name: kash_kashtransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashtransaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashtransaction_id_seq OWNER TO nelson;

--
-- Name: kash_kashtransaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashtransaction_id_seq OWNED BY public.kash_sendkash.id;


--
-- Name: kash_kashtransaction_id_seq1; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashtransaction_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashtransaction_id_seq1 OWNER TO nelson;

--
-- Name: kash_kashtransaction_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashtransaction_id_seq1 OWNED BY public.kash_kashtransaction.id;


--
-- Name: kash_sendkash_paid_recipients; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_sendkash_paid_recipients (
    id integer NOT NULL,
    sendkash_id bigint NOT NULL,
    userprofile_id bigint NOT NULL
);


ALTER TABLE public.kash_sendkash_paid_recipients OWNER TO nelson;

--
-- Name: kash_kashtransaction_paid_recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashtransaction_paid_recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashtransaction_paid_recipients_id_seq OWNER TO nelson;

--
-- Name: kash_kashtransaction_paid_recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashtransaction_paid_recipients_id_seq OWNED BY public.kash_sendkash_paid_recipients.id;


--
-- Name: kash_sendkash_recipients; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_sendkash_recipients (
    id integer NOT NULL,
    sendkash_id bigint NOT NULL,
    userprofile_id bigint NOT NULL
);


ALTER TABLE public.kash_sendkash_recipients OWNER TO nelson;

--
-- Name: kash_kashtransaction_recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_kashtransaction_recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_kashtransaction_recipients_id_seq OWNER TO nelson;

--
-- Name: kash_kashtransaction_recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_kashtransaction_recipients_id_seq OWNED BY public.kash_sendkash_recipients.id;


--
-- Name: kash_momoaccount; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_momoaccount (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    gateway character varying(20) NOT NULL,
    phone character varying(45) NOT NULL,
    profile_id bigint NOT NULL
);


ALTER TABLE public.kash_momoaccount OWNER TO nelson;

--
-- Name: kash_notification; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_notification (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    object_id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    sent_at timestamp with time zone,
    content_type_id integer NOT NULL,
    profile_id bigint NOT NULL
);


ALTER TABLE public.kash_notification OWNER TO nelson;

--
-- Name: kash_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_notification_id_seq OWNER TO nelson;

--
-- Name: kash_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_notification_id_seq OWNED BY public.kash_notification.id;


--
-- Name: kash_payoutmethod_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_payoutmethod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_payoutmethod_id_seq OWNER TO nelson;

--
-- Name: kash_payoutmethod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_payoutmethod_id_seq OWNED BY public.kash_momoaccount.id;


--
-- Name: kash_userprofile; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_userprofile (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    kashtag character varying(30) NOT NULL,
    device_ids character varying(255)[] NOT NULL,
    user_id bigint NOT NULL,
    avatar_url character varying(200) NOT NULL
);


ALTER TABLE public.kash_userprofile OWNER TO nelson;

--
-- Name: kash_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_profile_id_seq OWNER TO nelson;

--
-- Name: kash_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_profile_id_seq OWNED BY public.kash_userprofile.id;


--
-- Name: kash_virtualcard; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_virtualcard (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    external_id character varying(255) NOT NULL,
    service character varying(255) NOT NULL,
    nickname character varying(255) NOT NULL,
    profile_id bigint NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.kash_virtualcard OWNER TO nelson;

--
-- Name: kash_virtualcard_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_virtualcard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_virtualcard_id_seq OWNER TO nelson;

--
-- Name: kash_virtualcard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_virtualcard_id_seq OWNED BY public.kash_virtualcard.id;


--
-- Name: kash_withdrawalhistory; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.kash_withdrawalhistory (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    txn_ref character varying(255) NOT NULL,
    amount_currency character varying(3) NOT NULL,
    amount numeric(17,2) NOT NULL,
    card_id bigint NOT NULL
);


ALTER TABLE public.kash_withdrawalhistory OWNER TO nelson;

--
-- Name: kash_withdrawalhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.kash_withdrawalhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kash_withdrawalhistory_id_seq OWNER TO nelson;

--
-- Name: kash_withdrawalhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.kash_withdrawalhistory_id_seq OWNED BY public.kash_withdrawalhistory.id;


--
-- Name: migrations; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.migrations (
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);


ALTER TABLE public.migrations OWNER TO nelson;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.order_items (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    order_id bigint NOT NULL,
    product_id bigint NOT NULL,
    price numeric(14,2) NOT NULL,
    price_currency character varying(3) NOT NULL
);


ALTER TABLE public.order_items OWNER TO nelson;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.order_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_items_id_seq OWNER TO nelson;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    country character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    address text NOT NULL,
    ref_id character varying(40) NOT NULL,
    payment_method character varying(10) NOT NULL,
    customer_id bigint NOT NULL,
    shop_id bigint NOT NULL,
    shipping_fees numeric(14,2),
    shipping_fees_currency character varying(3) NOT NULL,
    shipping_profile_id bigint,
    zone character varying(255) NOT NULL
);


ALTER TABLE public.orders OWNER TO nelson;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO nelson;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: product_images; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.product_images (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    url character varying(200),
    product_id bigint NOT NULL
);


ALTER TABLE public.product_images OWNER TO nelson;

--
-- Name: product_image_new_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.product_image_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_image_new_id_seq OWNER TO nelson;

--
-- Name: product_image_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.product_image_new_id_seq OWNED BY public.product_images.id;


--
-- Name: product_images_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.product_images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_images_id_seq OWNER TO nelson;

--
-- Name: product_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.product_images_id_seq OWNED BY public.product_images.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.products (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name text,
    description text,
    slug character varying(255) NOT NULL,
    shop_id bigint NOT NULL,
    available_units integer,
    weight numeric(6,3) NOT NULL,
    price numeric(14,2) NOT NULL,
    price_currency character varying(3) NOT NULL,
    CONSTRAINT products_available_units_check CHECK ((available_units >= 0))
);


ALTER TABLE public.products OWNER TO nelson;

--
-- Name: product_new_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.product_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_new_id_seq OWNER TO nelson;

--
-- Name: product_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.product_new_id_seq OWNED BY public.products.id;


--
-- Name: products_categories; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.products_categories (
    id integer NOT NULL,
    product_id bigint NOT NULL,
    category_id bigint NOT NULL
);


ALTER TABLE public.products_categories OWNER TO nelson;

--
-- Name: products_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.products_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_categories_id_seq OWNER TO nelson;

--
-- Name: products_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.products_categories_id_seq OWNED BY public.products_categories.id;


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO nelson;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: qosic_transaction; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.qosic_transaction (
    id integer NOT NULL,
    object_id integer NOT NULL,
    gateway character varying(20) NOT NULL,
    reference character varying(20) NOT NULL,
    service_reference character varying(40),
    status character varying(40) NOT NULL,
    amount numeric(17,2) NOT NULL,
    phone character varying(45) NOT NULL,
    service_message character varying(512),
    last_status_checked timestamp with time zone,
    updated timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    content_type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    amount_currency character varying(3) NOT NULL,
    initiator_id bigint,
    transaction_type character varying(10) NOT NULL
);


ALTER TABLE public.qosic_transaction OWNER TO nelson;

--
-- Name: qosic_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.qosic_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qosic_transaction_id_seq OWNER TO nelson;

--
-- Name: qosic_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.qosic_transaction_id_seq OWNED BY public.qosic_transaction.id;


--
-- Name: shops; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.shops (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    avatar_url character varying(200),
    description text,
    phone_number character varying(255) NOT NULL,
    user_id bigint NOT NULL,
    cover_url character varying(200),
    affiliate_id bigint,
    domains character varying(255)[] NOT NULL,
    country_code character varying(10) NOT NULL,
    currency_iso character varying(10) NOT NULL,
    email character varying(254) NOT NULL
);


ALTER TABLE public.shops OWNER TO nelson;

--
-- Name: shop_new_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.shop_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shop_new_id_seq OWNER TO nelson;

--
-- Name: shop_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.shop_new_id_seq OWNED BY public.shops.id;


--
-- Name: shops_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.shops_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shops_id_seq OWNER TO nelson;

--
-- Name: shops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.shops_id_seq OWNED BY public.shops.id;


--
-- Name: sms_verification; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.sms_verification (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    security_code character varying(120) NOT NULL,
    phone_number character varying(128) NOT NULL,
    session_token character varying(500) NOT NULL,
    is_verified boolean NOT NULL
);


ALTER TABLE public.sms_verification OWNER TO nelson;

--
-- Name: users; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    username character varying(255),
    name character varying(255),
    phone_number character varying(255) NOT NULL,
    avatar_url text,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(150) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone,
    last_name character varying(150) NOT NULL,
    password character varying(128) NOT NULL
);


ALTER TABLE public.users OWNER TO nelson;

--
-- Name: user_new_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.user_new_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_new_id_seq OWNER TO nelson;

--
-- Name: user_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.user_new_id_seq OWNED BY public.users.id;


--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.users_groups (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_groups OWNER TO nelson;

--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.users_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_groups_id_seq OWNER TO nelson;

--
-- Name: users_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.users_groups_id_seq OWNED BY public.users_groups.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO nelson;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: nelson
--

CREATE TABLE public.users_user_permissions (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_permissions OWNER TO nelson;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nelson
--

CREATE SEQUENCE public.users_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_permissions_id_seq OWNER TO nelson;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nelson
--

ALTER SEQUENCE public.users_user_permissions_id_seq OWNED BY public.users_user_permissions.id;


--
-- Name: affiliate_agents id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.affiliate_agents ALTER COLUMN id SET DEFAULT nextval('public.affiliate_agents_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: banners id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.banners ALTER COLUMN id SET DEFAULT nextval('public.banner_new_id_seq'::regclass);


--
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- Name: carts id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.carts ALTER COLUMN id SET DEFAULT nextval('public.carts_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: checkouts id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts ALTER COLUMN id SET DEFAULT nextval('public.checkouts_id_seq'::regclass);


--
-- Name: core_bankaccount id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_bankaccount ALTER COLUMN id SET DEFAULT nextval('public.core_bankaccount_id_seq'::regclass);


--
-- Name: core_billingplan id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_billingplan ALTER COLUMN id SET DEFAULT nextval('public.core_billingplan_id_seq'::regclass);


--
-- Name: core_shippingmethod id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingmethod ALTER COLUMN id SET DEFAULT nextval('public.core_shippingmethod_id_seq'::regclass);


--
-- Name: core_shippingprofile id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile ALTER COLUMN id SET DEFAULT nextval('public.core_shippingprofile_id_seq'::regclass);


--
-- Name: core_shippingprofile_shops id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile_shops ALTER COLUMN id SET DEFAULT nextval('public.core_shippingprofile_shops_id_seq'::regclass);


--
-- Name: core_shippingzone id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingzone ALTER COLUMN id SET DEFAULT nextval('public.core_shippingzone_id_seq'::regclass);


--
-- Name: core_shopdesign id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shopdesign ALTER COLUMN id SET DEFAULT nextval('public.core_shopdesign_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: exchange_rate id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.exchange_rate ALTER COLUMN id SET DEFAULT nextval('public.exchange_rate_id_seq'::regclass);


--
-- Name: kash_checkoutsession id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession ALTER COLUMN id SET DEFAULT nextval('public.kash_checkoutsession_id_seq'::regclass);


--
-- Name: kash_fundinghistory id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_fundinghistory ALTER COLUMN id SET DEFAULT nextval('public.kash_fundinghistory_id_seq'::regclass);


--
-- Name: kash_invitecode id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode ALTER COLUMN id SET DEFAULT nextval('public.kash_invitecode_id_seq'::regclass);


--
-- Name: kash_kashrequest id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest ALTER COLUMN id SET DEFAULT nextval('public.kash_kashrequest_id_seq'::regclass);


--
-- Name: kash_kashrequest_recipients id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest_recipients ALTER COLUMN id SET DEFAULT nextval('public.kash_kashrequest_recipients_id_seq'::regclass);


--
-- Name: kash_kashrequestresponse id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequestresponse ALTER COLUMN id SET DEFAULT nextval('public.kash_kashrequestresponse_id_seq'::regclass);


--
-- Name: kash_kashtransaction id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction ALTER COLUMN id SET DEFAULT nextval('public.kash_kashtransaction_id_seq1'::regclass);


--
-- Name: kash_momoaccount id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_momoaccount ALTER COLUMN id SET DEFAULT nextval('public.kash_payoutmethod_id_seq'::regclass);


--
-- Name: kash_notification id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_notification ALTER COLUMN id SET DEFAULT nextval('public.kash_notification_id_seq'::regclass);


--
-- Name: kash_sendkash id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash ALTER COLUMN id SET DEFAULT nextval('public.kash_kashtransaction_id_seq'::regclass);


--
-- Name: kash_sendkash_paid_recipients id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_paid_recipients ALTER COLUMN id SET DEFAULT nextval('public.kash_kashtransaction_paid_recipients_id_seq'::regclass);


--
-- Name: kash_sendkash_recipients id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_recipients ALTER COLUMN id SET DEFAULT nextval('public.kash_kashtransaction_recipients_id_seq'::regclass);


--
-- Name: kash_userprofile id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_userprofile ALTER COLUMN id SET DEFAULT nextval('public.kash_profile_id_seq'::regclass);


--
-- Name: kash_virtualcard id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_virtualcard ALTER COLUMN id SET DEFAULT nextval('public.kash_virtualcard_id_seq'::regclass);


--
-- Name: kash_withdrawalhistory id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_withdrawalhistory ALTER COLUMN id SET DEFAULT nextval('public.kash_withdrawalhistory_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: product_images id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.product_images ALTER COLUMN id SET DEFAULT nextval('public.product_image_new_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.product_new_id_seq'::regclass);


--
-- Name: products_categories id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products_categories ALTER COLUMN id SET DEFAULT nextval('public.products_categories_id_seq'::regclass);


--
-- Name: qosic_transaction id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.qosic_transaction ALTER COLUMN id SET DEFAULT nextval('public.qosic_transaction_id_seq'::regclass);


--
-- Name: shops id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops ALTER COLUMN id SET DEFAULT nextval('public.shop_new_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.user_new_id_seq'::regclass);


--
-- Name: users_groups id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_groups ALTER COLUMN id SET DEFAULT nextval('public.users_groups_id_seq'::regclass);


--
-- Name: users_user_permissions id; Type: DEFAULT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.users_user_permissions_id_seq'::regclass);


--
-- Data for Name: affiliate_agents; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.affiliate_agents (id, created_at, updated_at, code, momo_number, avatar_url, user_id, commission) FROM stdin;
1	2020-09-16 18:11:34.193908+01	2020-09-16 18:12:05.716932+01	A-D7XD	90137010	https://kweek.sgp1.digitaloceanspaces.com/production/7643aee6-864e-4c7b-be0a-df3ac59681ba-avatar.jpeg	40	0.08000
2	2020-09-16 18:12:19.167455+01	2020-09-16 18:12:25.436509+01	A-C8PX	62606333	https://kweek.sgp1.digitaloceanspaces.com/production/3ce08683-d7a7-4f52-a43c-5b7dea8647bc-avatar.jpeg	41	0.08000
3	2020-09-16 20:17:39.865554+01	2020-09-16 20:17:43.076485+01	A-YYFR	61572694	https://kweek.sgp1.digitaloceanspaces.com/production/2ec5228b-05d7-4e95-842d-b362e4c96696-avatar.jpeg	52	0.08000
4	2020-09-18 17:23:21.881453+01	2020-09-18 17:23:28.456715+01	A-UTDZ	97182615	https://kweek.sgp1.digitaloceanspaces.com/production/48afb359-2058-4c99-ab3f-622d4979da2c-avatar.jpeg	54	0.08000
5	2020-09-19 12:41:51.600496+01	2020-09-19 12:42:01.249353+01	A-KQAZ	+22961001272	https://kweek.sgp1.digitaloceanspaces.com/production/71653c67-c98b-4d04-99b7-d6b88893cf76-avatar.jpeg	55	0.08000
6	2020-09-19 16:52:31.477404+01	2020-09-19 16:52:45.720714+01	A-QYED	62822779	https://kweek.sgp1.digitaloceanspaces.com/production/fab7374b-2891-478c-8ff8-445b85dfa1af-avatar.png	56	0.08000
7	2020-09-19 19:12:44.164201+01	2020-09-19 19:12:49.255874+01	A-NQMT	51446843	https://kweek.sgp1.digitaloceanspaces.com/production/256ca2a6-3f31-40e7-8782-a7189e9151a1-avatar.jpeg	46	0.08000
8	2020-09-20 22:26:18.37276+01	2020-09-20 22:26:22.780311+01	A-QJSF	97544875	https://kweek.sgp1.digitaloceanspaces.com/production/089fbeaa-01b7-48fd-a864-d35a255c6389-avatar.jpeg	47	0.08000
9	2020-09-23 20:20:15.131192+01	2020-09-23 20:20:18.896299+01	A-FZE5	97061335	https://kweek.sgp1.digitaloceanspaces.com/production/a1c98f7b-8c9e-4206-ba38-4f312542acfe-avatar.jpeg	67	0.08000
10	2020-09-28 21:20:38.021576+01	2020-09-28 21:20:41.657073+01	A-LJRH	96549599	https://kweek.sgp1.digitaloceanspaces.com/production/1d69b96b-8bb9-4655-bf28-d7ab6ef0846c-avatar.jpeg	73	0.08000
11	2020-10-07 21:19:41.795404+01	2020-10-07 21:19:51.721781+01	A-SEMF	0978511357	https://kweek.sgp1.digitaloceanspaces.com/production/cf3f99db-24f7-43a4-91d5-21d8258c1fcc-avatar.png	86	0.08000
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.alembic_version (version_num) FROM stdin;
b2fbb6ae6046
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add banner	6	add_banner
22	Can change banner	6	change_banner
23	Can delete banner	6	delete_banner
24	Can view banner	6	view_banner
25	Can add cart	7	add_cart
26	Can change cart	7	change_cart
27	Can delete cart	7	delete_cart
28	Can view cart	7	view_cart
29	Can add category	8	add_category
30	Can change category	8	change_category
31	Can delete category	8	delete_category
32	Can view category	8	view_category
33	Can add customer	9	add_customer
34	Can change customer	9	change_customer
35	Can delete customer	9	delete_customer
36	Can view customer	9	view_customer
37	Can add product	10	add_product
38	Can change product	10	change_product
39	Can delete product	10	delete_product
40	Can view product	10	view_product
41	Can add user	11	add_user
42	Can change user	11	change_user
43	Can delete user	11	delete_user
44	Can view user	11	view_user
45	Can add shop	12	add_shop
46	Can change shop	12	change_shop
47	Can delete shop	12	delete_shop
48	Can view shop	12	view_shop
49	Can add product image	13	add_productimage
50	Can change product image	13	change_productimage
51	Can delete product image	13	delete_productimage
52	Can view product image	13	view_productimage
53	Can add checkout	14	add_checkout
54	Can change checkout	14	change_checkout
55	Can delete checkout	14	delete_checkout
56	Can view checkout	14	view_checkout
57	Can add cart item	15	add_cartitem
58	Can change cart item	15	change_cartitem
59	Can delete cart item	15	delete_cartitem
60	Can view cart item	15	view_cartitem
61	Can add order	16	add_order
62	Can change order	16	change_order
63	Can delete order	16	delete_order
64	Can view order	16	view_order
65	Can add order item	17	add_orderitem
66	Can change order item	17	change_orderitem
67	Can delete order item	17	delete_orderitem
68	Can view order item	17	view_orderitem
69	Can add affiliate agent	18	add_affiliateagent
70	Can change affiliate agent	18	change_affiliateagent
71	Can delete affiliate agent	18	delete_affiliateagent
72	Can view affiliate agent	18	view_affiliateagent
73	Can add SMS Verification	19	add_smsverification
74	Can change SMS Verification	19	change_smsverification
75	Can delete SMS Verification	19	delete_smsverification
76	Can view SMS Verification	19	view_smsverification
77	Can add bank account	20	add_bankaccount
78	Can change bank account	20	change_bankaccount
79	Can delete bank account	20	delete_bankaccount
80	Can view bank account	20	view_bankaccount
81	Can add billing plan	21	add_billingplan
82	Can change billing plan	21	change_billingplan
83	Can delete billing plan	21	delete_billingplan
84	Can view billing plan	21	view_billingplan
85	Can add shop design	22	add_shopdesign
86	Can change shop design	22	change_shopdesign
87	Can delete shop design	22	delete_shopdesign
88	Can view shop design	22	view_shopdesign
89	Can add exchange backend	23	add_exchangebackend
90	Can change exchange backend	23	change_exchangebackend
91	Can delete exchange backend	23	delete_exchangebackend
92	Can view exchange backend	23	view_exchangebackend
93	Can add rate	24	add_rate
94	Can change rate	24	change_rate
95	Can delete rate	24	delete_rate
96	Can view rate	24	view_rate
97	Can add shipping profile	25	add_shippingprofile
98	Can change shipping profile	25	change_shippingprofile
99	Can delete shipping profile	25	delete_shippingprofile
100	Can view shipping profile	25	view_shippingprofile
101	Can add shipping zone	26	add_shippingzone
102	Can change shipping zone	26	change_shippingzone
103	Can delete shipping zone	26	delete_shippingzone
104	Can view shipping zone	26	view_shippingzone
105	Can add shipping method	27	add_shippingmethod
106	Can change shipping method	27	change_shippingmethod
107	Can delete shipping method	27	delete_shippingmethod
108	Can view shipping method	27	view_shippingmethod
109	Can add checkout session	28	add_checkoutsession
110	Can change checkout session	28	change_checkoutsession
111	Can delete checkout session	28	delete_checkoutsession
112	Can view checkout session	28	view_checkoutsession
113	Can add transaction	29	add_transaction
114	Can change transaction	29	change_transaction
115	Can delete transaction	29	delete_transaction
116	Can view transaction	29	view_transaction
117	Can add profile	30	add_profile
118	Can change profile	30	change_profile
119	Can delete profile	30	delete_profile
120	Can view profile	30	view_profile
121	Can add virtual card	31	add_virtualcard
122	Can change virtual card	31	change_virtualcard
123	Can delete virtual card	31	delete_virtualcard
124	Can view virtual card	31	view_virtualcard
125	Can add user profile	30	add_userprofile
126	Can change user profile	30	change_userprofile
127	Can delete user profile	30	delete_userprofile
128	Can view user profile	30	view_userprofile
129	Can add kash transaction	32	add_kashtransaction
130	Can change kash transaction	32	change_kashtransaction
131	Can delete kash transaction	32	delete_kashtransaction
132	Can view kash transaction	32	view_kashtransaction
133	Can add payout method	33	add_payoutmethod
134	Can change payout method	33	change_payoutmethod
135	Can delete payout method	33	delete_payoutmethod
136	Can view payout method	33	view_payoutmethod
137	Can add notification	34	add_notification
138	Can change notification	34	change_notification
139	Can delete notification	34	delete_notification
140	Can view notification	34	view_notification
141	Can add kash request	35	add_kashrequest
142	Can change kash request	35	change_kashrequest
143	Can delete kash request	35	delete_kashrequest
144	Can view kash request	35	view_kashrequest
145	Can add kash request response	36	add_kashrequestresponse
146	Can change kash request response	36	change_kashrequestresponse
147	Can delete kash request response	36	delete_kashrequestresponse
148	Can view kash request response	36	view_kashrequestresponse
149	Can add funding history	37	add_fundinghistory
150	Can change funding history	37	change_fundinghistory
151	Can delete funding history	37	delete_fundinghistory
152	Can view funding history	37	view_fundinghistory
153	Can add invite code	38	add_invitecode
154	Can change invite code	38	change_invitecode
155	Can delete invite code	38	delete_invitecode
156	Can view invite code	38	view_invitecode
157	Can add withdrawal history	39	add_withdrawalhistory
158	Can change withdrawal history	39	change_withdrawalhistory
159	Can delete withdrawal history	39	delete_withdrawalhistory
160	Can view withdrawal history	39	view_withdrawalhistory
161	Can add send kash	32	add_sendkash
162	Can change send kash	32	change_sendkash
163	Can delete send kash	32	delete_sendkash
164	Can view send kash	32	view_sendkash
165	Can add kash transaction	40	add_kashtransaction
166	Can change kash transaction	40	change_kashtransaction
167	Can delete kash transaction	40	delete_kashtransaction
168	Can view kash transaction	40	view_kashtransaction
169	Can add momo account	33	add_momoaccount
170	Can change momo account	33	change_momoaccount
171	Can delete momo account	33	delete_momoaccount
172	Can view momo account	33	view_momoaccount
\.


--
-- Data for Name: banners; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.banners (id, created_at, updated_at, link, image_url) FROM stdin;
1	2019-09-24 23:13:59.923278+01	2019-09-24 23:13:59.923278+01	https://wa.me/22996678729?text=J'aimerais%20vendre%20sur%20Kweek	https://kweek.sgp1.digitaloceanspaces.com/banners/Vendez%20SUR%20KWEEK.png
2	2019-09-24 23:14:50.404445+01	2019-09-24 23:14:50.404445+01	https://wa.me/22996678729?text=J'aimerais%20%C3%AAtre%20inform%C3%A9(e)%20de%20vos%20nouveaut%C3%A9s%20sur%20WhatsApp	https://kweek.sgp1.digitaloceanspaces.com/banners/information-whatsapp.png
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.cart_items (id, created_at, updated_at, quantity, cart_id, product_id, price, price_currency) FROM stdin;
964	2021-03-24 08:09:29.808264+01	2021-03-24 08:09:29.808314+01	1	93	232	15.00	NGN
988	2021-03-25 14:36:07.941117+01	2021-03-25 14:36:07.941257+01	4	95	232	15.00	NGN
989	2021-03-25 14:36:07.947349+01	2021-03-25 14:36:07.947386+01	1	95	232	15.00	NGN
931	2021-02-10 15:38:14.982699+01	2021-03-21 18:51:29.488397+01	1	77	238	1000.00	XOF
933	2021-02-10 15:46:20.279661+01	2021-03-21 18:51:29.502339+01	1	79	238	1000.00	XOF
935	2021-02-10 16:16:50.292971+01	2021-03-21 18:51:29.511811+01	1	81	238	1000.00	XOF
945	2021-02-10 16:37:28.563033+01	2021-03-21 18:51:29.520981+01	1	83	235	50.00	NGN
946	2021-02-10 16:37:28.567402+01	2021-03-21 18:51:29.530806+01	3	83	235	50.00	NGN
947	2021-02-10 16:37:28.569899+01	2021-03-21 18:51:29.540816+01	1	83	231	10.00	NGN
949	2021-02-10 18:07:27.593909+01	2021-03-21 18:51:29.549146+01	1	85	231	10.00	NGN
951	2021-02-12 22:23:58.953746+01	2021-03-21 18:51:29.553703+01	1	87	232	15.00	NGN
58	2020-09-18 21:06:33.091355+01	2021-03-21 18:51:29.557949+01	1	37	231	10.00	NGN
89	2020-10-06 15:49:03.80705+01	2021-03-21 18:51:29.562111+01	2	54	233	25.00	NGN
113	2020-12-02 18:28:32.629532+01	2021-03-21 18:51:29.566377+01	1	70	289	200000.00	XOF
91	2020-10-07 12:55:05.194418+01	2021-03-21 18:51:29.570391+01	1	56	279	17545.00	XOF
92	2020-10-08 17:24:27.137146+01	2021-03-21 18:51:29.574319+01	1	57	285	7000.00	XOF
95	2020-10-13 08:21:58.247794+01	2021-03-21 18:51:29.578299+01	1	60	242	20000.00	XOF
33	2020-09-16 07:55:58.326571+01	2021-03-21 18:51:29.58249+01	1	23	235	50.00	NGN
34	2020-09-16 10:41:29.149511+01	2021-03-21 18:51:29.586568+01	1	24	235	50.00	NGN
97	2020-10-13 09:55:41.809464+01	2021-03-21 18:51:29.59049+01	1	61	242	20000.00	XOF
98	2020-10-13 11:10:18.781558+01	2021-03-21 18:51:29.59448+01	1	62	242	20000.00	XOF
99	2020-10-13 11:46:42.522766+01	2021-03-21 18:51:29.598514+01	1	63	240	15000.00	XOF
38	2020-09-16 19:18:18.098427+01	2021-03-21 18:51:29.602434+01	1	26	237	10000.00	XOF
39	2020-09-16 19:20:42.850414+01	2021-03-21 18:51:29.607027+01	1	26	237	10000.00	XOF
40	2020-09-16 20:20:05.115516+01	2021-03-21 18:51:29.611029+01	1	27	235	50.00	NGN
41	2020-09-17 14:06:33.258028+01	2021-03-21 18:51:29.615129+01	2	28	231	10.00	NGN
21	2020-09-14 21:50:45.552099+01	2021-03-21 18:51:29.619121+01	1	17	234	30.00	NGN
22	2020-09-14 22:18:30.313934+01	2021-03-21 18:51:29.62308+01	2	18	232	15.00	NGN
24	2020-09-15 09:36:47.86005+01	2021-03-21 18:51:29.627038+01	1	20	231	10.00	NGN
25	2020-09-15 10:23:54.162817+01	2021-03-21 18:51:29.631275+01	1	21	231	10.00	NGN
44	2020-09-17 14:37:46.652479+01	2021-03-21 18:51:29.635218+01	2	9	231	10.00	NGN
45	2020-09-17 14:39:14.053293+01	2021-03-21 18:51:29.639137+01	2	29	231	10.00	NGN
47	2020-09-17 18:54:55.665072+01	2021-03-21 18:51:29.64327+01	1	30	237	10000.00	XOF
48	2020-09-17 19:15:58.447866+01	2021-03-21 18:51:29.647391+01	1	31	231	10.00	NGN
18	2020-09-14 20:00:52.302269+01	2021-03-21 18:51:29.651458+01	1	16	232	15.00	NGN
19	2020-09-14 20:17:07.206299+01	2021-03-21 18:51:29.655837+01	2	16	234	30.00	NGN
49	2020-09-17 19:16:01.237077+01	2021-03-21 18:51:29.660539+01	1	31	231	10.00	NGN
51	2020-09-18 15:30:06.130907+01	2021-03-21 18:51:29.664715+01	1	33	240	15000.00	XOF
52	2020-09-18 15:30:09.874524+01	2021-03-21 18:51:29.668679+01	1	33	240	15000.00	XOF
54	2020-09-18 15:42:27.739241+01	2021-03-21 18:51:29.672697+01	1	35	240	15000.00	XOF
55	2020-09-18 16:11:50.143002+01	2021-03-21 18:51:29.677085+01	1	36	241	20000.00	XOF
50	2020-09-18 15:10:10.514774+01	2021-03-21 18:51:29.681067+01	1	32	240	15000.00	XOF
59	2020-09-19 08:15:48.594504+01	2021-03-21 18:51:29.685026+01	1	38	242	20000.00	XOF
60	2020-09-19 08:15:53.637097+01	2021-03-21 18:51:29.688971+01	1	38	240	15000.00	XOF
101	2020-10-13 17:52:02.73868+01	2021-03-21 18:51:29.692972+01	1	64	286	7000.00	XOF
75	2020-09-22 12:12:37.661171+01	2021-03-21 18:51:29.697074+01	1	44	242	20000.00	XOF
76	2020-09-22 15:30:29.644816+01	2021-03-21 18:51:29.701016+01	1	45	242	20000.00	XOF
960	2021-03-24 07:58:31.173901+01	2021-03-24 07:58:31.173933+01	3	91	232	15.00	NGN
962	2021-03-24 08:07:35.296193+01	2021-03-24 08:07:35.296221+01	1	92	311	40.00	NGN
963	2021-03-24 08:07:35.299784+01	2021-03-24 08:07:35.299822+01	3	92	231	10.00	NGN
965	2021-03-24 10:33:59.47399+01	2021-03-24 10:33:59.474039+01	1	94	316	5000.00	XOF
77	2020-09-22 16:39:17.496187+01	2021-03-21 18:51:29.705047+01	1	46	260	130000.00	XOF
78	2020-09-22 16:39:27.055805+01	2021-03-21 18:51:29.712392+01	1	46	260	130000.00	XOF
79	2020-09-22 16:39:29.098675+01	2021-03-21 18:51:29.716532+01	1	46	260	130000.00	XOF
80	2020-09-22 16:39:31.255299+01	2021-03-21 18:51:29.720728+01	1	46	260	130000.00	XOF
105	2020-10-14 21:05:23.226961+01	2021-03-21 18:51:29.724824+01	1	67	286	7000.00	XOF
106	2020-10-14 21:05:28.671281+01	2021-03-21 18:51:29.728884+01	1	67	286	7000.00	XOF
82	2020-09-24 11:05:00.089831+01	2021-03-21 18:51:29.733021+01	1	48	255	270000.00	XOF
83	2020-09-26 04:16:21.213901+01	2021-03-21 18:51:29.737118+01	1	49	252	285000.00	XOF
84	2020-09-26 17:03:16.63671+01	2021-03-21 18:51:29.741396+01	1	50	250	300000.00	XOF
85	2020-09-29 15:12:50.06079+01	2021-03-21 18:51:29.745344+01	1	51	232	15.00	NGN
86	2020-09-29 16:40:45.199739+01	2021-03-21 18:51:29.74937+01	1	52	276	9000.00	XOF
87	2020-10-03 09:52:23.106429+01	2021-03-21 18:51:29.753381+01	1	53	231	10.00	NGN
107	2020-10-16 16:06:51.715361+01	2021-03-21 18:51:29.757359+01	1	65	286	7000.00	XOF
109	2020-11-01 14:53:00.420328+01	2021-03-21 18:51:29.761797+01	1	68	242	20000.00	XOF
110	2020-12-02 08:31:22.767651+01	2021-03-21 18:51:29.76599+01	1	69	288	218000.00	XOF
116	2021-02-07 13:26:31.569566+01	2021-03-21 18:51:29.769977+01	3	72	238	1000.00	XOF
909	2021-02-09 23:31:30.258455+01	2021-03-21 18:51:29.774139+01	1	73	238	1000.00	XOF
910	2021-02-09 23:31:30.263794+01	2021-03-21 18:51:29.778089+01	2	73	238	1000.00	XOF
911	2021-02-09 23:31:30.266489+01	2021-03-21 18:51:29.782191+01	1	73	238	1000.00	XOF
919	2021-02-10 01:28:14.603425+01	2021-03-21 18:51:29.786308+01	2	76	231	10.00	NGN
926	2021-02-10 08:41:01.675733+01	2021-03-21 18:51:29.790367+01	1	75	231	10.00	NGN
927	2021-02-10 08:41:01.679806+01	2021-03-21 18:51:29.794392+01	1	75	231	10.00	NGN
928	2021-02-10 08:41:01.684051+01	2021-03-21 18:51:29.798442+01	1	75	231	10.00	NGN
929	2021-02-10 08:41:01.687027+01	2021-03-21 18:51:29.802388+01	3	75	232	15.00	NGN
930	2021-02-10 08:41:01.689841+01	2021-03-21 18:51:29.806566+01	2	75	233	25.00	NGN
932	2021-02-10 15:42:42.376614+01	2021-03-21 18:51:29.810537+01	1	78	238	1000.00	XOF
934	2021-02-10 15:51:04.705208+01	2021-03-21 18:51:29.814605+01	1	80	238	1000.00	XOF
939	2021-02-10 16:35:44.356151+01	2021-03-21 18:51:29.818812+01	1	82	231	10.00	NGN
940	2021-02-10 16:35:44.363125+01	2021-03-21 18:51:29.82275+01	3	82	233	25.00	NGN
941	2021-02-10 16:35:44.366141+01	2021-03-21 18:51:29.826804+01	3	82	235	50.00	NGN
948	2021-02-10 17:56:13.383261+01	2021-03-21 18:51:29.831332+01	3	84	231	10.00	NGN
950	2021-02-12 14:26:52.96207+01	2021-03-21 18:51:29.835302+01	3	86	231	10.00	NGN
952	2021-02-12 23:10:52.721442+01	2021-03-21 18:51:29.839298+01	1	88	231	10.00	NGN
954	2021-02-22 17:57:53.069015+01	2021-03-21 18:51:29.843282+01	2	89	231	10.00	NGN
955	2021-02-22 17:57:53.078458+01	2021-03-21 18:51:29.847528+01	1	89	231	10.00	NGN
\.


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.carts (id, created_at, updated_at, uid, paid, shop_id) FROM stdin;
90	2021-03-24 07:56:43.850249+01	2021-03-24 07:56:43.8503+01	21KEGSRTFHk	f	23
92	2021-03-24 08:07:21.885926+01	2021-03-24 08:07:57.451572+01	GMD1MJBbbqc	t	23
94	2021-03-24 10:33:59.203043+01	2021-03-24 10:33:59.203131+01	V_tnXov4E_o	f	25
1	2020-09-03 11:34:49.171452+01	2021-03-05 18:24:01.782138+01	nTW3dxzahBu1fA	f	\N
2	2020-09-03 13:06:29.747664+01	2021-03-05 18:24:01.794048+01	xG0bPrnQ2wAuew	f	\N
3	2020-09-03 13:08:06.977441+01	2021-03-05 18:24:01.803158+01	Ma-9uHxdYqmuBg	f	\N
4	2020-09-04 12:39:46.646045+01	2021-03-05 18:24:01.812289+01	sbNOQNn2F-VvSg	f	\N
5	2020-09-04 12:39:46.946921+01	2021-03-05 18:24:01.820038+01	nZ0ehoDiNOTyhw	f	\N
6	2020-09-04 12:39:47.44675+01	2021-03-05 18:24:01.826259+01	SrpgSomV8NKWDQ	f	\N
7	2020-09-04 12:39:47.94422+01	2021-03-05 18:24:01.830728+01	CFpZqoKEmCfyXQ	f	\N
8	2020-09-04 12:39:54.394063+01	2021-03-05 18:24:01.835804+01	FmbH9T_5aawL2A	f	\N
9	2020-09-04 12:42:55.354907+01	2021-03-05 18:24:01.840808+01	PFBNSME3JhXf0Q	f	23
10	2020-09-05 15:35:29.002089+01	2021-03-05 18:24:01.84861+01	-VbvDsOnVeuRHg	f	\N
11	2020-09-05 15:35:46.132138+01	2021-03-05 18:24:01.853173+01	INI69UzJ8VB6Vw	f	\N
12	2020-09-12 22:17:31.282652+01	2021-03-05 18:24:01.857949+01	PzCLOmeeTPE	f	\N
13	2020-09-13 21:26:32.609779+01	2021-03-05 18:24:01.862436+01	sz-hDlDPErA	f	\N
14	2020-09-14 13:13:58.638866+01	2021-03-05 18:24:01.866849+01	iXzcAxFpzp0	f	\N
15	2020-09-14 19:04:23.222854+01	2021-03-05 18:24:01.871444+01	OjQJUDk6AxY	f	\N
16	2020-09-14 20:00:52.293353+01	2021-03-05 18:24:01.878586+01	tVuWFsFRB3c	f	23
17	2020-09-14 21:46:02.822513+01	2021-03-05 18:24:01.884264+01	thMYBnb3avs	f	23
18	2020-09-14 22:18:30.306563+01	2021-03-05 18:24:01.889568+01	MMO9Ao1DgAA	f	23
19	2020-09-15 07:20:22.721934+01	2021-03-05 18:24:01.894417+01	Ccm-fvPNB4s	f	\N
20	2020-09-15 09:36:47.848598+01	2021-03-05 18:24:01.899193+01	u3InBDhzVgU	f	23
21	2020-09-15 10:23:54.149458+01	2021-03-05 18:24:01.904375+01	Wqmm4CC40SI	f	23
22	2020-09-15 10:44:41.854974+01	2021-03-05 18:24:01.909089+01	FDA-hYxL_mI	f	\N
23	2020-09-16 07:55:58.311531+01	2021-03-05 18:24:01.913666+01	qA9CcYse3kk	f	23
24	2020-09-16 10:41:29.142168+01	2021-03-05 18:24:01.918547+01	QVeQOxxXjz4	f	23
25	2020-09-16 19:04:15.421411+01	2021-03-05 18:24:01.923266+01	dkfrelF1kTs	f	\N
26	2020-09-16 19:18:18.092949+01	2021-03-05 18:24:01.928099+01	FEdmBmaSzFo	f	29
27	2020-09-16 20:20:05.101132+01	2021-03-05 18:24:01.932765+01	lCF2YVI0gm4	f	23
28	2020-09-17 14:06:33.245852+01	2021-03-05 18:24:01.937367+01	r0MOfQKx_iY	f	23
29	2020-09-17 14:39:14.046988+01	2021-03-05 18:24:01.942029+01	Ks64BMsdzqk	f	23
30	2020-09-17 18:54:55.649663+01	2021-03-05 18:24:01.946862+01	CAbIWnWenLk	f	29
31	2020-09-17 19:15:58.441228+01	2021-03-05 18:24:01.953893+01	KyRd_jG-eKc	f	23
32	2020-09-18 15:10:10.50787+01	2021-03-05 18:24:01.958656+01	qwjA0rz6OwI	f	34
33	2020-09-18 15:30:06.123963+01	2021-03-05 18:24:01.963332+01	ibmSzXwZfbE	f	34
34	2020-09-18 15:39:03.71886+01	2021-03-05 18:24:01.967899+01	qq7tOIV_ZdA	f	\N
35	2020-09-18 15:42:27.734148+01	2021-03-05 18:24:01.972729+01	_6nNXUjhGlg	f	34
36	2020-09-18 16:11:50.134741+01	2021-03-05 18:24:01.977367+01	qgeyG9hl-pg	f	35
37	2020-09-18 21:06:33.082261+01	2021-03-05 18:24:01.982022+01	OpXC2aS3n_A	f	23
38	2020-09-19 08:15:48.586887+01	2021-03-05 18:24:01.98696+01	f-FDgIzZJx8	f	34
39	2020-09-19 11:36:23.839446+01	2021-03-05 18:24:01.991763+01	iiRZuDW-y-U	f	\N
40	2020-09-22 09:24:21.0757+01	2021-03-05 18:24:01.996985+01	XzlB1K0KNWE	f	\N
41	2020-09-22 09:53:04.613022+01	2021-03-05 18:24:02.001501+01	AaBnfCAZsTg	f	\N
42	2020-09-22 11:20:29.908647+01	2021-03-05 18:24:02.006602+01	5ZZpu3Jrg4k	f	\N
43	2020-09-22 11:23:34.327261+01	2021-03-05 18:24:02.011403+01	MDZak_okKMU	f	\N
44	2020-09-22 12:12:37.650378+01	2021-03-05 18:24:02.016488+01	LZX1fphwciw	f	34
45	2020-09-22 15:30:29.631258+01	2021-03-05 18:24:02.021693+01	wCK4sHJJ73c	f	34
46	2020-09-22 16:39:17.482346+01	2021-03-05 18:24:02.026711+01	mbhWHztGrYc	f	37
47	2020-09-23 07:07:34.817629+01	2021-03-05 18:24:02.031203+01	ozgBVMtzD20	f	\N
48	2020-09-24 11:05:00.041563+01	2021-03-05 18:24:02.035746+01	vpJsx5SFTFw	f	37
49	2020-09-26 04:16:21.202389+01	2021-03-05 18:24:02.040679+01	JVObt18Mc9A	f	37
50	2020-09-26 17:03:16.617375+01	2021-03-05 18:24:02.045569+01	TGzwQqMpiIU	f	37
51	2020-09-29 15:12:50.046471+01	2021-03-05 18:24:02.05042+01	AZavgc5s1w4	f	23
52	2020-09-29 16:40:45.188762+01	2021-03-05 18:24:02.055295+01	dwHxV8aTC5Q	f	36
53	2020-10-03 09:52:23.097725+01	2021-03-05 18:24:02.060981+01	ZcqDkqE15_A	f	23
54	2020-10-06 15:49:03.793058+01	2021-03-05 18:24:02.066264+01	-S57K1nZbrA	f	23
55	2020-10-06 16:30:43.926058+01	2021-03-05 18:24:02.071342+01	YgPb7JShNTY	f	\N
56	2020-10-07 12:55:05.185143+01	2021-03-05 18:24:02.076077+01	E8aYdH-mtkM	f	28
57	2020-10-08 17:24:27.12963+01	2021-03-05 18:24:02.080694+01	rbgn6F11Duk	f	54
58	2020-10-09 15:35:44.468374+01	2021-03-05 18:24:02.085547+01	E3NPRkO4Tww	f	\N
59	2020-10-10 11:27:12.419458+01	2021-03-05 18:24:02.090743+01	3HCYapBB-EU	f	\N
60	2020-10-13 08:21:58.236599+01	2021-03-05 18:24:02.095336+01	479qSoz4E4E	f	34
61	2020-10-13 09:55:41.793516+01	2021-03-05 18:24:02.099942+01	3LKsaqMVxMY	f	34
62	2020-10-13 11:10:18.768697+01	2021-03-05 18:24:02.104603+01	0r_7JbCAqYw	f	34
63	2020-10-13 11:46:42.509719+01	2021-03-05 18:24:02.109335+01	K4dmM-mIeo4	f	34
64	2020-10-13 17:51:59.202857+01	2021-03-05 18:24:02.114213+01	nfUmwShO4VA	f	47
65	2020-10-13 22:00:07.615438+01	2021-03-05 18:24:02.119294+01	0VI-DUXbxRY	f	47
66	2020-10-14 16:58:07.551603+01	2021-03-05 18:24:02.123954+01	L7A6MFjR9oM	f	\N
67	2020-10-14 21:05:23.216442+01	2021-03-05 18:24:02.128622+01	htCrNCw4vNg	f	47
68	2020-11-01 14:53:00.399384+01	2021-03-05 18:24:02.133513+01	uqk6aIOBKcQ	f	34
69	2020-12-02 08:31:22.754329+01	2021-03-05 18:24:02.138407+01	_9Li667T0Ro	f	29
70	2020-12-02 18:16:55.3807+01	2021-03-05 18:24:02.143145+01	kCmF_37Od-Y	f	29
71	2020-12-17 13:44:28.258952+01	2021-03-05 18:24:02.147834+01	nTvuUyAygu8	f	\N
72	2021-02-07 13:26:31.535528+01	2021-03-05 18:24:02.152573+01	1rCCYO7SS5U	f	33
73	2021-02-07 13:30:13.992211+01	2021-03-05 18:24:02.157587+01	IJT0gurLXVo	f	33
74	2021-02-07 20:13:54.337246+01	2021-03-05 18:24:02.162258+01	Y2kylQxGUOU	f	\N
75	2021-02-07 20:14:25.00495+01	2021-03-05 18:24:02.167152+01	rPVm24lYObM	f	23
76	2021-02-10 01:28:14.588818+01	2021-03-05 18:24:02.171993+01	DnrdKNRM8CA	f	23
77	2021-02-10 15:38:14.950699+01	2021-03-05 18:24:02.176803+01	09knu-Z3nI0	f	33
78	2021-02-10 15:42:42.362979+01	2021-03-05 18:24:02.181798+01	SquwkN670pI	f	33
79	2021-02-10 15:46:20.270906+01	2021-03-05 18:24:02.186692+01	1upS9kNUxRE	f	33
80	2021-02-10 15:51:04.69552+01	2021-03-05 18:24:02.19307+01	zd1PtDV1kVs	f	33
81	2021-02-10 16:16:50.284066+01	2021-03-05 18:24:02.197752+01	VxKTzvOxGds	f	33
82	2021-02-10 16:35:21.04683+01	2021-03-05 18:24:02.202534+01	K9hK9Rs_u5k	f	23
83	2021-02-10 16:37:15.431025+01	2021-03-05 18:24:02.207607+01	xqCspIJt3gE	f	23
84	2021-02-10 17:56:13.32872+01	2021-03-05 18:24:02.212401+01	RdWBmWxCPv8	f	23
85	2021-02-10 18:07:27.581885+01	2021-03-05 18:24:02.217079+01	f_057SUE8PQ	f	23
86	2021-02-12 14:26:52.913973+01	2021-03-05 18:24:02.221747+01	TwWdDG-Kcl0	t	23
87	2021-02-12 22:23:58.935674+01	2021-03-05 18:24:02.226633+01	GSeEEWP7OQI	t	23
88	2021-02-12 23:10:52.656304+01	2021-03-05 18:24:02.231498+01	z6jwLoSIYqE	t	23
89	2021-02-22 17:55:26.262495+01	2021-03-24 07:45:34.367055+01	W9i9x2nqMIg	t	23
91	2021-03-24 07:58:22.864523+01	2021-03-24 07:58:50.723298+01	sNGe3kvG-O0	t	23
93	2021-03-24 08:09:29.795786+01	2021-03-24 08:09:29.795815+01	9tX9p-Gt0NQ	f	23
95	2021-03-25 14:12:36.006631+01	2021-03-25 14:12:36.006661+01	p0NY56Rp1gs	f	23
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.categories (id, created_at, updated_at, name, slug, shop_id) FROM stdin;
1	2021-03-23 21:25:14.410249+01	2021-03-23 21:25:14.410303+01	T-shirts	t-shirts	\N
2	2021-03-23 21:27:45.444894+01	2021-03-23 22:50:21.116371+01	T-shirt	t-shirts	23
3	2021-03-23 23:43:43.771446+01	2021-03-23 23:43:43.771486+01	Shorts	shorts	23
4	2021-03-24 09:39:03.494856+01	2021-03-24 09:39:03.494916+01	Snacks	snacks	25
5	2021-03-24 09:49:22.440442+01	2021-03-24 09:49:22.440468+01	Boissons	boissons	25
\.


--
-- Data for Name: checkouts; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.checkouts (id, created_at, updated_at, country, city, address, uid, cart_id, customer_id, payment_method, ref_id, paid, shipping_fees, shipping_fees_currency, shipping_profile_id, zone) FROM stdin;
141	2021-03-24 00:57:17.79126+01	2021-03-24 00:57:17.791301+01	AO	Test	Test	06rlQH_KEFc	89	27	card	C-GEBEDY	f	\N	XOF	\N	
148	2021-03-24 06:54:19.992049+01	2021-03-24 06:54:19.992077+01	AO	Test	Test	3ToTtFTJY_Q	89	27	card	C-NY4JWH	f	\N	XOF	\N	
155	2021-03-24 07:43:18.516921+01	2021-03-24 07:45:34.370994+01	AO	Test	Test	oroK718067c	89	27	cash	C-UHOPLJ	t	693.09	NGN	1	
162	2021-03-30 20:16:04.868926+01	2021-03-30 20:16:27.580586+01	AO	Test	Test	MPaCONa_iKM	95	27	momo	C-FFNJLC	f	1039.64	NGN	1	Calavi
142	2021-03-24 00:57:31.780423+01	2021-03-24 00:57:31.78045+01	AO	Test	Test	nA04sBrzxMA	89	27	card	C-AA2CI2	f	\N	XOF	\N	
149	2021-03-24 07:23:25.663386+01	2021-03-24 07:23:25.66357+01	AO	Test	Test	gMgovv5SxV4	89	27	card	C-A8DU3A	f	\N	XOF	\N	
1	2020-09-03 11:35:47.268263+01	2020-09-13 19:36:11.047404+01	Benin	Calavi	Pharmacie arconville	uSKT45dOTtMLXw	1	1	card	C-K4XANM	f	\N	XOF	\N	
156	2021-03-24 07:58:37.368552+01	2021-03-24 07:58:50.726169+01	AO	Test	Test	rP1Wm2Zt3Kg	91	27	cash	C-CDY4UX	t	693.09	NGN	1	Cotonou
18	2020-09-16 19:05:07.351274+01	2020-09-16 19:05:07.351304+01	Benin	Cotonou	Segbeya	er7FI2dknrw	25	9	card	C-JV4DIJ	f	\N	XOF	\N	
19	2020-09-16 19:24:02.591306+01	2020-09-16 19:24:02.591325+01	Anguilla	Cotonou	qaz	FPMfCxryhwI	26	10	card	C-LFHFXQ	f	\N	XOF	\N	
22	2020-09-17 19:58:30.900809+01	2020-09-17 19:58:30.900838+01	Bonaire, Sint Eustatius and Saba	Goha	Some address	NWdW21RongE	29	1	card	C-J4WN7S	f	\N	XOF	\N	
30	2020-09-26 04:18:19.317743+01	2020-09-26 04:18:19.317763+01	Benin	Calavi	Carrefour tankpê	G0k0O0lChgo	49	20	momo	C-6BSXEJ	f	\N	XOF	\N	
12	2020-09-14 21:46:29.325116+01	2021-03-22 00:01:45.002855+01	Benin	Cotonou	Abomey-calavi, Gbodjo lot 41	44RIufCQSzA	17	4	card	C-BLZW8H	f	1000.00	XOF	1	
143	2021-03-24 00:58:38.817762+01	2021-03-24 00:58:38.817803+01	AO	Test	Test	EvB9Iuj9Vq8	89	27	card	C-W5KZND	f	\N	XOF	\N	
150	2021-03-24 07:29:40.075526+01	2021-03-24 07:29:40.075619+01	AO	Test	Test	qTndxPVzCu0	89	27	card	C-BYLFNH	f	\N	XOF	\N	
37	2021-02-09 22:32:21.09453+01	2021-02-09 22:32:21.094808+01	US	CLAYMONT	2803 Philadelphia Pike	YMPnlc2EM3I	73	1	card	C-IPWD3W	f	\N	XOF	\N	
38	2021-02-09 23:28:32.247662+01	2021-02-09 23:28:32.247853+01	US	CLAYMONT	2803 Philadelphia Pike	cimfm3M3PJE	73	1	card	C-NOCASV	f	\N	XOF	\N	
39	2021-02-09 23:28:49.843455+01	2021-02-09 23:28:49.843481+01	US	CLAYMONT	2803 Philadelphia Pike	_QSnYMA25JM	73	1	card	C-XQGHCD	f	\N	XOF	\N	
40	2021-02-09 23:29:46.311249+01	2021-02-09 23:29:46.311275+01	US	CLAYMONT	2803 Philadelphia Pike	b4seMM_fOpY	73	1	card	C-BNYSME	f	\N	XOF	\N	
41	2021-02-09 23:31:33.016222+01	2021-02-09 23:31:33.016248+01	US	CLAYMONT	2803 Philadelphia Pike	xZxKRqlA4zI	73	1	card	C-TKKYH6	f	\N	XOF	\N	
42	2021-02-09 23:34:08.98015+01	2021-02-09 23:34:08.980178+01	US	CLAYMONT	2803 Philadelphia Pike	CENiiz5HzdI	73	1	card	C-0MUN7N	f	\N	XOF	\N	
43	2021-02-09 23:34:32.627914+01	2021-02-09 23:34:32.627958+01	US	CLAYMONT	2803 Philadelphia Pike	DFhHwu4TZkU	73	1	card	C-DNU4CT	f	\N	XOF	\N	
44	2021-02-09 23:37:53.702443+01	2021-02-09 23:37:53.702512+01	US	CLAYMONT	2803 Philadelphia Pike	v6tKTMKPogY	73	1	card	C-ZYMJGR	f	\N	XOF	\N	
45	2021-02-09 23:40:42.136258+01	2021-02-09 23:40:42.136291+01	US	CLAYMONT	2803 Philadelphia Pike	fXJRG976KMQ	73	1	card	C-IGJEKS	f	\N	XOF	\N	
46	2021-02-09 23:42:05.622619+01	2021-02-09 23:42:05.622681+01	US	CLAYMONT	2803 Philadelphia Pike	zZcf1X8CVtw	73	1	card	C-YTV6LZ	f	\N	XOF	\N	
47	2021-02-09 23:43:35.19997+01	2021-02-09 23:43:35.200031+01	US	CLAYMONT	2803 Philadelphia Pike	z4QKuU38EkU	73	1	card	C-LKIXI6	f	\N	XOF	\N	
48	2021-02-09 23:44:23.351785+01	2021-02-09 23:44:23.351812+01	US	CLAYMONT	2803 Philadelphia Pike	A8H6ARdb1tc	73	1	card	C-GBNV9H	f	\N	XOF	\N	
49	2021-02-09 23:44:42.360284+01	2021-02-09 23:44:42.360314+01	US	CLAYMONT	2803 Philadelphia Pike	cgqaDfkzd_o	73	1	card	C-LUHDQL	f	\N	XOF	\N	
50	2021-02-09 23:45:06.128415+01	2021-02-09 23:45:06.128443+01	US	CLAYMONT	2803 Philadelphia Pike	L5Xh8k3wyaE	73	1	card	C-SEMJIK	f	\N	XOF	\N	
51	2021-02-09 23:48:35.15299+01	2021-02-09 23:48:35.153016+01	US	CLAYMONT	2803 Philadelphia Pike	KVAxSgdW3qQ	73	1	card	C-ATJFQW	f	\N	XOF	\N	
52	2021-02-09 23:59:47.842265+01	2021-02-09 23:59:47.84231+01	US	CLAYMONT	2803 Philadelphia Pike	3EnZOCbKKog	73	1	card	C-OSPU47	f	\N	XOF	\N	
53	2021-02-10 00:01:47.289372+01	2021-02-10 00:01:47.289401+01	US	CLAYMONT	2803 Philadelphia Pike	4VUlOmduYmw	73	1	card	C-TLYMUZ	f	\N	XOF	\N	
54	2021-02-10 00:04:03.683331+01	2021-02-10 00:04:03.683359+01	US	CLAYMONT	2803 Philadelphia Pike	u6NgGokQslc	73	1	card	C-5TG7UC	f	\N	XOF	\N	
55	2021-02-10 00:04:22.567266+01	2021-02-10 00:04:22.567323+01	US	CLAYMONT	2803 Philadelphia Pike	tr29quBqhSg	73	1	card	C-SJPN83	f	\N	XOF	\N	
56	2021-02-10 00:41:33.661549+01	2021-02-10 00:41:33.661578+01	US	CLAYMONT	2803 Philadelphia Pike	YQxOsK1164E	73	1	card	C-0XLYJH	f	\N	XOF	\N	
57	2021-02-10 00:45:18.917969+01	2021-02-10 00:45:18.917995+01	US	CLAYMONT	2803 Philadelphia Pike	E-f8iVNwiGU	73	1	card	C-SXAZ7W	f	\N	XOF	\N	
58	2021-02-10 00:46:38.060221+01	2021-02-10 00:46:38.060247+01	US	CLAYMONT	2803 Philadelphia Pike	EXtAZ2DuI78	73	1	card	C-VVCYZA	f	\N	XOF	\N	
59	2021-02-10 00:46:42.112706+01	2021-02-10 00:46:42.112733+01	US	CLAYMONT	2803 Philadelphia Pike	UG7rnjDE910	73	1	card	C-BORBYS	f	\N	XOF	\N	
60	2021-02-10 00:47:53.10831+01	2021-02-10 00:47:53.10834+01	US	CLAYMONT	2803 Philadelphia Pike	GgtwLu5jYdE	73	1	card	C-OSVF3S	f	\N	XOF	\N	
61	2021-02-10 00:51:43.085071+01	2021-02-10 00:51:43.0851+01	US	CLAYMONT	2803 Philadelphia Pike	IzNj156ROm4	73	1	card	C-HY6RCY	f	\N	XOF	\N	
62	2021-02-10 00:53:29.14823+01	2021-02-10 00:53:29.148256+01	US	CLAYMONT	2803 Philadelphia Pike	NhWylrc4I9U	73	1	card	C-PD2GIN	f	\N	XOF	\N	
63	2021-02-10 00:54:06.265511+01	2021-02-10 00:54:06.265544+01	US	CLAYMONT	2803 Philadelphia Pike	zgr7ZKuu7EQ	73	1	card	C-E10SJV	f	\N	XOF	\N	
64	2021-02-10 08:26:23.758581+01	2021-02-10 08:26:23.758769+01	US	CLAYMONT	2803 Philadelphia Pike	Z7C9nw8IpVg	73	1	card	C-GEXDIB	f	\N	XOF	\N	
65	2021-02-10 08:41:40.913381+01	2021-02-10 08:41:40.913431+01	BJ	Cotonou	Akpakpa	4x479Sozx4I	75	21	card	C-VJT9IX	f	\N	XOF	\N	
66	2021-02-10 08:44:26.521119+01	2021-02-10 08:44:26.521181+01	BJ	Cotonou	Akpakpa	OGsOXWHdxIg	75	21	card	C-PPB8SO	f	\N	XOF	\N	
67	2021-02-10 10:43:39.670293+01	2021-02-10 10:43:39.670556+01	AO	CLAYMONT	2803 Philadelphia Pike	PdymTYiZ9RQ	73	1	card	C-UEEZUZ	f	\N	XOF	\N	
68	2021-02-10 10:46:02.820402+01	2021-02-10 10:46:02.820435+01	AO	CLAYMONT	2803 Philadelphia Pike	ChoivBveOGo	73	1	card	C-PUWSJD	f	\N	XOF	\N	
69	2021-02-10 10:52:48.317049+01	2021-02-10 10:52:48.317128+01	AO	CLAYMONT	2803 Philadelphia Pike	j8Lv-JgeBxA	73	1	card	C-5YXTSM	f	\N	XOF	\N	
70	2021-02-10 10:52:57.164676+01	2021-02-10 10:52:57.164706+01	AO	CLAYMONT	2803 Philadelphia Pike	IfNQ5uFr-5g	73	1	card	C-OF6WAK	f	\N	XOF	\N	
71	2021-02-10 10:53:11.760936+01	2021-02-10 10:53:11.760993+01	AO	CLAYMONT	2803 Philadelphia Pike	CHLQVRKYez4	73	1	card	C-89TF2M	f	\N	XOF	\N	
72	2021-02-10 10:58:47.205432+01	2021-02-10 10:58:47.205539+01	AO	CLAYMONT	2803 Philadelphia Pike	5_eWK0O8FR4	73	1	card	C-2QBOMQ	f	\N	XOF	\N	
73	2021-02-10 10:59:34.818974+01	2021-02-10 10:59:34.819052+01	AO	CLAYMONT	2803 Philadelphia Pike	K0HcJHXFruY	73	1	card	C-MDQ6WA	f	\N	XOF	\N	
74	2021-02-10 11:30:55.718415+01	2021-02-10 11:30:55.718471+01	AO	CLAYMONT	2803 Philadelphia Pike	iUPFdHpmPeQ	73	1	card	C-X8NQE3	f	\N	XOF	\N	
75	2021-02-10 11:39:27.899717+01	2021-02-10 11:39:27.899747+01	AO	CLAYMONT	2803 Philadelphia Pike	mnsv4RcF_Ls	73	1	card	C-RNSOOY	f	\N	XOF	\N	
76	2021-02-10 13:30:37.07609+01	2021-02-10 13:30:37.076118+01	AO	CLAYMONT	2803 Philadelphia Pike	ZubuHKo96iU	73	1	card	C-6DL1OS	f	\N	XOF	\N	
157	2021-03-24 08:07:38.099125+01	2021-03-24 08:07:38.099154+01	AO	Test	Test	Ppygn2PPmWw	92	27	card	C-ECLMJ2	f	\N	XOF	\N	Cotonou
78	2021-02-10 15:18:38.481735+01	2021-02-10 15:18:38.481773+01	AO	CLAYMONT	2803 Philadelphia Pike	bEaumpHWuR4	73	1	card	C-T8GIXB	f	\N	XOF	\N	
84	2021-02-10 15:57:49.145181+01	2021-02-10 15:57:49.145213+01	US	CLAYMONT	2803 Philadelphia Pike	OWKuFqZrpFk	80	1	card	C-GMPLBU	f	\N	XOF	\N	
85	2021-02-10 15:59:22.1678+01	2021-02-10 15:59:22.167828+01	US	CLAYMONT	2803 Philadelphia Pike	30BmNgx6w00	80	1	card	C-ZPIISS	f	\N	XOF	\N	
144	2021-03-24 00:59:19.515298+01	2021-03-24 00:59:19.51533+01	AO	Test	Test	uUvdw8fXgjk	89	27	card	C-DOKQHI	f	\N	XOF	\N	
83	2021-02-10 15:51:07.351717+01	2021-03-22 00:01:45.215031+01	US	CLAYMONT	2803 Philadelphia Pike	s2rIVAZy6Q8	80	1	card	C-F3P7O3	f	22000.00	XOF	2	
151	2021-03-24 07:33:28.226664+01	2021-03-24 07:33:28.226694+01	AO	Test	Test	-cLthNNr1FI	89	27	card	C-YIQCO9	f	\N	XOF	\N	
158	2021-03-24 08:07:43.203349+01	2021-03-24 08:07:57.455543+01	AO	Test	Test	nahzcGycxqw	92	27	cash	C-9USFB8	t	1386.19	NGN	1	Porto-Novo
86	2021-02-10 16:00:35.426546+01	2021-02-10 16:00:35.426574+01	US	CLAYMONT	2803 Philadelphia Pike	nszEkYAMid8	80	1	card	C-GDDA8P	f	\N	XOF	\N	
87	2021-02-10 16:02:05.988266+01	2021-02-10 16:02:05.988297+01	US	CLAYMONT	2803 Philadelphia Pike	U-d5nCbXppY	80	1	card	C-KAOTXC	f	\N	XOF	\N	
88	2021-02-10 16:04:30.535815+01	2021-02-10 16:04:30.53592+01	US	CLAYMONT	2803 Philadelphia Pike	LbDWmTUtueM	80	1	card	C-CEMTSZ	f	\N	XOF	\N	
89	2021-02-10 16:06:51.322171+01	2021-02-10 16:06:51.322223+01	US	CLAYMONT	2803 Philadelphia Pike	DZXjmW8MesI	80	1	card	C-DIYK5N	f	\N	XOF	\N	
90	2021-02-10 16:08:06.192601+01	2021-02-10 16:08:06.192632+01	US	CLAYMONT	2803 Philadelphia Pike	6OuSZEsM2O8	80	1	card	C-PVA8DF	f	\N	XOF	\N	
91	2021-02-10 16:10:40.463128+01	2021-02-10 16:10:40.463156+01	US	CLAYMONT	2803 Philadelphia Pike	f9VBdCAgdNY	80	1	card	C-QO1RZ2	f	\N	XOF	\N	
92	2021-02-10 16:11:56.980423+01	2021-02-10 16:11:56.980476+01	US	CLAYMONT	2803 Philadelphia Pike	OOkO06ABjq0	80	1	card	C-QFCY56	f	\N	XOF	\N	
145	2021-03-24 01:02:06.722684+01	2021-03-24 01:02:06.722727+01	AO	Test	Test	_59k69uywgU	89	27	card	C-IGTWAX	f	\N	XOF	\N	
152	2021-03-24 07:34:19.774325+01	2021-03-24 07:34:19.774388+01	AO	Test	Test	NfSZbkjzsUg	89	27	card	C-FLEIMB	f	\N	XOF	\N	
159	2021-03-24 08:09:32.163838+01	2021-03-24 08:09:33.530956+01	AO	Test	Test	LPbzFcALIaU	93	27	card	C-A1BBDF	f	1386.19	NGN	1	Porto-Novo
95	2021-02-10 16:18:21.984142+01	2021-02-10 16:18:21.98417+01	BJ	Cotonou	Akpakpa	pRse0VrD36Q	75	21	card	C-TMGFFL	f	\N	XOF	\N	
96	2021-02-10 16:20:33.408725+01	2021-02-10 16:20:33.408814+01	BJ	Cotonou	Akpakpa	PgaiuA0nhDI	75	21	card	C-25IVSU	f	\N	XOF	\N	
100	2021-02-10 17:56:39.669374+01	2021-02-10 17:56:39.669404+01	BJ	Cotonou	Akpakpa	fDOgSvoNAP0	84	21	card	C-2XV5N9	f	\N	XOF	\N	
101	2021-02-10 18:00:20.410074+01	2021-02-10 18:00:20.410162+01	BJ	Cotonou	Akpakpa	pJcbixKmERc	84	21	card	C-GQQASD	f	\N	XOF	\N	
103	2021-02-10 18:07:40.198598+01	2021-02-10 18:07:40.198625+01	BJ	Cotonou	Akpakpa	FtCoxMihv20	85	21	card	C-LCPWPP	f	\N	XOF	\N	
104	2021-02-10 18:07:48.257613+01	2021-02-10 18:07:48.257718+01	US	Cotonou	Akpakpa	OTNCQzTFtKM	85	21	card	C-I2S4AS	f	\N	XOF	\N	
105	2021-02-10 18:18:32.927329+01	2021-02-10 18:18:32.927387+01	US	Cotonou	Akpakpa	zkAZSWpYTjw	85	21	card	C-PGV51A	f	\N	XOF	\N	
106	2021-02-11 10:15:02.380816+01	2021-02-11 10:15:02.380857+01	US	Cotonou	Akpakpa	auyFyTxF31g	85	21	card	C-HDIDO2	f	\N	XOF	\N	
107	2021-02-12 19:16:31.463757+01	2021-02-12 19:16:31.463782+01	BJ	Cotonou	Test	Yo9qKie863Y	86	26	card	C-BYSHNT	f	\N	XOF	\N	
108	2021-02-12 19:21:41.416578+01	2021-02-12 19:21:41.416615+01	BJ	Cotonou	Test	3OawDWY0VDU	86	26	card	C-4URNUY	f	\N	XOF	\N	
109	2021-02-12 19:23:12.194036+01	2021-02-12 19:23:12.194085+01	BJ	Cotonou	Test	JyZ3XIYt_eI	86	26	card	C-6H9XFB	f	\N	XOF	\N	
110	2021-02-12 19:27:11.542535+01	2021-02-12 19:27:11.542588+01	BJ	Cotonou	Test	gjLbCkf1tf0	86	26	card	C-VWYHAW	f	\N	XOF	\N	
111	2021-02-12 19:29:12.193973+01	2021-02-12 19:29:12.194002+01	BJ	Cotonou	Test	fXrRkEtUZkQ	86	26	card	C-KJJM7O	f	\N	XOF	\N	
112	2021-02-12 19:58:07.995345+01	2021-02-12 19:58:07.995391+01	BJ	Cotonou	Test	BV39skcnG7w	86	26	card	C-8B5NTL	f	\N	XOF	\N	
124	2021-02-12 22:31:42.335815+01	2021-02-12 22:31:42.335844+01	BJ	Cotonou	Test	LHTOcEHC4tA	87	26	card	C-DTNMQH	f	\N	XOF	\N	
146	2021-03-24 01:03:55.185054+01	2021-03-24 01:03:55.185083+01	AO	Test	Test	1UzYQ9VtqBQ	89	27	card	C-IKCHQU	f	\N	XOF	\N	
153	2021-03-24 07:36:31.309514+01	2021-03-24 07:36:31.309546+01	AO	Test	Test	yuDP46vA-cQ	89	27	card	C-3F2VAV	f	\N	XOF	\N	
160	2021-03-25 14:11:11.700786+01	2021-03-25 14:11:11.700867+01	AO	Test	Test	yKZDc1Fbkl8	93	27	card	C-M5QTTO	f	\N	XOF	\N	Calavi
2	2020-09-03 11:38:33.064377+01	2021-03-22 00:01:45.011441+01	Benin	Calavi	Pharmacie arconville	XEzTyG8PXubf-Q	1	1	card	C-VUIXYO	f	1500.00	XOF	1	
3	2020-09-03 11:41:43.616338+01	2021-03-22 00:01:45.016705+01	Benin	Calavi	Pharmacie arconville	KBJKImSHu11LpQ	1	1	card	C-FCFF1L	f	1500.00	XOF	1	
4	2020-09-03 13:06:45.445075+01	2021-03-22 00:01:45.021336+01	Benin	Calavi	Pharmacie arconville	bzJMkkikwN_68Q	2	1	card	C-KR3H8H	f	1500.00	XOF	1	
133	2021-02-22 17:58:15.966352+01	2021-02-22 17:58:15.966379+01	AO	Test	Test	VtXjvGfWvT4	89	27	card	C-Z44ZRZ	f	\N	XOF	\N	
135	2021-02-22 18:00:57.164282+01	2021-02-22 18:00:57.164328+01	AO	Test	Test	F1ZdV9-FQFs	89	27	card	C-MSKPXL	f	\N	XOF	\N	
5	2020-09-04 12:40:44.937135+01	2021-03-22 00:01:45.028105+01	Benin	Calavi	Pharmacie arconville	eLuTpx4OgsueYw	3	1	card	C-X2GATI	f	1500.00	XOF	1	
6	2020-09-04 12:43:10.058264+01	2021-03-22 00:01:45.035886+01	Benin	Calavi	Pharmacie arconville	f7r47l-MhfyLqA	9	1	card	C-ZSIGB7	f	1500.00	XOF	1	
7	2020-09-12 22:17:55.660302+01	2021-03-22 00:01:45.04224+01	Benin	Cotonou	Rue 1606, Akpakpa	54_G66pvyeQ	12	1	card	C-MU4GXX	f	1000.00	XOF	1	
10	2020-09-14 13:14:17.80648+01	2021-03-22 00:01:45.048232+01	Benin	Cotonou	Ciné Concorde	O3wxSbA-Y5k	14	3	card	C-CVC6AD	f	1000.00	XOF	1	
20	2020-09-17 14:07:58.39431+01	2021-03-22 00:01:45.05553+01	Benin	Cotonou	Aidjedo	4G8fjtnrEgI	28	11	card	C-BYRCMD	f	1000.00	XOF	1	
11	2020-09-14 20:19:58.979054+01	2021-03-22 00:01:45.061842+01	Benin	Cotonou	Ciné Coco	or_lvpLRrQ8	16	1	momo	C-BHPIFB	f	1000.00	XOF	1	
13	2020-09-14 22:19:29.605658+01	2021-03-22 00:01:45.068577+01	Algeria	Bain	78 Gris	8WFhL23cyTk	18	5	card	C-D7AZYQ	f	21000.00	XOF	1	
27	2020-09-22 12:13:59.494301+01	2021-03-22 00:01:45.074916+01	Brazil	Santa Maria	CEP 97105340	C3WJuddBqZA	44	17	card	C-L54TAT	f	14000.00	XOF	2	
14	2020-09-15 07:21:24.0802+01	2021-03-22 00:01:45.081797+01	Åland Islands	Tunu	Tunu	sJ62q6BXfh4	19	6	momo	C-0SM84B	f	21000.00	XOF	1	
15	2020-09-15 09:37:58.757234+01	2021-03-22 00:01:45.087983+01	Benin	Cotonou	Lot 1456	n730DVdktm0	20	7	momo	C-FRN97X	f	1000.00	XOF	1	
16	2020-09-15 10:24:32.703871+01	2021-03-22 00:01:45.144068+01	Gabon	Libreville	Rue 124	22DZTzLObAg	21	8	momo	C-K0QFG5	f	14000.00	XOF	1	
17	2020-09-15 10:46:00.358525+01	2021-03-22 00:01:45.148548+01	France	Paris	La Défense	7Mppd34cMc8	22	2	card	C-0JY6UB	f	86000.00	XOF	2	
8	2020-09-13 21:10:52.80507+01	2021-03-22 00:01:45.151318+01	Benin	Cotonou	Segbeya	2OFlNiSQ_Es	9	1	momo	C-8Q5GDL	f	1500.00	XOF	1	
9	2020-09-13 21:26:55.53932+01	2021-03-22 00:01:45.154039+01	British Indian Ocean Territory	Cotonou	Ciné concorde	9qgVXsn9c8Y	13	1	card	C-VYZ8GC	f	1000.00	XOF	1	
25	2020-09-18 21:07:53.951612+01	2021-03-22 00:01:45.156992+01	Benin	Cotonou	Aibatin	zrjUOZdhXws	37	15	momo	C-NOWPAC	f	1000.00	XOF	1	
21	2020-09-17 18:58:23.711668+01	2021-03-22 00:01:45.160124+01	Benin	Cotonou	Cotonou	HAkkHG7Q_Ug	30	12	card	C-ODHPZT	t	1000.00	XOF	1	
23	2020-09-18 15:12:23.288477+01	2021-03-22 00:01:45.163916+01	France	Newyork	Paris	MWqKqUbUv6k	32	13	momo	C-7LAGJI	f	22000.00	XOF	2	
24	2020-09-18 16:15:00.539215+01	2021-03-22 00:01:45.167195+01	Benin	Parakou	Agla	820hMHfoE7o	36	14	card	C-5FHHIF	f	2500.00	XOF	1	
26	2020-09-19 11:40:31.873527+01	2021-03-22 00:01:45.170095+01	France	Paris	12 rue des Pyrénées	Nx0ns0Hp1YA	39	16	momo	C-DT5UAB	f	6000.00	XOF	2	
29	2020-09-24 11:05:54.21065+01	2021-03-22 00:01:45.173014+01	France	Paris	Fhjui	Mz70d-DUnmQ	48	19	card	C-PQU3TM	f	18000.00	XOF	2	
28	2020-09-22 16:47:55.409185+01	2021-03-22 00:01:45.177416+01	Benin	Cotounou	Fifadji	SzDD1Lmcbg4	46	18	momo	C-7TEMHR	f	2500.00	XOF	1	
31	2020-10-06 15:49:48.087535+01	2021-03-22 00:01:45.181271+01	Algeria	Algers	233 Rue de la Voisine	t23X8MzgtPA	54	21	card	C-JZ7WS5	f	22000.00	XOF	2	
32	2020-10-08 17:29:52.314943+01	2021-03-22 00:01:45.184209+01	Benin	Godomey	C/SB Maison Antoine ASSOGBA Quartier Godomey Salamey Cotonou	t0wUjlD02po	57	22	momo	C-GAIOWZ	f	2500.00	XOF	1	
33	2020-10-13 08:23:22.722944+01	2021-03-22 00:01:45.187494+01	Benin	Cotonou	Fidjrossè	wqUop-FWHqc	60	23	momo	C-OH5CXL	f	1000.00	XOF	1	
34	2020-10-13 11:11:06.456237+01	2021-03-22 00:01:45.190712+01	Benin	Cotonou	Cjkc	qk2OblIV2No	62	24	card	C-ADD7WH	f	1000.00	XOF	1	
35	2020-12-02 10:11:08.563754+01	2021-03-22 00:01:45.193707+01	Benin	Cotonou	Arconville	4Ib7vFV4Has	69	2	card	C-TFU3YG	f	1000.00	XOF	1	
36	2020-12-02 18:18:31.179477+01	2021-03-22 00:01:45.196907+01	Benin	Cotonou	Calavi 50 villa	CX5fFKtkFg0	70	25	card	C-HGCMAI	t	1000.00	XOF	1	
79	2021-02-10 15:29:25.175173+01	2021-03-22 00:01:45.199884+01	AO	CLAYMONT	2803 Philadelphia Pike	Q-EEwdA3D0g	73	1	card	C-ORSPVI	t	34600.00	XOF	2	
77	2021-02-10 13:36:49.84938+01	2021-03-22 00:01:45.202703+01	AO	CLAYMONT	2803 Philadelphia Pike	S7eOXUNukKk	73	1	card	C-JGAUGN	t	34600.00	XOF	2	
80	2021-02-10 15:38:19.189874+01	2021-03-22 00:01:45.205618+01	AO	CLAYMONT	2803 Philadelphia Pike	n7BcoPI1DNI	77	1	card	C-DW2Q8Z	t	22000.00	XOF	2	
81	2021-02-10 15:42:50.563463+01	2021-03-22 00:01:45.208614+01	US	CLAYMONT	2803 Philadelphia Pike	7zEF80os2Z4	78	1	card	C-IJQBQ4	t	22000.00	XOF	2	
82	2021-02-10 15:46:24.03226+01	2021-03-22 00:01:45.212036+01	US	CLAYMONT	2803 Philadelphia Pike	y77hYrTEE8M	79	1	card	C-BYFRVZ	t	22000.00	XOF	2	
118	2021-02-12 20:13:02.047112+01	2021-03-22 00:01:45.218025+01	BJ	Cotonou	Test	OPfiI87QyeA	86	26	card	C-PWHZOG	f	1000.00	XOF	1	
93	2021-02-10 16:16:18.639649+01	2021-03-22 00:01:45.220985+01	US	CLAYMONT	2803 Philadelphia Pike	C0CHzhleUJ4	80	1	card	C-TJLWND	t	22000.00	XOF	2	
94	2021-02-10 16:16:53.755005+01	2021-03-22 00:01:45.224496+01	US	CLAYMONT	2803 Philadelphia Pike	M6ogvkK64HI	81	1	card	C-2M76WK	f	22000.00	XOF	2	
113	2021-02-12 20:04:04.418091+01	2021-03-22 00:01:45.227643+01	BJ	Cotonou	Test	RHeirGoccv0	86	26	card	C-XH9PZI	f	1000.00	XOF	1	
97	2021-02-10 16:20:55.48989+01	2021-03-22 00:01:45.230647+01	BJ	Cotonou	Akpakpa	hJcSNoCaQjU	75	21	card	C-76GRG1	t	1000.00	XOF	1	
98	2021-02-10 16:35:51.491356+01	2021-03-22 00:01:45.23401+01	BJ	Cotonou	Akpakpa	muLSLeXpYWU	82	21	card	C-NG2HGG	t	1000.00	XOF	1	
114	2021-02-12 20:08:18.192273+01	2021-03-22 00:01:45.236944+01	BJ	Cotonou	Test	nf71p7HgpXM	86	26	card	C-JXGNMI	f	1000.00	XOF	1	
99	2021-02-10 16:37:31.901494+01	2021-03-22 00:01:45.239956+01	BJ	Cotonou	Akpakpa	zYOzXVyCEJw	83	21	card	C-EXIQF1	t	1000.00	XOF	1	
102	2021-02-10 18:01:22.436123+01	2021-03-22 00:01:45.242843+01	BJ	Cotonou	Akpakpa	hVvGPLu5X4I	84	21	card	C-FM0UDM	t	1000.00	XOF	1	
115	2021-02-12 20:08:50.338405+01	2021-03-22 00:01:45.245848+01	BJ	Cotonou	Test	beHlb0R-2Dw	86	26	card	C-TLGKPG	f	1000.00	XOF	1	
116	2021-02-12 20:09:38.486279+01	2021-03-22 00:01:45.248826+01	BJ	Cotonou	Test	973HRigfD-I	86	26	card	C-3YGH4S	f	1000.00	XOF	1	
120	2021-02-12 21:33:59.07306+01	2021-03-22 00:01:45.252325+01	BJ	Cotonou	Test	BoHEYkIC39k	86	26	card	C-YZ5PWI	t	1000.00	XOF	1	
117	2021-02-12 20:10:30.16+01	2021-03-22 00:01:45.255404+01	BJ	Cotonou	Test	68q7CiAi_Tw	86	26	card	C-PMSPVP	f	1000.00	XOF	1	
119	2021-02-12 20:15:27.46357+01	2021-03-22 00:01:45.258624+01	BJ	Cotonou	Test	z3NxCpvrzYU	86	26	card	C-AMXKEO	t	1000.00	XOF	1	
121	2021-02-12 21:45:24.734728+01	2021-03-22 00:01:45.261684+01	BJ	Cotonou	Test	u-8ZshOkVZ0	86	26	card	C-DAMZ59	t	1000.00	XOF	1	
122	2021-02-12 22:24:01.480653+01	2021-03-22 00:01:45.265033+01	BJ	Cotonou	Test	_Q5InRdG7WM	87	26	card	C-PVDDY3	f	1000.00	XOF	1	
123	2021-02-12 22:24:49.593847+01	2021-03-22 00:01:45.268066+01	BJ	Cotonou	Test	caribRYgqeQ	87	26	card	C-HUO7KG	f	1000.00	XOF	1	
125	2021-02-12 22:34:27.336334+01	2021-03-22 00:01:45.270972+01	BJ	Cotonou	Test	mueb-z6nN1c	87	26	card	C-BLITXP	f	1000.00	XOF	1	
136	2021-02-22 18:01:48.592816+01	2021-03-22 00:01:45.273866+01	AO	Test	Test	Z9_losukngQ	89	27	card	C-0IXFMJ	f	43.21	EUR	2	
126	2021-02-12 22:35:08.164381+01	2021-03-22 00:01:45.276859+01	BJ	Cotonou	Test	3fb1Fz89qsk	87	26	momo	C-1QXWSW	f	1000.00	XOF	1	
127	2021-02-12 22:39:35.611167+01	2021-03-22 00:01:45.280555+01	BJ	Cotonou	Test	1bL1WqsbvfY	87	26	momo	C-NYEL7D	f	1000.00	XOF	1	
128	2021-02-12 22:41:41.619443+01	2021-03-22 00:01:45.283466+01	BJ	Cotonou	Test	EdSf61TaYOI	87	26	momo	C-9W4YLY	f	1000.00	XOF	1	
137	2021-02-22 18:05:38.739246+01	2021-03-22 00:01:45.286441+01	AO	Test	Test	KCwpZrXkGbU	89	27	card	C-1CALJR	f	43.21	EUR	2	
129	2021-02-12 22:43:39.988035+01	2021-03-22 00:01:45.289414+01	BJ	Cotonou	Test	ngm2LgA-eD4	87	26	momo	C-7AFKYY	f	1000.00	XOF	1	
130	2021-02-12 22:51:51.738325+01	2021-03-22 00:01:45.292704+01	BJ	Cotonou	Test	6D7y55SeAGA	87	26	momo	C-HRDETE	t	1000.00	XOF	1	
138	2021-02-22 18:11:45.636714+01	2021-03-22 00:01:45.295676+01	AO	Test	Test	RynIaOGfumc	89	27	card	C-N7IMDF	f	43.21	EUR	2	
131	2021-02-12 23:10:55.846028+01	2021-03-22 00:01:45.298746+01	BJ	Cotonou	Test	1MDCMmueSOU	88	26	cash	C-FJKDMH	f	1000.00	XOF	1	
132	2021-02-12 23:16:27.27661+01	2021-03-22 00:01:45.301615+01	BJ	Cotonou	Test	wrs3Iv0Evaw	88	26	cash	C-XPQOCG	t	1000.00	XOF	1	
139	2021-03-05 19:01:00.510359+01	2021-03-22 00:01:45.305007+01	AO	Test	Test	XCqCs8soSXo	89	27	card	C-IV60UH	f	43.21	NGN	2	
134	2021-02-22 17:59:20.844665+01	2021-03-22 00:01:45.308024+01	AO	Test	Test	-_No1JIaQN0	89	27	card	C-7GK8NE	f	28300.00	XOF	2	
140	2021-03-05 19:57:58.951658+01	2021-03-22 00:01:45.310887+01	AO	Test	Test	tl5REQnrz8E	89	27	card	C-D3ZTKT	f	43.21	NGN	2	
147	2021-03-24 06:52:34.904193+01	2021-03-24 06:52:34.904238+01	AO	Test	Test	Ov9eWEa1PDk	89	27	card	C-YACSMC	f	\N	XOF	\N	
154	2021-03-24 07:38:28.424859+01	2021-03-24 07:38:28.424886+01	AO	Test	Test	oZNVNAac944	89	27	card	C-FNQSG1	f	\N	XOF	\N	
161	2021-03-27 13:30:14.088786+01	2021-03-27 13:30:14.088934+01	AO	Test	Test	JQ_5f2XnQEA	95	27	card	C-HP2HNZ	f	\N	XOF	\N	Calavi
\.


--
-- Data for Name: core_bankaccount; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_bankaccount (id, created_at, updated_at, external_id, account_bank, account_number, rave_subaccount_id, service, shop_id) FROM stdin;
1	2021-03-05 17:03:39.431391+01	2021-03-24 08:06:13.03004+01	9080	mtn-momo	97000001	RS_08E7F23025C82416702F176780B23AD6	rave	23
\.


--
-- Data for Name: core_billingplan; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_billingplan (id, created_at, updated_at, plan_name, status, user_id, rc_app_user_id) FROM stdin;
1	2021-03-10 20:40:10.011817+01	2021-03-10 20:40:10.012126+01	free	active	84	
2	2021-03-10 20:40:10.025233+01	2021-03-10 20:40:10.025267+01	free	active	87	
3	2021-03-10 20:40:10.027264+01	2021-03-10 20:40:10.027301+01	free	active	90	
4	2021-03-10 20:40:10.029324+01	2021-03-10 20:40:10.029366+01	free	active	92	
5	2021-03-10 20:40:10.031206+01	2021-03-10 20:40:10.031242+01	free	active	94	
6	2021-03-10 20:40:10.033127+01	2021-03-10 20:40:10.03318+01	free	active	1	
7	2021-03-10 20:40:10.034932+01	2021-03-10 20:40:10.035013+01	free	active	3	
8	2021-03-10 20:40:10.036695+01	2021-03-10 20:40:10.036745+01	free	active	4	
9	2021-03-10 20:40:10.03817+01	2021-03-10 20:40:10.038224+01	free	active	5	
10	2021-03-10 20:40:10.040585+01	2021-03-10 20:40:10.04062+01	free	active	6	
11	2021-03-10 20:40:10.042226+01	2021-03-10 20:40:10.042258+01	free	active	7	
12	2021-03-10 20:40:10.043662+01	2021-03-10 20:40:10.043688+01	free	active	8	
13	2021-03-10 20:40:10.045421+01	2021-03-10 20:40:10.045459+01	free	active	9	
14	2021-03-10 20:40:10.048276+01	2021-03-10 20:40:10.04837+01	free	active	10	
15	2021-03-10 20:40:10.050062+01	2021-03-10 20:40:10.050093+01	free	active	11	
16	2021-03-10 20:40:10.051713+01	2021-03-10 20:40:10.051807+01	free	active	12	
17	2021-03-10 20:40:10.053434+01	2021-03-10 20:40:10.053468+01	free	active	13	
18	2021-03-10 20:40:10.055134+01	2021-03-10 20:40:10.055267+01	free	active	14	
19	2021-03-10 20:40:10.057135+01	2021-03-10 20:40:10.057175+01	free	active	15	
20	2021-03-10 20:40:10.059037+01	2021-03-10 20:40:10.059075+01	free	active	16	
21	2021-03-10 20:40:10.060644+01	2021-03-10 20:40:10.060728+01	free	active	17	
22	2021-03-10 20:40:10.062663+01	2021-03-10 20:40:10.062732+01	free	active	18	
23	2021-03-10 20:40:10.064436+01	2021-03-10 20:40:10.064472+01	free	active	19	
24	2021-03-10 20:40:10.066532+01	2021-03-10 20:40:10.066573+01	free	active	20	
25	2021-03-10 20:40:10.068176+01	2021-03-10 20:40:10.068207+01	free	active	21	
26	2021-03-10 20:40:10.069572+01	2021-03-10 20:40:10.069604+01	free	active	22	
27	2021-03-10 20:40:10.071474+01	2021-03-10 20:40:10.071553+01	free	active	23	
28	2021-03-10 20:40:10.0731+01	2021-03-10 20:40:10.073127+01	free	active	24	
29	2021-03-10 20:40:10.074042+01	2021-03-10 20:40:10.074065+01	free	active	25	
30	2021-03-10 20:40:10.074985+01	2021-03-10 20:40:10.075008+01	free	active	26	
31	2021-03-10 20:40:10.075888+01	2021-03-10 20:40:10.07591+01	free	active	27	
32	2021-03-10 20:40:10.076749+01	2021-03-10 20:40:10.07677+01	free	active	28	
33	2021-03-10 20:40:10.07766+01	2021-03-10 20:40:10.077682+01	free	active	29	
34	2021-03-10 20:40:10.078647+01	2021-03-10 20:40:10.078672+01	free	active	30	
35	2021-03-10 20:40:10.080903+01	2021-03-10 20:40:10.080937+01	free	active	95	
36	2021-03-10 20:40:10.081991+01	2021-03-10 20:40:10.082015+01	free	active	31	
37	2021-03-10 20:40:10.082887+01	2021-03-10 20:40:10.082908+01	free	active	85	
38	2021-03-10 20:40:10.083762+01	2021-03-10 20:40:10.083784+01	free	active	88	
39	2021-03-10 20:40:10.084621+01	2021-03-10 20:40:10.084642+01	free	active	32	
40	2021-03-10 20:40:10.085521+01	2021-03-10 20:40:10.085543+01	free	active	33	
41	2021-03-10 20:40:10.086432+01	2021-03-10 20:40:10.086454+01	free	active	34	
42	2021-03-10 20:40:10.087293+01	2021-03-10 20:40:10.087314+01	free	active	35	
43	2021-03-10 20:40:10.08814+01	2021-03-10 20:40:10.08816+01	free	active	36	
44	2021-03-10 20:40:10.088983+01	2021-03-10 20:40:10.089004+01	free	active	37	
45	2021-03-10 20:40:10.08986+01	2021-03-10 20:40:10.089881+01	free	active	38	
46	2021-03-10 20:40:10.090742+01	2021-03-10 20:40:10.090763+01	free	active	42	
47	2021-03-10 20:40:10.091648+01	2021-03-10 20:40:10.09167+01	free	active	43	
48	2021-03-10 20:40:10.092562+01	2021-03-10 20:40:10.092583+01	free	active	44	
49	2021-03-10 20:40:10.093419+01	2021-03-10 20:40:10.093441+01	free	active	45	
50	2021-03-10 20:40:10.094374+01	2021-03-10 20:40:10.094398+01	free	active	48	
51	2021-03-10 20:40:10.095534+01	2021-03-10 20:40:10.095562+01	free	active	49	
52	2021-03-10 20:40:10.096508+01	2021-03-10 20:40:10.096531+01	free	active	50	
53	2021-03-10 20:40:10.097431+01	2021-03-10 20:40:10.097454+01	free	active	83	
54	2021-03-10 20:40:10.09838+01	2021-03-10 20:40:10.098402+01	free	active	40	
55	2021-03-10 20:40:10.099269+01	2021-03-10 20:40:10.099291+01	free	active	41	
56	2021-03-10 20:40:10.100125+01	2021-03-10 20:40:10.100145+01	free	active	51	
57	2021-03-10 20:40:10.100966+01	2021-03-10 20:40:10.100987+01	free	active	52	
58	2021-03-10 20:40:10.101798+01	2021-03-10 20:40:10.101819+01	free	active	53	
59	2021-03-10 20:40:10.102688+01	2021-03-10 20:40:10.10271+01	free	active	54	
60	2021-03-10 20:40:10.103704+01	2021-03-10 20:40:10.103727+01	free	active	55	
61	2021-03-10 20:40:10.1046+01	2021-03-10 20:40:10.104622+01	free	active	56	
62	2021-03-10 20:40:10.105462+01	2021-03-10 20:40:10.105484+01	free	active	46	
63	2021-03-10 20:40:10.106345+01	2021-03-10 20:40:10.106367+01	free	active	57	
64	2021-03-10 20:40:10.107234+01	2021-03-10 20:40:10.107256+01	free	active	58	
65	2021-03-10 20:40:10.108092+01	2021-03-10 20:40:10.108113+01	free	active	59	
66	2021-03-10 20:40:10.109188+01	2021-03-10 20:40:10.109215+01	free	active	60	
67	2021-03-10 20:40:10.110161+01	2021-03-10 20:40:10.110184+01	free	active	47	
68	2021-03-10 20:40:10.111043+01	2021-03-10 20:40:10.111064+01	free	active	61	
69	2021-03-10 20:40:10.112003+01	2021-03-10 20:40:10.112029+01	free	active	62	
70	2021-03-10 20:40:10.11298+01	2021-03-10 20:40:10.113004+01	free	active	63	
71	2021-03-10 20:40:10.113866+01	2021-03-10 20:40:10.113888+01	free	active	64	
72	2021-03-10 20:40:10.114891+01	2021-03-10 20:40:10.114914+01	free	active	65	
73	2021-03-10 20:40:10.115783+01	2021-03-10 20:40:10.115805+01	free	active	66	
74	2021-03-10 20:40:10.116636+01	2021-03-10 20:40:10.116656+01	free	active	67	
75	2021-03-10 20:40:10.117479+01	2021-03-10 20:40:10.1175+01	free	active	68	
76	2021-03-10 20:40:10.118356+01	2021-03-10 20:40:10.118378+01	free	active	69	
77	2021-03-10 20:40:10.119217+01	2021-03-10 20:40:10.119238+01	free	active	70	
78	2021-03-10 20:40:10.120117+01	2021-03-10 20:40:10.120138+01	free	active	71	
79	2021-03-10 20:40:10.120995+01	2021-03-10 20:40:10.121016+01	free	active	72	
80	2021-03-10 20:40:10.121875+01	2021-03-10 20:40:10.121897+01	free	active	73	
81	2021-03-10 20:40:10.122751+01	2021-03-10 20:40:10.122773+01	free	active	74	
82	2021-03-10 20:40:10.123597+01	2021-03-10 20:40:10.123618+01	free	active	86	
83	2021-03-10 20:40:10.12455+01	2021-03-10 20:40:10.124572+01	free	active	89	
84	2021-03-10 20:40:10.125417+01	2021-03-10 20:40:10.125438+01	free	active	91	
85	2021-03-10 20:40:10.126323+01	2021-03-10 20:40:10.126344+01	free	active	93	
86	2021-03-10 20:40:10.127243+01	2021-03-10 20:40:10.127267+01	free	active	96	
\.


--
-- Data for Name: core_shippingmethod; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_shippingmethod (id, created_at, updated_at, name, description, price_currency, price, zone_id) FROM stdin;
1	2021-03-21 22:39:51.952531+01	2021-03-21 22:39:51.95256+01	Standard	1-2 jours	XOF	1000.00	1
2	2021-03-21 22:39:51.954877+01	2021-03-21 22:39:51.954912+01	Standard	1-2 jours	XOF	1500.00	2
3	2021-03-21 22:39:51.956505+01	2021-03-21 22:39:51.95655+01	Standard	2-3 jours	XOF	2000.00	3
\.


--
-- Data for Name: core_shippingprofile; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_shippingprofile (id, created_at, updated_at, name, avatar_url, backend, profile_type) FROM stdin;
1	2021-03-21 22:39:51.941707+01	2021-03-21 22:39:51.941743+01	Futurix Logistics	https://kweek-api.s3.amazonaws.com/futurix-logo.png		manual
2	2021-03-21 22:39:51.958398+01	2021-03-21 22:39:51.958446+01	DHL Express	https://kweek-api.s3.amazonaws.com/dhl.png	core.backends.shipping.DHLExpressBackend	auto
\.


--
-- Data for Name: core_shippingprofile_shops; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_shippingprofile_shops (id, shippingprofile_id, shop_id) FROM stdin;
1	1	45
2	2	45
3	1	28
4	2	28
5	1	48
6	2	48
7	1	49
8	2	49
9	1	59
10	2	59
11	1	41
12	2	41
13	1	60
14	2	60
15	1	26
16	2	26
17	1	33
18	2	33
19	1	35
20	2	35
21	1	32
22	2	32
23	1	40
24	2	40
25	1	43
26	2	43
27	1	46
28	2	46
29	1	58
30	2	58
31	1	52
32	2	52
33	1	55
34	2	55
35	1	44
36	2	44
37	1	47
38	2	47
39	1	53
40	2	53
41	1	50
42	2	50
43	1	61
44	2	61
45	1	29
46	2	29
47	1	23
48	2	23
49	1	25
50	2	25
51	1	27
52	2	27
53	1	30
54	2	30
55	1	31
56	2	31
57	1	34
58	2	34
59	1	36
60	2	36
61	1	37
62	2	37
63	1	42
64	2	42
65	1	38
66	2	38
67	1	51
68	2	51
69	1	54
70	2	54
71	1	57
72	2	57
73	1	39
74	2	39
75	1	56
76	2	56
\.


--
-- Data for Name: core_shippingzone; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_shippingzone (id, created_at, updated_at, name, profile_id) FROM stdin;
1	2021-03-21 22:39:51.948551+01	2021-03-21 22:39:51.948582+01	Cotonou	1
2	2021-03-21 22:39:51.950352+01	2021-03-21 22:39:51.950377+01	Calavi	1
3	2021-03-21 22:39:51.951292+01	2021-03-21 22:39:51.951313+01	Porto-Novo	1
\.


--
-- Data for Name: core_shopdesign; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.core_shopdesign (id, created_at, updated_at, tagline, hero_cta, instagram_link, facebook_link, language, shop_id, whatsapp_link, theme, color) FROM stdin;
1	2021-03-11 20:14:24.579183+01	2021-03-11 20:14:24.579217+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	45		storefront	black
2	2021-03-11 20:14:24.589137+01	2021-03-11 20:14:24.589183+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	28		storefront	black
3	2021-03-11 20:14:24.59086+01	2021-03-11 20:14:24.590902+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	48		storefront	black
4	2021-03-11 20:14:24.592623+01	2021-03-11 20:14:24.592668+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	49		storefront	black
5	2021-03-11 20:14:24.595619+01	2021-03-11 20:14:24.595696+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	59		storefront	black
6	2021-03-11 20:14:24.597538+01	2021-03-11 20:14:24.597612+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	41		storefront	black
7	2021-03-11 20:14:24.599321+01	2021-03-11 20:14:24.599361+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	60		storefront	black
8	2021-03-11 20:14:24.600924+01	2021-03-11 20:14:24.600995+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	26		storefront	black
9	2021-03-11 20:14:24.603121+01	2021-03-11 20:14:24.603163+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	33		storefront	black
10	2021-03-11 20:14:24.60491+01	2021-03-11 20:14:24.605001+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	35		storefront	black
11	2021-03-11 20:14:24.606756+01	2021-03-11 20:14:24.606792+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	32		storefront	black
12	2021-03-11 20:14:24.608321+01	2021-03-11 20:14:24.608383+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	40		storefront	black
13	2021-03-11 20:14:24.609956+01	2021-03-11 20:14:24.610136+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	43		storefront	black
14	2021-03-11 20:14:24.612753+01	2021-03-11 20:14:24.612797+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	46		storefront	black
15	2021-03-11 20:14:24.615709+01	2021-03-11 20:14:24.615903+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	58		storefront	black
16	2021-03-11 20:14:24.61855+01	2021-03-11 20:14:24.618653+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	52		storefront	black
17	2021-03-11 20:14:24.620777+01	2021-03-11 20:14:24.620818+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	55		storefront	black
18	2021-03-11 20:14:24.622341+01	2021-03-11 20:14:24.622384+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	44		storefront	black
19	2021-03-11 20:14:24.624201+01	2021-03-11 20:14:24.624283+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	47		storefront	black
20	2021-03-11 20:14:24.626263+01	2021-03-11 20:14:24.626337+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	53		storefront	black
21	2021-03-11 20:14:24.628161+01	2021-03-11 20:14:24.628203+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	50		storefront	black
22	2021-03-11 20:14:24.629803+01	2021-03-11 20:14:24.629846+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	61		storefront	black
23	2021-03-11 20:14:24.631942+01	2021-03-11 20:14:24.631991+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	29		storefront	black
24	2021-03-11 20:14:24.634334+01	2021-03-11 20:14:24.634427+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	23		storefront	black
26	2021-03-11 20:14:24.637804+01	2021-03-11 20:14:24.637858+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	27		storefront	black
27	2021-03-11 20:14:24.640635+01	2021-03-11 20:14:24.640678+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	30		storefront	black
28	2021-03-11 20:14:24.642106+01	2021-03-11 20:14:24.642146+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	31		storefront	black
29	2021-03-11 20:14:24.643524+01	2021-03-11 20:14:24.643561+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	34		storefront	black
30	2021-03-11 20:14:24.645123+01	2021-03-11 20:14:24.645151+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	36		storefront	black
31	2021-03-11 20:14:24.646576+01	2021-03-11 20:14:24.646623+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	37		storefront	black
32	2021-03-11 20:14:24.649094+01	2021-03-11 20:14:24.649327+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	42		storefront	black
33	2021-03-11 20:14:24.651578+01	2021-03-11 20:14:24.651622+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	38		storefront	black
34	2021-03-11 20:14:24.653464+01	2021-03-11 20:14:24.653508+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	51		storefront	black
35	2021-03-11 20:14:24.655164+01	2021-03-11 20:14:24.655212+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	54		storefront	black
36	2021-03-11 20:14:24.656838+01	2021-03-11 20:14:24.656943+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	57		storefront	black
37	2021-03-11 20:14:24.658611+01	2021-03-11 20:14:24.658652+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	39		storefront	black
38	2021-03-11 20:14:24.660434+01	2021-03-11 20:14:24.660477+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	56		storefront	black
25	2021-03-11 20:14:24.636162+01	2021-03-11 20:14:24.636202+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	25		food	black
39	2021-03-24 14:43:40.598176+01	2021-03-24 14:43:40.598204+01	Découvrez nos meilleurs produits et collections	Shoppez maintenant			fr	62		storefront	black
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.customers (id, created_at, updated_at, name, email, phone_number, user_id) FROM stdin;
1	2020-09-03 11:28:08.195739+01	2020-09-03 11:35:47.261732+01	Kamga	kamganelson@gmail.com	\N	\N
2	2020-09-03 18:15:36.533824+01	2020-09-03 18:15:36.533824+01	BATCHO Harold	\N	62606333	\N
3	2020-09-14 13:14:17.800593+01	2020-09-14 13:14:17.800623+01	Nelson	\N	+22998801811	\N
4	2020-09-14 21:46:29.319627+01	2020-09-14 21:46:29.319656+01	Gg	\N	5677888888	\N
5	2020-09-14 22:19:29.600794+01	2020-09-14 22:19:29.600828+01	Arielle	\N	909990999	\N
6	2020-09-15 07:21:24.074078+01	2020-09-15 07:21:24.074109+01	Gggg	333@5555.com	\N	\N
7	2020-09-15 09:37:58.751752+01	2020-09-15 09:37:58.751781+01	Elsie	\N	65321750	\N
8	2020-09-15 10:24:32.698327+01	2020-09-15 10:24:32.69836+01	Mangabo	onaelmangabo@gmail.com	\N	\N
9	2020-09-16 19:05:07.345589+01	2020-09-16 19:05:07.345618+01	Test	\N	98801811	\N
10	2020-09-16 19:24:02.58635+01	2020-09-16 19:24:02.586378+01	N	\N	9	\N
11	2020-09-17 14:07:58.389289+01	2020-09-17 14:07:58.389317+01	He	\N	96218062	\N
12	2020-09-17 18:58:23.705523+01	2020-09-17 18:58:23.705553+01	Houessou Langevin Memoris	langevinhouessou9@gmail.com	\N	\N
13	2020-09-18 15:12:23.283727+01	2020-09-18 15:12:23.283756+01	Domingo	\N	69136944	\N
14	2020-09-18 16:15:00.533403+01	2020-09-18 16:15:00.533432+01	Hounsinou victor	\N	97182615	\N
15	2020-09-18 21:07:53.946189+01	2020-09-18 21:07:53.94622+01	Harold	\N	+22962606333	\N
16	2020-09-19 11:40:31.868761+01	2020-09-19 11:40:31.86879+01	Franck Reinbolit	Franckreinbolit@gmail.com	\N	\N
17	2020-09-22 12:13:59.48908+01	2020-09-22 12:13:59.489109+01	Octave	octaviog107@gmail.com	\N	\N
18	2020-09-22 16:47:55.40448+01	2020-09-22 16:47:55.404511+01	Wallys	\N	97819176	\N
19	2020-09-24 11:05:54.205395+01	2020-09-24 11:05:54.205425+01	Thh	\N	3366	\N
20	2020-09-26 04:18:19.311659+01	2020-09-26 04:18:19.311689+01	Adjahouisso Dieudonné	\N	96463019	\N
21	2020-10-06 15:49:48.082716+01	2020-10-06 15:49:48.082745+01	Nelson	\N	90909090	\N
22	2020-10-08 17:29:52.310103+01	2020-10-08 17:29:52.310131+01	Hier	agbalohoundele@gmail.com	\N	\N
23	2020-10-13 08:23:22.717344+01	2020-10-13 08:23:22.717372+01	Kayossi	\N	67146432	\N
24	2020-10-13 11:11:06.450681+01	2020-10-13 11:11:06.450709+01	Lb	ilsonrich@icloud.com	\N	\N
25	2020-12-02 18:18:31.173271+01	2020-12-02 18:18:31.173301+01	Hilarion	Lisalinep7@gmail.com	\N	\N
26	2021-02-12 19:16:31.419107+01	2021-02-12 19:16:31.419163+01	Nelson	\N	Kamga	\N
27	2021-02-22 17:58:15.955449+01	2021-02-22 17:58:15.955504+01	Nelson	\N	4567899999	\N
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	core	banner
7	core	cart
8	core	category
9	core	customer
10	core	product
11	core	user
12	core	shop
13	core	productimage
14	core	checkout
15	core	cartitem
16	core	order
17	core	orderitem
18	core	affiliateagent
19	phone_verify	smsverification
20	core	bankaccount
21	core	billingplan
22	core	shopdesign
23	exchange	exchangebackend
24	exchange	rate
25	core	shippingprofile
26	core	shippingzone
27	core	shippingmethod
29	kash	transaction
28	kash	checkoutsession
31	kash	virtualcard
30	kash	userprofile
34	kash	notification
35	kash	kashrequest
36	kash	kashrequestresponse
37	kash	fundinghistory
38	kash	invitecode
39	kash	withdrawalhistory
32	kash	sendkash
40	kash	kashtransaction
33	kash	momoaccount
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	core	0001_initial	2021-01-07 11:39:08.766641+01
2	contenttypes	0001_initial	2021-01-07 11:39:09.147382+01
3	admin	0001_initial	2021-01-07 11:39:09.19151+01
4	admin	0002_logentry_remove_auto_add	2021-01-07 11:39:09.213402+01
5	admin	0003_logentry_add_action_flag_choices	2021-01-07 11:39:09.232841+01
6	contenttypes	0002_remove_content_type_name	2021-01-07 11:39:09.297477+01
7	auth	0001_initial	2021-01-07 11:39:09.394477+01
8	auth	0002_alter_permission_name_max_length	2021-01-07 11:39:09.46271+01
9	auth	0003_alter_user_email_max_length	2021-01-07 11:39:09.482478+01
10	auth	0004_alter_user_username_opts	2021-01-07 11:39:09.496683+01
11	auth	0005_alter_user_last_login_null	2021-01-07 11:39:09.526144+01
12	auth	0006_require_contenttypes_0002	2021-01-07 11:39:09.535639+01
13	auth	0007_alter_validators_add_error_messages	2021-01-07 11:39:09.559375+01
14	auth	0008_alter_user_username_max_length	2021-01-07 11:39:09.583783+01
15	auth	0009_alter_user_last_name_max_length	2021-01-07 11:39:09.599241+01
16	auth	0010_alter_group_name_max_length	2021-01-07 11:39:09.645698+01
17	auth	0011_update_proxy_permissions	2021-01-07 11:39:09.688255+01
18	auth	0012_alter_user_first_name_max_length	2021-01-07 11:39:09.766901+01
19	core	0002_auto_20200909_0010	2021-01-07 11:39:10.003467+01
20	core	0003_auto_20200909_0011	2021-01-07 11:39:10.068068+01
21	core	0004_auto_20200909_0014	2021-01-07 11:39:10.111362+01
22	core	0005_auto_20200909_1827	2021-01-07 11:39:10.382894+01
23	core	0006_auto_20200911_2156	2021-01-07 11:39:10.470788+01
24	core	0007_auto_20200911_2216	2021-01-07 11:39:10.50467+01
25	core	0008_auto_20200912_1157	2021-01-07 11:39:10.542128+01
26	core	0009_checkout_payment_method	2021-01-07 11:39:10.557393+01
27	core	0010_auto_20200913_1834	2021-01-07 11:39:10.678573+01
28	core	0011_auto_20200913_1835	2021-01-07 11:39:10.812515+01
29	core	0012_auto_20200913_1849	2021-01-07 11:39:10.897411+01
30	core	0013_auto_20200913_1933	2021-01-07 11:39:10.923111+01
31	core	0014_shop_cover_url	2021-01-07 11:39:10.954604+01
32	core	0015_auto_20200916_1254	2021-01-07 11:39:11.092277+01
33	core	0016_auto_20200916_1402	2021-01-07 11:39:11.198534+01
34	core	0017_auto_20200916_1534	2021-01-07 11:39:11.246199+01
35	phone_verify	0001_initial	2021-01-07 11:39:11.270328+01
36	phone_verify	0002_auto_20190817_1753	2021-01-07 11:39:11.305538+01
37	sessions	0001_initial	2021-01-07 11:39:11.322726+01
38	core	0018_shop_domains	2021-01-07 12:10:35.259588+01
39	core	0019_auto_20210107_1104	2021-01-07 12:10:35.478541+01
40	core	0020_auto_20210212_1345	2021-02-12 14:48:24.485022+01
41	core	0021_auto_20210212_1351	2021-02-12 14:52:32.530406+01
42	core	0022_auto_20210212_2044	2021-02-12 21:45:04.596722+01
43	core	0023_auto_20210217_0040	2021-02-17 01:41:03.534881+01
44	core	0024_auto_20210222_1652	2021-02-22 17:54:45.504771+01
45	core	0025_bankaccount	2021-03-05 16:18:46.071114+01
46	core	0026_remove_bankaccount_country	2021-03-05 16:54:51.269484+01
47	core	0027_shop_email	2021-03-05 17:26:58.519724+01
48	core	0028_cart_shop	2021-03-05 18:24:01.707721+01
49	core	0029_auto_20210305_1721	2021-03-05 18:24:02.239166+01
50	core	0030_billingplan	2021-03-10 20:37:18.558256+01
51	core	0031_auto_20210310_1938	2021-03-10 20:40:10.129622+01
52	core	0032_auto_20210310_1949	2021-03-10 20:49:29.328115+01
53	core	0033_billingplan_rc_app_user_id	2021-03-10 21:07:07.140588+01
54	core	0030_shopdesign	2021-03-11 20:13:16.164192+01
55	core	0031_auto_20210311_1909	2021-03-11 20:14:24.664733+01
56	core	0032_shopdesign_whatsapp_link	2021-03-18 14:01:38.80326+01
57	core	0033_auto_20210321_1749	2021-03-21 18:49:50.787303+01
58	core	0034_auto_20210321_1749	2021-03-21 18:51:29.850402+01
59	core	0035_auto_20210321_1801	2021-03-21 19:01:30.584454+01
60	core	0036_auto_20210321_1801	2021-03-21 19:03:37.894893+01
61	core	0037_auto_20210321_1806	2021-03-21 19:08:27.81252+01
62	core	0038_auto_20210321_1807	2021-03-21 19:08:27.932454+01
63	core	0039_auto_20210321_1810	2021-03-21 19:11:25.351567+01
64	exchange	0001_initial	2021-03-21 20:20:43.081425+01
65	core	0040_auto_20210321_1949	2021-03-21 20:51:13.089123+01
66	core	0041_auto_20210321_1950	2021-03-21 20:51:13.283452+01
67	core	0042_auto_20210321_2128	2021-03-21 22:39:51.825709+01
68	core	0043_auto_20210321_2129	2021-03-21 22:39:52.116703+01
69	core	0044_auto_20210321_2255	2021-03-22 00:01:24.45872+01
70	core	0045_auto_20210321_2255	2021-03-22 00:01:45.314525+01
71	core	0046_auto_20210321_2307	2021-03-22 00:08:27.135643+01
72	core	0047_auto_20210321_2307	2021-03-22 00:08:27.32417+01
73	core	0048_auto_20210323_1945	2021-03-23 20:45:32.524919+01
74	core	0049_auto_20210323_1947	2021-03-23 20:47:52.004756+01
75	core	0050_auto_20210323_2020	2021-03-23 21:20:35.162958+01
76	core	0051_auto_20210324_0623	2021-03-24 07:23:20.013126+01
77	core	0052_auto_20210324_0654	2021-03-24 07:54:36.47753+01
78	core	0053_shopdesign_theme	2021-03-24 09:50:46.993934+01
79	core	0054_shopdesign_color	2021-03-26 12:02:08.498599+01
82	kash	0001_initial	2021-04-02 00:18:26.516803+01
83	kash	0002_transaction	2021-04-02 00:18:26.675646+01
84	core	0055_auto_20210402_1036	2021-04-02 11:37:06.74953+01
85	kash	0003_auto_20210402_1036	2021-04-02 11:37:07.039188+01
86	kash	0004_auto_20210402_1204	2021-04-02 13:04:14.277946+01
87	kash	0005_auto_20210402_1537	2021-04-02 16:37:41.477202+01
89	kash	0006_auto_20210403_1420	2021-04-03 15:21:27.290263+01
90	kash	0007_auto_20210403_1425	2021-04-03 15:25:07.240836+01
91	kash	0008_auto_20210403_1508	2021-04-03 16:08:50.054267+01
92	kash	0009_auto_20210404_1234	2021-04-04 13:35:06.544448+01
93	kash	0010_auto_20210404_1240	2021-04-04 16:02:28.555877+01
94	kash	0011_transaction_transaction_type	2021-04-04 16:02:28.636411+01
95	kash	0012_payoutmethod	2021-04-04 16:24:35.848846+01
96	kash	0013_notification	2021-04-04 17:02:30.352347+01
97	kash	0014_kashrequest	2021-04-04 22:41:50.500564+01
98	kash	0015_kashrequestresponse	2021-04-05 10:32:54.521417+01
99	kash	0016_kashtransaction_paid_recipients	2021-04-05 13:20:25.625326+01
100	kash	0017_fundinghistory	2021-04-06 13:10:21.44358+01
101	kash	0018_auto_20210406_1310	2021-04-06 14:10:25.264494+01
102	kash	0019_auto_20210406_1310	2021-04-06 14:10:43.57704+01
103	kash	0020_virtualcard_is_active	2021-04-06 14:23:17.017276+01
104	kash	0021_invitecode	2021-04-06 19:42:36.648835+01
105	kash	0022_auto_20210406_1844	2021-04-06 19:44:27.282998+01
106	kash	0023_auto_20210406_1954	2021-04-06 20:54:37.612837+01
107	kash	0024_userprofile_avatar_url	2021-04-07 01:48:34.020184+01
108	kash	0025_auto_20210407_0155	2021-04-07 02:56:04.218625+01
109	kash	0026_withdrawalhistory	2021-04-07 12:40:44.085313+01
110	kash	0027_fundinghistory_status	2021-04-09 21:15:43.016019+01
111	kash	0028_auto_20210413_1258	2021-04-13 13:58:50.093575+01
113	kash	0029_kashtransaction	2021-04-13 15:54:22.347155+01
116	kash	0030_auto_20210413_1436	2021-04-13 16:13:08.952392+01
117	kash	0031_auto_20210415_1433	2021-04-15 15:33:55.619186+01
118	kash	0032_auto_20210415_1433	2021-04-15 15:33:55.892636+01
119	kash	0033_auto_20210415_2318	2021-04-16 00:42:20.44236+01
120	kash	0034_auto_20210415_2334	2021-04-16 00:42:20.551981+01
121	kash	0035_auto_20210415_2335	2021-04-16 00:42:46.541611+01
122	kash	0036_auto_20210415_2345	2021-04-16 00:46:08.2805+01
123	kash	0037_auto_20210417_1018	2021-04-17 11:22:36.101567+01
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: exchange_exchangebackend; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.exchange_exchangebackend (name, last_update, base_currency) FROM stdin;
openexchangerates.org	2021-04-17 13:00:14.171975+01	USD
\.


--
-- Data for Name: exchange_rate; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.exchange_rate (id, currency, value, backend_id) FROM stdin;
44201	AED	3.673050	openexchangerates.org
44202	AFN	77.599996	openexchangerates.org
44203	ALL	102.754572	openexchangerates.org
44204	AMD	521.493127	openexchangerates.org
44205	ANG	1.796035	openexchangerates.org
44206	AOA	650.911000	openexchangerates.org
44207	ARS	92.777636	openexchangerates.org
44208	AUD	1.292992	openexchangerates.org
44209	AWG	1.800000	openexchangerates.org
44210	AZN	1.700805	openexchangerates.org
44211	BAM	1.632314	openexchangerates.org
44212	BBD	2.000000	openexchangerates.org
44213	BDT	84.793114	openexchangerates.org
44214	BGN	1.632497	openexchangerates.org
44215	BHD	0.377067	openexchangerates.org
44216	BIF	1949.483123	openexchangerates.org
44217	BMD	1.000000	openexchangerates.org
44218	BND	1.333923	openexchangerates.org
44219	BOB	6.909892	openexchangerates.org
44220	BRL	5.588260	openexchangerates.org
44221	BSD	1.000000	openexchangerates.org
44222	BTC	0.000016	openexchangerates.org
44223	BTN	74.293670	openexchangerates.org
44224	BWP	10.828705	openexchangerates.org
44225	BYN	2.598158	openexchangerates.org
44226	BZD	2.016867	openexchangerates.org
44227	CAD	1.250850	openexchangerates.org
44228	CDF	1982.930556	openexchangerates.org
44229	CHF	0.920051	openexchangerates.org
44230	CLF	0.025477	openexchangerates.org
44231	CLP	702.800000	openexchangerates.org
44232	CNH	6.524400	openexchangerates.org
44233	CNY	6.520900	openexchangerates.org
44234	COP	3614.019450	openexchangerates.org
44235	CRC	613.631184	openexchangerates.org
44236	CUC	1.000000	openexchangerates.org
44237	CUP	25.750000	openexchangerates.org
44238	CVE	92.400000	openexchangerates.org
44239	CZK	21.627000	openexchangerates.org
44240	DJF	178.126297	openexchangerates.org
44241	DKK	6.206200	openexchangerates.org
44242	DOP	56.892242	openexchangerates.org
44243	DZD	132.210000	openexchangerates.org
44244	EGP	15.683591	openexchangerates.org
44245	ERN	15.001970	openexchangerates.org
44246	ETB	41.799040	openexchangerates.org
44247	EUR	0.834589	openexchangerates.org
44248	FJD	2.026400	openexchangerates.org
44249	FKP	0.722883	openexchangerates.org
44250	GBP	0.722883	openexchangerates.org
44251	GEL	3.425000	openexchangerates.org
44252	GGP	0.722883	openexchangerates.org
44253	GHS	5.778275	openexchangerates.org
44254	GIP	0.722883	openexchangerates.org
44255	GMD	51.080000	openexchangerates.org
44256	GNF	10011.609503	openexchangerates.org
44257	GTQ	7.721865	openexchangerates.org
44258	GYD	209.331575	openexchangerates.org
44259	HKD	7.771400	openexchangerates.org
44260	HNL	24.057019	openexchangerates.org
44261	HRK	6.317700	openexchangerates.org
44262	HTG	82.888180	openexchangerates.org
44263	HUF	301.620479	openexchangerates.org
44264	IDR	14577.000000	openexchangerates.org
44265	ILS	3.278690	openexchangerates.org
44266	IMP	0.722883	openexchangerates.org
44267	INR	74.540485	openexchangerates.org
44268	IQD	1459.827367	openexchangerates.org
44269	IRR	42105.000000	openexchangerates.org
44270	ISK	126.420000	openexchangerates.org
44271	JEP	0.722883	openexchangerates.org
44272	JMD	150.084945	openexchangerates.org
44273	JOD	0.709000	openexchangerates.org
44274	JPY	108.785000	openexchangerates.org
44275	KES	107.561047	openexchangerates.org
44276	KGS	84.801901	openexchangerates.org
44277	KHR	4050.280974	openexchangerates.org
44278	KMF	410.849684	openexchangerates.org
44279	KPW	900.000000	openexchangerates.org
44280	KRW	1116.650000	openexchangerates.org
44281	KWD	0.301529	openexchangerates.org
44282	KYD	0.833838	openexchangerates.org
44283	KZT	430.497745	openexchangerates.org
44284	LAK	9430.236658	openexchangerates.org
44285	LBP	1513.024887	openexchangerates.org
44286	LKR	200.929468	openexchangerates.org
44287	LRD	172.524971	openexchangerates.org
44288	LSL	14.340000	openexchangerates.org
44289	LYD	4.500178	openexchangerates.org
44290	MAD	8.936108	openexchangerates.org
44291	MDL	17.858826	openexchangerates.org
44292	MGA	3800.274873	openexchangerates.org
44293	MKD	51.423183	openexchangerates.org
44294	MMK	1410.802944	openexchangerates.org
44295	MNT	2850.826192	openexchangerates.org
44296	MOP	8.006793	openexchangerates.org
44297	MRO	356.999828	openexchangerates.org
44298	MRU	35.930000	openexchangerates.org
44299	MUR	40.405393	openexchangerates.org
44300	MVR	15.450000	openexchangerates.org
44301	MWK	787.657429	openexchangerates.org
44302	MXN	19.916055	openexchangerates.org
44303	MYR	4.126000	openexchangerates.org
44304	MZN	55.550000	openexchangerates.org
44305	NAD	14.340000	openexchangerates.org
44306	NGN	380.500000	openexchangerates.org
44307	NIO	34.920028	openexchangerates.org
44308	NOK	8.371000	openexchangerates.org
44309	NPR	118.869641	openexchangerates.org
44310	NZD	1.399874	openexchangerates.org
44311	OMR	0.385104	openexchangerates.org
44312	PAB	1.000000	openexchangerates.org
44313	PEN	3.628625	openexchangerates.org
44314	PGK	3.558185	openexchangerates.org
44315	PHP	48.330000	openexchangerates.org
44316	PKR	152.800000	openexchangerates.org
44317	PLN	3.791286	openexchangerates.org
44318	PYG	6296.703611	openexchangerates.org
44319	QAR	3.640750	openexchangerates.org
44320	RON	4.110800	openexchangerates.org
44321	RSD	98.064186	openexchangerates.org
44322	RUB	75.608900	openexchangerates.org
44323	RWF	1000.931342	openexchangerates.org
44324	SAR	3.751080	openexchangerates.org
44325	SBD	7.981354	openexchangerates.org
44326	SCR	13.970000	openexchangerates.org
44327	SDG	381.500000	openexchangerates.org
44328	SEK	8.435300	openexchangerates.org
44329	SGD	1.334255	openexchangerates.org
44330	SHP	0.722883	openexchangerates.org
44331	SLL	10218.750170	openexchangerates.org
44332	SOS	578.787804	openexchangerates.org
44333	SRD	14.154000	openexchangerates.org
44334	SSP	130.260000	openexchangerates.org
44335	STD	20738.069016	openexchangerates.org
44336	STN	20.750000	openexchangerates.org
44337	SVC	8.754836	openexchangerates.org
44338	SYP	1257.595803	openexchangerates.org
44339	SZL	14.255109	openexchangerates.org
44340	THB	31.202767	openexchangerates.org
44341	TJS	11.408494	openexchangerates.org
44342	TMT	3.510000	openexchangerates.org
44343	TND	2.756500	openexchangerates.org
44344	TOP	2.266876	openexchangerates.org
44345	TRY	8.072950	openexchangerates.org
44346	TTD	6.791466	openexchangerates.org
44347	TWD	28.266500	openexchangerates.org
44348	TZS	2320.316328	openexchangerates.org
44349	UAH	28.005375	openexchangerates.org
44350	UGX	3619.040508	openexchangerates.org
44351	USD	1.000000	openexchangerates.org
44352	UYU	44.159756	openexchangerates.org
44353	UZS	10518.093810	openexchangerates.org
44354	VES	2378817.000000	openexchangerates.org
44355	VND	23081.384500	openexchangerates.org
44356	VUV	109.544432	openexchangerates.org
44357	WST	2.531864	openexchangerates.org
44358	XAF	547.454300	openexchangerates.org
44359	XAG	0.038521	openexchangerates.org
44360	XAU	0.000563	openexchangerates.org
44361	XCD	2.702550	openexchangerates.org
44362	XDR	0.699628	openexchangerates.org
44363	XOF	547.454300	openexchangerates.org
44364	XPD	0.000360	openexchangerates.org
44365	XPF	99.592924	openexchangerates.org
44366	XPT	0.000831	openexchangerates.org
44367	YER	250.399984	openexchangerates.org
44368	ZAR	14.312970	openexchangerates.org
44369	ZMW	22.202563	openexchangerates.org
44370	ZWL	322.000000	openexchangerates.org
\.


--
-- Data for Name: kash_checkoutsession; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_checkoutsession (id, created_at, updated_at, uid, paid_at, cancel_url, cart_id, shop_id, order_id, user_id) FROM stdin;
\.


--
-- Data for Name: kash_fundinghistory; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_fundinghistory (id, created_at, updated_at, txn_ref, card_id, amount, amount_currency, status) FROM stdin;
1	2021-04-06 14:06:14.022394+01	2021-04-06 14:06:14.022421+01	1b7c173d5f7b183914a1	3	1.00	XOF	success
4	2021-04-07 02:53:02.047677+01	2021-04-07 02:53:02.047775+01	8182db5083694b50b93a	9	1.00	USD	success
\.


--
-- Data for Name: kash_invitecode; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_invitecode (id, created_at, updated_at, code, used_at, invited_id, inviter_id) FROM stdin;
1	2021-04-06 20:37:19.362324+01	2021-04-06 20:37:19.362493+01	8MDZ2W	\N	\N	2
2	2021-04-06 21:42:26.267963+01	2021-04-06 21:42:26.267988+01	3AKK	2021-04-06 21:42:26.26728+01	4	4
3	2021-04-07 02:08:30.494288+01	2021-04-07 02:08:50.404929+01	0C4W	2021-04-07 02:08:50.401489+01	3	4
4	2021-04-07 02:28:17.300428+01	2021-04-07 02:28:17.300551+01	VLJY	\N	\N	3
5	2021-04-07 02:34:57.458108+01	2021-04-07 02:34:57.45816+01	B553	\N	\N	3
6	2021-04-07 02:37:50.696988+01	2021-04-07 02:37:50.697043+01	RUER	\N	\N	3
7	2021-04-07 02:37:54.894515+01	2021-04-07 02:37:54.894555+01	C01N	\N	\N	3
8	2021-04-07 18:56:43.212866+01	2021-04-07 18:56:43.212894+01	D0UR	2021-04-07 18:56:43.212311+01	2	2
\.


--
-- Data for Name: kash_kashrequest; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_kashrequest (id, created_at, updated_at, note, amount_currency, amount, initiator_id, accepted_at, recipient_id, rejected_at) FROM stdin;
7	2021-04-16 00:42:46.388836+01	2021-04-16 00:42:46.402061+01	Bouffer	XOF	4000.00	2	\N	3	\N
9	2021-04-16 00:42:46.433955+01	2021-04-16 00:42:46.440601+01	Bouffer	XOF	4000.00	2	\N	3	\N
10	2021-04-16 00:42:46.44465+01	2021-04-16 00:42:46.450086+01	Bouffer	XOF	4000.00	2	2021-04-05 12:21:50.453624+01	4	\N
11	2021-04-16 00:42:46.468311+01	2021-04-16 00:42:46.47428+01	Test	XOF	1500.00	2	\N	3	\N
12	2021-04-16 00:42:46.476207+01	2021-04-16 00:42:46.47992+01	Test	XOF	1500.00	2	\N	4	2021-04-05 12:42:40.655916+01
4	2021-04-05 12:46:58.239293+01	2021-04-16 00:42:46.498743+01	Gotham	XOF	1400.00	2	2021-04-05 12:59:39.685663+01	4	\N
13	2021-04-16 00:42:46.507807+01	2021-04-16 00:42:46.511729+01	Ko	XOF	5000.00	2	\N	3	2021-04-07 02:31:33.812765+01
14	2021-04-16 00:42:46.513883+01	2021-04-16 00:42:46.517072+01	Ko	XOF	5000.00	2	2021-04-05 13:08:55.555003+01	4	\N
6	2021-04-07 02:18:42.506236+01	2021-04-16 00:42:46.53838+01	Nn	XOF	1200.00	4	2021-04-07 02:31:14.857595+01	3	\N
8	2021-04-16 00:42:46.405786+01	2021-04-16 12:06:45.799424+01	Bouffer	XOF	4000.00	2	2021-04-16 12:06:45.799218+01	4	\N
\.


--
-- Data for Name: kash_kashrequest_recipients; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_kashrequest_recipients (id, kashrequest_id, userprofile_id) FROM stdin;
\.


--
-- Data for Name: kash_kashrequestresponse; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_kashrequestresponse (id, created_at, updated_at, accepted, request_id, sender_id, transaction_id) FROM stdin;
3	2021-04-05 12:59:39.685663+01	2021-04-05 12:59:39.685718+01	t	4	4	18
5	2021-04-07 02:31:14.857595+01	2021-04-07 02:31:14.857624+01	t	6	3	29
\.


--
-- Data for Name: kash_kashtransaction; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_kashtransaction (id, created_at, updated_at, amount_currency, amount, receiver_id, txn_ref, narration, txn_type, "timestamp", profile_id, receiver_type_id, sender_id) FROM stdin;
127	2021-04-13 16:13:08.471926+01	2021-04-13 16:13:08.472077+01	XOF	2200.00	3	a11066867a4a395afefa	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-03 17:17:25.209812+01	2	31	2
128	2021-04-13 16:13:08.495823+01	2021-04-13 16:13:08.495894+01	XOF	150.00	2	1eff9641991bc1540c11	Demande de kash 💰	credit	2021-04-05 12:56:32.376784+01	2	30	4
129	2021-04-13 16:13:08.513233+01	2021-04-13 16:13:08.513258+01	XOF	4120.00	15	1a6de09b917f722ed124	Demande de kash 💰	debit	2021-04-05 12:21:14.838383+01	4	32	4
130	2021-04-13 16:13:08.520964+01	2021-04-13 16:13:08.520996+01	XOF	500.00	1	2b6cd7734183d8e038fc	Tester	debit	2021-04-04 17:06:18.12336+01	2	32	2
131	2021-04-13 16:13:08.530793+01	2021-04-13 16:13:08.530818+01	XOF	500.00	3	0dc9c8bfdbadbcd2fef5	Demande de kash 💰	credit	2021-04-04 17:06:31.052053+01	3	30	2
132	2021-04-13 16:13:08.538646+01	2021-04-13 16:13:08.538673+01	XOF	1500.00	2	5a7393646eba4fea5e81	Teste	debit	2021-04-04 17:12:36.566611+01	2	32	2
133	2021-04-13 16:13:08.545569+01	2021-04-13 16:13:08.545598+01	XOF	1500.00	3	fccd602c416ddd3c1136	Demande de kash 💰	credit	2021-04-04 17:12:57.995658+01	3	30	2
134	2021-04-13 16:13:08.55358+01	2021-04-13 16:13:08.553609+01	XOF	400.00	3	2abfe602d6c7f4e3802e	Test	debit	2021-04-04 20:23:35.028741+01	2	32	2
135	2021-04-13 16:13:08.560664+01	2021-04-13 16:13:08.560691+01	XOF	199.00	3	2b8fff98469c192fa41d	Demande de kash 💰	credit	2021-04-04 20:29:10.506902+01	3	30	2
136	2021-04-13 16:13:08.567762+01	2021-04-13 16:13:08.567788+01	XOF	199.00	2	9f72eb85701a5bcf5858	Demande de kash 💰	credit	2021-04-04 20:29:13.08203+01	2	30	2
137	2021-04-13 16:13:08.57564+01	2021-04-13 16:13:08.575666+01	XOF	400.00	6	fbf5fc17967bcf5b47f3	yeah	debit	2021-04-04 20:46:22.609087+01	3	32	3
138	2021-04-13 16:13:08.583869+01	2021-04-13 16:13:08.583897+01	XOF	200.00	7	38ea95ce2f69c1e5a87a	O	debit	2021-04-04 20:54:52.299577+01	2	32	2
139	2021-04-13 16:13:08.592169+01	2021-04-13 16:13:08.592196+01	XOF	500.00	8	c05f64a3d4b9ab743dd8	Noel	debit	2021-04-04 20:56:53.587687+01	2	32	2
140	2021-04-13 16:13:08.599412+01	2021-04-13 16:13:08.599437+01	XOF	345.00	3	bc0cca22d185dea9d63c	Demande de kash 💰	credit	2021-04-04 20:57:14.357328+01	3	30	2
141	2021-04-13 16:13:08.606156+01	2021-04-13 16:13:08.60618+01	XOF	153.00	2	7f3929712387268f3bb5	Demande de kash 💰	credit	2021-04-04 20:57:17.198922+01	2	30	2
142	2021-04-13 16:13:08.612933+01	2021-04-13 16:13:08.612958+01	XOF	4000.00	2	513cd8b7540fc200d5b6	Demande de kash 💰	credit	2021-04-05 12:21:45.471024+01	2	30	4
143	2021-04-13 16:13:08.620296+01	2021-04-13 16:13:08.620324+01	XOF	4120.00	13	88b3eabc0287fe3c990f	Demande de kash 💰	debit	2021-04-05 11:12:09.132185+01	4	32	4
144	2021-04-13 16:13:08.626957+01	2021-04-13 16:13:08.626981+01	XOF	4000.00	2	7f5687447e557121f6a0	Demande de kash 💰	credit	2021-04-05 11:15:42.787097+01	2	30	4
145	2021-04-13 16:13:08.633574+01	2021-04-13 16:13:08.633598+01	XOF	150.00	2	28cb19108ce64413d57f	Demande de kash 💰	credit	2021-04-05 12:59:35.822028+01	2	30	4
146	2021-04-13 16:13:08.641256+01	2021-04-13 16:13:08.641281+01	XOF	1400.00	17	5df505b4a8c8313ce5c6	Piizza	debit	2021-04-05 12:45:49.406833+01	2	32	2
147	2021-04-13 16:13:08.648625+01	2021-04-13 16:13:08.64865+01	XOF	4120.00	14	ecbcc3111522af56e773	Demande de kash 💰	debit	2021-04-05 11:19:26.319322+01	4	32	4
148	2021-04-13 16:13:08.655257+01	2021-04-13 16:13:08.655284+01	XOF	4000.00	2	4b1e4d992f7e59fa720b	Demande de kash 💰	credit	2021-04-05 11:20:33.203326+01	2	30	4
149	2021-04-13 16:13:08.661731+01	2021-04-13 16:13:08.661755+01	XOF	1400.00	3	ab76c78b1f364662b0fe	Demande de kash 💰	credit	2021-04-05 12:46:09.335146+01	3	30	2
150	2021-04-13 16:13:08.66858+01	2021-04-13 16:13:08.668605+01	XOF	500.00	2	51e124efb30066b34073	Demande de kash 💰	credit	2021-04-05 13:08:48.933674+01	2	30	4
151	2021-04-13 16:13:08.677237+01	2021-04-13 16:13:08.677263+01	XOF	500.00	19	de7746a2c16449b64eae	Demande de kash 💰	debit	2021-04-05 13:08:34.967391+01	4	32	4
152	2021-04-13 16:13:08.684147+01	2021-04-13 16:13:08.684172+01	XOF	500.00	2	14bcc5931c989f59a01e	Demande de kash 💰	credit	2021-04-05 13:08:49.656139+01	2	30	4
153	2021-04-13 16:13:08.69173+01	2021-04-13 16:13:08.691756+01	XOF	400.00	20	6e557b2df89a1ec0f07d	P	debit	2021-04-05 13:18:41.342861+01	2	32	2
154	2021-04-13 16:13:08.698501+01	2021-04-13 16:13:08.698526+01	XOF	400.00	2	8d43fbea1af42ff41015	Demande de kash 💰	credit	2021-04-05 13:25:37.206342+01	2	30	2
155	2021-04-13 16:13:08.706136+01	2021-04-13 16:13:08.70616+01	XOF	400.00	21	b3106e16dd1c22a7bbcb	D	debit	2021-04-05 13:25:24.363104+01	2	32	2
156	2021-04-13 16:13:08.71281+01	2021-04-13 16:13:08.712835+01	XOF	400.00	2	ebb9a412dd5a53bf7c8e	Demande de kash 💰	credit	2021-04-05 13:25:38.375441+01	2	30	2
157	2021-04-13 16:13:08.719521+01	2021-04-13 16:13:08.719546+01	XOF	400.00	2	ce8e85a04093627fe38c	Demande de kash 💰	credit	2021-04-05 14:00:51.867277+01	2	30	2
158	2021-04-13 16:13:08.727115+01	2021-04-13 16:13:08.72714+01	XOF	400.00	22	c77b48eaa39efbee0f83	N	debit	2021-04-05 14:00:36.894681+01	2	32	2
159	2021-04-13 16:13:08.736814+01	2021-04-13 16:13:08.736892+01	XOF	2000.00	8	5812ae54e8c6e523dd89	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-05 14:53:46.54957+01	4	31	4
160	2021-04-13 16:13:08.744943+01	2021-04-13 16:13:08.744968+01	XOF	4000.00	9	b41beea3288ac899992f	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-05 15:04:35.57845+01	4	31	4
161	2021-04-13 16:13:08.751818+01	2021-04-13 16:13:08.751843+01	XOF	125.00	2	e55af8d1e43cd440c36d	Demande de kash 💰	credit	2021-04-07 02:15:28.385201+01	2	30	3
162	2021-04-13 16:13:08.75946+01	2021-04-13 16:13:08.759485+01	XOF	4000.00	10	e6a4b8736111272c3252	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-05 15:35:15.612301+01	4	31	4
163	2021-04-13 16:13:08.767076+01	2021-04-13 16:13:08.767102+01	XOF	400.00	23	4a42e905db98583086bf	Be	debit	2021-04-05 17:23:27.447784+01	4	32	4
164	2021-04-13 16:13:08.773787+01	2021-04-13 16:13:08.773812+01	XOF	400.00	2	6672bdf214e25d37de48	Demande de kash 💰	credit	2021-04-05 17:23:44.673327+01	2	30	4
165	2021-04-13 16:13:08.78121+01	2021-04-13 16:13:08.781235+01	XOF	125.00	27	6c154566735db424aa5d	Note	debit	2021-04-07 02:15:07.05857+01	3	32	3
166	2021-04-13 16:13:08.788786+01	2021-04-13 16:13:08.788811+01	XOF	2778.00	3	6c8eb111a2c90f735a0d	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-06 13:58:30.381137+01	2	31	2
167	2021-04-13 16:13:08.795502+01	2021-04-13 16:13:08.795528+01	XOF	125.00	2	748fa0c0722733841d10	Demande de kash 💰	credit	2021-04-07 02:15:24.808487+01	2	30	3
168	2021-04-13 16:13:08.802185+01	2021-04-13 16:13:08.80221+01	XOF	125.00	2	a75ab4f7593e9af88e7b	Demande de kash 💰	credit	2021-04-07 02:15:25.173265+01	2	30	3
169	2021-04-13 16:13:08.808991+01	2021-04-13 16:13:08.809017+01	XOF	125.00	2	a762b6aa49259bafda25	Demande de kash 💰	credit	2021-04-07 02:15:25.716817+01	2	30	3
170	2021-04-13 16:13:08.816461+01	2021-04-13 16:13:08.816487+01	XOF	2778.00	3	930c992697c78c69ddb6	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-06 14:02:55.043394+01	2	31	2
171	2021-04-13 16:13:08.823182+01	2021-04-13 16:13:08.823206+01	XOF	125.00	2	e3fb78892022aacb28c4	Demande de kash 💰	credit	2021-04-07 02:15:25.49236+01	2	30	3
172	2021-04-13 16:13:08.830044+01	2021-04-13 16:13:08.83007+01	XOF	125.00	2	f936a69459bf6aff5c6c	Demande de kash 💰	credit	2021-04-07 02:15:25.776008+01	2	30	3
173	2021-04-13 16:13:08.838676+01	2021-04-13 16:13:08.838706+01	XOF	6668.00	3	1b7c173d5f7b183914a1	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-06 14:05:49.777806+01	2	31	2
174	2021-04-13 16:13:08.845371+01	2021-04-13 16:13:08.845395+01	XOF	125.00	2	0abcfd39a4009c98c596	Demande de kash 💰	credit	2021-04-07 02:15:27.992539+01	2	30	3
175	2021-04-13 16:13:08.853121+01	2021-04-13 16:13:08.853146+01	XOF	5556.00	3	885aa08f288d095e2c8b	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-06 13:51:49.43123+01	2	31	2
176	2021-04-13 16:13:08.860103+01	2021-04-13 16:13:08.860128+01	XOF	125.00	2	7f3c28e3cc6414e73bb5	Demande de kash 💰	credit	2021-04-07 02:15:27.969844+01	2	30	3
177	2021-04-13 16:13:08.866749+01	2021-04-13 16:13:08.866785+01	XOF	125.00	2	29eaae8a0e7d7c93f612	Demande de kash 💰	credit	2021-04-07 02:15:28.064882+01	2	30	3
178	2021-04-13 16:13:08.873497+01	2021-04-13 16:13:08.873522+01	XOF	125.00	2	a68aaa4eb1b93f2098ea	Demande de kash 💰	credit	2021-04-07 02:15:28.044687+01	2	30	3
179	2021-04-13 16:13:08.880251+01	2021-04-13 16:13:08.880275+01	XOF	125.00	2	1fce30420709086d4722	Demande de kash 💰	credit	2021-04-07 02:15:28.374081+01	2	30	3
180	2021-04-13 16:13:08.886774+01	2021-04-13 16:13:08.886801+01	XOF	125.00	2	43fea0dcdd4fe8b44f89	Demande de kash 💰	credit	2021-04-07 02:15:28.287454+01	2	30	3
181	2021-04-13 16:13:08.894141+01	2021-04-13 16:13:08.894165+01	XOF	125.00	2	7d2f81cd8a8f8a00c035	Demande de kash 💰	credit	2021-04-07 02:15:28.466788+01	2	30	3
182	2021-04-13 16:13:08.900903+01	2021-04-13 16:13:08.900929+01	XOF	125.00	2	6366bd2d2ee354614583	Demande de kash 💰	credit	2021-04-07 02:15:28.633088+01	2	30	3
183	2021-04-13 16:13:08.907891+01	2021-04-13 16:13:08.907917+01	XOF	125.00	2	a26c99c941b92e30caf1	Demande de kash 💰	credit	2021-04-07 02:15:28.63919+01	2	30	3
184	2021-04-13 16:13:08.91472+01	2021-04-13 16:13:08.914747+01	XOF	125.00	2	83970fe33ac578c488ae	Demande de kash 💰	credit	2021-04-07 02:15:28.667548+01	2	30	3
185	2021-04-13 16:13:08.922439+01	2021-04-13 16:13:08.922463+01	XOF	552.00	9	8182db5083694b50b93a	Achat/recharge d'une carte virtuelle 💳	debit	2021-04-07 02:52:47.108173+01	4	31	4
186	2021-04-13 16:13:08.929057+01	2021-04-13 16:13:08.929082+01	XOF	352.00	2	a26b2100119df3781ec9	Demande de kash 💰	credit	2021-04-07 12:39:34.25817+01	2	30	4
187	2021-04-13 16:13:08.936515+01	2021-04-13 16:13:08.93654+01	XOF	1200.00	29	d41e9262c6b3a1b51cde	Demande de kash 💰	debit	2021-04-07 02:30:56.868121+01	3	32	3
188	2021-04-13 16:13:08.94318+01	2021-04-13 16:13:08.943205+01	XOF	1200.00	2	ccf5d43afcda2569d6a7	Demande de kash 💰	credit	2021-04-07 02:31:11.406158+01	2	30	3
189	2021-04-13 16:13:08.949744+01	2021-04-13 16:13:08.949769+01	XOF	352.00	2	2e6cf4dc17c682c5674b	Demande de kash 💰	credit	2021-04-07 12:41:10.290573+01	2	30	4
190	2021-04-14 10:14:34.031546+01	2021-04-14 10:14:34.031591+01	XOF	125.00	4	bb25a0aac936e0a12770	Test	debit	2021-04-14 10:14:34.02744+01	2	30	2
191	2021-04-14 10:14:34.073589+01	2021-04-14 10:14:34.073644+01	XOF	125.00	4	3d8f359fd42fabaee798	Test	credit	2021-04-14 10:14:34.071798+01	4	30	2
192	2021-04-15 22:40:59.032291+01	2021-04-15 22:40:59.03232+01	XOF	25000.00	2	5b45a88033a70a5183e6	Demande de kash 💰	debit	2021-04-15 22:40:59.029909+01	4	30	4
193	2021-04-15 22:40:59.041929+01	2021-04-15 22:40:59.041978+01	XOF	25000.00	2	3b06def773729c2a8570	Demande de kash 💰	credit	2021-04-15 22:40:59.040831+01	2	30	4
196	2021-04-15 22:46:21.756056+01	2021-04-15 22:46:21.756092+01	XOF	25000.00	2	8c014e3560f364a5b9ea	Demande de kash 💰	debit	2021-04-15 22:46:21.75519+01	4	30	4
197	2021-04-15 22:46:21.76037+01	2021-04-15 22:46:21.760398+01	XOF	25000.00	2	239c7c838af38c7cbcb0	Demande de kash 💰	credit	2021-04-15 22:46:21.759814+01	2	30	4
199	2021-04-16 12:06:42.947932+01	2021-04-16 12:06:42.948196+01	XOF	4000.00	2	212c317cc4bee0411b80	Demande de kash 💰	debit	2021-04-16 12:06:42.904741+01	4	30	4
201	2021-04-17 12:40:04.37443+01	2021-04-17 12:40:04.374481+01	XOF	2000.00	4	13e1c881d970a80db5bf	Test 1	debit	2021-04-17 12:40:04.364139+01	2	30	2
202	2021-04-17 12:40:04.393579+01	2021-04-17 12:40:04.393672+01	XOF	2000.00	4	61a72cade0418bc5902b	Test 1	credit	2021-04-17 12:40:04.388803+01	4	30	2
203	2021-04-17 13:12:33.018398+01	2021-04-17 13:12:33.018432+01	XOF	200.00	4	9ecc5656ea4aa958530d	Anonymous test	debit	2021-04-17 13:12:33.015441+01	2	30	2
205	2021-04-17 13:12:33.027595+01	2021-04-17 13:12:33.027625+01	XOF	200.00	4	09c9995e5f5d0a690c7d	Anonymous test	credit	2021-04-17 13:12:33.026937+01	4	30	2
\.


--
-- Data for Name: kash_momoaccount; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_momoaccount (id, created_at, updated_at, gateway, phone, profile_id) FROM stdin;
2	2021-04-04 16:35:29.15344+01	2021-04-04 16:35:29.153484+01	moov-bj	98801811	2
3	2021-04-04 16:35:49.930156+01	2021-04-04 16:35:49.930193+01	mtn-bj	90137010	3
5	2021-04-06 21:39:11.204945+01	2021-04-06 21:39:11.205521+01	moov-bj	98801811	4
6	2021-04-06 23:52:29.910405+01	2021-04-06 23:52:29.916108+01	mtn-bj	90137010	4
\.


--
-- Data for Name: kash_notification; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_notification (id, created_at, updated_at, object_id, title, description, sent_at, content_type_id, profile_id) FROM stdin;
1	2021-04-04 17:13:04.717879+01	2021-04-04 17:13:05.585547+01	2	Le gout de ça 🤑	$nel vient de t'envoyer $1500.00 FCFA	2021-04-04 17:13:05.585293+01	32	3
2	2021-04-04 20:29:15.925209+01	2021-04-04 20:29:17.290529+01	4	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "$Eat"	2021-04-04 20:29:17.290338+01	32	3
4	2021-04-04 20:29:19.688018+01	2021-04-04 20:29:22.071376+01	4	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "$Eat"	2021-04-04 20:29:22.071123+01	32	3
6	2021-04-04 20:57:22.088468+01	2021-04-04 20:57:24.123807+01	8	Le goût de ça 🤑	Quelqu'un vient de te faroter CFA345.00 FCFA pour "Noel"	2021-04-04 20:57:24.123409+01	32	3
8	2021-04-04 20:57:25.043466+01	2021-04-04 20:57:25.924129+01	8	Le goût de ça 🤑	Quelqu'un vient de te faroter CFA153.00 FCFA pour "Noel"	2021-04-04 20:57:25.92367+01	32	3
10	2021-04-04 22:44:50.350219+01	2021-04-04 22:44:51.376295+01	2	Besoin de kash 💰	$nel a besoin de 4000.00 FCFA pour "Bouffer"	2021-04-04 22:44:51.376122+01	35	3
14	2021-04-05 12:42:07.031939+01	2021-04-05 12:42:07.896933+01	3	Besoin de kash 💰	$nel a besoin de 1500.00 FCFA pour "Test"	2021-04-05 12:42:07.896627+01	35	3
16	2021-04-05 12:46:11.69178+01	2021-04-05 12:46:13.031849+01	17	Le goût de ça 🤑	$nel vient de t'envoyer 1400.00 FCFA pour "Piizza"	2021-04-05 12:46:13.031676+01	32	3
20	2021-04-05 13:07:37.792608+01	2021-04-05 13:07:38.66691+01	5	Besoin de kash 💰	$nel a besoin de 5000.00 FCFA pour "Ko"	2021-04-05 13:07:38.666646+01	35	3
44	2021-04-07 02:18:42.556263+01	2021-04-07 02:18:44.083227+01	6	Besoin de kash 💰	$batman a besoin de 1200.00 FCFA pour "Nn"	2021-04-07 02:18:44.082878+01	35	3
3	2021-04-04 20:29:17.315901+01	2021-04-07 02:48:02.339773+01	4	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "$Eat"	2021-04-07 02:48:02.251472+01	32	4
15	2021-04-05 12:42:07.902255+01	2021-04-07 02:48:11.458113+01	3	Besoin de kash 💰	$nel a besoin de 1500.00 FCFA pour "Test"	2021-04-07 02:48:11.457754+01	35	4
5	2021-04-04 20:29:22.101115+01	2021-04-07 02:48:03.769834+01	4	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "$Eat"	2021-04-07 02:48:03.769605+01	32	4
7	2021-04-04 20:57:24.196024+01	2021-04-07 02:48:05.073568+01	8	Le goût de ça 🤑	Quelqu'un vient de te faroter CFA345.00 FCFA pour "Noel"	2021-04-07 02:48:05.073302+01	32	4
11	2021-04-04 22:44:51.396002+01	2021-04-07 02:48:07.585763+01	2	Besoin de kash 💰	$nel a besoin de 4000.00 FCFA pour "Bouffer"	2021-04-07 02:48:07.58551+01	35	4
9	2021-04-04 20:57:25.954278+01	2021-04-07 02:48:06.295021+01	8	Le goût de ça 🤑	Quelqu'un vient de te faroter CFA153.00 FCFA pour "Noel"	2021-04-07 02:48:06.294624+01	32	4
17	2021-04-05 12:46:58.276613+01	2021-04-07 02:48:13.165685+01	4	Besoin de kash 💰	$nel a besoin de 1400.00 FCFA pour "Gotham"	2021-04-07 02:48:13.165461+01	35	4
21	2021-04-05 13:07:38.67625+01	2021-04-07 02:48:17.894639+01	5	Besoin de kash 💰	$nel a besoin de 5000.00 FCFA pour "Ko"	2021-04-07 02:48:17.894173+01	35	4
26	2021-04-05 14:00:54.396193+01	2021-04-07 02:48:24.471577+01	22	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "N"	2021-04-07 02:48:24.471355+01	32	4
28	2021-04-07 02:15:29.23928+01	2021-04-07 02:48:27.008235+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:27.007884+01	32	4
34	2021-04-07 02:15:30.739101+01	2021-04-07 02:48:35.813589+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:35.813353+01	32	4
32	2021-04-07 02:15:30.096922+01	2021-04-07 02:48:32.276219+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:32.275977+01	32	4
29	2021-04-07 02:15:29.843081+01	2021-04-07 02:48:28.264597+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:28.264098+01	32	4
36	2021-04-07 02:15:30.829642+01	2021-04-07 02:48:38.331374+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:38.331133+01	32	4
25	2021-04-05 13:25:41.214324+01	2021-04-07 02:48:23.236674+01	21	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "D"	2021-04-07 02:48:23.236288+01	32	4
43	2021-04-07 02:15:33.093163+01	2021-04-07 02:48:47.420874+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:47.420421+01	32	4
30	2021-04-07 02:15:29.88969+01	2021-04-07 02:48:29.555632+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:29.555406+01	32	4
18	2021-04-05 12:56:36.235729+01	2021-04-16 12:30:03.350844+01	18	Le goût de ça 🤑	$batman vient de t'envoyer 150.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:03.350591+01	32	2
31	2021-04-07 02:15:30.027902+01	2021-04-07 02:48:31.029269+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:31.028975+01	32	4
33	2021-04-07 02:15:30.731838+01	2021-04-07 02:48:34.585265+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:34.584365+01	32	4
39	2021-04-07 02:15:32.422426+01	2021-04-07 02:48:42.09934+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:42.099102+01	32	4
35	2021-04-07 02:15:30.829202+01	2021-04-07 02:48:37.076344+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:37.076061+01	32	4
13	2021-04-05 11:20:41.379029+01	2021-04-16 12:30:02.41814+01	14	Le goût de ça 🤑	$batman vient de t'envoyer 4000.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:02.417892+01	32	2
38	2021-04-07 02:15:31.30567+01	2021-04-07 02:48:40.863144+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:40.862292+01	32	4
37	2021-04-07 02:15:31.30318+01	2021-04-07 02:48:39.593951+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:39.593728+01	32	4
40	2021-04-07 02:15:32.430053+01	2021-04-07 02:48:43.39084+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:43.390544+01	32	4
42	2021-04-07 02:15:32.435506+01	2021-04-07 02:48:46.155635+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:46.155356+01	32	4
12	2021-04-05 11:15:45.467846+01	2021-04-16 12:30:01.151754+01	13	Le goût de ça 🤑	$batman vient de t'envoyer 4000.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:01.150887+01	32	2
41	2021-04-07 02:15:32.430061+01	2021-04-07 02:48:44.647666+01	27	Le goût de ça 🤑	$test vient de t'envoyer 125.00 FCFA pour "Note"	2021-04-07 02:48:44.647439+01	32	4
22	2021-04-05 13:08:56.700724+01	2021-04-16 12:30:09.577234+01	19	Le goût de ça 🤑	$batman vient de t'envoyer 500.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:09.576659+01	32	2
23	2021-04-05 13:08:56.700742+01	2021-04-16 12:30:06.123909+01	19	Le goût de ça 🤑	$batman vient de t'envoyer 500.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:06.123591+01	32	2
19	2021-04-05 12:59:42.514533+01	2021-04-16 12:30:04.600643+01	18	Le goût de ça 🤑	$batman vient de t'envoyer 150.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:04.600384+01	32	2
27	2021-04-05 17:23:47.276757+01	2021-04-16 12:30:10.930034+01	23	Le goût de ça 🤑	$batman vient de t'envoyer 400.00 FCFA pour "Be"	2021-04-16 12:30:10.929776+01	32	2
24	2021-04-05 13:25:40.009321+01	2021-04-07 02:48:21.682838+01	21	Le goût de ça 🤑	$nel vient de t'envoyer 400.00 FCFA pour "D"	2021-04-07 02:48:21.682408+01	32	4
45	2021-04-07 02:31:14.073651+01	2021-04-07 02:48:48.927508+01	29	Le goût de ça 🤑	$test vient de t'envoyer 1200.00 FCFA pour "Demande de kash 💰"	2021-04-07 02:48:48.927061+01	32	4
46	2021-04-14 10:14:34.127108+01	2021-04-14 10:14:35.147786+01	30	Le goût de ça 🤑	$nel vient de t'envoyer 125.00 FCFA pour "Test"	2021-04-14 10:14:35.147491+01	32	4
47	2021-04-15 22:40:59.064174+01	2021-04-16 12:30:14.558678+01	37	Le goût de ça 🤑	$batman vient de t'envoyer 25000.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:14.558369+01	32	2
48	2021-04-15 22:46:21.771289+01	2021-04-16 12:30:15.430904+01	38	Le goût de ça 🤑	$batman vient de t'envoyer 25000.00 FCFA pour "Demande de kash 💰"	2021-04-16 12:30:15.430654+01	32	2
49	2021-04-17 12:40:04.456111+01	2021-04-17 12:40:05.658332+01	39	Le goût de ça 🤑	$nel vient de t'envoyer 2000.00 FCFA pour "Test 1"	2021-04-17 12:40:05.657947+01	32	4
50	2021-04-17 13:12:33.03532+01	2021-04-17 13:12:33.880516+01	40	Le goût de ça 🤑	Quelqu'un vient de t'envoyer 200.00 FCFA pour "Anonymous test"	2021-04-17 13:12:33.880229+01	32	4
\.


--
-- Data for Name: kash_sendkash; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_sendkash (id, created_at, updated_at, note, group_mode, is_incognito, amount_currency, amount, initiator_id) FROM stdin;
1	2021-04-04 17:05:47.823155+01	2021-04-04 17:05:47.880847+01	Tester		f	XOF	500.00	2
2	2021-04-04 17:12:18.897004+01	2021-04-04 17:12:18.915562+01	Teste		f	XOF	1500.00	2
3	2021-04-04 20:23:03.339677+01	2021-04-04 20:23:03.42616+01	Test	normal	f	XOF	400.00	2
4	2021-04-04 20:28:15.613068+01	2021-04-04 20:28:15.639789+01	Eat	normal	f	XOF	400.00	2
5	2021-04-04 20:38:17.950454+01	2021-04-04 20:38:17.968687+01	Manger	faro	f	XOF	400.00	3
6	2021-04-04 20:46:09.591858+01	2021-04-04 20:46:09.621595+01	yeah	faro	t	XOF	400.00	3
7	2021-04-04 20:54:42.309623+01	2021-04-04 20:54:42.333344+01	O	faro	f	XOF	200.00	2
8	2021-04-04 20:56:46.166705+01	2021-04-04 20:56:46.186975+01	Noel	faro	t	XOF	500.00	2
9	2021-04-05 10:57:53.310143+01	2021-04-05 10:57:53.337832+01	Demande de kash 💰		f	XOF	3500.00	4
10	2021-04-05 11:07:17.910769+01	2021-04-05 11:07:17.92485+01	Demande de kash 💰		f	XOF	4000.00	4
11	2021-04-05 11:07:18.146976+01	2021-04-05 11:07:18.160368+01	Demande de kash 💰		f	XOF	4000.00	4
12	2021-04-05 11:10:57.60573+01	2021-04-05 11:10:57.623023+01	Demande de kash 💰		f	XOF	4000.00	4
13	2021-04-05 11:11:43.6808+01	2021-04-05 11:11:43.69365+01	Demande de kash 💰		f	XOF	4000.00	4
14	2021-04-05 11:19:05.437318+01	2021-04-05 11:19:05.451168+01	Demande de kash 💰		f	XOF	4000.00	4
15	2021-04-05 12:21:03.063082+01	2021-04-05 12:21:03.087642+01	Demande de kash 💰		f	XOF	4000.00	4
16	2021-04-05 12:44:24.009804+01	2021-04-05 12:44:24.033613+01	Pizza		f	XOF	1400.00	2
17	2021-04-05 12:45:19.308199+01	2021-04-05 12:45:19.328892+01	Piizza		f	XOF	1400.00	2
18	2021-04-05 12:55:38.597851+01	2021-04-05 12:55:38.612538+01	Demande de kash 💰		f	XOF	150.00	4
19	2021-04-05 13:08:17.388707+01	2021-04-05 13:08:17.415262+01	Demande de kash 💰		f	XOF	500.00	4
20	2021-04-05 13:18:30.271915+01	2021-04-05 13:18:30.290449+01	P		f	XOF	400.00	2
34	2021-04-15 19:57:58.015818+01	2021-04-15 19:57:58.033144+01	Demande de kash 💰		f	XOF	30000.00	4
21	2021-04-05 13:25:08.071615+01	2021-04-05 13:25:41.20812+01	D		f	XOF	400.00	2
35	2021-04-15 19:57:58.377784+01	2021-04-15 19:57:58.401454+01	Demande de kash 💰		f	XOF	30000.00	4
22	2021-04-05 14:00:27.610996+01	2021-04-05 14:00:54.387321+01	N		f	XOF	400.00	2
23	2021-04-05 17:22:59.819992+01	2021-04-05 17:23:47.263794+01	Be		f	XOF	400.00	4
24	2021-04-06 11:29:00.219243+01	2021-04-06 11:29:00.266075+01	N		f	XOF	2500.00	2
25	2021-04-06 11:46:51.338429+01	2021-04-06 11:46:51.354088+01	N		f	XOF	1400.00	2
26	2021-04-07 02:14:36.021497+01	2021-04-07 02:14:36.071802+01	Note		f	XOF	125.00	3
36	2021-04-15 20:02:08.892787+01	2021-04-15 20:02:08.906299+01	Demande de kash 💰		f	XOF	30000.00	4
37	2021-04-15 22:39:06.919967+01	2021-04-15 22:40:59.058591+01	Demande de kash 💰		f	XOF	25000.00	4
38	2021-04-15 22:45:56.816609+01	2021-04-15 22:46:21.767268+01	Demande de kash 💰		f	XOF	25000.00	4
39	2021-04-17 12:39:25.948896+01	2021-04-17 12:40:04.436658+01	Test 1		f	XOF	2000.00	2
40	2021-04-17 13:12:09.180532+01	2021-04-17 13:12:33.032839+01	Anonymous test		t	XOF	200.00	2
27	2021-04-07 02:14:59.562035+01	2021-04-07 02:15:33.081506+01	Note		f	XOF	125.00	3
28	2021-04-07 02:30:20.281745+01	2021-04-07 02:30:20.313712+01	Demande de kash 💰		f	XOF	1200.00	3
29	2021-04-07 02:30:43.296205+01	2021-04-07 02:31:14.060533+01	Demande de kash 💰		f	XOF	1200.00	3
30	2021-04-14 10:11:10.584095+01	2021-04-14 10:14:34.122362+01	Test		f	XOF	125.00	2
31	2021-04-15 19:30:16.842741+01	2021-04-15 19:30:16.962232+01	Demande de kash 💰		f	XOF	25000.00	4
32	2021-04-15 19:31:49.371331+01	2021-04-15 19:31:49.385269+01	Demande de kash 💰		f	XOF	20000.00	4
33	2021-04-15 19:34:39.378681+01	2021-04-15 19:34:39.404746+01	Demande de kash 💰		f	XOF	30000.00	4
\.


--
-- Data for Name: kash_sendkash_paid_recipients; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_sendkash_paid_recipients (id, sendkash_id, userprofile_id) FROM stdin;
1	21	4
3	22	4
4	23	2
5	27	4
21	29	4
22	30	4
23	37	2
24	38	2
25	39	4
26	40	4
\.


--
-- Data for Name: kash_sendkash_recipients; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_sendkash_recipients (id, sendkash_id, userprofile_id) FROM stdin;
1	1	3
2	2	3
3	3	3
4	3	4
5	4	3
6	4	4
7	5	2
8	5	4
9	6	2
10	6	4
11	7	3
12	7	4
13	8	3
14	8	4
15	9	2
16	10	2
17	11	2
18	12	2
19	13	2
20	14	2
21	15	2
22	16	3
23	17	3
24	18	2
25	19	2
26	20	4
27	21	4
28	22	4
29	23	2
30	24	3
31	25	3
32	26	4
33	27	4
34	28	4
35	29	4
36	30	4
37	31	2
38	32	2
39	33	2
40	34	2
41	35	2
42	36	2
43	37	2
44	38	2
45	39	4
46	40	4
\.


--
-- Data for Name: kash_userprofile; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_userprofile (id, created_at, updated_at, kashtag, device_ids, user_id, avatar_url) FROM stdin;
3	2021-04-04 00:25:19.256319+01	2021-04-07 02:20:44.970095+01	test	{3ada282f-00f1-463b-bd70-f36e4dabb091,b2c65fc6-b5b6-4301-8d24-54eee00275f3}	40	
4	2021-04-16 11:31:09.822678+01	2021-04-16 11:31:31.054703+01	batman	{b12bb1b3-7664-4627-b08d-d10b0b5bc151,b6d1e3c5-5423-4340-9c76-7ba9430e8bb5,b2c65fc6-b5b6-4301-8d24-54eee00275f3}	98	https://kweek.sgp1.digitaloceanspaces.com/dev/ae055ed6-738b-40f0-a556-2867368e9086-5D8FD716-7535-4BF3-8DBC-1364D86B74A4.jpg
2	2021-04-02 13:38:03.624667+01	2021-04-16 12:29:07.183688+01	nel	{b6d1e3c5-5423-4340-9c76-7ba9430e8bb5,e5372505-cb27-4009-9f77-37a7306b0916}	94	
\.


--
-- Data for Name: kash_virtualcard; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_virtualcard (id, created_at, updated_at, external_id, service, nickname, profile_id, is_active) FROM stdin;
1	2021-04-03 16:09:00.773176+01	2021-04-03 16:09:00.773223+01		rave	Netflix	2	t
2	2021-04-03 17:12:29.95835+01	2021-04-03 17:12:29.95852+01		rave	Netflix	2	t
4	2021-04-04 00:25:57.489435+01	2021-04-04 00:25:57.489466+01		rave	Netflix	3	t
5	2021-04-04 00:31:53.484174+01	2021-04-04 00:31:53.484203+01		rave	Netflix	3	t
6	2021-04-04 09:33:50.013552+01	2021-04-04 09:33:50.015199+01		rave	Test	2	t
7	2021-04-04 09:41:35.192994+01	2021-04-04 09:41:35.193053+01		rave	Test	2	t
11	2021-04-06 11:22:52.33743+01	2021-04-06 11:22:52.337498+01		rave	Test	2	t
3	2021-04-03 17:17:05.859746+01	2021-04-06 15:17:26.923053+01	3_jPhRXNcFJ7QLEjAyIGyZV1few	rave	Netflix	2	t
12	2021-04-07 02:29:10.356367+01	2021-04-07 02:29:10.356455+01		rave	Test	3	t
10	2021-04-05 15:34:10.240086+01	2021-04-07 13:47:52.655299+01	9bd2b7c9-4f6e-4d60-8006-48cc2d23df84	rave	Netflix	4	t
8	2021-04-05 14:52:01.449172+01	2021-04-14 10:12:12.630566+01	aHx-9efPmavj_ybSfxUJD92u4LM	rave	Bmc	4	t
9	2021-04-05 15:04:00.860639+01	2021-04-14 10:12:12.641862+01	sbHjz3ldPbTJ4GXasrLWODlLwr4	rave	BMC	4	f
13	2021-04-15 01:14:34.815793+01	2021-04-15 01:14:34.815907+01		rave	Test	4	t
14	2021-04-15 01:16:15.743783+01	2021-04-15 01:16:15.743839+01		rave	T	4	t
15	2021-04-15 01:19:27.324317+01	2021-04-15 01:19:27.324348+01		rave	T	4	t
\.


--
-- Data for Name: kash_withdrawalhistory; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.kash_withdrawalhistory (id, created_at, updated_at, txn_ref, amount_currency, amount, card_id) FROM stdin;
1	2021-04-07 12:41:21.897509+01	2021-04-07 12:41:21.897546+01	2e6cf4dc17c682c5674b	USD	1.00	10
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.migrations (migration, batch) FROM stdin;
2020_08_27_181233_create_users_table	1
2020_08_27_182853_create_shops_table	1
2020_08_27_183403_create_categories_table	1
2020_08_27_183626_create_products_table	1
2020_08_27_184241_create_product_images_table	1
2020_08_27_184600_create_banners_table	1
2020_08_27_184927_migrate_from_uuid_to_int	1
2020_08_30_144936_add_slug_to_products	1
2020_08_30_145155_fill_slug_fields_in_products	1
2020_08_30_145613_make_slug_non_nullable	1
2020_09_01_095727_create_carts_table	2
2020_09_01_101348_create_cart_items_table	2
2020_09_01_191423_create_customers_table	2
2020_09_01_191517_create_checkouts_table	2
2020_09_03_071028_add_shipping_option_to_checkouts	2
2020_08_27_181233_create_users_table	1
2020_08_27_182853_create_shops_table	1
2020_08_27_183403_create_categories_table	1
2020_08_27_183626_create_products_table	1
2020_08_27_184241_create_product_images_table	1
2020_08_27_184600_create_banners_table	1
2020_08_27_184927_migrate_from_uuid_to_int	1
2020_08_30_144936_add_slug_to_products	1
2020_08_30_145155_fill_slug_fields_in_products	1
2020_08_30_145613_make_slug_non_nullable	1
2020_09_01_095727_create_carts_table	2
2020_09_01_101348_create_cart_items_table	2
2020_09_01_191423_create_customers_table	2
2020_09_01_191517_create_checkouts_table	2
2020_09_03_071028_add_shipping_option_to_checkouts	2
2020_08_27_181233_create_users_table	1
2020_08_27_182853_create_shops_table	1
2020_08_27_183403_create_categories_table	1
2020_08_27_183626_create_products_table	1
2020_08_27_184241_create_product_images_table	1
2020_08_27_184600_create_banners_table	1
2020_08_27_184927_migrate_from_uuid_to_int	1
2020_08_30_144936_add_slug_to_products	1
2020_08_30_145155_fill_slug_fields_in_products	1
2020_08_30_145613_make_slug_non_nullable	1
2020_09_01_095727_create_carts_table	2
2020_09_01_101348_create_cart_items_table	2
2020_09_01_191423_create_customers_table	2
2020_09_01_191517_create_checkouts_table	2
2020_09_03_071028_add_shipping_option_to_checkouts	2
2020_08_27_181233_create_users_table	1
2020_08_27_182853_create_shops_table	1
2020_08_27_183403_create_categories_table	1
2020_08_27_183626_create_products_table	1
2020_08_27_184241_create_product_images_table	1
2020_08_27_184600_create_banners_table	1
2020_08_27_184927_migrate_from_uuid_to_int	1
2020_08_30_144936_add_slug_to_products	1
2020_08_30_145155_fill_slug_fields_in_products	1
2020_08_30_145613_make_slug_non_nullable	1
2020_09_01_095727_create_carts_table	2
2020_09_01_101348_create_cart_items_table	2
2020_09_01_191423_create_customers_table	2
2020_09_01_191517_create_checkouts_table	2
2020_09_03_071028_add_shipping_option_to_checkouts	2
2020_08_27_181233_create_users_table	1
2020_08_27_182853_create_shops_table	1
2020_08_27_183403_create_categories_table	1
2020_08_27_183626_create_products_table	1
2020_08_27_184241_create_product_images_table	1
2020_08_27_184600_create_banners_table	1
2020_08_27_184927_migrate_from_uuid_to_int	1
2020_08_30_144936_add_slug_to_products	1
2020_08_30_145155_fill_slug_fields_in_products	1
2020_08_30_145613_make_slug_non_nullable	1
2020_09_01_095727_create_carts_table	2
2020_09_01_101348_create_cart_items_table	2
2020_09_01_191423_create_customers_table	2
2020_09_01_191517_create_checkouts_table	2
2020_09_03_071028_add_shipping_option_to_checkouts	2
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.order_items (id, created_at, updated_at, quantity, order_id, product_id, price, price_currency) FROM stdin;
1	2020-09-17 19:59:49.896341+01	2021-03-21 20:51:13.154663+01	1	1	237	10000.00	XOF
2	2020-12-02 19:30:49.120093+01	2021-03-21 20:51:13.161273+01	1	2	289	200000.00	XOF
3	2021-02-10 13:41:04.309052+01	2021-03-21 20:51:13.164005+01	1	3	238	1000.00	XOF
4	2021-02-10 13:41:04.320975+01	2021-03-21 20:51:13.16656+01	2	3	238	1000.00	XOF
5	2021-02-10 13:41:04.327991+01	2021-03-21 20:51:13.169402+01	1	3	238	1000.00	XOF
6	2021-02-10 15:30:54.093333+01	2021-03-21 20:51:13.172002+01	1	4	238	1000.00	XOF
7	2021-02-10 15:30:54.099896+01	2021-03-21 20:51:13.175844+01	2	4	238	1000.00	XOF
8	2021-02-10 15:30:54.103819+01	2021-03-21 20:51:13.178804+01	1	4	238	1000.00	XOF
9	2021-02-10 15:38:38.303676+01	2021-03-21 20:51:13.18144+01	1	5	238	1000.00	XOF
10	2021-02-10 15:43:19.045745+01	2021-03-21 20:51:13.184131+01	1	6	238	1000.00	XOF
11	2021-02-10 15:48:53.906096+01	2021-03-21 20:51:13.186847+01	1	7	238	1000.00	XOF
12	2021-02-10 16:16:21.658952+01	2021-03-21 20:51:13.189467+01	1	8	238	1000.00	XOF
13	2021-02-10 16:21:42.790104+01	2021-03-21 20:51:13.192409+01	1	9	231	10.00	NGN
14	2021-02-10 16:21:42.794704+01	2021-03-21 20:51:13.195131+01	1	9	231	10.00	NGN
15	2021-02-10 16:21:42.798645+01	2021-03-21 20:51:13.19808+01	1	9	231	10.00	NGN
16	2021-02-10 16:21:42.802371+01	2021-03-21 20:51:13.200809+01	3	9	232	15.00	NGN
17	2021-02-10 16:21:42.805479+01	2021-03-21 20:51:13.203409+01	2	9	233	25.00	NGN
18	2021-02-10 16:21:43.872886+01	2021-03-21 20:51:13.206227+01	1	10	231	10.00	NGN
19	2021-02-10 16:21:43.876134+01	2021-03-21 20:51:13.208992+01	1	10	231	10.00	NGN
20	2021-02-10 16:21:43.879236+01	2021-03-21 20:51:13.211857+01	1	10	231	10.00	NGN
21	2021-02-10 16:21:43.882806+01	2021-03-21 20:51:13.214621+01	3	10	232	15.00	NGN
22	2021-02-10 16:21:43.885909+01	2021-03-21 20:51:13.217286+01	2	10	233	25.00	NGN
23	2021-02-10 16:21:45.324053+01	2021-03-21 20:51:13.219871+01	1	11	231	10.00	NGN
24	2021-02-10 16:21:45.326887+01	2021-03-21 20:51:13.222428+01	1	11	231	10.00	NGN
25	2021-02-10 16:21:45.329703+01	2021-03-21 20:51:13.225201+01	1	11	231	10.00	NGN
26	2021-02-10 16:21:45.333645+01	2021-03-21 20:51:13.227817+01	3	11	232	15.00	NGN
27	2021-02-10 16:21:45.336552+01	2021-03-21 20:51:13.230416+01	2	11	233	25.00	NGN
28	2021-02-10 16:35:55.807159+01	2021-03-21 20:51:13.232991+01	1	12	231	10.00	NGN
29	2021-02-10 16:35:55.810839+01	2021-03-21 20:51:13.235675+01	3	12	233	25.00	NGN
30	2021-02-10 16:35:55.814584+01	2021-03-21 20:51:13.238295+01	3	12	235	50.00	NGN
31	2021-02-10 16:35:56.885405+01	2021-03-21 20:51:13.241022+01	1	13	231	10.00	NGN
32	2021-02-10 16:35:56.888422+01	2021-03-21 20:51:13.243704+01	3	13	233	25.00	NGN
33	2021-02-10 16:35:56.891558+01	2021-03-21 20:51:13.246258+01	3	13	235	50.00	NGN
34	2021-02-10 16:35:57.807059+01	2021-03-21 20:51:13.251089+01	1	14	231	10.00	NGN
35	2021-02-10 16:35:57.809743+01	2021-03-21 20:51:13.25392+01	3	14	233	25.00	NGN
36	2021-02-10 16:35:57.812861+01	2021-03-21 20:51:13.256609+01	3	14	235	50.00	NGN
37	2021-02-10 16:37:35.358462+01	2021-03-21 20:51:13.259245+01	1	15	235	50.00	NGN
38	2021-02-10 16:37:35.36227+01	2021-03-21 20:51:13.261933+01	3	15	235	50.00	NGN
39	2021-02-10 16:37:35.365194+01	2021-03-21 20:51:13.264511+01	1	15	231	10.00	NGN
40	2021-02-10 18:03:17.764062+01	2021-03-21 20:51:13.267146+01	3	16	231	10.00	NGN
41	2021-02-12 21:20:22.093962+01	2021-03-21 20:51:13.269717+01	3	18	231	10.00	NGN
42	2021-02-12 21:34:39.651053+01	2021-03-21 20:51:13.272339+01	3	19	231	10.00	NGN
43	2021-02-12 21:46:12.386741+01	2021-03-21 20:51:13.275108+01	3	20	231	10.00	NGN
44	2021-02-12 22:52:16.775412+01	2021-03-21 20:51:13.277754+01	1	21	232	15.00	NGN
45	2021-02-12 23:16:31.110302+01	2021-03-21 20:51:13.280627+01	1	22	231	10.00	NGN
46	2021-03-24 07:43:47.759414+01	2021-03-24 07:43:47.759464+01	1	23	231	10.00	NGN
47	2021-03-24 07:43:47.773891+01	2021-03-24 07:43:47.773934+01	2	23	231	10.00	NGN
48	2021-03-24 07:45:33.239223+01	2021-03-24 07:45:33.239248+01	1	24	231	10.00	NGN
49	2021-03-24 07:45:33.24299+01	2021-03-24 07:45:33.243016+01	2	24	231	10.00	NGN
50	2021-03-24 07:58:49.647046+01	2021-03-24 07:58:49.647078+01	3	25	232	15.00	NGN
51	2021-03-24 08:07:56.436642+01	2021-03-24 08:07:56.436667+01	1	26	311	40.00	NGN
52	2021-03-24 08:07:56.440731+01	2021-03-24 08:07:56.440757+01	3	26	231	10.00	NGN
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.orders (id, created_at, updated_at, country, city, address, ref_id, payment_method, customer_id, shop_id, shipping_fees, shipping_fees_currency, shipping_profile_id, zone) FROM stdin;
1	2020-09-17 19:59:49.889096+01	2021-03-22 00:08:27.215763+01	Benin	Cotonou	Cotonou	O-9Y9NEG	card	12	29	1000.00	XOF	1	
2	2020-12-02 19:30:49.114751+01	2021-03-22 00:08:27.226025+01	Benin	Cotonou	Calavi 50 villa	O-QJKWBK	card	25	29	1000.00	XOF	1	
3	2021-02-10 13:41:04.290262+01	2021-03-22 00:08:27.232171+01	AO	CLAYMONT	2803 Philadelphia Pike	O-LYLNL4	card	1	33	34600.00	XOF	2	
4	2021-02-10 15:30:54.083102+01	2021-03-22 00:08:27.238818+01	AO	CLAYMONT	2803 Philadelphia Pike	O-MGHUK9	card	1	33	34600.00	XOF	2	
5	2021-02-10 15:38:38.293877+01	2021-03-22 00:08:27.24423+01	AO	CLAYMONT	2803 Philadelphia Pike	O-CIWIE5	card	1	33	22000.00	XOF	2	
6	2021-02-10 15:43:19.03551+01	2021-03-22 00:08:27.250509+01	US	CLAYMONT	2803 Philadelphia Pike	O-BNHHAW	card	1	33	22000.00	XOF	2	
7	2021-02-10 15:48:53.895818+01	2021-03-22 00:08:27.256583+01	US	CLAYMONT	2803 Philadelphia Pike	O-63XWHC	card	1	33	22000.00	XOF	2	
8	2021-02-10 16:16:21.650387+01	2021-03-22 00:08:27.261662+01	US	CLAYMONT	2803 Philadelphia Pike	O-3QTU1R	card	1	33	22000.00	XOF	2	
9	2021-02-10 16:21:42.781117+01	2021-03-22 00:08:27.266532+01	BJ	Cotonou	Akpakpa	O-F34NF8	card	21	23	1000.00	XOF	1	
10	2021-02-10 16:21:43.866788+01	2021-03-22 00:08:27.271383+01	BJ	Cotonou	Akpakpa	O-XNZ37W	card	21	23	1000.00	XOF	1	
11	2021-02-10 16:21:45.3167+01	2021-03-22 00:08:27.276332+01	BJ	Cotonou	Akpakpa	O-IA9DUI	card	21	23	1000.00	XOF	1	
12	2021-02-10 16:35:55.800018+01	2021-03-22 00:08:27.280814+01	BJ	Cotonou	Akpakpa	O-0UGJOK	card	21	23	1000.00	XOF	1	
13	2021-02-10 16:35:56.878057+01	2021-03-22 00:08:27.286003+01	BJ	Cotonou	Akpakpa	O-GK1SJB	card	21	23	1000.00	XOF	1	
14	2021-02-10 16:35:57.800076+01	2021-03-22 00:08:27.291658+01	BJ	Cotonou	Akpakpa	O-B0P30H	card	21	23	1000.00	XOF	1	
15	2021-02-10 16:37:35.350037+01	2021-03-22 00:08:27.296124+01	BJ	Cotonou	Akpakpa	O-VYZTNE	card	21	23	1000.00	XOF	1	
16	2021-02-10 18:03:17.744842+01	2021-03-22 00:08:27.30142+01	BJ	Cotonou	Akpakpa	O-C6CDDZ	card	21	23	1000.00	XOF	1	
17	2021-02-12 21:20:10.515968+01	2021-03-22 00:08:27.306118+01	BJ	Cotonou	Test	O-FSXRUD	card	26	23	1000.00	XOF	1	
18	2021-02-12 21:20:22.06322+01	2021-03-22 00:08:27.308848+01	BJ	Cotonou	Test	O-ERNWHW	card	26	23	1000.00	XOF	1	
19	2021-02-12 21:34:39.64372+01	2021-03-22 00:08:27.311653+01	BJ	Cotonou	Test	O-ORN40C	card	26	23	1000.00	XOF	1	
20	2021-02-12 21:46:12.37495+01	2021-03-22 00:08:27.314539+01	BJ	Cotonou	Test	O-GZOX0W	card	26	23	1000.00	XOF	1	
21	2021-02-12 22:52:16.764653+01	2021-03-22 00:08:27.317218+01	BJ	Cotonou	Test	O-Y75R4K	momo	26	23	1000.00	XOF	1	
22	2021-02-12 23:16:31.096578+01	2021-03-22 00:08:27.321089+01	BJ	Cotonou	Test	O-FIV8EZ	cash	26	23	1000.00	XOF	1	
23	2021-03-24 07:43:47.737182+01	2021-03-24 07:43:47.737212+01	AO	Test	Test	O-I4XVQV	cash	27	23	693.09	NGN	1	
24	2021-03-24 07:45:33.225987+01	2021-03-24 07:45:33.226018+01	AO	Test	Test	O-FQ4L0Q	cash	27	23	693.09	NGN	1	
25	2021-03-24 07:58:49.630543+01	2021-03-24 07:58:49.630576+01	AO	Test	Test	O-RPSQFW	cash	27	23	693.09	NGN	1	Cotonou
26	2021-03-24 08:07:56.42474+01	2021-03-24 08:07:56.424768+01	AO	Test	Test	O-S3R38I	cash	27	23	1386.19	NGN	1	Porto-Novo
\.


--
-- Data for Name: product_images; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.product_images (id, created_at, updated_at, url, product_id) FROM stdin;
359	2021-02-18 18:47:03.825388+01	2021-02-18 18:47:03.825429+01	https://kweek.sgp1.digitaloceanspaces.com/dev/e847e1d1-ff07-487f-b46f-db3cb0733a04-image-0.jpeg	311
361	2021-02-20 13:55:29.423635+01	2021-02-20 13:55:29.423676+01	https://kweek.sgp1.digitaloceanspaces.com/dev/77fbec0a-3c36-4a70-a2ab-941b182396dd-image-0.jpeg	312
364	2021-02-26 16:07:01.91778+01	2021-02-26 16:07:01.917834+01	https://kweek.sgp1.digitaloceanspaces.com/dev/ac3b3a0a-34c3-40b1-bd92-d27328e1880b-image-0.jpeg	310
366	2021-03-18 16:49:20.487847+01	2021-03-18 16:49:20.487886+01	https://kweek.sgp1.digitaloceanspaces.com/dev/2b8569e1-fa24-4a67-b447-da6a323b58e9-image-1.png	313
369	2021-03-24 09:43:00.549625+01	2021-03-24 09:43:00.549665+01	https://kweek.sgp1.digitaloceanspaces.com/dev/b0868d44-ec53-4c8d-ac6b-d812a9c41ebe-image-0.jpeg	316
367	2021-03-18 16:50:23.657637+01	2021-03-18 16:50:23.657685+01	https://kweek.sgp1.digitaloceanspaces.com/dev/0aa3dfc6-4bb7-496a-9684-5ad9265352c3-image-0.png	314
370	2021-03-24 09:48:52.967511+01	2021-03-24 09:48:52.967566+01	https://kweek.sgp1.digitaloceanspaces.com/dev/13fd9d21-df7c-4974-b9ae-0a4d81f0fd41-image-0.jpeg	317
368	2021-03-18 16:51:23.89486+01	2021-03-18 16:51:23.894899+01	https://kweek.sgp1.digitaloceanspaces.com/dev/9917ec08-962f-47c2-8921-fffba5b1cbf5-image-0.png	315
240	2020-09-16 19:08:30.340452+01	2020-09-16 19:08:30.340478+01	https://kweek.sgp1.digitaloceanspaces.com/production/a6e98a81-4e16-488f-a4a3-fd25e3a3dfef-image-0.png	238
283	2020-09-22 07:32:40.737377+01	2020-09-22 07:32:40.737411+01	https://kweek.sgp1.digitaloceanspaces.com/production/682bbb49-0d48-4363-88b0-f35dcd22b253-image-0.jpeg	260
284	2020-09-22 07:32:44.776101+01	2020-09-22 07:32:44.77613+01	https://kweek.sgp1.digitaloceanspaces.com/production/7d196496-bf3c-488e-a46d-6b56f30acb74-image-1.jpeg	260
304	2020-09-24 09:15:51.738235+01	2020-09-24 09:15:51.738265+01	https://kweek.sgp1.digitaloceanspaces.com/production/2f901fd8-88b6-4690-bea1-4f4099a4fbfe-image-0.jpeg	276
346	2021-01-07 04:16:47.987126+01	2021-01-07 04:16:47.987154+01	https://kweek.sgp1.digitaloceanspaces.com/production/84b7c28f-6aff-4715-ae9f-0dd23b5c86ee-image-0.jpeg	297
358	2021-01-07 05:22:56.693075+01	2021-01-07 05:22:56.693104+01	https://kweek.sgp1.digitaloceanspaces.com/production/e10aaece-f139-40ca-8196-473e03e67fab-image-0.png	309
260	2020-09-21 08:27:32.85139+01	2020-09-21 08:27:32.851418+01	https://kweek.sgp1.digitaloceanspaces.com/production/2b3f2177-4a82-4d75-8dc2-ab80569cd807-image-0.jpeg	249
285	2020-09-22 07:35:21.921788+01	2020-09-22 07:35:21.921816+01	https://kweek.sgp1.digitaloceanspaces.com/production/596f6d48-d86a-4c2c-b553-5e28e9d035bd-image-0.jpeg	261
286	2020-09-22 07:35:25.106447+01	2020-09-22 07:35:25.106475+01	https://kweek.sgp1.digitaloceanspaces.com/production/017b5ea6-03d0-48e7-ae94-f6cb7ae096d7-image-1.jpeg	261
305	2020-10-02 11:12:15.569389+01	2020-10-02 11:12:15.569416+01	https://kweek.sgp1.digitaloceanspaces.com/production/c7a32e66-187f-4e31-b51f-02d078e1f0d9-image-0.jpeg	278
306	2020-10-02 11:12:19.505442+01	2020-10-02 11:12:19.505469+01	https://kweek.sgp1.digitaloceanspaces.com/production/ff9f06a2-5a79-487a-a2ca-90e110f31b76-image-1.jpeg	278
307	2020-10-02 11:12:22.400451+01	2020-10-02 11:12:22.400478+01	https://kweek.sgp1.digitaloceanspaces.com/production/028c43a5-6097-4f16-87bf-2ee301547309-image-2.jpeg	278
308	2020-10-02 11:12:25.276799+01	2020-10-02 11:12:25.276825+01	https://kweek.sgp1.digitaloceanspaces.com/production/7eabd49b-5d70-433b-95d0-d2c09f0447df-image-3.jpeg	278
333	2020-10-10 11:23:06.032375+01	2020-10-10 11:23:06.032403+01	https://kweek.sgp1.digitaloceanspaces.com/production/5631459a-0803-4e2f-92c7-0169f369f872-image-0.jpeg	286
334	2020-10-10 11:23:08.547622+01	2020-10-10 11:23:08.547649+01	https://kweek.sgp1.digitaloceanspaces.com/production/73d9073b-2950-49b5-8069-2b39f0e622d5-image-1.jpeg	286
335	2020-10-10 11:23:13.293825+01	2020-10-10 11:23:13.293852+01	https://kweek.sgp1.digitaloceanspaces.com/production/bff48094-9d77-403d-b485-49ea16fe29e8-image-2.jpeg	286
347	2021-01-07 04:23:59.457932+01	2021-01-07 04:23:59.45796+01	https://kweek.sgp1.digitaloceanspaces.com/production/95f4e1ec-3c9c-45a7-9f09-32e4d6d27025-image-0.jpeg	298
243	2020-09-18 15:06:21.006623+01	2020-09-18 15:06:21.006654+01	https://kweek.sgp1.digitaloceanspaces.com/production/73e1cd03-e138-4de0-bb66-52f08dd88ccd-image-0.jpeg	240
261	2020-09-21 15:04:12.19609+01	2020-09-21 15:04:12.196118+01	https://kweek.sgp1.digitaloceanspaces.com/production/46320580-9dc5-4c96-a85a-75d11fc40c40-image-0.jpeg	250
262	2020-09-21 15:04:17.49007+01	2020-09-21 15:04:17.490101+01	https://kweek.sgp1.digitaloceanspaces.com/production/ba891265-2af9-46f7-83eb-0cccc32a7cfa-image-1.jpeg	250
287	2020-09-22 07:37:57.56064+01	2020-09-22 07:37:57.560668+01	https://kweek.sgp1.digitaloceanspaces.com/production/f8cdabf5-d60a-4702-9275-dbe8f594f1d2-image-0.jpeg	262
288	2020-09-22 07:38:00.90952+01	2020-09-22 07:38:00.909548+01	https://kweek.sgp1.digitaloceanspaces.com/production/68ef2717-cbfa-4f16-ad3a-5a568d4863d5-image-1.jpeg	262
309	2020-10-02 11:24:27.64493+01	2020-10-02 11:24:27.644959+01	https://kweek.sgp1.digitaloceanspaces.com/production/3262e857-39c2-4847-8135-f7755022446a-image-0.jpeg	279
310	2020-10-02 11:24:31.017418+01	2020-10-02 11:24:31.017445+01	https://kweek.sgp1.digitaloceanspaces.com/production/883e88b1-da60-4dfd-91bd-d2b67b6ac8e0-image-1.jpeg	279
311	2020-10-02 11:24:33.655958+01	2020-10-02 11:24:33.655985+01	https://kweek.sgp1.digitaloceanspaces.com/production/d23922db-7365-4b17-bb5e-4f954076c9dd-image-2.jpeg	279
336	2020-12-02 07:17:43.226557+01	2020-12-02 07:17:43.226585+01	https://kweek.sgp1.digitaloceanspaces.com/production/93647d6b-e0bd-4d6c-a60c-6b790546c80b-image-0.jpeg	287
348	2021-01-07 04:29:45.647468+01	2021-01-07 04:29:45.647496+01	https://kweek.sgp1.digitaloceanspaces.com/production/9a1cf73f-d625-4d34-a46f-7e69ff047a61-image-0.jpeg	299
233	2020-09-14 19:38:36.177855+01	2020-09-14 19:38:36.177882+01	https://kweek.sgp1.digitaloceanspaces.com/production/f1c0ec4b-110c-426c-b72b-a6210830d184-image-0.jpeg	231
244	2020-09-18 15:59:45.492947+01	2020-09-18 15:59:45.492976+01	https://kweek.sgp1.digitaloceanspaces.com/production/d584be41-7e04-40e5-a0cc-cf5186511cf7-image-0.jpeg	241
289	2020-09-22 07:40:15.907159+01	2020-09-22 07:40:15.907189+01	https://kweek.sgp1.digitaloceanspaces.com/production/b7471152-56ad-4751-ba36-4781db4e3e55-image-0.jpeg	263
290	2020-09-22 07:40:17.77185+01	2020-09-22 07:40:17.771878+01	https://kweek.sgp1.digitaloceanspaces.com/production/11f9a74b-fd36-4852-a5ae-bd051357dd8f-image-1.jpeg	263
312	2020-10-02 11:30:28.985912+01	2020-10-02 11:30:28.985939+01	https://kweek.sgp1.digitaloceanspaces.com/production/c1e78697-8073-4be1-ad20-93a2b3f6ac48-image-0.jpeg	280
313	2020-10-02 11:30:31.945598+01	2020-10-02 11:30:31.945625+01	https://kweek.sgp1.digitaloceanspaces.com/production/1221ec55-4070-4bf7-8bd0-a2411e0def95-image-1.jpeg	280
314	2020-10-02 11:30:34.02201+01	2020-10-02 11:30:34.022037+01	https://kweek.sgp1.digitaloceanspaces.com/production/5e331a4d-0305-4e49-9e25-c7d92b42ad5e-image-2.jpeg	280
315	2020-10-02 11:30:36.407363+01	2020-10-02 11:30:36.40739+01	https://kweek.sgp1.digitaloceanspaces.com/production/856e5373-b3c3-4c56-a31a-ad2c241fe63e-image-3.jpeg	280
316	2020-10-02 11:30:40.203071+01	2020-10-02 11:30:40.203097+01	https://kweek.sgp1.digitaloceanspaces.com/production/18d4f7a6-63ae-4986-a186-d47d8f48c0b4-image-4.jpeg	280
337	2020-12-02 07:38:50.720777+01	2020-12-02 07:38:50.720805+01	https://kweek.sgp1.digitaloceanspaces.com/production/fbd7c548-af28-4cd0-b5ed-6401ed0e4b88-image-0.jpeg	288
349	2021-01-07 04:32:39.08896+01	2021-01-07 04:32:39.088988+01	https://kweek.sgp1.digitaloceanspaces.com/production/bda2593f-5106-440b-b5d6-212dbf0d2115-image-0.jpeg	300
234	2020-09-14 19:42:18.016931+01	2020-09-14 19:42:18.016959+01	https://kweek.sgp1.digitaloceanspaces.com/production/452dadf6-9d00-4211-86a9-0a18fba210f4-image-0.jpeg	232
245	2020-09-19 07:59:39.054547+01	2020-09-19 07:59:39.054577+01	https://kweek.sgp1.digitaloceanspaces.com/production/a7bea1e0-5911-4b8d-b228-dab878bd12cd-image-0.jpeg	242
270	2020-09-22 06:55:48.630055+01	2020-09-22 06:55:48.630083+01	https://kweek.sgp1.digitaloceanspaces.com/production/3203d98a-4cb4-42ff-ba3b-f58d1fa5a5f8-image-0.jpeg	252
271	2020-09-22 06:55:50.603537+01	2020-09-22 06:55:50.603567+01	https://kweek.sgp1.digitaloceanspaces.com/production/b6a53d4a-65ca-421e-8668-86334a135cde-image-1.jpeg	252
291	2020-09-22 07:42:40.630828+01	2020-09-22 07:42:40.630857+01	https://kweek.sgp1.digitaloceanspaces.com/production/fb2c429a-04d8-4798-a968-67373adf4a67-image-0.jpeg	264
292	2020-09-22 07:42:42.814062+01	2020-09-22 07:42:42.81409+01	https://kweek.sgp1.digitaloceanspaces.com/production/58e65680-1c94-4447-8c00-e9a9b003094d-image-1.jpeg	264
317	2020-10-02 11:54:12.201787+01	2020-10-02 11:54:12.201813+01	https://kweek.sgp1.digitaloceanspaces.com/production/0dfc302b-8155-45cf-a16d-cae641a261d1-image-0.jpeg	281
318	2020-10-02 11:54:15.24153+01	2020-10-02 11:54:15.241558+01	https://kweek.sgp1.digitaloceanspaces.com/production/db23679c-a72a-431b-81ee-7931976e88cb-image-1.jpeg	281
319	2020-10-02 11:54:17.677499+01	2020-10-02 11:54:17.677525+01	https://kweek.sgp1.digitaloceanspaces.com/production/674adecd-4d0b-431d-ac3a-b67ecf0f0a20-image-2.jpeg	281
320	2020-10-02 11:54:20.246992+01	2020-10-02 11:54:20.247019+01	https://kweek.sgp1.digitaloceanspaces.com/production/3aadd71c-d0a7-4a52-b9ab-d382d8b4de96-image-3.jpeg	281
338	2020-12-02 18:27:17.717306+01	2020-12-02 18:27:17.717333+01	https://kweek.sgp1.digitaloceanspaces.com/production/9708770f-50fa-49d8-a8d8-92ba8fd7a0fa-image-0.jpeg	289
350	2021-01-07 04:34:19.191583+01	2021-01-07 04:34:19.191609+01	https://kweek.sgp1.digitaloceanspaces.com/production/1bdd1958-dadb-42ec-b862-9f35b82a8fa7-image-0.jpeg	301
235	2020-09-14 19:43:57.475596+01	2020-09-14 19:43:57.475623+01	https://kweek.sgp1.digitaloceanspaces.com/production/cc2d4fa3-a15d-4c39-b63e-1ffec21ba34a-image-0.jpeg	233
246	2020-09-19 16:46:29.654569+01	2020-09-19 16:46:29.654596+01	https://kweek.sgp1.digitaloceanspaces.com/production/34d23ca5-9ead-4cb8-944a-466a6c204609-image-0.jpeg	243
272	2020-09-22 06:58:31.84844+01	2020-09-22 06:58:31.848473+01	https://kweek.sgp1.digitaloceanspaces.com/production/0106eee2-1749-48dc-90ba-b1173b053b2e-image-0.jpeg	253
293	2020-09-22 07:45:59.291957+01	2020-09-22 07:45:59.291987+01	https://kweek.sgp1.digitaloceanspaces.com/production/c7622709-a19c-4848-9693-4421d659475f-image-0.jpeg	265
294	2020-09-22 07:46:03.231727+01	2020-09-22 07:46:03.231755+01	https://kweek.sgp1.digitaloceanspaces.com/production/c571377d-ce5c-4979-924a-82c157ad30e0-image-1.jpeg	265
321	2020-10-02 11:58:07.018009+01	2020-10-02 11:58:07.018036+01	https://kweek.sgp1.digitaloceanspaces.com/production/c3258bf3-07ee-416f-8358-20a47f1e2fa5-image-0.webp	281
322	2020-10-02 11:58:09.405753+01	2020-10-02 11:58:09.40578+01	https://kweek.sgp1.digitaloceanspaces.com/production/3a645ac9-794c-48cf-8ac5-7bb5b777aaa9-image-1.webp	281
339	2020-12-31 12:59:34.074719+01	2020-12-31 12:59:34.074746+01	https://kweek.sgp1.digitaloceanspaces.com/production/72408773-1830-4f6b-907f-9cf18eca0710-image-0.jpeg	290
351	2021-01-07 04:37:17.493427+01	2021-01-07 04:37:17.493454+01	https://kweek.sgp1.digitaloceanspaces.com/production/911faf91-ad97-4c7a-98bd-e40434eba884-image-0.jpeg	302
247	2020-09-19 16:46:29.945479+01	2020-09-19 16:46:29.945507+01	https://kweek.sgp1.digitaloceanspaces.com/production/97cac866-88bd-4fd1-86a8-6f182de11752-image-0.jpeg	244
273	2020-09-22 07:03:17.791211+01	2020-09-22 07:03:17.791239+01	https://kweek.sgp1.digitaloceanspaces.com/production/c8d7cb2c-7dca-4141-a67b-27b9c4ad5292-image-0.jpeg	254
274	2020-09-22 07:03:20.085269+01	2020-09-22 07:03:20.085298+01	https://kweek.sgp1.digitaloceanspaces.com/production/9e82c1a1-9c57-4684-ab8c-20068aa56014-image-1.jpeg	254
323	2020-10-02 12:08:05.886308+01	2020-10-02 12:08:05.886336+01	https://kweek.sgp1.digitaloceanspaces.com/production/88fb0b34-9cda-4786-a23b-46bc9b6792ea-image-0.webp	279
340	2020-12-31 13:03:48.037064+01	2020-12-31 13:03:48.037091+01	https://kweek.sgp1.digitaloceanspaces.com/production/3d4a5a5c-2f3b-4aea-a38c-fcd9217d8ff4-image-0.jpeg	291
352	2021-01-07 04:39:33.071355+01	2021-01-07 04:39:33.071383+01	https://kweek.sgp1.digitaloceanspaces.com/production/bb8bb2ac-44aa-4ea6-b39d-a567369496b4-image-0.jpeg	303
236	2020-09-14 19:54:09.54673+01	2020-09-14 19:54:09.546758+01	https://kweek.sgp1.digitaloceanspaces.com/production/764a6c11-28a5-4226-ae63-1673fc91eda6-image-0.jpeg	234
248	2020-09-19 17:00:32.370771+01	2020-09-19 17:00:32.370798+01	https://kweek.sgp1.digitaloceanspaces.com/production/0c6e266d-6b60-46c5-89df-e330697a12f7-image-0.jpeg	245
275	2020-09-22 07:06:31.37671+01	2020-09-22 07:06:31.37674+01	https://kweek.sgp1.digitaloceanspaces.com/production/64891db1-7e0a-4474-b3ba-38d02c32d93f-image-0.jpeg	255
276	2020-09-22 07:06:33.339062+01	2020-09-22 07:06:33.339091+01	https://kweek.sgp1.digitaloceanspaces.com/production/ec6fb1cc-ea00-40ca-a452-97a904324127-image-1.jpeg	255
299	2020-09-22 08:08:01.971357+01	2020-09-22 08:08:01.971388+01	https://kweek.sgp1.digitaloceanspaces.com/production/adf80640-a967-4e05-b80b-b36b7ad21589-image-0.jpeg	267
324	2020-10-07 12:32:32.588531+01	2020-10-07 12:32:32.588559+01	https://kweek.sgp1.digitaloceanspaces.com/production/85493c4a-6d48-4eb8-a2fb-ab990221c5d3-image-0.jpeg	282
353	2021-01-07 04:44:01.971679+01	2021-01-07 04:44:01.971706+01	https://kweek.sgp1.digitaloceanspaces.com/production/96ae5c66-ff81-447b-aa48-61da2f08a010-image-0.jpeg	304
237	2020-09-14 19:56:31.602304+01	2020-09-14 19:56:31.602333+01	https://kweek.sgp1.digitaloceanspaces.com/production/b3d14e5a-1cd0-4eea-8d88-416f131a208a-image-0.jpeg	235
249	2020-09-19 17:03:29.180499+01	2020-09-19 17:03:29.180528+01	https://kweek.sgp1.digitaloceanspaces.com/production/94059f08-ccf9-4ee8-8ae2-db7265959d25-image-0.jpeg	246
277	2020-09-22 07:09:30.206797+01	2020-09-22 07:09:30.206824+01	https://kweek.sgp1.digitaloceanspaces.com/production/eae9d8a3-2a34-4683-80f3-0152ca408aac-image-0.jpeg	256
278	2020-09-22 07:09:36.745827+01	2020-09-22 07:09:36.745856+01	https://kweek.sgp1.digitaloceanspaces.com/production/4c9cc2a2-cecd-4523-a4b5-8d6b5c021cd8-image-1.jpeg	256
300	2020-09-22 21:39:38.915067+01	2020-09-22 21:39:38.915096+01	https://kweek.sgp1.digitaloceanspaces.com/production/55654a21-4652-4046-a364-ba0e7bfa45c0-image-0.jpeg	272
325	2020-10-07 12:36:36.325542+01	2020-10-07 12:36:36.32557+01	https://kweek.sgp1.digitaloceanspaces.com/production/eb4cf25d-70b6-4283-a966-c4647a7c9443-image-0.jpeg	283
342	2021-01-05 20:01:39.926273+01	2021-01-05 20:01:39.9263+01	https://kweek.sgp1.digitaloceanspaces.com/production/16e868ba-cef1-4524-8e6c-11288f6f4e5b-image-0.png	293
354	2021-01-07 05:00:37.326594+01	2021-01-07 05:00:37.326621+01	https://kweek.sgp1.digitaloceanspaces.com/production/44e87e29-000c-4e8f-a080-3be6abe7af4e-image-0.png	305
250	2020-09-19 17:05:46.991784+01	2020-09-19 17:05:46.991824+01	https://kweek.sgp1.digitaloceanspaces.com/production/097f0df6-1f65-4a38-9072-21c1688914b4-image-0.jpeg	246
252	2020-09-19 17:05:50.688221+01	2020-09-19 17:05:50.688249+01	https://kweek.sgp1.digitaloceanspaces.com/production/d4876dfc-2df5-414b-8366-cee30ea9a7a9-image-1.jpeg	246
254	2020-09-19 17:05:52.956275+01	2020-09-19 17:05:52.956302+01	https://kweek.sgp1.digitaloceanspaces.com/production/ac55ca7f-8766-4ff8-8549-60b0cc675687-image-2.jpeg	246
279	2020-09-22 07:13:47.461006+01	2020-09-22 07:13:47.461034+01	https://kweek.sgp1.digitaloceanspaces.com/production/98efe9d6-cfd6-4d9e-83a9-d638d9cd39e9-image-0.jpeg	257
280	2020-09-22 07:14:02.548433+01	2020-09-22 07:14:02.54846+01	https://kweek.sgp1.digitaloceanspaces.com/production/35476d99-757d-4ccd-8eca-d86c8580fd8a-image-1.jpeg	257
301	2020-09-23 17:32:30.906116+01	2020-09-23 17:32:30.906146+01	https://kweek.sgp1.digitaloceanspaces.com/production/cee65def-ef60-4e45-b6ed-082bed1c7b80-image-0.jpeg	273
326	2020-10-08 11:23:08.369288+01	2020-10-08 11:23:08.36932+01	https://kweek.sgp1.digitaloceanspaces.com/production/d23da927-8043-4ed7-a760-fb21076a781b-image-0.jpeg	284
327	2020-10-08 11:23:11.8674+01	2020-10-08 11:23:11.867427+01	https://kweek.sgp1.digitaloceanspaces.com/production/9989b7fc-db01-459c-9923-1e6c6f3c89a5-image-1.jpeg	284
355	2021-01-07 05:04:02.20759+01	2021-01-07 05:04:02.207617+01	https://kweek.sgp1.digitaloceanspaces.com/production/bbb8ea5b-cb7d-411f-9cb7-e17ba222646c-image-0.png	306
251	2020-09-19 17:05:48.749649+01	2020-09-19 17:05:48.749676+01	https://kweek.sgp1.digitaloceanspaces.com/production/47647dea-8849-4266-929a-5114fc7fe086-image-0.jpeg	246
253	2020-09-19 17:05:52.371468+01	2020-09-19 17:05:52.371496+01	https://kweek.sgp1.digitaloceanspaces.com/production/3ff30bc1-57e9-4abf-acea-6d828e7a67a3-image-1.jpeg	246
255	2020-09-19 17:05:54.464477+01	2020-09-19 17:05:54.464505+01	https://kweek.sgp1.digitaloceanspaces.com/production/2822d674-8d14-403f-85d0-db5c159b97a7-image-2.jpeg	246
281	2020-09-22 07:18:48.307158+01	2020-09-22 07:18:48.307187+01	https://kweek.sgp1.digitaloceanspaces.com/production/7ac6f8f9-b60d-4f01-a745-b51c635a5efc-image-0.jpeg	258
302	2020-09-23 17:35:39.496566+01	2020-09-23 17:35:39.496595+01	https://kweek.sgp1.digitaloceanspaces.com/production/c16894fa-7530-4a00-b704-3015873e1065-image-0.jpeg	274
328	2020-10-08 17:21:45.240504+01	2020-10-08 17:21:45.240532+01	https://kweek.sgp1.digitaloceanspaces.com/production/483900ad-6426-49cd-86f8-e21141b04e67-image-0.jpeg	285
356	2021-01-07 05:12:58.374885+01	2021-01-07 05:12:58.374913+01	https://kweek.sgp1.digitaloceanspaces.com/production/f96ca1e4-ece3-439c-a0c9-75a09c60a35c-image-0.png	307
256	2020-09-19 22:50:30.635776+01	2020-09-19 22:50:30.635804+01	https://kweek.sgp1.digitaloceanspaces.com/production/1fbca2d1-52b4-4afb-95dc-cc5332103b57-image-0.jpeg	247
257	2020-09-19 22:50:32.944125+01	2020-09-19 22:50:32.944153+01	https://kweek.sgp1.digitaloceanspaces.com/production/26080adb-8e17-4a9e-8f76-5d6eca4177e7-image-1.jpeg	247
258	2020-09-19 22:50:35.186789+01	2020-09-19 22:50:35.186816+01	https://kweek.sgp1.digitaloceanspaces.com/production/eb13bebd-0a26-4bb3-9d7c-1f283a32ddb6-image-2.jpeg	247
282	2020-09-22 07:29:41.835199+01	2020-09-22 07:29:41.835228+01	https://kweek.sgp1.digitaloceanspaces.com/production/875d874c-3b3e-484b-b57a-96eecec351da-image-0.jpeg	259
303	2020-09-23 17:50:25.077593+01	2020-09-23 17:50:25.077621+01	https://kweek.sgp1.digitaloceanspaces.com/production/64f785d6-a670-40b9-b0a5-28f1bd8babe9-image-0.jpeg	275
329	2020-10-10 11:17:55.881363+01	2020-10-10 11:17:55.881392+01	https://kweek.sgp1.digitaloceanspaces.com/production/15a14060-0602-4bc1-b294-5ce9d93502b2-image-0.jpeg	286
345	2021-01-06 09:25:27.426291+01	2021-01-06 09:25:27.426319+01	https://kweek.sgp1.digitaloceanspaces.com/production/710e9dbf-56a0-4d50-81af-499703cd0354-image-0.png	295
357	2021-01-07 05:16:52.979379+01	2021-01-07 05:16:52.979406+01	https://kweek.sgp1.digitaloceanspaces.com/production/0bbcefea-0769-40da-8a07-44d5df1518cf-image-0.png	308
239	2020-09-16 10:20:20.032196+01	2020-09-16 10:20:20.032225+01	https://kweek.sgp1.digitaloceanspaces.com/production/a56b894c-54b8-47a6-bea3-092df769b324-image-0.jpeg	237
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.products (id, created_at, updated_at, name, description, slug, shop_id, available_units, weight, price, price_currency) FROM stdin;
313	2021-03-18 16:49:07.166664+01	2021-03-24 00:33:30.273935+01	Another one	\N	another-one-VpA	23	\N	3.000	1000.00	NGN
238	2020-09-16 19:08:26.250116+01	2021-03-21 19:03:37.545182+01	Cake	Fuzuiei\nHksloe\nGuod😊	cake-y3w	33	10	1.000	1000.00	XOF
249	2020-09-21 08:27:00.395926+01	2021-03-21 19:03:37.545182+01	Mèche naturelle	Perruque frontale 180 disponible	meche-naturelle-JzQ	40	1	1.000	30000.00	XOF
316	2021-03-24 09:42:53.137425+01	2021-03-24 09:42:53.137467+01	Pizza	Jambon, fromage, champignon, calzone	pizza-CIs	25	\N	1.000	5000.00	XOF
242	2020-09-19 07:59:09.074377+01	2021-03-21 19:03:37.545182+01	Inside life	Tous les couleurs sont disponibles	inside-life--YU	34	10	1.000	20000.00	XOF
317	2021-03-24 09:48:47.232201+01	2021-03-24 09:48:47.232227+01	Cocktail	Agrume et liqueurs	cocktail-aLM	25	\N	1.000	2500.00	XOF
260	2020-09-22 07:32:37.35733+01	2021-03-21 19:03:37.545182+01	Toshiba c660	*PC Toshiba c660* 💻\nProcesseur *Intel dual core* \nRAM 4 | HDD 3200\nÉcran 15 pouce  Avec pavé numérique  | Couleur Noire 🔥	toshiba-c660-Ng0	37	1	2.000	130000.00	XOF
289	2020-12-02 18:27:00.553381+01	2021-03-21 19:03:37.545182+01	Icy	Ice	icy-Rs8	29	10000	1.000	200000.00	XOF
309	2021-01-07 05:22:47.978559+01	2021-03-21 19:03:37.545182+01	BLEU DE CHARNEL (1flacon de 6 ml)	*Bleu de Chanel* est un Senteur pour les hommes, aussi fraiche, qu’élégante qui ne ressemble à aucune autre. Bleu de Chanel est une fragrance mystérieuse qui enveloppe l’être d’une aura irrésistible. L’homme Chanel refuse l’uniformité, et s’affranchit de tous les codes, c’est avant tout un homme charismatique. Sa composition révèle un esprit libre, déterminé, et plus que tout, anticonformiste. Elle débute alors par un accord hespéridé composé de citron, de pamplemousse et d’orange, accord rehaussé par la menthe poivrée, les baies de rose et la noix de muscade. *Soyez Exceptionnel*	bleu-de-charnel-1flacon-de-6-ml-Au4	58	145	1.000	2500.00	XOF
298	2021-01-07 04:23:56.609026+01	2021-03-21 19:03:37.545182+01	10 Douzaines De Flacons De 6 Ml Des Huiles De Parfum Concentrée Originale	Livraison partout dans le monde seulement en 3 jours.\nMélange de 20 différentes marques au maximum\nFaîtes nous un message au +229 97462924 pour nous notifier vos choix de marques.	10-douzaines-des-huiles-de-parfum-concentree-qrI	58	592	4.000	128250.00	XOF
271	2020-09-22 10:23:05.211629+01	2021-03-21 19:03:37.545182+01	Mèches naturelle	Mèches naturelles avec closure	meches-naturelle-zv8	40	1	1.000	30000.00	XOF
282	2020-10-07 12:32:28.25741+01	2021-03-21 19:03:37.545182+01	Durag Original en soie	Produits 100% original \nQualité supérieure \nMatière en soie	durag-original-en-soie-i60	48	10	0.100	4000.00	XOF
293	2021-01-05 20:01:35.647654+01	2021-03-21 19:03:37.545182+01	Test	Une description	test-2Qs	59	10	1.000	100.00	XOF
304	2021-01-07 04:43:59.018802+01	2021-03-21 19:03:37.545182+01	12 Flacons de 6 ml ( 1 paquet) des huiles de parfum concentrée Originale	Livraison seulement au partout au Bénin en 24h.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	12-flacons-de-6-ml-1-paquet-des-huiles-de-parfum-concentree-originale-0e4	58	10143	1.000	17500.00	XOF
250	2020-09-21 15:03:19.550748+01	2021-03-21 19:03:37.545182+01	ENVY TS 15 notebook	👑 *ENVY TS 15 Notebook*\nRAM *12Gb*\nDD *1To*\nProcesseur *Intel Core i7*\nFréquence *2.40GHz*\nMémoire graphique *NVIDIA Gforce 8gb total* \nMémoire *vidéo dédiée  2Gb*\nClavier *lumineux* ☀️\nÉcran 15.6 avec pavé numérique	envy-ts-15-notebook-8G4	37	1	2.000	300000.00	XOF
261	2020-09-22 07:35:09.184371+01	2021-03-21 19:03:37.545182+01	Toshiba	💧Disque dure 250gb\n💧Ram 2gb\n💧Autonomie 3h\n💧Ecran 15.6 sans pavé numérique\n Avec lecteur DVD, WIFI	toshiba-utw	37	1	2.000	95000.00	XOF
272	2020-09-22 21:39:31.972686+01	2021-03-21 19:03:37.545182+01	Livraison de repas de colis sur Cotonou et environs	Livraison à partir  de 500 pour les repas et a partir de 1000f pour les colis	livraison-de-repas-de-colis-sur-cotonou-et-environs-I5M	41	0	1.000	500.00	XOF
283	2020-10-07 12:36:07.618731+01	2021-03-21 19:03:37.545182+01	Montre casio tactile	Cadran tactile \nRésistant à l’eau \nOriginal	montre-casio-tactile-WV8	48	50	0.400	8000.00	XOF
305	2021-01-07 05:00:26.094957+01	2021-03-21 19:03:37.545182+01	SCANDAL ( 1 flacon de 6 ml)	*Scandal* est un parfum qui joue sur deux registres olfactifs différents. Il est à la fois chypré tout en étant particulièrement gourmand. Il tient son aspect sucré de la présence du miel au centre de sa recette. Néanmoins, il ose travailler l'odeur gourmande de façon résolument moderne. Ainsi, *Scandal n'est pas un parfum pour les « petites filles »*. Il s'adresse aux femmes qui s'assument et affiche un sillage puissant et élégant. Le tout révèle des nuances chaleureuses, parfois profondes et souvent boisées. La féminité de Scandal ressurgit de toutes parts et s'exprime notamment au travers d'un énorme bouquet de fleurs blanches. *Vivez vos fantasmes sans limite.*	scandal-1-flacon-de-6-ml-RoE	58	10143	1.000	2500.00	XOF
240	2020-09-18 15:05:36.076138+01	2021-03-21 19:03:37.545182+01	Inside Life	Inside Life T-shirt \nBy Capitaine Jago-off\n#Insidelife	inside-life-sLU	34	100	1.000	15000.00	XOF
262	2020-09-22 07:37:53.935431+01	2021-03-21 19:03:37.545182+01	SAMSUNG	*PC SAMSUNG* 💻\nProcesseur *Intel CORE I3* \nRAM 4 | HDD 500 | Carte graphique NVIDIA 1gb\nÉcran 15 pouce  Avec pavé numérique  | Couleur Noire-grise 🔥	samsung-COI	37	1	2.000	155000.00	XOF
273	2020-09-23 17:32:19.041393+01	2021-03-21 19:03:37.545182+01	Carte mémoire	Bonne qualité	carte-memoire-pFY	43	109	1.000	7000.00	XOF
284	2020-10-08 11:22:10.080237+01	2021-03-21 19:03:37.545182+01	Modern skirt	Pour la plage, vos sorties en copines, de petites courses😉. Possibilité de les avoir en couleur unie et en d’autres motifs. Disponibles sur commande	skirt-1-vb8	49	1	1.000	8000.00	XOF
295	2021-01-06 09:25:11.583883+01	2021-03-21 19:03:37.545182+01	HUGO BOSS (1 flacons de 6 ml)	*HUGO BOSS*  incarne l'aspiration de l'homme d'aujourd'hui à se reconnecter avec ce qui lui est essentiel. Celui qui navigue à travers les différents rôles de sa vie, que ce soit dans la poursuite du succès ou dans la recherche de l'équilibre et de l'authenticité. Un parfum énergisant et sensuel qui allie la fraîcheur des notes d'agrumes et l'intensité des notes aromatiques et boisées. *SOYEZ UN HOMME DE GRAND VISION*\n\n10 douzaines	hugo-boss-n-o	58	10143	1.000	2500.00	XOF
287	2020-12-02 07:16:33.846176+01	2021-03-21 19:03:37.545182+01	Pains 🙂🙂Extra	Un pain super bon	pains-extra-yQI	29	10000	1.000	163000.00	XOF
306	2021-01-07 05:03:43.091024+01	2021-03-21 19:03:37.545182+01	LA NUIT DE L'HOMME ( 1 flacon de 6 ml)	*LA NUIT DE L'HOMME* est un Senteur qui se porte dès la nuit tombée. Là, tout commence, là tout devient permis et la séduction impose ses propres codes. Mystérieux, mais terriblement attirant, il aide l'homme à pousser ici la séduction à son apogée. *La Nuit de l’Homme* un Senteur, une virilité hors norme pour des hommes modernes. Il est devenue un grand succès en jouant toujours dans le registre de la séduction masculine. Il pousse l’interdit encore plus loin. Ce Senteur nous emmène au cœur de la capitale, dans ses rues pavées et mystérieuses. La nuit ne fait que commencer et pourtant l’homme a dévoilé sa meilleure arme, la séduction sans limites. Ici, *La nuit de l'homme* a souhaité lever le voile sur les interdits, aller à l’encontre des conventions, une fois n’étant pas coutume… *Jouez aux interdits avec LA NUIT DE L'HOMME*	la-nuit-de-lhomme-1-flacon-de-6-ml-b9c	58	10143	1.000	2500.00	XOF
241	2020-09-18 15:59:42.837381+01	2021-03-21 19:03:37.545182+01	Ecouteur bluetooth	Porté 10m	ecouteur-bluetooth-HnQ	35	500	0.300	20000.00	XOF
252	2020-09-22 06:55:44.928738+01	2021-03-21 19:03:37.545182+01	Lenovo Thinkpad X1 Carbon X180	🍎 *Lenevo ThinkPad X1 Carbon X180° ultra slim et rapide*\n🍓 *Avec lecteur de Carte SIM😍*\n🍓 *Possibilité de partager la connexion avec d'autre appareils😍*\n🍓 *Le PC deviens wifi😍*\n🍅 *Clavier rétro éclairé avancé😍*\n🍅 SSD *180Go* \n🍅 RAM *8Go* \n🍅 Processeur Intel *core i5* \n🍅 Fréquence *2,4Ghz* \n🍅 Sans *lecteur DVD* \n🍅 Sans pavé numérique\n🍅 *Écran 14''* \n🍅 *Touche de fonction tactile*	lenovo-thinkpad-x1-carbon-x180-LtQ	37	1	1.500	285000.00	XOF
263	2020-09-22 07:40:11.26211+01	2021-03-21 19:03:37.545182+01	LENOVO SLIM IDEAPAD 80T7	*LENOVO SLIM IDEAPAD 80T7*\nDisque dur *500gb*\nRam *4gb*\nProcesseur *Intel dualcord*\nFréquence *2 x 1.60Ghz*\nÉcran 15,6 *avec pavé numérique*	lenovo-slim-ideapad-80t7-Fw8	37	1	1.500	175000.00	XOF
274	2020-09-23 17:35:25.63688+01	2021-03-21 19:03:37.545182+01	Écoute sans fil	Clé originale	ecoute-sans-fil-3KE	43	100	5.000	15000.00	XOF
285	2020-10-08 17:20:56.986108+01	2021-03-21 19:03:37.545182+01	L'art de négocier avec la méthode Havard	Livre pour vous permettre d'avoir des aptitudes de négociation. Recommandé pour les étudiants en marketing.	lart-de-negocier-avec-la-methode-havard-M-U	54	5	0.500	7000.00	XOF
277	2020-09-29 17:56:21.378987+01	2021-03-21 19:03:37.545182+01	Pc et divers	Puissants	pc-et-divers-1Oo	39	0	2.000	180000.00	XOF
288	2020-12-02 07:38:47.37311+01	2021-03-21 19:03:37.545182+01	Special 🤩🤩	So fine, so good	special-ekk	29	10000000	1.000	218000.00	XOF
307	2021-01-07 05:12:10.940533+01	2021-03-21 19:03:37.545182+01	BLACK OPIUM (1 flacon de 6 ml)	*BLACK OPIUM* Vivre sa vie au superlatif… Suivre ses envies et son instinct, briser les codes et assumer sa singularité. Icône puissante et femme indépendante à la beauté magnétique, la femme Black Opium dessine sa vie selon ses propres règles. Charismatique et sensuelle, elle éveille à son passage un désir incontrôlable. Succombez à son appel, laissez-vous hypnotiser par l’addiction . BLACK OPIUM, senteur pour femme vibrante, terriblement addictif. Une dose d’adrénaline qui révèle un sillage irrésistible. *Soyez une femme d'action*	black-opium-1-flacon-de-6-ml-wzY	58	10143	1.000	2500.00	XOF
253	2020-09-22 06:58:26.71238+01	2021-03-21 19:03:37.545182+01	MEDION	MEDION\nWin 7\nDD 250 gb\nCore 2 duo\nFréquence 1.83ghz \nRAM 3\nMémoire dédiée 128 Mo	medion-4Bc	37	1	2.000	110000.00	XOF
264	2020-09-22 07:42:33.8438+01	2021-03-21 19:03:37.545182+01	DELL Intel core i5	⚡ _PC Dell ™️ Processeur Intel Corei5 | HDD 500gb Ram 4gb | Fréquence_ *2.60Ghz* |	dell-intel-core-i5-jPk	37	1	2.000	195000.00	XOF
275	2020-09-23 17:50:06.906168+01	2021-03-21 19:03:37.545182+01	Clé	Très bonne qualité	cle-r0g	43	100	1.000	15000.00	XOF
286	2020-10-10 11:17:45.25158+01	2021-03-21 19:03:37.545182+01	Montre rechargeable RoHS	Cette montre est un model de série de la marque RoHS. Elle est faite de silicone, rechargeable et dispose des fonctions suivantes : charge par USB, une tension d’alimentation de 5V, une batterie de 50mAh, un pédomètre, un écran d’affichage LED et un mode de vibration moteur plat 8*2mm. Disponible en plusieurs couleurs.	montre-rechargeable-rohs-o_g	47	50	1.000	7000.00	XOF
297	2021-01-07 04:16:44.206644+01	2021-03-21 19:03:37.545182+01	5 Douzaines De Flacons De 6 Ml Des Huiles De Parfum Concentrée Originale	Livraison seulement au Bénin\nMélange de 10 différentes marques au maximum\nLaissez vos choix en nous faisant un message au +22997462924	5-douzaines-des-huiles-parfum-concentree-Rag	58	592	2.000	65000.00	XOF
308	2021-01-07 05:16:25.221272+01	2021-03-21 19:03:37.545182+01	TERRE D'HERMÈS (1 flacon de 6 ml)	*Terre d'Hermès* est un Senteurs Boisé Chypré avec ses notes de tête, Orange et Pamplemousse, il incarne le regard que porte la marque sur les hommes : complexes et simples à la fois, les pieds ancrés dans la réalité sans jamais renoncer à ses rêves, l'homme portant Terre d'Hermès devient une allégorie de la nature, qui offre un visage uni et harmonieux tout en affirmant une identité forgée par sa complexité. *Soyez Réaliste.*	terre-dhermes-1-flacon-de-6-ml-Zpc	58	765	1.000	2500.00	XOF
243	2020-09-19 16:46:27.19017+01	2021-03-21 19:03:37.545182+01	Expedion et réception de colis,courriers et marchandises.	-Envoyez  et recevez vos colis et courriers express partout dans le monde entier !  \n-faites l'achat de vos produits(ordinateurs, vetements, chaussures, montres....   sur Alibaba ou amazone ou autres...\n Livraison en 72 heures(3 jours)	expedion-et-reception-de-coliscourriers-et-marchandises-RWY	36	10000	2.000	46000.00	XOF
254	2020-09-22 07:02:28.738064+01	2021-03-21 19:03:37.545182+01	LENOVO IDEAPAD U330P	👑 *LENOVO IDEAPAD U330P*\nDisque dur *500Go*\nRAM *8Go*\nProcesseur Intel *Core i5*\nFréquence *1.70Ghz up to 2.40ghz*\nÉcran *13. 3pouce*\n*Clavier lumineux☀️*\nUsb 3.0, 2USB, éthernet, HDMI \nCouleur *gris argent*\nPoid *1.53kg*\nL xL H *32.2 22.4 1.8 centimètres*\nAutonomie 4h+++	lenovo-ideapad-u330p-lLE	37	1	1.530	295000.00	XOF
265	2020-09-22 07:45:51.071766+01	2021-03-21 19:03:37.545182+01	ACER ASPIRE V3-572-C4FA	*ACER ASPIRE V3-572-C4FA*\nDisque dur *500gb*\nRam *4gb*\nProcesseur *Intel dualcord*\nFréquence *2 x 1.4Ghz*\nClavier *lumineux* ☀️\nÉcran 15.6 avec 15.6 avec *pavé numérique*\nAutonomie 6h+++\nC’est des pc professionnel différents des dual core simple	acer-aspire-v3-572-c4fa-rJg	37	1	1.500	165000.00	XOF
276	2020-09-24 09:14:24.94724+01	2021-03-21 19:03:37.545182+01	Expedions  et réception de marchandises	L'opportunité de faire de bonnes affaires et de racommoder son BUSNESS y est désormais. Profitez des offres exceptionnelles qu'offre FUTURIX société spécialisée dans l'envoi et réception de colis venant du monde entier , envoi de courriers express partout dans le monde en 48h ou 2jours. \n\nCommandez vos produits électroniques(telephones de toutes marques, ordinateurs, bateries, écouteurs, smartwatch,  congélateur et tant d'autres...) les vêtements, chaussures de bonnes marques ( Adidas, Nike ...) les produits cosmétiques, les parfums de luxes et mèches en provenance de la Chine, Hongkong États-Unis d'Amérique Alibaba, Ali express ou DOUBAÏ . Et vous les aurez ici au BÉNIN ! Livraison en 72heures (3jours) en toute sécurité ! \n\nAvec FUTURIX réaliser aisément votre rêve d'homme ou femme d'affaire ! \n\nWhatsApp : +229 95580983\nTéléphone : +229 62822779\n\nAdresse mail : kalifabdouarafat@gmail.com	expedions-et-reception-de-marchandises-kp8	36	2222	1.000	9000.00	XOF
244	2020-09-19 16:46:27.19114+01	2021-03-21 19:03:37.545182+01	Expedion et réception de colis,courriers et marchandises.	-Envoyez  et recevez vos colis et courriers express partout dans le monde entier !  \n-faites l'achat de vos produits(ordinateurs, vetements, chaussures, montres....   sur Alibaba ou amazone ou autres...\n Livraison en 72 heures(3 jours)	expedion-et-reception-de-coliscourriers-et-marchandises-UqQ	36	10000	2.000	46000.00	XOF
255	2020-09-22 07:06:28.078213+01	2021-03-21 19:03:37.545182+01	HP ELITEBOOK FOLIO 9470m	*HP ELITEBOOK FOLIO 9470m* 💻\n\nÉcran 14 pouce \nProcesseur *Intel Core i5*\nFréquence *2.40Ghz*\nDisque dur *SSD 275gb*\nRam *8Gb*\nClavier *rétro éclairé* ☀️ \nAutonomie 5h+	hp-elitebook-folio-9470m-I50	37	1	1.500	270000.00	XOF
232	2020-09-14 19:42:15.10564+01	2021-03-21 19:03:37.545182+01	Hip Hop Trousers	Pantalon Hip Hop\nCouleur: Comme sur l'image\nSexe: M	hip-hop-trousers-a-0	23	100	1.000	15.00	NGN
234	2020-09-14 19:54:06.739675+01	2021-03-21 19:03:37.545182+01	Harajuku Hoodie	Hoodie s'inspirant du style Harajuku\nCouleur: Comme sur l'image\nTaille: M\nSexe: F	harajuku-hoodie-M7g	23	100	1.000	30.00	NGN
299	2021-01-07 04:29:42.861047+01	2021-03-21 19:03:37.545182+01	20 Douzaines De Flacons De 6 Ml Des Huiles De Parfum Concentrée Originale	Livraison partout en 72 heures au maximum.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	20-douzaines-des-huiles-de-parfum-concentree-originale-Hpg	58	592	8.000	236150.00	XOF
245	2020-09-19 17:00:27.616357+01	2021-03-21 19:03:37.545182+01	Ordinateur portable Samsung	*PC SAMSUNG* 💻\nProcesseur *Intel CORE I3* \nRAM 4 | HDD 500 | Carte graphique NVIDIA 1gb\nÉcran 15 pouce  Avec pavé numérique  | Couleur Noire-grise 🔥	ordinateur-portable-samsung-vCY	36	12	3.000	150000.00	XOF
256	2020-09-22 07:09:25.84474+01	2021-03-21 19:03:37.545182+01	HP PROBOOK	*HP PROBOOK 4530s* 💻\nStockage 500Go\nRAM 4\nIntel *Core i5*\nFréquence *2.30Ghz*\nClavier Alphanumérique\nÉcran LED 15.6"\nCoque Allure \nWebcam HD	hp-probook-o5Q	37	1	1.500	195000.00	XOF
267	2020-09-22 08:06:13.595536+01	2021-03-21 19:03:37.545182+01	Montre casio tactile	Montre élégante pour vos sorties	montre-casio-tactile-K2U	37	15	0.500	10000.00	XOF
278	2020-10-02 11:11:56.682148+01	2021-03-21 19:03:37.545182+01	Oreilles de lapin flexibles imperméables 9 vitesses fort double moteur femmes adultes jouets sexuels gode vibrateur	Oreilles de lapin flexibles imperméables 9 vitesses fort double moteur femmes adultes jouets sexuels gode vibrateur .	oreilles-de-lapin-flexibles-impermeables-9-vitesses-fort-double-moteur-femmes-adultes-jouets-sexuels-gode-vibrateur-8-w	28	30	1.000	20000.00	XOF
300	2021-01-07 04:32:35.819305+01	2021-03-21 19:03:37.545182+01	50 Douzaines De Flacons De 6 Ml Des Huiles De Parfum Concentrée Originale	Livraison partout en 72 heures au maximum.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	50-douzaines-des-huiles-de-parfum-concentree-originale-wt4	58	592	18.000	512800.00	XOF
246	2020-09-19 17:03:24.887163+01	2021-03-21 19:03:37.545182+01	HP pro book	*HP PROBOOK 4530s* 💻\nStockage 500Go\nRAM 4\nIntel *Core i5*\nFréquence *2.30Ghz*\nClavier Alphanumérique\nÉcran LED 15.6"\nCoque Allure \nWebcam HD\n*Prix: 180.000Fr* ⚡	hp-pro-book-uTQ	36	14	2.000	180000.00	XOF
257	2020-09-22 07:13:43.776987+01	2021-03-21 19:03:37.545182+01	ACER SLIM DUAL CORE	⚡ *Acer Slim Dual core* 💻 \nRAM 4 | HDD 500\nÉcran 14 pouce	acer-slim-dual-core-UCE	37	1	2.000	145000.00	XOF
268	2020-09-22 10:04:04.956732+01	2021-03-21 19:03:37.545182+01	Mèches naturelle	Mèches naturelles avec closure	meches-naturelle-bdk	40	1	1.000	30000.00	XOF
279	2020-10-02 11:24:13.49945+01	2021-03-21 19:03:37.545182+01	Vibrateur de sexe de lapin de vibrateur de Sextoy à télécommande sans fil imperméable pour des femmes	Vibrateur de sexe de lapin de vibrateur de Sextoy à télécommande sans fil imperméable pour des femmes\nLieu d'origine:\nChine\nNuméro de modèle:\nVJS-E01 DuDu\nType:\nJouet de sexe adulte\nMarque:\nVJS\nMatériel:\nSilicone + ABS\nCouleur standard:\nRose rouge / violet\nLa vitesse:\n9 vibrations de vitesse\nPoids:\n156 g\nMOQ:\n1 PCS\nBatterie:\n3,7 V / 600 mAh\nImperméable:\nIPX 7\nTemps de travail:\n1,5 heures\nCertification:\nCE, ROHS\nMéthode de charge:\nUSB\nPaquet:\nBoite cadeau	vibrateur-de-sexe-de-lapin-de-vibrateur-de-sextoy-a-telecommande-sans-fil-impermeable-pour-des-femmes-jF4	28	30	1.000	17545.00	XOF
290	2020-12-31 12:59:31.228967+01	2021-03-21 19:03:37.545182+01	Motopompe à eau moteur essence	Marque : PM&T original, PARSUN Original\nApplication: Agriculture, Chantier etc	motopompe-a-eau-moteur-essence-gQc	57	20	27.500	120000.00	XOF
301	2021-01-07 04:34:15.189372+01	2021-03-21 19:03:37.545182+01	100 Douzaines De Flacons De 6 Ml Des Huiles De Parfum Concentrée Originale	Livraison partout en 72 heures au maximum.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	100-douzaines-des-huiles-de-parfum-concentree-originale-fkU	58	592	35.000	997600.00	XOF
247	2020-09-19 22:50:26.639086+01	2021-03-21 19:03:37.545182+01	Nissan rogue SL 2013	Nissan Rogue SL 2013 <= Système de Navigation, 4 caméras d'assistance, son BOSE, fauteuils en cuir noir, V4 bon pour essence en Afrique, climatisation top👌🏽\nÇa quitte New York ce mercredi...si tu as des amis qui sont intéressés...je vend👍🏽	nissan-rogue-sl-2013--qo	38	50	23.000	10.00	XOF
258	2020-09-22 07:18:44.674084+01	2021-03-21 19:03:37.545182+01	Asus slim dual core	⚡ *Asus Slim Dual core* 💻 \nRAM 4 | HDD 320\nÉcran 15pouce  Avec pavé numérique	asus-slim-dual-core-o10	37	1	1.500	130000.00	XOF
269	2020-09-22 10:04:04.966865+01	2021-03-21 19:03:37.545182+01	Mèches naturelle	Mèches naturelles avec closure	meches-naturelle-ETY	40	1	1.000	30000.00	XOF
280	2020-10-02 11:30:16.86838+01	2021-03-21 19:03:37.545182+01	Masturbateur vibrant de femme de vibrateur sans fil de masseur de baguette de corps de jouets sexuels adultes imperméables	Masturbateur vibrant de femme de vibrateur sans fil de masseur de baguette de corps de jouets sexuels adultes imperméables \n\nTaille : 202 * 48 mm	masturbateur-vibrant-de-femme-de-vibrateur-sans-fil-de-masseur-de-baguette-de-corps-de-jouets-sexuels-adultes-impermeables-18A	28	30	1.000	15542.00	XOF
291	2020-12-31 13:03:45.688644+01	2021-03-21 19:03:37.545182+01	Honda vibreur à béton	Structure : Type de cylindre \nProductivité: 70m²/h \nType : Vibreur à béton	honda-vibreur-a-beton-aH0	57	15	24.000	150000.00	XOF
302	2021-01-07 04:37:14.681093+01	2021-03-21 19:03:37.545182+01	3 Flacons de 6 ml des huiles de parfum concentrée Originale	Livraison partout au Bénin en seulement 24 h.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	3-flacons-des-huiles-de-parfum-concentree-originale-XUI	58	10134	1.000	6500.00	XOF
237	2020-09-16 10:20:16.005534+01	2021-03-21 19:03:37.545182+01	Jollof Rice	Jollof Rice 🍚 ,Pomme sauté accompagné de viande de boeuf sauter au fromage Wallangachi	jollof-rice-6j0	29	100	1.000	10000.00	XOF
259	2020-09-22 07:29:38.626689+01	2021-03-21 19:03:37.545182+01	Sony Intel core i3	*PC Sony intel Core i3* 💻 \nRAM 4 | HDD 500\nÉcran 14.6 pouce  Avec pavé numérique  | Couleur Blanche 🔥	sony-intel-core-i3-qNw	37	1	1.500	155000.00	XOF
270	2020-09-22 10:04:04.967245+01	2021-03-21 19:03:37.545182+01	Mèches naturelle	Mèches naturelles avec closure	meches-naturelle-qQA	40	1	1.000	30000.00	XOF
231	2020-09-14 19:38:33.420907+01	2021-03-21 19:03:37.545182+01	Love is our Culture	T-Shirt avec l'inscription "Love is our Culture"\nCouleur: Jaune\nSexe: F\nTaille: M	love-is-our-culture-deo	23	100	1.000	10.00	NGN
312	2021-02-20 12:10:58.15695+01	2021-03-21 19:03:37.545182+01	First Product	Test description QAZWSX	first-product-RII	60	100	1.000	1000.00	EUR
235	2020-09-14 19:56:28.658159+01	2021-03-21 19:03:37.545182+01	Hoodie TRASHER	Hoodie TRASHERRR (haha)\nCouleur: Rouge\nSexe: M\nTaille: XL	hoodie-trasher-H1Y	23	100	1.000	50.00	NGN
233	2020-09-14 19:43:54.569823+01	2021-03-21 19:03:37.545182+01	Queens Hoodie	Hoodie avec l'inscription "Streetwear from head to toe"\nCouleur: Grise\nTaille: L	queens-hoodie-i2g	23	100	1.000	25.00	NGN
311	2021-02-18 18:46:59.149143+01	2021-03-21 19:03:37.545182+01	Long Sleeve Crop Top	Test description	crop-top-6Uo	23	1000	1.000	40.00	NGN
314	2021-03-18 16:50:12.80878+01	2021-03-21 19:03:37.545182+01	Other product	\N	other-product-d2s	23	\N	5.000	1200.00	NGN
281	2020-10-02 11:53:57.180944+01	2021-03-21 19:03:37.545182+01	Réglage multi-angle C et G fort stimulateur adulte mâle jouets sexuels anneau de coq en silicone vibrant pour homme	Marque\n\nVJS\n\nN ° de modèle\n\nRanger VJS-C04\n\nspécification\n\nMatériel: silicone médical de qualité et ABS\n\nCouleur: rouge / Biack  peut être personnalisé\n\nBatterie :            3,7 V / 280 mAh\n\nPoids:             100 g\n\nMode:            9 vibrations intenses  \n\nTemps de travail: 1,5 h\n\nVoix: <40 dB\n\nÉtanche:     IPX7  \n\nPort FOB\n\nShenzhen\n\nCertificat\n\nRoHS CE FCC FDA \n\nMOQ\n\n1 pc\n\nEmballage\n\nEmballage de boîte de couleur\n\n\n \n\n \n\nCaractéristique principale\n\n \n\n \n\nForme 1.Roadster avec des vibrations super fortes\n2.Deux anneaux extensibles fixent le pénis et les testicules séparément et fermement, offrant une\ntélécommande sans fil à portée de 3,12 m pour un plaisir mains libres et des possibilités de\npréliminaires 4.Fun pour les deux: longue érection pour l'homme, et un meilleur orgasme pour la femme.\n\n \n\n Caractéristique principale:\n\n1.Anatomiquement parfait et esthétiquement beau dans la conception                                                     \n\n2.Le Rocket Bullet est conçu pour être compatible avec tous les jouets et accessoires                 \n\n3. moteur puissant et une batterie rechargeable               \n\n4.9 réglages puissants peuvent fournir des climax clitoridiens et vaginaux arqués                           \n\n5. charge rapide pour des heures de plaisir	reglage-multi-angle-c-et-g-fort-stimulateur-adulte-male-jouets-sexuels-anneau-de-coq-en-silicone-vibrant-pour-homme-jvo	28	15	1.000	16927.00	XOF
303	2021-01-07 04:39:29.448356+01	2021-03-21 19:03:37.545182+01	6 Flacons de 6 ml des huiles de parfum concentrée Originale	Livraison partout au Bénin en seulement 24 h.\nMélange de marques possible.\nFaîtes nous parvenir vos choix sur vos marques désirés au +229 97462924.	6-flacons-des-huiles-de-parfum-concentree-originale-RoY	58	10143	1.000	10000.00	XOF
310	2021-02-18 18:46:07.214207+01	2021-03-21 19:03:37.545182+01	Classic Crop Top	Un crop top super chic	crop-top-ugk	23	100	1.000	35.00	NGN
315	2021-03-18 16:51:19.865755+01	2021-03-21 19:03:37.545182+01	Test Product	\N	test-product-qMc	23	\N	1.000	1700.00	NGN
\.


--
-- Data for Name: products_categories; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.products_categories (id, product_id, category_id) FROM stdin;
3	313	3
4	316	4
5	317	5
\.


--
-- Data for Name: qosic_transaction; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.qosic_transaction (id, object_id, gateway, reference, service_reference, status, amount, phone, service_message, last_status_checked, updated, created, content_type_id, name, amount_currency, initiator_id, transaction_type) FROM stdin;
2	1	moov-bj	53e164008cd88477863d	\N	failed	2200.00	98801811	\N	2021-04-03 16:16:38.919828+01	2021-04-03 16:16:38.920063+01	2021-04-03 16:12:54.073963+01	31		XOF	94	payment
3	2	mtn-bj	54fdbb06b783a077f561	\N	failed	16000.00	90137010	\N	\N	2021-04-03 17:13:19.035131+01	2021-04-03 17:13:19.035158+01	31		XOF	94	payment
4	3	moov-bj	a11066867a4a395afefa	\N	success	2200.00	98801811	SUCCESS	2021-04-03 17:17:39.968237+01	2021-04-03 17:17:39.968627+01	2021-04-03 17:17:25.209812+01	31		XOF	94	payment
37	18	moov-bj	1eff9641991bc1540c11	\N	success	150.00	98801811	SUCCESS	2021-04-05 12:56:36.227811+01	2021-04-05 12:56:36.228568+01	2021-04-05 12:56:32.376784+01	32	Nelson K	XOF	98	payout
32	15	mtn-bj	1a6de09b917f722ed124	1586679511	success	4120.00	90137010	SUCCESSFUL	2021-04-05 12:21:45.437043+01	2021-04-05 12:21:45.437632+01	2021-04-05 12:21:14.838383+01	32	Bruce Wayne	XOF	98	payment
5	7	mtn-bj	7d92117b65e6389ed51c	\N	failed	2500.00	98801811	Pending	\N	2021-04-04 09:46:03.399691+01	2021-04-04 09:45:57.902775+01	31		XOF	94	payment
6	1	mtn-bj	bb170b8d40204ad04db7	\N	pending	1.00	90137010	\N	\N	2021-04-04 16:06:42.088417+01	2021-04-04 16:06:42.088451+01	11	Bot	XOF	1	payout
7	1	mtn-bj	d5b86bec9d9e0d688c5f	\N	pending	1.00	90137010	\N	\N	2021-04-04 16:08:04.31186+01	2021-04-04 16:08:04.311884+01	11	Bot	XOF	1	payout
8	1	mtn-bj	af31be19fe8594d8f411	\N	pending	1.00	90137010	\N	\N	2021-04-04 16:08:18.976539+01	2021-04-04 16:08:18.976611+01	11	Bot	XOF	1	payout
9	1	mtn-bj	2964d83ab5706cdedf44	\N	pending	1000.00	90137010	\N	\N	2021-04-04 16:08:36.432337+01	2021-04-04 16:08:36.432362+01	11	Bot	XOF	1	payout
10	1	mtn-bj	124a5f9816ad5eb8d0e7	\N	pending	1000.00	98801811	\N	\N	2021-04-04 16:09:08.437931+01	2021-04-04 16:09:08.437957+01	11	Bot	XOF	1	payout
11	1	moov-bj	579b566d8e7ac5adeaf1	\N	pending	1000.00	98801811	\N	\N	2021-04-04 16:15:17.359428+01	2021-04-04 16:15:17.359454+01	11	Bot	XOF	1	payout
12	1	moov-bj	42f8c030a99455ff5b5b	\N	pending	1.00	90137010	\N	\N	2021-04-04 16:15:42.737293+01	2021-04-04 16:15:42.737317+01	11	Bot	XOF	1	payout
13	1	moov-bj	4947e1f4db28a44b6f5a	\N	pending	1000.00	98801811	\N	\N	2021-04-04 16:16:16.64436+01	2021-04-04 16:16:16.644397+01	11	Bot	XOF	1	payout
14	1	moov-bj	2b6cd7734183d8e038fc	\N	success	500.00	98801811	SUCCESS	2021-04-04 17:06:30.992846+01	2021-04-04 17:06:30.994219+01	2021-04-04 17:06:18.12336+01	32		XOF	94	payment
15	1	mtn-bj	0dc9c8bfdbadbcd2fef5	\N	success	500.00	90137010	Successfully processed transaction.	2021-04-04 17:06:33.20907+01	2021-04-04 17:06:33.209381+01	2021-04-04 17:06:31.052053+01	32	Test Bot	XOF	94	payout
16	2	moov-bj	5a7393646eba4fea5e81	\N	success	1500.00	98801811	SUCCESS	2021-04-04 17:12:57.948777+01	2021-04-04 17:12:57.950199+01	2021-04-04 17:12:36.566611+01	32		XOF	94	payment
17	2	mtn-bj	fccd602c416ddd3c1136	\N	success	1500.00	90137010	Successfully processed transaction.	2021-04-04 17:13:04.694388+01	2021-04-04 17:13:04.694688+01	2021-04-04 17:12:57.995658+01	32	Test Bot	XOF	94	payout
18	3	moov-bj	2abfe602d6c7f4e3802e	\N	success	400.00	98801811	SUCCESS	2021-04-04 20:24:02.539889+01	2021-04-04 20:24:02.543154+01	2021-04-04 20:23:35.028741+01	32	Nelson K	XOF	94	payment
19	4	moov-bj	2e6b22ba1aadf09b4306	\N	failed	400.00	98801811		2021-04-04 20:29:10.447054+01	2021-04-04 20:29:10.447907+01	2021-04-04 20:28:41.897816+01	32	Nelson K	XOF	94	payment
20	4	mtn-bj	2b8fff98469c192fa41d	\N	success	199.00	90137010	Successfully processed transaction.	2021-04-04 20:29:13.056033+01	2021-04-04 20:29:13.056355+01	2021-04-04 20:29:10.506902+01	32	Test Bot	XOF	94	payout
21	4	moov-bj	9f72eb85701a5bcf5858	\N	success	199.00	98801811	SUCCESS	2021-04-04 20:29:15.875884+01	2021-04-04 20:29:15.876203+01	2021-04-04 20:29:13.08203+01	32	Bruce Wayne	XOF	94	payout
22	5	moov-bj	d101b40c513e29d2f5d5	\N	failed	400.00	98801811		2021-04-04 20:40:09.897612+01	2021-04-04 20:40:09.898938+01	2021-04-04 20:39:54.921894+01	32	Test Bot	XOF	40	payment
23	6	moov-bj	fbf5fc17967bcf5b47f3	\N	success	400.00	98801811	SUCCESS	2021-04-04 20:46:45.053964+01	2021-04-04 20:46:45.054724+01	2021-04-04 20:46:22.609087+01	32	Test Bot	XOF	40	payment
24	7	moov-bj	38ea95ce2f69c1e5a87a	\N	success	200.00	98801811	SUCCESS	2021-04-04 20:55:08.98138+01	2021-04-04 20:55:08.981785+01	2021-04-04 20:54:52.299577+01	32	Nelson K	XOF	94	payment
25	8	moov-bj	c05f64a3d4b9ab743dd8	\N	success	500.00	98801811	SUCCESS	2021-04-04 20:57:14.289598+01	2021-04-04 20:57:14.290187+01	2021-04-04 20:56:53.587687+01	32	Nelson K	XOF	94	payment
26	8	mtn-bj	bc0cca22d185dea9d63c	\N	success	345.00	90137010	Successfully processed transaction.	2021-04-04 20:57:17.177763+01	2021-04-04 20:57:17.177978+01	2021-04-04 20:57:14.357328+01	32	Test Bot	XOF	94	payout
27	8	moov-bj	7f3929712387268f3bb5	\N	success	153.00	98801811	SUCCESS	2021-04-04 20:57:22.020672+01	2021-04-04 20:57:22.020903+01	2021-04-04 20:57:17.198922+01	32	Bruce Wayne	XOF	94	payout
33	15	moov-bj	513cd8b7540fc200d5b6	\N	success	4000.00	98801811	SUCCESS	2021-04-05 12:21:52.904913+01	2021-04-05 12:21:52.905229+01	2021-04-05 12:21:45.471024+01	32	Nelson K	XOF	98	payout
28	13	mtn-bj	88b3eabc0287fe3c990f	1586513313	success	4120.00	90137010	Successfully processed transaction.	2021-04-05 11:15:42.676162+01	2021-04-05 11:15:42.676387+01	2021-04-05 11:12:09.132185+01	32	Bruce Wayne	XOF	98	payment
29	13	moov-bj	7f5687447e557121f6a0	\N	success	4000.00	98801811	SUCCESS	2021-04-05 11:15:45.416996+01	2021-04-05 11:15:45.417266+01	2021-04-05 11:15:42.787097+01	32	Nelson K	XOF	98	payout
38	18	moov-bj	28cb19108ce64413d57f	\N	success	150.00	98801811	SUCCESS	2021-04-05 12:59:42.508982+01	2021-04-05 12:59:42.509196+01	2021-04-05 12:59:35.822028+01	32	Nelson K	XOF	98	payout
34	17	moov-bj	5df505b4a8c8313ce5c6	\N	success	1400.00	98801811	SUCCESS	2021-04-05 12:46:09.300575+01	2021-04-05 12:46:09.30141+01	2021-04-05 12:45:49.406833+01	32	Nelson K	XOF	94	payment
30	14	mtn-bj	ecbcc3111522af56e773	1586531473	success	4120.00	90137010	Successfully processed transaction.	2021-04-05 11:20:33.171392+01	2021-04-05 11:20:33.17172+01	2021-04-05 11:19:26.319322+01	32	Bruce Wayne	XOF	98	payment
31	14	moov-bj	4b1e4d992f7e59fa720b	\N	success	4000.00	98801811	SUCCESS	2021-04-05 11:20:35.719432+01	2021-04-05 11:20:35.719615+01	2021-04-05 11:20:33.203326+01	32	Nelson K	XOF	98	payout
35	17	mtn-bj	ab76c78b1f364662b0fe	\N	success	1400.00	90137010	Successfully processed transaction.	2021-04-05 12:46:11.683893+01	2021-04-05 12:46:11.684218+01	2021-04-05 12:46:09.335146+01	32	Test Bot	XOF	94	payout
40	19	moov-bj	51e124efb30066b34073	\N	success	500.00	98801811	SUCCESS	2021-04-05 13:08:56.695372+01	2021-04-05 13:08:56.695602+01	2021-04-05 13:08:48.933674+01	32	Nelson K	XOF	98	payout
39	19	moov-bj	de7746a2c16449b64eae	\N	success	500.00	98801811	SUCCESS	2021-04-05 13:08:49.626248+01	2021-04-05 13:08:49.627362+01	2021-04-05 13:08:34.967391+01	32	Bruce Wayne	XOF	98	payment
36	18	moov-bj	e61bb98078e8455a35e0	\N	failed	150.00	98801811	SUCCESS	2021-04-05 12:59:35.780035+01	2021-04-05 12:59:35.780804+01	2021-04-05 12:56:19.763768+01	32	Bruce Wayne	XOF	98	payment
41	19	moov-bj	14bcc5931c989f59a01e	\N	success	500.00	98801811	SUCCESS	2021-04-05 13:08:56.694632+01	2021-04-05 13:08:56.694951+01	2021-04-05 13:08:49.656139+01	32	Nelson K	XOF	98	payout
42	20	moov-bj	6e557b2df89a1ec0f07d	\N	success	400.00	98801811	SUCCESS	2021-04-05 13:18:57.273188+01	2021-04-05 13:18:57.274585+01	2021-04-05 13:18:41.342861+01	32	Nelson K	XOF	94	payment
44	21	moov-bj	8d43fbea1af42ff41015	\N	success	400.00	98801811	SUCCESS	2021-04-05 13:25:39.914539+01	2021-04-05 13:25:39.914812+01	2021-04-05 13:25:37.206342+01	32	Bruce Wayne	XOF	94	payout
43	21	moov-bj	b3106e16dd1c22a7bbcb	\N	success	400.00	98801811	SUCCESS	2021-04-05 13:25:38.341543+01	2021-04-05 13:25:38.342208+01	2021-04-05 13:25:24.363104+01	32	Nelson K	XOF	94	payment
45	21	moov-bj	ebb9a412dd5a53bf7c8e	\N	success	400.00	98801811	SUCCESS	2021-04-05 13:25:41.200803+01	2021-04-05 13:25:41.201139+01	2021-04-05 13:25:38.375441+01	32	Bruce Wayne	XOF	94	payout
47	22	moov-bj	ce8e85a04093627fe38c	\N	success	400.00	98801811	SUCCESS	2021-04-05 14:00:54.378614+01	2021-04-05 14:00:54.378944+01	2021-04-05 14:00:51.867277+01	32	Bruce Wayne	XOF	94	payout
46	22	moov-bj	c77b48eaa39efbee0f83	\N	success	400.00	98801811	SUCCESS	2021-04-05 14:00:51.821443+01	2021-04-05 14:00:51.828636+01	2021-04-05 14:00:36.894681+01	32	Nelson K	XOF	94	payment
48	8	moov-bj	5812ae54e8c6e523dd89	\N	success	2000.00	98801811	SUCCESS	2021-04-05 14:53:57.759913+01	2021-04-05 14:53:57.770489+01	2021-04-05 14:53:46.54957+01	31	Bruce Wayne	XOF	98	payment
49	9	moov-bj	b41beea3288ac899992f	\N	success	4000.00	98801811	SUCCESS	2021-04-05 15:04:50.554963+01	2021-04-05 15:04:50.56349+01	2021-04-05 15:04:35.57845+01	31	Bruce Wayne	XOF	98	payment
72	27	moov-bj	e55af8d1e43cd440c36d	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:32.408649+01	2021-04-07 02:15:32.409283+01	2021-04-07 02:15:28.385201+01	32	Bruce Wayne	XOF	40	payout
50	10	moov-bj	e6a4b8736111272c3252	\N	success	4000.00	98801811	SUCCESS	2021-04-05 15:35:34.708421+01	2021-04-05 15:35:34.714835+01	2021-04-05 15:35:15.612301+01	31	Bruce Wayne	XOF	98	payment
51	23	moov-bj	4a42e905db98583086bf	\N	success	400.00	98801811	SUCCESS	2021-04-05 17:23:44.499101+01	2021-04-05 17:23:44.506485+01	2021-04-05 17:23:27.447784+01	32	Bruce Wayne	XOF	98	payment
52	23	moov-bj	6672bdf214e25d37de48	\N	success	400.00	98801811	SUCCESS	2021-04-05 17:23:47.241078+01	2021-04-05 17:23:47.241535+01	2021-04-05 17:23:44.673327+01	32	Nelson K	XOF	98	payout
60	27	moov-bj	6c154566735db424aa5d	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:28.083206+01	2021-04-07 02:15:28.146304+01	2021-04-07 02:15:07.05857+01	32	Test Bot	XOF	40	payment
57	3	moov-bj	6c8eb111a2c90f735a0d	\N	success	2778.00	98801811	SUCCESS	2021-04-06 13:58:42.968904+01	2021-04-06 13:58:42.97862+01	2021-04-06 13:58:30.381137+01	31	Nelson K	XOF	94	payment
53	11	moov-bj	018f42454eceb090a0e4	\N	failed	6000.00	98801811		2021-04-06 11:30:52.131861+01	2021-04-06 11:30:52.132279+01	2021-04-06 11:24:37.77909+01	31	Nelson K	XOF	94	payment
54	24	moov-bj	1e72d277ed417d4803a6	\N	failed	2500.00	98801811		2021-04-06 11:32:18.080436+01	2021-04-06 11:32:18.088384+01	2021-04-06 11:29:13.27982+01	32	Nelson K	XOF	94	payment
61	27	moov-bj	748fa0c0722733841d10	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:29.195313+01	2021-04-07 02:15:29.203+01	2021-04-07 02:15:24.808487+01	32	Bruce Wayne	XOF	40	payout
55	25	moov-bj	e2d5fc6f8c98d9bc10fa	\N	failed	1400.00	98801811	\N	2021-04-06 11:47:41.697941+01	2021-04-06 11:47:41.70677+01	2021-04-06 11:46:58.607756+01	32	Nelson K	XOF	94	payment
62	27	moov-bj	a75ab4f7593e9af88e7b	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:29.796875+01	2021-04-07 02:15:29.803209+01	2021-04-07 02:15:25.173265+01	32	Bruce Wayne	XOF	40	payout
64	27	moov-bj	a762b6aa49259bafda25	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:29.859874+01	2021-04-07 02:15:29.862771+01	2021-04-07 02:15:25.716817+01	32	Bruce Wayne	XOF	40	payout
58	3	moov-bj	930c992697c78c69ddb6	\N	success	2778.00	98801811	SUCCESS	2021-04-06 14:03:10.863223+01	2021-04-06 14:03:10.870985+01	2021-04-06 14:02:55.043394+01	31	Nelson K	XOF	94	payment
63	27	moov-bj	e3fb78892022aacb28c4	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.003262+01	2021-04-07 02:15:30.005299+01	2021-04-07 02:15:25.49236+01	32	Bruce Wayne	XOF	40	payout
65	27	moov-bj	f936a69459bf6aff5c6c	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.05726+01	2021-04-07 02:15:30.06041+01	2021-04-07 02:15:25.776008+01	32	Bruce Wayne	XOF	40	payout
59	3	moov-bj	1b7c173d5f7b183914a1	\N	success	6668.00	98801811	SUCCESS	2021-04-06 14:06:13.990599+01	2021-04-06 14:06:13.996929+01	2021-04-06 14:05:49.777806+01	31	Nelson K	XOF	94	payment
67	27	moov-bj	0abcfd39a4009c98c596	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.713612+01	2021-04-07 02:15:30.713892+01	2021-04-07 02:15:27.992539+01	32	Bruce Wayne	XOF	40	payout
56	3	moov-bj	885aa08f288d095e2c8b	\N	success	5556.00	98801811	SUCCESS	2021-04-06 13:52:04.735236+01	2021-04-06 13:52:04.74253+01	2021-04-06 13:51:49.43123+01	31	Nelson K	XOF	94	payment
66	27	moov-bj	7f3c28e3cc6414e73bb5	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.713203+01	2021-04-07 02:15:30.713496+01	2021-04-07 02:15:27.969844+01	32	Bruce Wayne	XOF	40	payout
69	27	moov-bj	29eaae8a0e7d7c93f612	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.807337+01	2021-04-07 02:15:30.807586+01	2021-04-07 02:15:28.064882+01	32	Bruce Wayne	XOF	40	payout
68	27	moov-bj	a68aaa4eb1b93f2098ea	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:30.807592+01	2021-04-07 02:15:30.807862+01	2021-04-07 02:15:28.044687+01	32	Bruce Wayne	XOF	40	payout
71	27	moov-bj	1fce30420709086d4722	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:31.284334+01	2021-04-07 02:15:31.284624+01	2021-04-07 02:15:28.374081+01	32	Bruce Wayne	XOF	40	payout
70	27	moov-bj	43fea0dcdd4fe8b44f89	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:31.285691+01	2021-04-07 02:15:31.286039+01	2021-04-07 02:15:28.287454+01	32	Bruce Wayne	XOF	40	payout
73	27	moov-bj	7d2f81cd8a8f8a00c035	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:32.398041+01	2021-04-07 02:15:32.398442+01	2021-04-07 02:15:28.466788+01	32	Bruce Wayne	XOF	40	payout
74	27	moov-bj	6366bd2d2ee354614583	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:32.404228+01	2021-04-07 02:15:32.404835+01	2021-04-07 02:15:28.633088+01	32	Bruce Wayne	XOF	40	payout
75	27	moov-bj	a26c99c941b92e30caf1	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:32.40613+01	2021-04-07 02:15:32.406475+01	2021-04-07 02:15:28.63919+01	32	Bruce Wayne	XOF	40	payout
76	27	moov-bj	83970fe33ac578c488ae	\N	success	125.00	98801811	SUCCESS	2021-04-07 02:15:33.056607+01	2021-04-07 02:15:33.05682+01	2021-04-07 02:15:28.667548+01	32	Bruce Wayne	XOF	40	payout
86	37	moov-bj	69efe7348d2262463691	\N	success	25000.00	98801811	SUCCESS	2021-04-15 22:40:59.395786+01	2021-04-15 22:40:59.396208+01	2021-04-15 22:40:56.857541+01	32	Nelson K	XOF	98	payout
82	30	mtn-bj	bb25a0aac936e0a12770	1606261089	success	125.00	90137010	Successfully processed transaction.	2021-04-14 10:14:28.028561+01	2021-04-14 10:14:28.753406+01	2021-04-14 10:11:24.449299+01	32	Nelson K	XOF	94	payment
83	30	mtn-bj	3d8f359fd42fabaee798	\N	success	125.00	90137010	Successfully processed transaction.	2021-04-14 10:14:33.999837+01	2021-04-14 10:14:34.000188+01	2021-04-14 10:14:30.585905+01	32	Bruce Wayne	XOF	94	payout
79	9	moov-bj	8182db5083694b50b93a	\N	success	552.00	98801811	SUCCESS	2021-04-07 02:53:02.438415+01	2021-04-07 02:53:02.576021+01	2021-04-07 02:52:47.108173+01	31	Bruce Wayne	XOF	98	payment
80	10	moov-bj	a26b2100119df3781ec9	\N	success	352.00	98801811	SUCCESS	2021-04-07 12:39:37.150398+01	2021-04-07 12:39:37.150741+01	2021-04-07 12:39:34.25817+01	31	Bruce Wayne	XOF	98	payout
77	29	moov-bj	d41e9262c6b3a1b51cde	\N	success	1200.00	98801811	SUCCESS	2021-04-07 02:31:10.945646+01	2021-04-07 02:31:11.005314+01	2021-04-07 02:30:56.868121+01	32	Test Bot	XOF	40	payment
78	29	moov-bj	ccf5d43afcda2569d6a7	\N	success	1200.00	98801811	SUCCESS	2021-04-07 02:31:14.020755+01	2021-04-07 02:31:14.021025+01	2021-04-07 02:31:11.406158+01	32	Bruce Wayne	XOF	40	payout
81	10	moov-bj	2e6cf4dc17c682c5674b	\N	success	352.00	98801811	SUCCESS	2021-04-07 12:41:21.892435+01	2021-04-07 12:41:21.892781+01	2021-04-07 12:41:10.290573+01	31	Bruce Wayne	XOF	98	payout
84	37	moov-bj	5b45a88033a70a5183e6	\N	success	25750.00	98801811	SUCCESS	2021-04-15 22:40:56.23817+01	2021-04-15 22:40:56.252269+01	2021-04-15 22:39:56.38105+01	32	Bruce Wayne	XOF	98	payment
85	37	moov-bj	3b06def773729c2a8570	\N	success	25000.00	98801811	SUCCESS	2021-04-15 22:40:59.025629+01	2021-04-15 22:40:59.025924+01	2021-04-15 22:40:56.741248+01	32	Nelson K	XOF	98	payout
88	38	moov-bj	239c7c838af38c7cbcb0	\N	success	25000.00	98801811	SUCCESS	2021-04-15 22:46:21.750942+01	2021-04-15 22:46:21.751255+01	2021-04-15 22:46:19.113589+01	32	Nelson K	XOF	98	payout
87	38	moov-bj	8c014e3560f364a5b9ea	\N	success	25750.00	98801811	SUCCESS	2021-04-15 22:46:18.846507+01	2021-04-15 22:46:18.853586+01	2021-04-15 22:46:09.017968+01	32	Bruce Wayne	XOF	98	payment
89	8	moov-bj	10853d4485b04d24de27	\N	success	4000.00	98801811	SUCCESS	2021-04-16 11:58:21.413389+01	2021-04-16 11:58:21.42316+01	2021-04-16 11:58:06.070599+01	35	Bruce Wayne	XOF	98	payment
90	8	moov-bj	7f1ced6a6d9460c9da71	\N	failed	4000.00	98801811	PASSWORD_ERROR	2021-04-16 12:02:48.948792+01	2021-04-16 12:02:48.95643+01	2021-04-16 12:02:39.601444+01	35	Bruce Wayne	XOF	98	payment
91	8	moov-bj	1a3b3f0e0cbc20e7f306	\N	success	4000.00	98801811	SUCCESS	2021-04-16 12:03:52.250208+01	2021-04-16 12:03:52.260185+01	2021-04-16 12:03:39.350064+01	35	Bruce Wayne	XOF	98	payment
98	40	moov-bj	02e8dfa1c629ba780d6f	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.011296+01	2021-04-17 13:12:33.011551+01	2021-04-17 13:12:28.149245+01	32	Bruce Wayne	XOF	94	payout
97	40	moov-bj	09c9995e5f5d0a690c7d	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.011209+01	2021-04-17 13:12:33.011475+01	2021-04-17 13:12:28.140252+01	32	Bruce Wayne	XOF	94	payout
92	8	moov-bj	212c317cc4bee0411b80	\N	success	4000.00	98801811	SUCCESS	2021-04-16 12:06:42.996094+01	2021-04-16 12:06:43.048485+01	2021-04-16 12:06:31.125876+01	35	Bruce Wayne	XOF	98	payment
93	8	moov-bj	e6e7237d62a6159147d5	\N	success	4000.00	98801811	SUCCESS	2021-04-16 12:06:45.795945+01	2021-04-16 12:06:45.796166+01	2021-04-16 12:06:43.252581+01	35	Nelson K	XOF	98	payout
99	40	moov-bj	833e427c0c1f1f5b7b2b	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.072603+01	2021-04-17 13:12:33.072813+01	2021-04-17 13:12:28.20097+01	32	Bruce Wayne	XOF	94	payout
100	40	moov-bj	d3af19d5bfdf926ce5ad	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.3426+01	2021-04-17 13:12:33.342886+01	2021-04-17 13:12:28.319349+01	32	Bruce Wayne	XOF	94	payout
101	40	moov-bj	430efbe477d88695f7c2	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.679883+01	2021-04-17 13:12:33.680276+01	2021-04-17 13:12:28.749464+01	32	Bruce Wayne	XOF	94	payout
102	40	moov-bj	d945e4f60fa363e83419	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:33.684509+01	2021-04-17 13:12:33.684729+01	2021-04-17 13:12:28.759038+01	32	Bruce Wayne	XOF	94	payout
96	40	moov-bj	9ecc5656ea4aa958530d	\N	success	200.00	98801811	SUCCESS	2021-04-17 13:12:38.513694+01	2021-04-17 13:12:38.521176+01	2021-04-17 13:12:15.753337+01	32	Nelson K	XOF	94	payment
94	39	moov-bj	13e1c881d970a80db5bf	\N	success	2000.00	98801811	SUCCESS	2021-04-17 12:39:51.16304+01	2021-04-17 12:39:51.175771+01	2021-04-17 12:39:36.377252+01	32	Nelson K	XOF	94	payment
95	39	moov-bj	61a72cade0418bc5902b	\N	success	2000.00	98801811	SUCCESS	2021-04-17 12:40:04.357715+01	2021-04-17 12:40:04.358072+01	2021-04-17 12:39:52.54214+01	32	Bruce Wayne	XOF	94	payout
\.


--
-- Data for Name: shops; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.shops (id, created_at, updated_at, name, username, avatar_url, description, phone_number, user_id, cover_url, affiliate_id, domains, country_code, currency_iso, email) FROM stdin;
45	2020-09-24 07:59:35.969105+01	2021-02-12 14:52:32.423669+01	Le Cellier	yves-kouton	https://kweek.sgp1.digitaloceanspaces.com/production/13a7b746-acd6-45a7-99e1-9007bf639cf3-avatar.jpeg	\N	97128517	68	\N	8	{yves_kouton.kweek.shop,yves-kouton.kweek.shop}	BJ	XOF	
28	2020-09-16 09:05:26.350305+01	2021-02-12 14:52:32.423669+01	BIG DEALS	serge-adjaho	https://kweek.sgp1.digitaloceanspaces.com/production/6f8cd7b1-d5ab-48aa-aafc-8d1a85ee1cc7-avatar.png	\N	+22951446843	46	https://kweek.sgp1.digitaloceanspaces.com/production/4931e9d0-a7a6-47b4-8484-4fc913b1d8f5-cover.jpeg	\N	{serge_adjaho.kweek.shop,serge-adjaho.kweek.shop}	BJ	XOF	
48	2020-09-28 20:23:55.319444+01	2021-02-12 14:52:32.423669+01	Luxury shop	marcel-deluxe	https://kweek.sgp1.digitaloceanspaces.com/production/85d9a3eb-948e-4def-b8cb-9643e6e80a3a-avatar.jpeg	•Vente de téléphones et accessoires \n•Montres\n•Durag	0022960596199	73	\N	10	{marcel_deluxe.kweek.shop,marcel-deluxe.kweek.shop}	BJ	XOF	
49	2020-10-01 07:04:10.066694+01	2021-02-12 14:52:32.423669+01	Skirt glam	wina-aj	https://kweek.sgp1.digitaloceanspaces.com/production/6c17692e-3a9f-41b3-884f-e5fb539f0659-avatar.jpeg	Vente en ligne de tout type de jupes(longue,moyenne,courte,moderne,classique etc) sur commande.	61283500	74	\N	8	{wina_aj.kweek.shop,wina-aj.kweek.shop}	BJ	XOF	
59	2021-01-05 20:00:03.379452+01	2021-02-12 14:52:32.423669+01	Kweek Test	kweek-test	https://kweek.sgp1.digitaloceanspaces.com/production/fbf2510f-f2f6-4f48-a173-b7954f2c6f1b-avatar.png	\N	+22998801811	94	\N	\N	{kweek_test.kweek.shop,kweek-test.kweek.shop}	BJ	XOF	
41	2020-09-22 21:25:46.777531+01	2021-02-12 14:52:32.423669+01	SQUIRREL express delivery	oswald-01	https://kweek.sgp1.digitaloceanspaces.com/production/39a24c2a-fe8e-40f7-a5db-e4132eed1e28-avatar.png	SQUIRREL express delivery  est une entreprise spécialisée dans l'organisation de transport de colis de repas et de courrier  en milieu urbain et périurbain.  Nous organisons aussi des opération à l'import et à l'export .	69239999	42	https://kweek.sgp1.digitaloceanspaces.com/production/c4312dbd-b50b-4054-a261-ccc69028e236-cover.jpeg	\N	{oswald_01.kweek.shop,oswald-01.kweek.shop}	BJ	XOF	
60	2021-02-17 02:25:02.446875+01	2021-02-17 02:25:02.44691+01	Second Store	second-store	\N	\N		95	\N	\N	{}	FR	EUR	
62	2021-03-24 14:43:36.927557+01	2021-03-24 14:43:40.631958+01	Good	good	\N	\N		40	\N	\N	{good.kweek.shop}	BJ	XOF	
26	2020-09-14 19:20:05.56392+01	2021-02-12 14:52:32.423669+01	KFUT	kfutur	https://kweek.sgp1.digitaloceanspaces.com/production/36707735-be21-484b-ab0e-469cad126074-avatar.jpeg	\N	62606333	41	\N	\N	{kfutur.kweek.shop,kfutur.kweek.shop}	BJ	XOF	
33	2020-09-16 19:05:43.740916+01	2021-02-12 14:52:32.423669+01	Mfood	marco	https://kweek.sgp1.digitaloceanspaces.com/production/a2888ee3-f34d-4690-94ec-808107be32fa-avatar.jpeg	Fioskjd	61572694	52	https://kweek.sgp1.digitaloceanspaces.com/production/2d7ea133-6d1e-4ff1-bc41-0999248cbd35-cover.jpeg	\N	{marco.kweek.shop,marco.kweek.shop}	BJ	XOF	
35	2020-09-18 15:56:27.379611+01	2021-02-12 14:52:32.423669+01	Diaspora	diaspo	https://kweek.sgp1.digitaloceanspaces.com/production/523e6385-ea75-4c8e-83ea-78464ec3e53c-avatar.jpeg	Produits electroniques\nDiaspora GSM\n#TECHSOLUTION	95009416	54	https://kweek.sgp1.digitaloceanspaces.com/production/6cb92ef0-1cb6-4e3f-bb69-d121787793fa-cover.jpeg	\N	{diaspo.kweek.shop,diaspo.kweek.shop}	BJ	XOF	
32	2020-09-16 15:34:19.018844+01	2021-02-12 14:52:32.423669+01	Chez Lataille	lataille	https://kweek.sgp1.digitaloceanspaces.com/production/1cec630a-095b-4b01-b288-8577352a4caa-avatar.jpeg	Boutique de vente divers ( Électroménagers, Sac, Meubles, Téléphones, Laptop)\nVêtements hommes, femmes, vêtements haut de gamme, vêtements pour soirée, Friperie, Prêt-à-porter à des prix Cadeaux.	+22967715329	50	https://kweek.sgp1.digitaloceanspaces.com/production/ffd946ab-4115-4627-bc2c-773aa1fe883d-cover.jpeg	\N	{lataille.kweek.shop,lataille.kweek.shop}	BJ	XOF	
40	2020-09-21 08:24:36.846445+01	2021-02-12 14:52:32.423669+01	DAYASHOP 💞	dayanath	https://kweek.sgp1.digitaloceanspaces.com/production/41595bf3-e648-496c-8402-331164faa4a6-avatar.jpeg	Ventes de mèches naturelles	90589306	63	https://kweek.sgp1.digitaloceanspaces.com/production/4bd011c6-a7e1-47f9-b957-5b958bab0fa5-cover.jpeg	7	{dayanath.kweek.shop,dayanath.kweek.shop}	BJ	XOF	
43	2020-09-23 17:26:06.352456+01	2021-02-12 14:52:32.423669+01	Hamidou	alassane	https://kweek.sgp1.digitaloceanspaces.com/production/71541f93-11ef-4e8f-ab3b-e41b6d092d1c-avatar.jpeg	\N	66061252	66	\N	7	{alassane.kweek.shop,alassane.kweek.shop}	BJ	XOF	
46	2020-09-24 18:29:34.806049+01	2021-02-12 14:52:32.423669+01	M-J cosmetics & mode	cosmetics	https://kweek.sgp1.digitaloceanspaces.com/production/94a43789-cdc0-43df-8512-f9d522fb1882-avatar.jpeg	\N	62668847	70	\N	\N	{cosmetics.kweek.shop,cosmetics.kweek.shop}	BJ	XOF	
58	2021-01-04 11:02:58.996117+01	2021-02-12 14:52:32.423669+01	LA MAISON DES SENTEURS	lamaisondessenteurs	https://kweek.sgp1.digitaloceanspaces.com/production/4d054871-ff6e-45c8-8216-6b2d0d8c2573-avatar.jpeg	Vente en gros et en détails des huiles de parfum concentrée Original de grandes marques de renommée internationale. Plus de 30 marques disponibles.\n\nPrix de  gros:       \n05 douzaines à 65.000f                                     Prix de détails:\n10 douzaines à 128.250f                                  3 flacons à 6500f\n20 douzaines à 236.150f.                                 6 flacons à 10.000f\n50 douzaines à 512.800f.                                 1 douzaine 17500f\n100 douzaines à 997.600f	+229 97462924	93	https://kweek.sgp1.digitaloceanspaces.com/production/e92693f0-680e-47fa-9260-8155078f558e-cover.jpeg	\N	{lamaisondessenteurs.kweek.shop,lamaisondessenteurs.kweek.shop}	BJ	XOF	
52	2020-10-03 16:59:28.755397+01	2021-02-12 14:52:32.423669+01	AMOUR D'OR	naziifbijoux	https://kweek.sgp1.digitaloceanspaces.com/production/314a7839-0fb5-457d-b512-d124b5b5df63-avatar.jpeg	\N	61311421	84	\N	\N	{naziifbijoux.kweek.shop,naziifbijoux.kweek.shop}	BJ	XOF	
55	2020-10-14 13:19:02.696185+01	2021-02-12 14:52:32.423669+01	Primus Inter	primusinter	https://kweek.sgp1.digitaloceanspaces.com/production/c188e6cd-388b-41b0-b150-f6bed5c02097-avatar.jpeg	\N	+229 61888333	88	\N	\N	{primusinter.kweek.shop,primusinter.kweek.shop}	BJ	XOF	
44	2020-09-23 19:46:55.833518+01	2021-02-12 14:52:32.423669+01	AT CENTER	adewumi	https://kweek.sgp1.digitaloceanspaces.com/production/4e8427d1-1409-4fca-a9fd-6bd652ed474b-avatar.jpeg	\N	97061335	67	\N	9	{adewumi.kweek.shop,adewumi.kweek.shop}	BJ	XOF	
47	2020-09-25 11:20:11.078956+01	2021-02-12 14:52:32.423669+01	Dav store	davbray10	https://kweek.sgp1.digitaloceanspaces.com/production/d7de696e-a26f-4906-a852-2c425a3fc7ad-avatar.jpeg	Dav store vous propose des services de webmarketing et met à votre disposition des articles de tout genre.	+22961001272	55	\N	5	{davbray10.kweek.shop,davbray10.kweek.shop}	BJ	XOF	
53	2020-10-07 17:14:24.288475+01	2021-02-12 14:52:32.423669+01	Boma	theophile	https://kweek.sgp1.digitaloceanspaces.com/production/25d6f0ba-66e7-493f-bcd7-66ed9e38e478-avatar.jpeg	\N	0978511357	86	\N	\N	{theophile.kweek.shop,theophile.kweek.shop}	BJ	XOF	
50	2020-10-02 10:08:02.581137+01	2021-02-12 14:52:32.423669+01	Tampico	hghh	https://kweek.sgp1.digitaloceanspaces.com/production/a1c4c2f9-fb13-4c06-b8fd-53aba7ddebfe-avatar.webp	Fan DANGO	66173541	51	https://kweek.sgp1.digitaloceanspaces.com/production/0565b6dc-8561-4ce5-8b11-1dd5722eea54-cover.webp	\N	{hghh.kweek.shop,hghh.kweek.shop}	BJ	XOF	
61	2021-02-17 02:26:28.101174+01	2021-02-17 02:26:28.101205+01	Momo Shop	momo	\N	\N		95	\N	\N	{}	FR	EUR	
29	2020-09-16 10:04:58.710307+01	2021-02-12 14:52:32.423669+01	Pablo’s	billy	https://kweek.sgp1.digitaloceanspaces.com/production/8360dd7a-60c6-415f-99ad-cf27f2e9e111-avatar.jpeg	Pablo’s \nPablo’s \nPablo’s 🚚	60507951	47	https://kweek.sgp1.digitaloceanspaces.com/production/20e5e82f-f2a7-4f4f-8564-f53888e2e8b9-cover.png	\N	{billy.kweek.shop,billy.kweek.shop}	BJ	XOF	
23	2020-09-13 09:25:14.434116+01	2021-03-05 17:27:50.82751+01	Demo Shop	demo	https://kweek.sgp1.digitaloceanspaces.com/dev/a4a5e024-9347-4f2a-b1bc-002dcfc36be5-avatar.png	🤙🏾  Urban & Streetwear\n🤳🏾  Tagues tes looks avec #UrbanActivated\n✌🏾  Ton style. Ton monde. Tu déchires.\n👩‍💻  [Ceci est un compte test]	+22998801811	40	https://kweek.sgp1.digitaloceanspaces.com/production/da5b0090-3e1e-49ea-97f4-43235aeb8b81-cover.jpeg	\N	{demo.kweek.shop,localhost,demo.kweek.local,demo.kweek.shop}	NG	NGN	nelson@kweek.africa
25	2020-09-14 07:52:22.527184+01	2021-03-24 09:58:46.33941+01	My Shop	my-shoppp	https://kweek.sgp1.digitaloceanspaces.com/production/afb77e58-13a7-43f3-b288-48bcb45a8589-avatar.jpeg	Une description	+22998801811	40	https://kweek.sgp1.digitaloceanspaces.com/production/d480304b-4b77-4d04-b626-9859749c68ba-cover.jpeg	\N	{test.kweek.local,my_shoppp.kweek.shop,my-shoppp.kweek.shop}	BJ	XOF	
27	2020-09-15 13:16:11.068071+01	2021-02-12 14:52:32.423669+01	Shoplinecontinental	shoplinecontinental	https://kweek.sgp1.digitaloceanspaces.com/production/7cc3497a-cf31-4682-8874-76d9cb48d2fd-avatar.jpeg	Votre boutique spécialisée dans la vente des dernières collections de grandes marques STREETWEAR .	95585292	43	https://kweek.sgp1.digitaloceanspaces.com/production/6d052aee-780e-47c1-951f-3f6907149931-cover.jpeg	\N	{shoplinecontinental.kweek.shop,shoplinecontinental.kweek.shop}	BJ	XOF	
30	2020-09-16 11:11:26.005932+01	2021-02-12 14:52:32.423669+01	CrepsUrban🇧🇯	crepsurban	https://kweek.sgp1.digitaloceanspaces.com/production/9431bf8d-df7b-48c5-8664-19d80088c258-avatar.jpeg	\N	95704725	48	\N	\N	{crepsurban.kweek.shop,crepsurban.kweek.shop}	BJ	XOF	
31	2020-09-16 14:04:21.308717+01	2021-02-12 14:52:32.423669+01	PHINIX	laleye	https://kweek.sgp1.digitaloceanspaces.com/production/21eb62a4-dfc0-4916-bda2-df71de09371d-avatar.jpeg	Batéries en gris huile d’arachide en gros piment en gros  tout ce qui es agroalimentaire import -export	60242042	49	https://kweek.sgp1.digitaloceanspaces.com/production/dbef4fc9-98a5-41a9-a871-ca0fd09a9b5e-cover.jpeg	\N	{laleye.kweek.shop,laleye.kweek.shop}	BJ	XOF	
34	2020-09-18 14:47:27.940581+01	2021-02-12 14:52:32.423669+01	Capitaine Jago	fernando	https://kweek.sgp1.digitaloceanspaces.com/production/e230569c-da80-4308-8933-162a62e5c9d7-avatar.jpeg	Street wear clothe\nBy Capitaine Jago\n#insideLife	69136944	53	https://kweek.sgp1.digitaloceanspaces.com/production/344040f5-f815-4eb8-8ab1-4afca053a58f-cover.jpeg	\N	{fernando.kweek.shop,fernando.kweek.shop}	BJ	XOF	
36	2020-09-19 16:01:36.727409+01	2021-02-12 14:52:32.423669+01	Elhadj arafat Trade Center	abdouarafat	https://kweek.sgp1.digitaloceanspaces.com/production/a27a6d52-5a7e-49cf-b6b3-009527497b60-avatar.png	\N	(229)62822779	56	\N	6	{abdouarafat.kweek.shop,abdouarafat.kweek.shop}	BJ	XOF	
37	2020-09-19 18:24:25.826478+01	2021-02-12 14:52:32.423669+01	Elohim service	zayed	https://kweek.sgp1.digitaloceanspaces.com/production/9680b01b-6ed1-4ea5-8329-11db21d3ee72-avatar.jpeg	Elohim service est une boutique en ligne de vente divers. En allant des ordinateurs portables, matériels informatiques aux vêtements(hommes, femmes).	0022990589307	57	https://kweek.sgp1.digitaloceanspaces.com/production/bcdcbcad-cc2f-480f-8e61-ea0d4f042a28-cover.jpeg	7	{zayed.kweek.shop,zayed.kweek.shop}	BJ	XOF	
42	2020-09-23 09:36:53.908812+01	2021-02-12 14:52:32.423669+01	Mèches shopping	fara	https://kweek.sgp1.digitaloceanspaces.com/production/1b8ab24b-22e2-463a-abde-1dc20d566757-avatar.jpeg	\N	51464813	65	\N	7	{fara.kweek.shop,fara.kweek.shop}	BJ	XOF	
38	2020-09-19 20:45:54.76103+01	2021-02-12 14:52:32.423669+01	winner Center Top Bizness	gbeganfollyedoh	https://kweek.sgp1.digitaloceanspaces.com/production/cf131ccc-f018-4e92-9df1-3233696788a8-avatar.jpeg	vente de tous genres de produits. import export.	+22965651024	58	https://kweek.sgp1.digitaloceanspaces.com/production/3e33694e-c1df-404b-beb7-dce2e6ec0807-cover.jpeg	7	{gbeganfollyedoh.kweek.shop,gbeganfollyedoh.kweek.shop}	BJ	XOF	
51	2020-10-02 13:03:29.130446+01	2021-02-12 14:52:32.423669+01	LalaBeauties	lala	https://kweek.sgp1.digitaloceanspaces.com/production/9c40edd3-4041-4643-8c14-739c9d204a42-avatar.jpeg	\N	96157994	83	\N	\N	{lala.kweek.shop,lala.kweek.shop}	BJ	XOF	
54	2020-10-08 17:15:17.417604+01	2021-02-12 14:52:32.423669+01	Mon Livre	tinodele	https://kweek.sgp1.digitaloceanspaces.com/production/cd0c1265-a700-4768-9189-788cd5847ac7-avatar.jpeg	\N	62814106	87	\N	\N	{tinodele.kweek.shop,tinodele.kweek.shop}	BJ	XOF	
57	2020-12-31 12:47:00.201814+01	2021-02-12 14:52:32.423669+01	CML Global Service	cisseml	https://kweek.sgp1.digitaloceanspaces.com/production/cf14bc66-c1df-441f-ae40-7fdaafe5ee65-avatar.jpeg	Votre satisfaction notre objectif	90395639	92	\N	\N	{cisseml.kweek.shop,cisseml.kweek.shop}	BJ	XOF	
39	2020-09-19 22:55:07.202112+01	2021-02-12 14:52:32.423669+01	La nouvelle technologie	gbeganbruno	https://kweek.sgp1.digitaloceanspaces.com/production/700b5da2-369a-4e8c-b4af-4dca43121837-avatar.jpeg	🛫🛫🛫🛫📢🔊\nTous ceux qui veulent commander des ordinateurs de toutes marques , des téléphones portables de toutes marques y compris les autres outils informatiques et des produits cosmétiques (mèches,parfums, pommades....), les habits et chaussures de qualités et de bonnes marques . N'hésitez plus la meilleure solution c'est nous, FUTURIX  est disposé à vous aider et surtout à un coût très moins chère. En effet toutes nos commandes s'effectuent en ligne depuis Hongkong, en Chine de surcroît sur Alibaba. La livraison se fait dans un bref délai au plus tard 72h et en toute sécurité , principalement par voie aérienne.🛬🛬🛬\n\nEn dehors de cela, nous expedions et réceptionnons  des colis, des marchandises et autres articles venant et vers tous les pays du monde 🌐 sans exception. \n\nNB: Nous exerçons notre activité en toute légalité. Sans arnaque, sans abus. \n\nCommercer avec FUTURIX, vous ne serez jamais déçus puisque notre force réside dans la confiance et la sincérité. \n\nAvançons ensemble avec FUTURIX ! \n\nAvec FUTURIX réaliser votre rêve d'homme d'affaire. Avec FUTURIX Devenez de vrais business man ! \n\n\nSiège social: calavi arconvil, en fasse du siège de l'union progresisite (calavi) \n\nTel, whatsap: +22951219955.ou appeler sur +22998322113\ngbeganenos@gmail.comExpedion et réception de colis, courriers et marchandises.\nOrdinateur portable Samsung\n\nExpedion et réception de colis, courriers et marchandises.	+22998322113	59	https://kweek.sgp1.digitaloceanspaces.com/production/b6cdedbe-72cb-4107-9429-a2c1fbce5e8e-cover.jpeg	6	{gbeganbruno.kweek.shop,gbeganbruno.kweek.shop}	BJ	XOF	
56	2020-10-16 16:23:17.638965+01	2021-02-12 14:52:32.423669+01	Dcc boutique	dcc-boutique	https://kweek.sgp1.digitaloceanspaces.com/production/99559f1a-4b86-4db3-9083-05f6d965ce1e-avatar.jpeg	\N	+229 62 65 78 48	90	\N	7	{dcc_boutique.kweek.shop,dcc-boutique.kweek.shop}	BJ	XOF	
\.


--
-- Data for Name: sms_verification; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.sms_verification (id, created_at, modified_at, security_code, phone_number, session_token, is_verified) FROM stdin;
7a41160d-e3a6-4695-9b80-7ae28c634da5	2021-01-06 08:27:11.241632+01	2021-01-06 08:27:31.149788+01	537243	+22997462924	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTc0NjI5MjQiLCJub25jZSI6MC45NjU0MTMzODU5MTI2NDZ9.kMz5fq6YycwmJVz_eAB3dNv-gEdbWiMv6A2AjM7w0DI	t
dd5be02b-d257-442d-b187-9ff925dc7f3c	2020-09-16 15:01:58.302385+01	2020-09-16 15:02:22.924956+01	568651	+22960242042	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjAyNDIwNDIiLCJub25jZSI6MC4yMDAzMjQ2NDQ5MjUzNDU5Nn0.w7ZwnGUr2bP8XtQRnQ85s-dSg7322fuMXEjJRZYymn4	t
58b88551-5b6c-4401-ae29-7f06071f9c38	2020-09-22 10:58:40.397567+01	2020-09-22 10:58:40.397594+01	016256	+22990589306	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTA1ODkzMDYiLCJub25jZSI6MC4xNjc4NTY3OTY2ODk1ODk0Mn0.ezwfyAKzUv7XTGwYVVx2yDdzzhQw29n35uKofMq7B6c	f
6e73adeb-3d3d-4432-a6ec-e2f57da22cd5	2020-09-12 23:19:56.343343+01	2020-09-12 23:19:56.343369+01	134568	+22990137018	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTAxMzcwMTgiLCJub25jZSI6MC42NjU4MzMyODgxMjEyNDY1fQ.GYjKCOX7fBpCUlgCery-95j07pINS3XpVjKzJzZHd_U	f
80903520-bcfb-43e1-9a55-0c42022fba05	2020-09-22 10:58:40.399063+01	2020-09-22 10:58:57.814512+01	133523	+22990589306	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTA1ODkzMDYiLCJub25jZSI6MC42ODkzMDEyNTc2NjkyMDk4fQ.xevIuXuZHR7qdGVitZkEVAHtwlYrHuvjg3JtF0a3s_Q	t
1162785d-8f80-4ad0-846b-b50d4371b567	2020-10-16 13:20:06.912665+01	2020-10-16 13:20:30.702397+01	078767	+22967596733	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc1OTY3MzMiLCJub25jZSI6MC4wNzk4Mjk1NzA0ODY2MjM1NH0.cc5s29jnalj4YG4Dh_B86-v3ybAixPtKWoxtyc1Xrgo	t
337444f7-5b4c-46d3-85e3-f896ffe4b50a	2020-09-22 18:10:25.928089+01	2020-09-22 18:10:25.928121+01	023516	+22997819176	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTc4MTkxNzYiLCJub25jZSI6MC4xNDE5OTczNDE3OTMwOTk5N30.km-bZ_KIOiJEINeHMbMOL-1huv5d3yZAAYGvYEQvEDs	f
c63763a2-ada1-4570-aec3-c18a48505c84	2020-09-22 14:34:52.714801+01	2020-09-22 14:35:53.833645+01	826627	+22967648468	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc2NDg0NjgiLCJub25jZSI6MC44ODM4NzUxNDcxODgxOTI0fQ.KsbD0n-DlyWlt6WmUphNRS9bvYeVNJhto-5vrct-RiU	t
e183909c-3f32-43f6-850f-af307d1158ad	2020-09-15 14:11:38.334649+01	2020-09-15 14:12:13.663426+01	665885	+22995585292	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTU1ODUyOTIiLCJub25jZSI6MC4xMzE4MDUzNzY2NjQzNDJ9.1iFMazd-M5B8xZwmd_BzaKiGvf9kskYtl9X3742pjJc	t
3b439472-f9a9-41ea-9254-850830b80138	2020-09-15 19:32:10.942841+01	2020-09-15 19:32:40.207732+01	887007	+22996393676	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYzOTM2NzYiLCJub25jZSI6MC4yOTg2NjQ4MDYxMjA5Mjc3fQ.i1ip6CVKc6XHR4AFmIcao1AdulFtWLSct916BZNO23w	t
31410dc5-e050-41d6-bac0-1227309f2fb9	2020-12-31 17:30:26.399622+01	2020-12-31 17:30:38.222563+01	582920	+22990395639	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTAzOTU2MzkiLCJub25jZSI6MC4wNTMyODMwMjMwNDkwNzAwNjZ9.9oGWi3LpHqlLi09JK2boGTpL1CmFsy6jTGQ9cQtkypM	t
4f30350b-a0db-4e62-b799-4df7738cbc79	2020-09-22 22:24:31.631515+01	2020-09-22 22:24:45.622759+01	584250	+22996330428	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYzMzA0MjgiLCJub25jZSI6MC42MTIyMzE0MzY5NDMxNTY2fQ.o8aM_yF2E8VfkY45-yM0QgTPqyFE_NioF5hyp9HJabk	t
997cd537-fc2a-4ef1-ad13-52d4956267a2	2020-12-02 08:10:00.875271+01	2020-12-02 08:10:12.95389+01	011027	+22960507951	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjA1MDc5NTEiLCJub25jZSI6MC41NDMyMTQ5NzEyNDY5OTA3fQ.SP49dWUa02LFr_TtfJ0xsuKYCBA693g9UWAxPNSzWRQ	t
5895a98a-fd37-47e7-8eb0-7a98343afee6	2020-09-16 09:56:00.715475+01	2020-09-16 09:56:24.404523+01	680829	+22967585597	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc1ODU1OTciLCJub25jZSI6MC4wNTU0NDI0ODU1NDg4MzM0NjR9.1_xJmnKcr0_ye_1ocsvPCxDg-ssKMUzTmm-I5OpRYZw	t
bd08629d-1be9-4ac9-a4c1-ca0415275b00	2020-09-16 16:17:11.899433+01	2020-09-16 16:31:41.890056+01	933072	+22967715329	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc3MTUzMjkiLCJub25jZSI6MC43MDM1OTc1NzQ1MzA5Mjc1fQ.eeMCyQaj7_NJc7MSzPyNilNYnUrw1pV5BOdnfH8m3-M	t
2430e230-66ec-4fa5-9663-15284dc49343	2020-09-20 23:01:57.79153+01	2020-09-20 23:02:16.777368+01	770603	+22996285122	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYyODUxMjIiLCJub25jZSI6MC43Mzk5NzEyODQzODU5NzQ1fQ.-C2RbkW8jfZCuUUz0g7gBzEmXRF5mvQKYTM-h4br0m0	t
3e7007b1-4422-4944-8ba9-ae2f44cada19	2020-09-16 12:09:39.654697+01	2020-09-16 12:09:47.568329+01	958416	+22995704725	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTU3MDQ3MjUiLCJub25jZSI6MC4yMzcwNDYxODYxODAzOTg5N30.aaae4QL38GnaEqPoDNHafNPYbsqhQsKsrJia41QNnqM	t
fcd80efc-898b-4b20-a3b2-b42d54bb0055	2020-09-16 20:15:07.444395+01	2020-09-16 20:15:49.626058+01	009441	+22961572694	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjE1NzI2OTQiLCJub25jZSI6MC43NzIzMjU0MDM1MTM2MTczfQ.WXnC907wCe7Zp6NacZBPTa47Jr8J2eUWnJALDV57VXY	t
4ba75ae4-ac63-4afe-9f18-0470d0fe7a88	2020-09-18 17:17:55.051475+01	2020-09-18 17:19:20.555137+01	636320	+22995009416	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTUwMDk0MTYiLCJub25jZSI6MC4xMTgyOTIwMjUwMjk3MjMwMn0.X2bqZaxT1moXcNIGr8Xwf1w6hvVT0YUkgPIUkGHafOs	t
6562bbfc-c52a-4e84-9bfc-fff776cccdac	2020-09-19 08:49:39.381778+01	2020-09-19 08:49:50.370172+01	605531	+22969136944	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjkxMzY5NDQiLCJub25jZSI6MC41NTk0MjY5NDU3NzA4NzM5fQ.qMQXBrX5YTetBS7HG_M4C6ziYuAejtsMQvJhwKvIYkk	t
9988a4d4-5c2d-4ff3-a3b5-a6215c31abb5	2020-09-20 01:51:58.210167+01	2020-09-20 01:53:01.355158+01	483718	+22997073662	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTcwNzM2NjIiLCJub25jZSI6MC4yMzQxODM0MjM4NTAzNTIwN30.Xm3m2zGvybw7ixEBb_kCQV4Qz3nitVBmc3qAMmYnlA0	t
0d72541e-4ef3-428e-9340-ec4b7456c463	2020-09-20 22:33:35.268038+01	2020-09-20 22:33:50.656788+01	684098	+22997164343	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTcxNjQzNDMiLCJub25jZSI6MC43NjE5NTg2NzkwMDM5MzQ3fQ.t3WSkG_fHkKAIpVcfsYD9N7tnGwz3_6DcmmhvSMs_jY	t
858553e9-9f44-4c2b-b9b4-c3ed48852f9e	2020-09-23 10:34:26.346051+01	2020-09-23 10:34:43.94899+01	104242	+22996013057	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYwMTMwNTciLCJub25jZSI6MC4xODI5MjA1MTg0OTI4NjMwNn0.Vc_1xbUldTQ109sqhsJx-iLr8WuL-KScdemoUh9Lwlc	t
3745aa3a-d579-47be-8404-e65091f15534	2020-09-24 17:43:27.224585+01	2020-09-24 17:43:27.224613+01	886461	+22967721249	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc3MjEyNDkiLCJub25jZSI6MC44MTc5NjM2NjkzNTQxMDk3fQ.ojJlgst5LBMIiHlwIbwX85ZX-anHvrp14R2JkO86-N4	f
adece8de-a56c-4a32-8c6a-70c1de6ebbd1	2020-09-24 19:26:55.850715+01	2020-09-24 19:27:29.750379+01	042772	+22962668847	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI2Njg4NDciLCJub25jZSI6MC4xNDQzOTM5MDQ0Mzc2NzM4Nn0.Pvxm-IkaRHgzz4FtxARC0EXyaTz_dBbk2j-kLxNBdAM	t
40dc7586-2f04-487f-95e6-22a7932fb4ac	2020-09-23 18:47:33.294474+01	2020-09-23 18:48:32.674555+01	727716	+22966061252	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjYwNjEyNTIiLCJub25jZSI6MC4wODg0MDI4NzUzMTg3MzU3fQ.kYWk6nT6r7W3PiwgXXsoq50F9gfGHs6GnOKVW4dZfhc	t
b03a2a55-31af-43c6-a223-c0e20d44e076	2020-10-14 14:16:55.373133+01	2020-10-14 14:17:32.843773+01	857581	+22961888333	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjE4ODgzMzMiLCJub25jZSI6MC4zMzczNjY0OTYwNzY4MTQ5fQ.Sc2GBBM-s1DCAwrnjFtDaWei13T78r1OBVwrcYza1SY	t
0f19ff48-f696-4d53-96a7-925d75499ffc	2020-09-24 22:32:38.597853+01	2020-09-24 22:32:51.05531+01	895177	+22996959610	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTY5NTk2MTAiLCJub25jZSI6MC40MzkyMzYxOTA5MTUxNzc1fQ.2MFBFj_zZ8lqTvB_0_a16kmMij-cAsPciGbl8lQyUQo	t
7602bb51-6365-49de-bc1d-606f95dd5287	2020-09-29 22:40:41.515295+01	2020-09-29 22:40:58.240641+01	827634	+22990589307	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTA1ODkzMDciLCJub25jZSI6MC44MTg2NzMxNzUzOTA3NzQ4fQ.zAnwIoCw7WrZUheflO4meNFkdbWw2hpAzUyvvQqHP_M	t
f18921a9-4ea0-4ac7-a9f2-1940f7775481	2020-10-16 17:28:32.104332+01	2020-10-16 17:29:01.810272+01	072140	+22962657848	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI2NTc4NDgiLCJub25jZSI6MC42ODkxNTA0NTMwMTY0NzI0fQ.pRwY2pB9fboKi_N946NHkg1SXbuwW9IoMwoVn-E1UNI	t
a31d6233-7581-4f4c-a4a4-5eda55bbebc7	2020-11-20 13:44:26.010446+01	2020-11-20 13:44:39.915749+01	841134	+22961001272	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjEwMDEyNzIiLCJub25jZSI6MC44NTc2NjA1NjM5NjU3OTk5fQ.Jd1u9tt7HyEFdlCJrqgPW9Xofm0YrsHMYScTpzJa288	t
a7e4801b-8fbe-4fa8-ba0c-709ee4023dc3	2020-10-07 17:19:14.534506+01	2020-10-07 17:19:14.534534+01	922070	+22997128517	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTcxMjg1MTciLCJub25jZSI6MC4yMjU2MDI5MzU3MTUzMDI2NX0.t6epuddJ6S7DQI-YIT_ZY29vs3i76RxENiiyYfM1KHw	f
8c59e8e8-aa5b-400a-b07f-6193e2c57e2e	2020-09-24 08:51:24.324362+01	2020-09-24 08:51:36.795129+01	469287	+22997259370	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTcyNTkzNzAiLCJub25jZSI6MC4zMjEzNDE1NzgxMzU5MjUyM30.0RaLVwEUsQQ_WOrSZ38vKoLogcU8oxxf9DKuyRLmcZ0	t
a4787ebf-6af4-4fec-82b7-c53312b0e412	2020-09-24 10:09:55.499946+01	2020-09-24 10:10:26.834683+01	417976	+22962822779	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI4MjI3NzkiLCJub25jZSI6MC42NTY3MDYzMzk5NjYzODA2fQ._Apn2S_bSLKi--BcrB9OreC3KefqUs2iYPwqzfEJANA	t
1b852444-de17-4ad6-b29b-bb5207185557	2020-09-24 10:20:30.731614+01	2020-09-24 10:20:56.820031+01	496446	+22967520043	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc1MjAwNDMiLCJub25jZSI6MC45OTYzNTc2NDYzNjI5ODl9.qYjznKGzWLMPXof3LBBvy4ib_btvsq9At4ouvHWtDb8	t
d2a4e54f-e44c-4c96-9afd-f901ca5a7e73	2020-09-25 17:56:46.882394+01	2020-09-25 17:57:01.926537+01	074528	+22997061335	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTcwNjEzMzUiLCJub25jZSI6MC41NTEwNjE4NTMxOTc2ODkxfQ.rfTrKXMZ0RgfRdJyAVX_qjkD42_ggCL4Zc6d-MZtGdI	t
f74de51f-8cec-4f89-a12e-571785883142	2020-09-28 14:40:27.850737+01	2020-09-28 14:40:50.206617+01	590488	+22966266562	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjYyNjY1NjIiLCJub25jZSI6MC4zODU3MDE3NjU3NzM2MjgxNH0.8dR-ejFtte7IGTg7ATqV9eG7uZbIO_lwmV6bAJBHLIg	t
9ea429f9-7775-40df-ad87-13f622947e7f	2020-10-04 17:27:07.097777+01	2020-10-04 17:27:07.097803+01	876681	+22962667580	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI2Njc1ODAiLCJub25jZSI6MC4xNjgyMjk1MDU1MjkwNjAwMn0.HkxmofN-QpWiRRU6gS_sxM1wIdYV19czbhCPi17ZfXQ	f
23402102-95f9-480a-b2b2-e271b2863213	2020-09-28 16:10:19.13463+01	2020-09-28 16:10:19.134661+01	586595	+22965651024	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjU2NTEwMjQiLCJub25jZSI6MC42NDY5NDE2NDA4NTQxMTQ1fQ.eHeN-0xUt3Fj40XrhGkryo2p910HQPP5n-GgVUsNQIQ	f
b547f2ac-5ed6-4aaf-ae13-f8e15b956014	2020-10-03 10:45:02.73793+01	2020-10-03 10:45:09.615307+01	227284	+22962606333	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI2MDYzMzMiLCJub25jZSI6MC4yNDcyMzI3MTkzMDgxOTl9.mYZUHqzYrxym9BiEM3UCTa31bIKZTpY-bpjgpIBQSMU	t
37538073-107e-4bf9-a304-0ed5f5b5d4e9	2020-09-29 20:50:32.06695+01	2020-09-29 20:50:53.55102+01	291640	+22951219955	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NTEyMTk5NTUiLCJub25jZSI6MC4yMzQ3NjAxMjE0NjAwMjAyM30.7TvPA_p-9vArh16L-_qniS18KZQ5IjAqq6X4d6vmK3Q	t
064ab19f-562a-4157-bc0c-77fa28ccc27a	2020-10-03 14:23:13.186077+01	2020-10-03 14:23:25.774599+01	261104	+22951446843	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NTE0NDY4NDMiLCJub25jZSI6MC4zNDEzNTAyMDkyNzkyOTk3fQ.9ZmnDhayiI0xuageX3w8TlNZihxc0GwvmtKcRcBcNlo	t
9e854dfd-9b8a-4add-9d31-9519c3bff7a8	2020-10-02 13:49:05.900019+01	2020-10-02 13:49:17.130396+01	561221	+22996157994	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYxNTc5OTQiLCJub25jZSI6MC4yMzM0NDA5MzE4NzA0NDYxMn0.bxmXKctpcBd28NCQnyLB6ioNawvqzWQghkO6oGxfFro	t
9f968d22-6a31-42bc-836c-c406d3680248	2020-10-03 17:57:37.385847+01	2020-10-03 17:57:50.00169+01	296836	+22961311421	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjEzMTE0MjEiLCJub25jZSI6MC40NzUxMzYwNDg5MTUxMjAzfQ.SFYtizGLCFHH2up__hsOxb6EeBuVnQpVo1hQJLf-GzQ	t
bde7efaf-b656-432e-a803-ff45b762d8bf	2020-10-06 09:37:18.575637+01	2020-10-06 09:37:33.700685+01	761938	+22962477472	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI0Nzc0NzIiLCJub25jZSI6MC40MTQ0NTkzNzIyNDE1MzY3fQ.mNBLryfZeThlusLchR1wRhSI-DLiMnTU5P_6jzJY-xI	t
d131df6e-5251-4341-b1fd-2bd9efffb55b	2020-10-09 22:09:41.15279+01	2020-10-09 22:09:41.152818+01	372469	+22967529587	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc1Mjk1ODciLCJub25jZSI6MC4wNDc2NTcyNTgwMzYxNjcyN30.GP61twsCf5FjcRrCe0GEAYSOlfLMb_ur8QGlW7o_I7U	f
39958ded-c3dd-45d1-bc88-c989fd26b4f0	2020-10-07 15:34:53.51712+01	2020-10-07 15:34:53.517146+01	789203	+22996005609	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTYwMDU2MDkiLCJub25jZSI6MC4wMzkzMzQ4Nzg1OTE0NDY1NzZ9.xOa_pKd3P1eruZmiTcngFcPPvanP7gTdqREjjScB3dE	f
a075c4ad-9330-4fc2-a5cd-88ec7dd2b3b6	2020-10-08 08:44:18.664037+01	2020-10-08 08:44:26.112785+01	676184	+22960596199	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjA1OTYxOTkiLCJub25jZSI6MC4xNDQ4NjM0MjczNTUzNzczOH0.uW1yG1BUnOV_JOGpKe4bO5GDVDpvqLG42FBahZK-dS8	t
fceb05fe-9b48-435a-8733-a9de5389bf60	2020-10-08 18:11:25.211913+01	2020-10-08 18:11:51.113116+01	910242	+22962814106	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjI4MTQxMDYiLCJub25jZSI6MC4yNjY4NDk5Njg5MTE3NTY4M30.5HBCCGdPfMHEiVSyGaQocvLRgMFf7NKANARrNGrrYzs	t
587f4d8b-bf6c-4b80-adbb-7098b4dac343	2020-10-09 08:40:14.897462+01	2020-10-09 08:40:55.954598+01	200078	+243978511357	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjQzOTc4NTExMzU3Iiwibm9uY2UiOjAuNDU4NTMyMjI4ODg3OTY4NX0.Ir02sgGOTtkYr5JG5D6Qs_iIbkx3BqmIzImBa0-cBlo	t
58db8b77-6da7-404a-b0cb-03626b2c069b	2020-10-09 22:11:45.814404+01	2020-10-09 22:12:00.245983+01	626988	+22966173541	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjYxNzM1NDEiLCJub25jZSI6MC45MTQzODIwMjQwODcwNDExfQ.lDRS9IUSDD6jmVUYuRopMTe6jTidkqa34RSO-qdAdi4	t
2f44cd79-7fea-4bdd-803a-8a69c36bdd9d	2020-10-10 07:29:54.391625+01	2020-10-10 07:30:11.634101+01	565901	+22961283500	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjEyODM1MDAiLCJub25jZSI6MC41MjMwODEyNTIzMDE5NTl9.9juO3IYAzIxveGdvwRFEXrY9fJDb9sZ_KQlPyrXYggE	t
83286c53-2d0d-4bd9-b9ae-41d57c0b18a5	2021-04-05 21:54:15.774619+01	2021-04-05 21:54:40.529806+01	183993	+22967964049	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5Njc5NjQwNDkiLCJub25jZSI6MC42ODkzOTE3MTg1MTA5OTAyfQ.0sp92KGi4MOqjfGK9bXAespAZDndpfyRSMpKWKxN00s	t
ab967717-eb4f-4808-ba6f-fb41ba3678ab	2021-04-07 02:07:21.136138+01	2021-04-07 02:07:51.885308+01	712230	+22990137010	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTAxMzcwMTAiLCJub25jZSI6MC43NTE2NTI4NjE4ODgxNzU3fQ.fjCXEKx3_TCOBrZ3pqFuPlwmulBpOteR6RemSsCMWF8	t
d9e0c6dc-93c8-4eda-bbe1-752cd5e5425e	2021-04-08 10:59:59.264304+01	2021-04-08 11:00:20.353691+01	161532	+22966147258	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjYxNDcyNTgiLCJub25jZSI6MC4zMjgyMzAzNzM2MjIzMzY4N30.xKgyYsLDYVk8e1D0NKgEAPZEB_GKrlZKac_WaVXOjYg	t
554072e4-79d0-47c7-980b-5b38f319fa31	2021-04-14 10:22:37.842522+01	2021-04-14 10:22:47.854992+01	104390	+22966123456	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5NjYxMjM0NTYiLCJub25jZSI6MC40ODYxNzIxOTI3NjQ5NDc2fQ.shjKnPYB6rFLp27UtSeeq2Af9RwSWS2YOnIIWHuoRBc	t
82d2ebe2-3ca5-4e4c-9fcf-990a3787cf31	2021-04-16 12:28:48.88468+01	2021-04-16 12:29:04.828029+01	220390	+22998801811	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTg4MDE4MTEiLCJub25jZSI6MC4yNDE3NDkwMDA5MjI5NTM4Mn0.thwSn5vajAvwp6Ujxqy1Y6RQLeRcQTo40XEp-Re5vvA	t
8457e71a-9637-445f-a276-41528c5fd9d2	2021-02-16 20:38:20.649181+01	2021-02-16 20:44:34.86013+01	218027	+22990909090	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5OTA5MDkwOTAiLCJub25jZSI6MC43OTY2MDg0MTc1MzkxODUyfQ.si4LdS6H4KWBUvV_KyXVWXZdNpsjPGufDBKEEyc1KqM	t
bdee6a66-47fa-439f-8b53-4b2180177686	2021-02-26 22:50:56.002792+01	2021-02-26 22:51:53.991386+01	123456	+22921000000	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiIrMjI5MjEwMDAwMDAiLCJub25jZSI6MC4wOTQ2OTk0NTY4OTc2MzU4MX0.bjmOfdjpG_UAlOaySwjbR_sX1qXKRkCSwdgprM70RRw	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.users (id, created_at, updated_at, username, name, phone_number, avatar_url, date_joined, email, first_name, is_active, is_staff, is_superuser, last_login, last_name, password) FROM stdin;
84	2020-10-03 16:57:50.036181+01	2020-10-03 16:57:50.036195+01	+22961311421	\N	+22961311421	\N	2020-10-03 17:57:50.035766+01			t	f	f	\N		
87	2020-10-08 17:11:51.11847+01	2020-10-08 17:11:51.118483+01	+22962814106	\N	+22962814106	\N	2020-10-08 18:11:51.118216+01			t	f	f	\N		
90	2020-10-16 16:21:36.755656+01	2020-10-16 16:21:36.755669+01	+22962 65 78 48	\N	+22962 65 78 48	\N	2020-10-16 17:21:36.75533+01			t	f	f	\N		
92	2020-12-31 12:43:01.281399+01	2020-12-31 12:43:01.281412+01	+22990395639	\N	+22990395639	\N	2020-12-31 13:43:01.281098+01			t	f	f	\N		
1	2019-07-20 15:50:48.826098+01	2020-09-12 21:07:59.914681+01	bot_one	Bot One	+22912345678	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bx8aKxc2xb8xab4fb39f82-0899-4ec3-989c-f6619263eebf.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!qqEi2lcehdo9YS8GCBo0hFQk6JIFcxikzV2E3ogS
3	2019-07-21 13:31:36.513842+01	2020-09-12 21:07:59.914681+01	kiyani	Kiyani 	+15145776547	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxafqxa0x86xc3xe8d0f9887e-d21a-4eaa-8953-7b002156e417.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!9mno51U4QJ3rPMTU56TGqYf886kZZVdKV1rdbQC1
4	2019-07-24 01:02:52.763459+01	2020-09-12 21:07:59.914681+01	test	Test	+22923456789	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bqxE8xd37094cbd9-aacc-4a26-b0ad-22df82a5c61c.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!Cl2nXr2DkWkVVOq8E8oaQnr8ZtVGDTDXc7aJADkR
5	2019-07-24 02:30:54.673439+01	2020-09-12 21:07:59.914681+01	bintou	Bintou	+15148147810	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxe0x94xf3..798704e2-c648-4b6c-9316-eb075f8158ff.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!UsO2O9YbLTPedr7lkl5yX86vfLEXQeX9Uimi4VgM
6	2019-07-24 12:06:02.645759+01	2020-09-12 21:07:59.914681+01	window_shoppa	Deschant Kounou	+250784492637	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bGwxb3G924477c2b-888c-4fa5-98a3-abb793492e3f.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!eTwl6NUE47GDtRasfwv7Tpnqu9lKbP5wR1X2mByr
7	2019-07-24 15:38:05.041432+01	2020-09-12 21:07:59.914681+01	chapi_black	chapi	+22967186699	https://kweekfiles.sgp1.digitaloceanspaces.com/production/b7xaex03ecaa208e9-a0e7-4676-95ed-b52796e6887a.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!apcQKYLjRElInNzY5kFBDEYpWf09wzoyKqimyHbx
8	2019-07-24 16:05:51.421731+01	2020-09-12 21:07:59.914681+01	ifedeejoy	Israel Ifedayo	+2349035217974	https://kweekfiles.sgp1.digitaloceanspaces.com/production/brx89_xf4_5de8669b-9ab3-44b6-8635-c853ba89aa91.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!pG1ElodSst81A5j9Juo3H0tqWyNc4ADl0D0orue2
9	2019-07-24 19:15:56.556395+01	2020-09-12 21:07:59.914681+01	tchemadon	Armelle	+22994441836	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxd5xbf.xf8x16f2003065-c8a8-4713-affd-e036f14255e8.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!QyQCub2cvCFEhE8v5Cypn2f0DuTVorJCyzP9Xwq1
10	2019-07-25 13:57:49.99567+01	2020-09-12 21:07:59.914681+01	cynthia	Cynthia 	+15149072229	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bx07xcaxbdx1bxa7xb1baa27e21-4df1-4e3c-b225-f483026f2e36.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!BZIfO4sxvlVFbPB22rei1TTEEWlRjgQv2WYe8tiB
11	2019-07-26 04:46:24.467463+01	2020-09-12 21:07:59.914681+01	bamba	mikail	+15145775622	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bx02ex0e.dc1eff9a-8e22-43b6-bc84-491ea46b64d0.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!e5VeGatHWzJgeogzoI6KfFmabzY8K9Yy3z4Tcdvd
12	2019-07-29 14:36:24.584385+01	2020-09-12 21:07:59.914681+01	basile	Basile	+22963302235	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxbcx13xe3xf0xf991d981db-4151-49be-b865-392603718bba.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!Wj7Yppsgh2AM77JxwPsnVoNA1bmCa7iHBzxJtUuk
13	2019-07-29 18:12:28.502659+01	2020-09-12 21:07:59.914681+01	hermann	Hermann	+33695056016	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxb6xf5Eexe1m94765dd5-eafe-4160-8a4c-a2e5b1846785.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!1uahPQk0l3Sj9JUffuzy644X0o3PyBUT3kv0fUWc
14	2019-08-07 09:59:57.527242+01	2020-09-12 21:07:59.914681+01	sossou	winnie	+22962168075	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bTxddzqiVb78f7257-8672-4a13-8995-056a3588f11e.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!8XjXirbf2YirGJ5ULOVtvbo29AXcnGvrlc53lydv
15	2019-08-07 17:03:20.076782+01	2020-09-12 21:07:59.914681+01	ina	Marina	+233549048368	https://kweekfiles.sgp1.digitaloceanspaces.com/production/bxbaxbdW.nx9edcc978f1-a067-4769-af0c-8b7abc98c5d6.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!h09Za0L2GB6IABYBQQmc5M4SmhINI6lI9Pm7nTb9
16	2019-09-12 12:07:49.843718+01	2020-09-12 21:07:59.914681+01	\N	Inès	+22967964049	https://kweek.sgp1.digitaloceanspaces.com/production/bxeb3xfaxf3K51f46372-adcc-411c-ad07-e1dc1ffab9ee.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!hdWaUp8JMMtDiWbfK9bnLorJZTx6hJpOznComhiF
17	2019-09-12 13:02:53.12965+01	2020-09-12 21:07:59.914681+01	\N	Souraya	+22995541610	https://kweek.sgp1.digitaloceanspaces.com/production/bxa231xb8x1fx867f739340-3888-47b9-86d7-182c61e749af.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!lCSwmE64KrIBWxfFAq0JVSEtOoQPK0p4rJwnf6dp
18	2019-09-12 14:07:59.784024+01	2020-09-12 21:07:59.914681+01	\N	Lala Shop👗👙👖👠👜	+22962820640	https://kweek.sgp1.digitaloceanspaces.com/production/bx85xcfZtx8a38b830a59-3a4b-4f23-9ba1-413a584bbb1d.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!JnHeYh5Wv7bcxPrDVzwPtBUVRxD4YpeeyC0kbupL
19	2019-09-12 15:06:49.404183+01	2020-09-12 21:07:59.914681+01	\N	Loulou Fashion House	+22997143431	https://kweek.sgp1.digitaloceanspaces.com/production/bVxfdJ9x97a273730b-6f0f-4682-bc5e-cc10ece7f91d.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!WXMFKhINbute4UjVzdfP2p5u5ljPc3W5IKnsF61m
20	2019-09-13 07:58:02.098882+01	2020-09-12 21:07:59.914681+01	\N	Edith	+22962593189	https://kweek.sgp1.digitaloceanspaces.com/production/bxa8x8ax9ex9ex86d25d8631-5b14-4276-ac02-38c2cbffa67a.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!tqDI52ybb1RYejmwzGesev1zEN9EI3JTBGyJL32C
21	2019-09-13 10:11:56.821218+01	2020-09-12 21:07:59.914681+01	\N	Nikè_Store	+22969020109	https://kweek.sgp1.digitaloceanspaces.com/production/btxd0x88xd7x0cxdb9cb43650-b561-4abb-880d-a04ba3becf7f.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!p0LuLrhCGDEwudTbGOYDDecSzoMbW7DU6HsenXKO
22	2019-09-13 11:33:43.922507+01	2020-09-12 21:07:59.914681+01	\N	Ari fashion 	+22996506247	https://kweek.sgp1.digitaloceanspaces.com/production/bx93xccx03xb1Nx865c497957-4fab-462e-9099-1a457e5072f2.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!QWhtYGbUV7Z8JIw3rPM0tX2IR49w2Tplmvejm3An
23	2019-09-13 15:07:10.834187+01	2020-09-12 21:07:59.914681+01	\N	Shadé	+221773383725	https://kweek.sgp1.digitaloceanspaces.com/production/bx95xf7xcdxa1Bx9ec3a74b90-b494-4e29-aa8c-b0fb2fa96934.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!SQZyYbV0VSbRmwWub2880eefGz3iOiRrduCDeRKz
24	2019-09-13 22:08:41.618229+01	2020-09-12 21:07:59.914681+01	\N	Pamela	+22962968616	https://kweek.sgp1.digitaloceanspaces.com/production/bx81kox1cM3cd3f4b96-e1af-4245-8a6f-34fec20fabba.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!FzgqBKkP8R5L5BzyuQbOkj04ANBcot9e6ovl8W4f
25	2019-09-14 17:29:37.657054+01	2020-09-12 21:07:59.914681+01	\N	Natasha	+22997244124	https://kweek.sgp1.digitaloceanspaces.com/production/bGxa6Qx9dx0c6d1d5366-67b0-47d0-a029-de40209e0b54.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!f8jOPzL37gzhksfUYFeoSwS5zkXyE6TTPLx5ba2o
26	2019-09-14 18:27:52.098045+01	2020-09-12 21:07:59.914681+01	\N	Joyce	+22969062324	https://kweek.sgp1.digitaloceanspaces.com/production/bHYxfd6xabx1f9594e0b8-8770-4a4d-ab22-195dcc21d370.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!sgO0YUKKQM6QTsIpIqVI8XAXu4hCRZragHuC93kM
27	2019-09-16 18:13:41.444278+01	2020-09-12 21:07:59.914681+01	\N	Cyrus	+22963003046	https://kweek.sgp1.digitaloceanspaces.com/production/b26x9dx03x9752843a99-f253-4124-9b9d-d5352d1d286d.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!EpIphClvHyAo0k13gDdmYpclqXW13026NQnZO3N8
28	2019-09-17 07:50:43.985289+01	2020-09-12 21:07:59.914681+01	\N	Aquilasdress 	+22961362697	https://kweek.sgp1.digitaloceanspaces.com/production/bxe6Axc3xcexf9bf13f0a8-1c58-4320-ad62-3f6b49106f8b.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!L4CM4ppy0MLnaHqPExEhO2NPoipoY6gpkaJWYrbk
29	2019-09-18 20:53:06.394389+01	2020-09-12 21:07:59.914681+01	\N	M Fashion🧚‍♀️✨	+22997611691	https://kweek.sgp1.digitaloceanspaces.com/production/bx02G2xcfxf8Ie0898076-f6c9-427b-a6f1-c98f3090f290.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!ic3UtVL0UQJRpdxTQNaEfaqtaMeAlGpDKOmw1KRd
30	2019-09-24 10:51:59.541195+01	2020-09-12 21:07:59.914681+01	\N	MLC Boutik	+22990192571	https://kweek.sgp1.digitaloceanspaces.com/production/bNx86x12xc1xe2sed72b5d6-4acd-4470-82fb-2240e9f7113e.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!DbOfiOwAMKF7eKBfSlftNIQAwHktUBFMDF9vD1IB
95	2021-02-16 20:40:22.352396+01	2021-02-16 20:40:22.352415+01	+22990909090	\N	+22990909090	\N	2021-02-16 20:40:22.343863+01			t	f	f	\N		
31	2019-09-25 12:49:52.890713+01	2020-09-12 21:07:59.914681+01	\N	Caro	+22961329177	https://kweek.sgp1.digitaloceanspaces.com/production/bxd3x15xb8xfcY126a5b96-38e7-4d79-8489-28f811859f5d.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!lTt2saj7brOnImmBCHAruhZY50JiDnfD1jDvtSIW
85	2020-10-06 08:37:33.704896+01	2020-10-06 08:37:33.704909+01	+22962477472	\N	+22962477472	\N	2020-10-06 09:37:33.704607+01			t	f	f	\N		
88	2020-10-14 12:41:16.960659+01	2020-10-14 12:41:16.960671+01	+22961888333	\N	+22961888333	\N	2020-10-14 13:41:16.960313+01			t	f	f	\N		
32	2019-09-27 09:03:23.369922+01	2020-09-12 21:07:59.914681+01	\N	Boutique Couleurs et style 	+22996870115	https://kweek.sgp1.digitaloceanspaces.com/production/btxf5x94wxe3xcaaf1b6851-105f-4e9a-91b6-26de56f4b0fa.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!MbQyLMbwkNPIkQbktzqCr84ieJCDiZB0pEPt1t0u
33	2019-09-27 17:39:44.207003+01	2020-09-12 21:07:59.914681+01	\N	Ramépearl&waxaccessories	+22966938411	https://kweek.sgp1.digitaloceanspaces.com/production/b9x12xc1Gxbfx1f67f0d710-bb02-4783-b7f4-0a532d023bb8.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!Xxt8MzQ6wph7DGd1jSXjF9pW3p1QFP71iGS5gHjQ
34	2019-09-30 14:07:44.83171+01	2020-09-12 21:07:59.914681+01	\N	Bérille	+22962398061	https://kweek.sgp1.digitaloceanspaces.com/production/bx13xb7x83x9ex803004f20a-de49-43d0-b89c-28c290899cea.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!LolBJ8uLi9jJlfiSON74iqTYDYvkFqd7tqtjiqRp
35	2019-09-30 17:53:40.406862+01	2020-09-12 21:07:59.914681+01	\N	Nasline	+22967200441	https://kweek.sgp1.digitaloceanspaces.com/production/bx06xd7xxabf7b53413-1644-47ef-89ac-abbae2c4f6aa.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!UaKig579Bh8XbVmfWT4mFhpxJn5lURyvEyzRecEM
36	2019-10-01 11:56:42.494924+01	2020-09-12 21:07:59.914681+01	\N	A_healthy_you😍	+22997422188	https://kweek.sgp1.digitaloceanspaces.com/production/bxd0Oxf0xa9kxf2eeda7dea-3029-46bc-84b8-a2bc4ff547f3.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!b2EwxjGhGrtURqXKUSLyjZ56OqXJvBhUVvjr2JO1
37	2019-11-26 14:10:46.884629+01	2020-09-12 21:07:59.914681+01	\N	Senami	+22961544002	https://kweek.sgp1.digitaloceanspaces.com/production/b49xf3txb2n6f6f44b2-e211-4ccf-a2da-445b35c26511.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!zQ532wwHXUMlAcWl0LkNaWESsJl1eocHFBZS9lJM
38	2020-06-11 08:51:49.031057+01	2020-09-12 21:07:59.914681+01	\N	Sagar	+917790047764	https://kweek.sgp1.digitaloceanspaces.com/production/bx9bx04xf3193d13ee-02a4-4898-98fe-2d292dcc34f7.jpg	2020-09-12 22:07:59.77293+01			t	f	f	\N		!4Ll1zJqvydM0EKq7l2witaImJnbettczWS9Nko8k
42	2020-09-14 23:03:47.445194+01	2020-09-14 23:03:47.445207+01	+22996330428	\N	+22996330428	\N	2020-09-15 00:03:47.444859+01			t	f	f	\N		
43	2020-09-15 13:12:13.670363+01	2020-09-15 13:12:13.670375+01	+22995585292	\N	+22995585292	\N	2020-09-15 14:12:13.670009+01			t	f	f	\N		
44	2020-09-15 18:32:40.220303+01	2020-09-15 18:32:40.220316+01	+22996393676	\N	+22996393676	\N	2020-09-15 19:32:40.219946+01			t	f	f	\N		
45	2020-09-16 08:56:24.419175+01	2020-09-16 08:56:24.419188+01	+22967585597	\N	+22967585597	\N	2020-09-16 09:56:24.418832+01			t	f	f	\N		
48	2020-09-16 11:09:47.575142+01	2020-09-16 11:09:47.575156+01	+22995704725	\N	+22995704725	\N	2020-09-16 12:09:47.574775+01			t	f	f	\N		
49	2020-09-16 14:02:22.938044+01	2020-09-16 14:02:22.938058+01	+22960242042	\N	+22960242042	\N	2020-09-16 15:02:22.937685+01			t	f	f	\N		
50	2020-09-16 15:17:45.74106+01	2020-09-16 15:17:45.741073+01	+22967715329	\N	+22967715329	\N	2020-09-16 16:17:45.74077+01			t	f	f	\N		
83	2020-10-02 12:49:17.138648+01	2020-10-02 12:49:17.138661+01	+22996157994	\N	+22996157994	\N	2020-10-02 13:49:17.138296+01			t	f	f	\N		
41	2020-09-14 19:18:59.637476+01	2020-09-16 17:12:19.161129+01	+22962606333	Harold	+22962606333	\N	2020-09-14 20:18:59.637101+01			t	f	f	\N		
51	2020-09-16 18:41:26.681923+01	2020-09-16 18:41:26.681936+01	+22966173541	\N	+22966173541	\N	2020-09-16 19:41:26.681536+01			t	f	f	\N		
52	2020-09-16 18:59:13.046427+01	2020-09-16 19:17:39.85847+01	+22961572694	Marc_Aurel	+22961572694	\N	2020-09-16 19:59:13.046071+01			t	f	f	\N		
53	2020-09-18 14:45:31.465581+01	2020-09-18 14:45:31.465595+01	+22969136944	\N	+22969136944	\N	2020-09-18 15:45:31.465235+01			t	f	f	\N		
54	2020-09-18 15:47:49.347072+01	2020-09-18 16:23:21.875776+01	+22995009416	HOUNOUVI Kossi Richard	+22995009416	\N	2020-09-18 16:47:49.34672+01			t	f	f	\N		
55	2020-09-19 11:40:01.643624+01	2020-09-19 11:41:51.589141+01	+22961001272	David	+22961001272	\N	2020-09-19 12:40:01.643147+01			t	f	f	\N		
56	2020-09-19 15:50:48.939508+01	2020-09-19 15:52:31.471072+01	+22962822779	Abdou Arafat	+22962822779	\N	2020-09-19 16:50:48.939176+01			t	f	f	\N		
46	2020-09-16 09:03:01.258248+01	2020-09-19 18:12:44.155609+01	+22951446843	Serge	+22951446843	\N	2020-09-16 10:03:01.257962+01			t	f	f	\N		
57	2020-09-19 18:18:08.392446+01	2020-09-19 18:18:08.392459+01	+22990589307	\N	+22990589307	\N	2020-09-19 19:18:08.392193+01			t	f	f	\N		
58	2020-09-19 20:39:54.550167+01	2020-09-19 20:39:54.550196+01	+22965651024	\N	+22965651024	\N	2020-09-19 21:39:54.549806+01			t	f	f	\N		
59	2020-09-19 22:49:07.024805+01	2020-09-19 22:49:07.024818+01	+22951219955	\N	+22951219955	\N	2020-09-19 23:49:07.024472+01			t	f	f	\N		
60	2020-09-20 00:53:01.363146+01	2020-09-20 00:53:01.363163+01	+22997073662	\N	+22997073662	\N	2020-09-20 01:53:01.362761+01			t	f	f	\N		
47	2020-09-16 09:53:46.532414+01	2020-09-20 21:26:18.365395+01	+22960507951	Billy Pereira	+22960507951	\N	2020-09-16 10:53:46.532169+01			t	f	f	\N		
61	2020-09-20 21:33:50.66275+01	2020-09-20 21:33:50.662764+01	+22997164343	\N	+22997164343	\N	2020-09-20 22:33:50.662388+01			t	f	f	\N		
62	2020-09-20 22:02:16.786113+01	2020-09-20 22:02:16.786127+01	+22996285122	\N	+22996285122	\N	2020-09-20 23:02:16.785759+01			t	f	f	\N		
63	2020-09-21 08:20:56.115862+01	2020-09-21 08:20:56.115876+01	+22990589306	\N	+22990589306	\N	2020-09-21 09:20:56.114699+01			t	f	f	\N		
64	2020-09-22 13:35:53.839178+01	2020-09-22 13:35:53.839191+01	+22967648468	\N	+22967648468	\N	2020-09-22 14:35:53.838936+01			t	f	f	\N		
65	2020-09-23 09:34:43.957046+01	2020-09-23 09:34:43.95706+01	+22996013057	\N	+22996013057	\N	2020-09-23 10:34:43.956799+01			t	f	f	\N		
66	2020-09-23 17:24:04.050706+01	2020-09-23 17:24:04.05072+01	+22966061252	\N	+22966061252	\N	2020-09-23 18:24:04.050305+01			t	f	f	\N		
67	2020-09-23 19:16:42.476608+01	2020-09-23 19:20:15.120775+01	+22997061335	Awad	+22997061335	\N	2020-09-23 20:16:42.476351+01			t	f	f	\N		
68	2020-09-24 07:51:36.80602+01	2020-09-24 07:51:36.806033+01	+22997259370	\N	+22997259370	\N	2020-09-24 08:51:36.805756+01			t	f	f	\N		
69	2020-09-24 09:20:56.824083+01	2020-09-24 09:20:56.824097+01	+22967520043	\N	+22967520043	\N	2020-09-24 10:20:56.823832+01			t	f	f	\N		
70	2020-09-24 18:27:29.762409+01	2020-09-24 18:27:29.762422+01	+22962668847	\N	+22962668847	\N	2020-09-24 19:27:29.761996+01			t	f	f	\N		
71	2020-09-24 21:32:51.060239+01	2020-09-24 21:32:51.060253+01	+22996959610	\N	+22996959610	\N	2020-09-24 22:32:51.059973+01			t	f	f	\N		
72	2020-09-28 13:40:50.214898+01	2020-09-28 13:40:50.214911+01	+22966266562	\N	+22966266562	\N	2020-09-28 14:40:50.214561+01			t	f	f	\N		
73	2020-09-28 20:19:52.738857+01	2020-09-28 20:20:38.008815+01	+22960596199	Marcel	+22960596199	\N	2020-09-28 21:19:52.738495+01			t	f	f	\N		
74	2020-09-29 11:30:12.125511+01	2020-09-29 11:30:12.125524+01	+22961283500	\N	+22961283500	\N	2020-09-29 12:30:12.125167+01			t	f	f	\N		
86	2020-10-06 16:51:54.770283+01	2020-10-07 20:19:41.781827+01	+243978511357	Momo	+243978511357	\N	2020-10-06 17:51:54.770012+01			t	f	f	\N		
89	2020-10-16 12:20:30.711138+01	2020-10-16 12:20:30.711156+01	+22967596733	\N	+22967596733	\N	2020-10-16 13:20:30.710881+01			t	f	f	\N		
91	2020-10-16 16:29:01.817316+01	2020-10-16 16:29:01.817329+01	+22962657848	\N	+22962657848	\N	2020-10-16 17:29:01.816969+01			t	f	f	\N		
93	2021-01-04 10:48:04.927844+01	2021-01-04 10:48:04.927856+01	+22997462924	\N	+22997462924	\N	2021-01-04 11:48:04.927586+01			t	f	f	\N		
96	2021-02-26 22:51:54.005692+01	2021-02-26 22:51:54.005706+01	+22921000000	\N	+22921000000	\N	2021-02-26 22:51:54.005298+01			t	f	f	\N		
97	2021-03-27 13:03:14.603348+01	2021-03-27 13:03:14.603373+01	+229 98 80 18 11	\N	+229 98 80 18 11	\N	2021-03-27 13:03:14.602556+01			t	f	f	\N		
40	2020-09-12 22:12:48.845062+01	2021-04-04 00:25:19.288814+01	+22990137010	Test Bot	+22998801811	\N	2020-09-12 23:12:48.844663+01			t	f	f	\N		
98	2021-04-04 17:56:55.505885+01	2021-04-04 18:00:02.271532+01	+22966123456	Bruce Wayne	+22966123456	\N	2021-04-04 17:56:55.505331+01			t	f	f	\N		
94	2021-01-05 19:59:12.681117+01	2021-04-04 18:42:57.666248+01	+22998801811	Nelson K	+22998801811	\N	2021-01-05 20:59:12.680868+01			t	f	f	\N		
99	2021-04-05 21:54:40.546707+01	2021-04-05 21:54:40.546749+01	+22967964049	\N	+22967964049	\N	2021-04-05 21:54:40.54547+01			t	f	f	\N		
100	2021-04-08 11:00:20.374852+01	2021-04-08 11:00:20.374868+01	+22966147258	\N	+22966147258	\N	2021-04-08 11:00:20.374399+01			t	f	f	\N		
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.users_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: nelson
--

COPY public.users_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: affiliate_agents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.affiliate_agents_id_seq', 11, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 172, true);


--
-- Name: banner_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.banner_new_id_seq', 2, true);


--
-- Name: banners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.banners_id_seq', 1, false);


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 989, true);


--
-- Name: carts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.carts_id_seq', 95, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.categories_id_seq', 5, true);


--
-- Name: checkouts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.checkouts_id_seq', 162, true);


--
-- Name: core_bankaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_bankaccount_id_seq', 1, true);


--
-- Name: core_billingplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_billingplan_id_seq', 86, true);


--
-- Name: core_shippingmethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_shippingmethod_id_seq', 3, true);


--
-- Name: core_shippingprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_shippingprofile_id_seq', 2, true);


--
-- Name: core_shippingprofile_shops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_shippingprofile_shops_id_seq', 76, true);


--
-- Name: core_shippingzone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_shippingzone_id_seq', 3, true);


--
-- Name: core_shopdesign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.core_shopdesign_id_seq', 39, true);


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.customers_id_seq', 27, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 40, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 123, true);


--
-- Name: exchange_rate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.exchange_rate_id_seq', 44370, true);


--
-- Name: kash_checkoutsession_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_checkoutsession_id_seq', 1, false);


--
-- Name: kash_fundinghistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_fundinghistory_id_seq', 4, true);


--
-- Name: kash_invitecode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_invitecode_id_seq', 8, true);


--
-- Name: kash_kashrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashrequest_id_seq', 6, true);


--
-- Name: kash_kashrequest_recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashrequest_recipients_id_seq', 10, true);


--
-- Name: kash_kashrequestresponse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashrequestresponse_id_seq', 6, true);


--
-- Name: kash_kashtransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashtransaction_id_seq', 40, true);


--
-- Name: kash_kashtransaction_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashtransaction_id_seq1', 209, true);


--
-- Name: kash_kashtransaction_paid_recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashtransaction_paid_recipients_id_seq', 26, true);


--
-- Name: kash_kashtransaction_recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_kashtransaction_recipients_id_seq', 46, true);


--
-- Name: kash_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_notification_id_seq', 50, true);


--
-- Name: kash_payoutmethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_payoutmethod_id_seq', 6, true);


--
-- Name: kash_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_profile_id_seq', 4, true);


--
-- Name: kash_virtualcard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_virtualcard_id_seq', 15, true);


--
-- Name: kash_withdrawalhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.kash_withdrawalhistory_id_seq', 1, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.order_items_id_seq', 52, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.orders_id_seq', 26, true);


--
-- Name: product_image_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.product_image_new_id_seq', 370, true);


--
-- Name: product_images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.product_images_id_seq', 1, false);


--
-- Name: product_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.product_new_id_seq', 317, true);


--
-- Name: products_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.products_categories_id_seq', 5, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.products_id_seq', 1, false);


--
-- Name: qosic_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.qosic_transaction_id_seq', 102, true);


--
-- Name: shop_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.shop_new_id_seq', 62, true);


--
-- Name: shops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.shops_id_seq', 1, false);


--
-- Name: user_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.user_new_id_seq', 100, true);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nelson
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- Name: affiliate_agents affiliate_agents_code_e9f85c16_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.affiliate_agents
    ADD CONSTRAINT affiliate_agents_code_e9f85c16_uniq UNIQUE (code);


--
-- Name: affiliate_agents affiliate_agents_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.affiliate_agents
    ADD CONSTRAINT affiliate_agents_pkey PRIMARY KEY (id);


--
-- Name: affiliate_agents affiliate_agents_user_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.affiliate_agents
    ADD CONSTRAINT affiliate_agents_user_id_key UNIQUE (user_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: banners banners_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.banners
    ADD CONSTRAINT banners_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: carts carts_uid_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_uid_key UNIQUE (uid);


--
-- Name: carts carts_uid_unique; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_uid_unique UNIQUE (uid);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: checkouts checkouts_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_pkey PRIMARY KEY (id);


--
-- Name: checkouts checkouts_ref_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_ref_id_key UNIQUE (ref_id);


--
-- Name: checkouts checkouts_uid_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_uid_key UNIQUE (uid);


--
-- Name: checkouts checkouts_uid_unique; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_uid_unique UNIQUE (uid);


--
-- Name: core_bankaccount core_bankaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_bankaccount
    ADD CONSTRAINT core_bankaccount_pkey PRIMARY KEY (id);


--
-- Name: core_bankaccount core_bankaccount_shop_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_bankaccount
    ADD CONSTRAINT core_bankaccount_shop_id_key UNIQUE (shop_id);


--
-- Name: core_billingplan core_billingplan_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_billingplan
    ADD CONSTRAINT core_billingplan_pkey PRIMARY KEY (id);


--
-- Name: core_billingplan core_billingplan_user_id_92db090d_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_billingplan
    ADD CONSTRAINT core_billingplan_user_id_92db090d_uniq UNIQUE (user_id);


--
-- Name: core_shippingmethod core_shippingmethod_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingmethod
    ADD CONSTRAINT core_shippingmethod_pkey PRIMARY KEY (id);


--
-- Name: core_shippingprofile core_shippingprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile
    ADD CONSTRAINT core_shippingprofile_pkey PRIMARY KEY (id);


--
-- Name: core_shippingprofile_shops core_shippingprofile_sho_shippingprofile_id_shop__49430e17_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile_shops
    ADD CONSTRAINT core_shippingprofile_sho_shippingprofile_id_shop__49430e17_uniq UNIQUE (shippingprofile_id, shop_id);


--
-- Name: core_shippingprofile_shops core_shippingprofile_shops_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile_shops
    ADD CONSTRAINT core_shippingprofile_shops_pkey PRIMARY KEY (id);


--
-- Name: core_shippingzone core_shippingzone_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingzone
    ADD CONSTRAINT core_shippingzone_pkey PRIMARY KEY (id);


--
-- Name: core_shopdesign core_shopdesign_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shopdesign
    ADD CONSTRAINT core_shopdesign_pkey PRIMARY KEY (id);


--
-- Name: core_shopdesign core_shopdesign_shop_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shopdesign
    ADD CONSTRAINT core_shopdesign_shop_id_key UNIQUE (shop_id);


--
-- Name: customers customers_email_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);


--
-- Name: customers customers_email_unique; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_unique UNIQUE (email);


--
-- Name: customers customers_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_phone_number_key UNIQUE (phone_number);


--
-- Name: customers customers_phone_number_unique; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_phone_number_unique UNIQUE (phone_number);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: customers customers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: exchange_exchangebackend exchange_exchangebackend_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.exchange_exchangebackend
    ADD CONSTRAINT exchange_exchangebackend_pkey PRIMARY KEY (name);


--
-- Name: exchange_rate exchange_rate_currency_backend_id_c6037b21_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.exchange_rate
    ADD CONSTRAINT exchange_rate_currency_backend_id_c6037b21_uniq UNIQUE (currency, backend_id);


--
-- Name: exchange_rate exchange_rate_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.exchange_rate
    ADD CONSTRAINT exchange_rate_pkey PRIMARY KEY (id);


--
-- Name: kash_checkoutsession kash_checkoutsession_order_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_order_id_key UNIQUE (order_id);


--
-- Name: kash_checkoutsession kash_checkoutsession_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_pkey PRIMARY KEY (id);


--
-- Name: kash_fundinghistory kash_fundinghistory_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_fundinghistory
    ADD CONSTRAINT kash_fundinghistory_pkey PRIMARY KEY (id);


--
-- Name: kash_fundinghistory kash_fundinghistory_txn_ref_3eeb202b_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_fundinghistory
    ADD CONSTRAINT kash_fundinghistory_txn_ref_3eeb202b_uniq UNIQUE (txn_ref);


--
-- Name: kash_invitecode kash_invitecode_code_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode
    ADD CONSTRAINT kash_invitecode_code_key UNIQUE (code);


--
-- Name: kash_invitecode kash_invitecode_invited_id_29fe192a_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode
    ADD CONSTRAINT kash_invitecode_invited_id_29fe192a_uniq UNIQUE (invited_id);


--
-- Name: kash_invitecode kash_invitecode_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode
    ADD CONSTRAINT kash_invitecode_pkey PRIMARY KEY (id);


--
-- Name: kash_kashrequest kash_kashrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest
    ADD CONSTRAINT kash_kashrequest_pkey PRIMARY KEY (id);


--
-- Name: kash_kashrequest_recipients kash_kashrequest_recipie_kashrequest_id_userprofi_95c889ff_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest_recipients
    ADD CONSTRAINT kash_kashrequest_recipie_kashrequest_id_userprofi_95c889ff_uniq UNIQUE (kashrequest_id, userprofile_id);


--
-- Name: kash_kashrequest_recipients kash_kashrequest_recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest_recipients
    ADD CONSTRAINT kash_kashrequest_recipients_pkey PRIMARY KEY (id);


--
-- Name: kash_kashrequestresponse kash_kashrequestresponse_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequestresponse
    ADD CONSTRAINT kash_kashrequestresponse_pkey PRIMARY KEY (id);


--
-- Name: kash_sendkash_paid_recipients kash_kashtransaction_pai_kashtransaction_id_userp_cd77101f_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_paid_recipients
    ADD CONSTRAINT kash_kashtransaction_pai_kashtransaction_id_userp_cd77101f_uniq UNIQUE (sendkash_id, userprofile_id);


--
-- Name: kash_sendkash_paid_recipients kash_kashtransaction_paid_recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_paid_recipients
    ADD CONSTRAINT kash_kashtransaction_paid_recipients_pkey PRIMARY KEY (id);


--
-- Name: kash_sendkash kash_kashtransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash
    ADD CONSTRAINT kash_kashtransaction_pkey PRIMARY KEY (id);


--
-- Name: kash_kashtransaction kash_kashtransaction_pkey1; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction
    ADD CONSTRAINT kash_kashtransaction_pkey1 PRIMARY KEY (id);


--
-- Name: kash_sendkash_recipients kash_kashtransaction_rec_kashtransaction_id_userp_0bc7fb23_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_recipients
    ADD CONSTRAINT kash_kashtransaction_rec_kashtransaction_id_userp_0bc7fb23_uniq UNIQUE (sendkash_id, userprofile_id);


--
-- Name: kash_sendkash_recipients kash_kashtransaction_recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_recipients
    ADD CONSTRAINT kash_kashtransaction_recipients_pkey PRIMARY KEY (id);


--
-- Name: kash_kashtransaction kash_kashtransaction_txn_ref_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction
    ADD CONSTRAINT kash_kashtransaction_txn_ref_key UNIQUE (txn_ref);


--
-- Name: kash_notification kash_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_notification
    ADD CONSTRAINT kash_notification_pkey PRIMARY KEY (id);


--
-- Name: kash_momoaccount kash_payoutmethod_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_momoaccount
    ADD CONSTRAINT kash_payoutmethod_pkey PRIMARY KEY (id);


--
-- Name: kash_userprofile kash_profile_kashtag_7f170fa5_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_userprofile
    ADD CONSTRAINT kash_profile_kashtag_7f170fa5_uniq UNIQUE (kashtag);


--
-- Name: kash_userprofile kash_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_userprofile
    ADD CONSTRAINT kash_profile_pkey PRIMARY KEY (id);


--
-- Name: kash_userprofile kash_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_userprofile
    ADD CONSTRAINT kash_profile_user_id_key UNIQUE (user_id);


--
-- Name: kash_virtualcard kash_virtualcard_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_virtualcard
    ADD CONSTRAINT kash_virtualcard_pkey PRIMARY KEY (id);


--
-- Name: kash_withdrawalhistory kash_withdrawalhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_withdrawalhistory
    ADD CONSTRAINT kash_withdrawalhistory_pkey PRIMARY KEY (id);


--
-- Name: kash_withdrawalhistory kash_withdrawalhistory_txn_ref_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_withdrawalhistory
    ADD CONSTRAINT kash_withdrawalhistory_txn_ref_key UNIQUE (txn_ref);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: orders orders_ref_id_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_ref_id_key UNIQUE (ref_id);


--
-- Name: product_images product_images_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_images_pkey PRIMARY KEY (id);


--
-- Name: products_categories products_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products_categories
    ADD CONSTRAINT products_categories_pkey PRIMARY KEY (id);


--
-- Name: products_categories products_categories_product_id_category_id_1475aa05_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products_categories
    ADD CONSTRAINT products_categories_product_id_category_id_1475aa05_uniq UNIQUE (product_id, category_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: products products_slug_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_slug_key UNIQUE (slug);


--
-- Name: products products_slug_unique; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_slug_unique UNIQUE (slug);


--
-- Name: qosic_transaction qosic_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.qosic_transaction
    ADD CONSTRAINT qosic_transaction_pkey PRIMARY KEY (id);


--
-- Name: qosic_transaction qosic_transaction_reference_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.qosic_transaction
    ADD CONSTRAINT qosic_transaction_reference_key UNIQUE (reference);


--
-- Name: shops shop_username_key1; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shop_username_key1 UNIQUE (username);


--
-- Name: shops shops_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_pkey PRIMARY KEY (id);


--
-- Name: shops shops_username_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_username_key UNIQUE (username);


--
-- Name: sms_verification sms_verification_otp_phone_number_session_code_f31b942e_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.sms_verification
    ADD CONSTRAINT sms_verification_otp_phone_number_session_code_f31b942e_uniq UNIQUE (security_code, phone_number, session_token);


--
-- Name: sms_verification sms_verification_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.sms_verification
    ADD CONSTRAINT sms_verification_pkey PRIMARY KEY (id);


--
-- Name: categories unique_category_slug_per_shop; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT unique_category_slug_per_shop UNIQUE (shop_id, slug);


--
-- Name: users user_username_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_user_id_group_id_fc7788e8_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq UNIQUE (user_id, group_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_user_id_permission_id_3b86cbdf_uniq; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq UNIQUE (user_id, permission_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: affiliate_agents_code_e9f85c16_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX affiliate_agents_code_e9f85c16_like ON public.affiliate_agents USING btree (code varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: cart_items_cart_id_54d2714b; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX cart_items_cart_id_54d2714b ON public.cart_items USING btree (cart_id);


--
-- Name: cart_items_product_id_9398bb89; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX cart_items_product_id_9398bb89 ON public.cart_items USING btree (product_id);


--
-- Name: carts_shop_id_b3319ed3; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX carts_shop_id_b3319ed3 ON public.carts USING btree (shop_id);


--
-- Name: carts_uid_4a761320_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX carts_uid_4a761320_like ON public.carts USING btree (uid varchar_pattern_ops);


--
-- Name: categories_shop_id_7fdd920b; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX categories_shop_id_7fdd920b ON public.categories USING btree (shop_id);


--
-- Name: categories_slug_9bedfe6b; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX categories_slug_9bedfe6b ON public.categories USING btree (slug);


--
-- Name: categories_slug_9bedfe6b_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX categories_slug_9bedfe6b_like ON public.categories USING btree (slug varchar_pattern_ops);


--
-- Name: checkouts_cart_id_999df4ad; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX checkouts_cart_id_999df4ad ON public.checkouts USING btree (cart_id);


--
-- Name: checkouts_customer_id_213d2e87; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX checkouts_customer_id_213d2e87 ON public.checkouts USING btree (customer_id);


--
-- Name: checkouts_ref_id_adcc0088_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX checkouts_ref_id_adcc0088_like ON public.checkouts USING btree (ref_id varchar_pattern_ops);


--
-- Name: checkouts_shipping_profile_id_8c6be142; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX checkouts_shipping_profile_id_8c6be142 ON public.checkouts USING btree (shipping_profile_id);


--
-- Name: checkouts_uid_2dd7fe26_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX checkouts_uid_2dd7fe26_like ON public.checkouts USING btree (uid varchar_pattern_ops);


--
-- Name: core_shippingmethod_zone_id_51ff5d8c; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX core_shippingmethod_zone_id_51ff5d8c ON public.core_shippingmethod USING btree (zone_id);


--
-- Name: core_shippingprofile_shops_shippingprofile_id_82b14099; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX core_shippingprofile_shops_shippingprofile_id_82b14099 ON public.core_shippingprofile_shops USING btree (shippingprofile_id);


--
-- Name: core_shippingprofile_shops_shop_id_c3842613; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX core_shippingprofile_shops_shop_id_c3842613 ON public.core_shippingprofile_shops USING btree (shop_id);


--
-- Name: core_shippingzone_profile_id_92750062; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX core_shippingzone_profile_id_92750062 ON public.core_shippingzone USING btree (profile_id);


--
-- Name: customers_email_af8f39bb_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX customers_email_af8f39bb_like ON public.customers USING btree (email varchar_pattern_ops);


--
-- Name: customers_phone_number_1e2e2966_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX customers_phone_number_1e2e2966_like ON public.customers USING btree (phone_number varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: exchange_exchangebackend_name_8f97aa6b_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX exchange_exchangebackend_name_8f97aa6b_like ON public.exchange_exchangebackend USING btree (name varchar_pattern_ops);


--
-- Name: exchange_rate_backend_id_d57e3a62; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX exchange_rate_backend_id_d57e3a62 ON public.exchange_rate USING btree (backend_id);


--
-- Name: exchange_rate_backend_id_d57e3a62_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX exchange_rate_backend_id_d57e3a62_like ON public.exchange_rate USING btree (backend_id varchar_pattern_ops);


--
-- Name: kash_checkoutsession_cart_id_cbb308da; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_checkoutsession_cart_id_cbb308da ON public.kash_checkoutsession USING btree (cart_id);


--
-- Name: kash_checkoutsession_shop_id_2c254b1e; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_checkoutsession_shop_id_2c254b1e ON public.kash_checkoutsession USING btree (shop_id);


--
-- Name: kash_checkoutsession_user_id_d21678a6; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_checkoutsession_user_id_d21678a6 ON public.kash_checkoutsession USING btree (user_id);


--
-- Name: kash_fundinghistory_card_id_053f9d3f; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_fundinghistory_card_id_053f9d3f ON public.kash_fundinghistory USING btree (card_id);


--
-- Name: kash_fundinghistory_txn_ref_3eeb202b_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_fundinghistory_txn_ref_3eeb202b_like ON public.kash_fundinghistory USING btree (txn_ref varchar_pattern_ops);


--
-- Name: kash_invitecode_code_c009d54c_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_invitecode_code_c009d54c_like ON public.kash_invitecode USING btree (code varchar_pattern_ops);


--
-- Name: kash_invitecode_inviter_id_07e11b31; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_invitecode_inviter_id_07e11b31 ON public.kash_invitecode USING btree (inviter_id);


--
-- Name: kash_kashrequest_initiator_id_b2a52673; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequest_initiator_id_b2a52673 ON public.kash_kashrequest USING btree (initiator_id);


--
-- Name: kash_kashrequest_recipient_id_823d2981; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequest_recipient_id_823d2981 ON public.kash_kashrequest USING btree (recipient_id);


--
-- Name: kash_kashrequest_recipients_kashrequest_id_8daa10bf; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequest_recipients_kashrequest_id_8daa10bf ON public.kash_kashrequest_recipients USING btree (kashrequest_id);


--
-- Name: kash_kashrequest_recipients_userprofile_id_9b486648; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequest_recipients_userprofile_id_9b486648 ON public.kash_kashrequest_recipients USING btree (userprofile_id);


--
-- Name: kash_kashrequestresponse_request_id_4fd0434d; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequestresponse_request_id_4fd0434d ON public.kash_kashrequestresponse USING btree (request_id);


--
-- Name: kash_kashrequestresponse_sender_id_d1e7bcdc; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequestresponse_sender_id_d1e7bcdc ON public.kash_kashrequestresponse USING btree (sender_id);


--
-- Name: kash_kashrequestresponse_transaction_id_bcf42fe3; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashrequestresponse_transaction_id_bcf42fe3 ON public.kash_kashrequestresponse USING btree (transaction_id);


--
-- Name: kash_kashtransaction_initiator_id_9ee47f0d; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_initiator_id_9ee47f0d ON public.kash_sendkash USING btree (initiator_id);


--
-- Name: kash_kashtransaction_paid__kashtransaction_id_514c2090; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_paid__kashtransaction_id_514c2090 ON public.kash_sendkash_paid_recipients USING btree (sendkash_id);


--
-- Name: kash_kashtransaction_paid_recipients_userprofile_id_84a5cf51; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_paid_recipients_userprofile_id_84a5cf51 ON public.kash_sendkash_paid_recipients USING btree (userprofile_id);


--
-- Name: kash_kashtransaction_profile_id_64677415; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_profile_id_64677415 ON public.kash_kashtransaction USING btree (profile_id);


--
-- Name: kash_kashtransaction_receiver_type_id_ef186451; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_receiver_type_id_ef186451 ON public.kash_kashtransaction USING btree (receiver_type_id);


--
-- Name: kash_kashtransaction_recipients_kashtransaction_id_a52b6ff6; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_recipients_kashtransaction_id_a52b6ff6 ON public.kash_sendkash_recipients USING btree (sendkash_id);


--
-- Name: kash_kashtransaction_recipients_userprofile_id_67f5c645; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_recipients_userprofile_id_67f5c645 ON public.kash_sendkash_recipients USING btree (userprofile_id);


--
-- Name: kash_kashtransaction_sender_id_fb3cfd81; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_sender_id_fb3cfd81 ON public.kash_kashtransaction USING btree (sender_id);


--
-- Name: kash_kashtransaction_txn_ref_92b8b874_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_kashtransaction_txn_ref_92b8b874_like ON public.kash_kashtransaction USING btree (txn_ref varchar_pattern_ops);


--
-- Name: kash_notification_content_type_id_cc4a1cca; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_notification_content_type_id_cc4a1cca ON public.kash_notification USING btree (content_type_id);


--
-- Name: kash_notification_profile_id_246c4acb; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_notification_profile_id_246c4acb ON public.kash_notification USING btree (profile_id);


--
-- Name: kash_payoutmethod_profile_id_17e33730; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_payoutmethod_profile_id_17e33730 ON public.kash_momoaccount USING btree (profile_id);


--
-- Name: kash_profile_kashtag_7f170fa5_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_profile_kashtag_7f170fa5_like ON public.kash_userprofile USING btree (kashtag varchar_pattern_ops);


--
-- Name: kash_virtualcard_profile_id_8f77d62e; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_virtualcard_profile_id_8f77d62e ON public.kash_virtualcard USING btree (profile_id);


--
-- Name: kash_withdrawalhistory_card_id_baff692a; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_withdrawalhistory_card_id_baff692a ON public.kash_withdrawalhistory USING btree (card_id);


--
-- Name: kash_withdrawalhistory_txn_ref_7ffaecf9_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX kash_withdrawalhistory_txn_ref_7ffaecf9_like ON public.kash_withdrawalhistory USING btree (txn_ref varchar_pattern_ops);


--
-- Name: order_items_order_id_412ad78b; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX order_items_order_id_412ad78b ON public.order_items USING btree (order_id);


--
-- Name: order_items_product_id_dd557d5a; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX order_items_product_id_dd557d5a ON public.order_items USING btree (product_id);


--
-- Name: orders_customer_id_b7016332; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX orders_customer_id_b7016332 ON public.orders USING btree (customer_id);


--
-- Name: orders_ref_id_3fc550e3_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX orders_ref_id_3fc550e3_like ON public.orders USING btree (ref_id varchar_pattern_ops);


--
-- Name: orders_shipping_profile_id_ddf93ff4; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX orders_shipping_profile_id_ddf93ff4 ON public.orders USING btree (shipping_profile_id);


--
-- Name: orders_shop_id_6c078d53; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX orders_shop_id_6c078d53 ON public.orders USING btree (shop_id);


--
-- Name: product_images_product_id_28ebf5f0; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX product_images_product_id_28ebf5f0 ON public.product_images USING btree (product_id);


--
-- Name: products_categories_category_id_a3d618ca; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX products_categories_category_id_a3d618ca ON public.products_categories USING btree (category_id);


--
-- Name: products_categories_product_id_14cbb9b0; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX products_categories_product_id_14cbb9b0 ON public.products_categories USING btree (product_id);


--
-- Name: products_shop_id_a08e8f39; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX products_shop_id_a08e8f39 ON public.products USING btree (shop_id);


--
-- Name: products_slug_8f20884e_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX products_slug_8f20884e_like ON public.products USING btree (slug varchar_pattern_ops);


--
-- Name: qosic_transaction_content_type_id_d7f2815d; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX qosic_transaction_content_type_id_d7f2815d ON public.qosic_transaction USING btree (content_type_id);


--
-- Name: qosic_transaction_initiator_id_6301f752; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX qosic_transaction_initiator_id_6301f752 ON public.qosic_transaction USING btree (initiator_id);


--
-- Name: qosic_transaction_reference_01773e2e_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX qosic_transaction_reference_01773e2e_like ON public.qosic_transaction USING btree (reference varchar_pattern_ops);


--
-- Name: shops_affiliate_id_1dd7007f; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX shops_affiliate_id_1dd7007f ON public.shops USING btree (affiliate_id);


--
-- Name: shops_user_id_b95bae63; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX shops_user_id_b95bae63 ON public.shops USING btree (user_id);


--
-- Name: shops_username_0114a079_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX shops_username_0114a079_like ON public.shops USING btree (username varchar_pattern_ops);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_groups_user_id_f500bee5; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX users_groups_user_id_f500bee5 ON public.users_groups USING btree (user_id);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: users_user_permissions_user_id_92473840; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX users_user_permissions_user_id_92473840 ON public.users_user_permissions USING btree (user_id);


--
-- Name: users_username_e8658fc8_like; Type: INDEX; Schema: public; Owner: nelson
--

CREATE INDEX users_username_e8658fc8_like ON public.users USING btree (username varchar_pattern_ops);


--
-- Name: banners set_public_banner_updated_at; Type: TRIGGER; Schema: public; Owner: nelson
--

CREATE TRIGGER set_public_banner_updated_at BEFORE UPDATE ON public.banners FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();


--
-- Name: TRIGGER set_public_banner_updated_at ON banners; Type: COMMENT; Schema: public; Owner: nelson
--

COMMENT ON TRIGGER set_public_banner_updated_at ON public.banners IS 'trigger to set value of column "updated_at" to current timestamp on row update';


--
-- Name: product_images set_public_product_image_updated_at; Type: TRIGGER; Schema: public; Owner: nelson
--

CREATE TRIGGER set_public_product_image_updated_at BEFORE UPDATE ON public.product_images FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();


--
-- Name: TRIGGER set_public_product_image_updated_at ON product_images; Type: COMMENT; Schema: public; Owner: nelson
--

COMMENT ON TRIGGER set_public_product_image_updated_at ON public.product_images IS 'trigger to set value of column "updated_at" to current timestamp on row update';


--
-- Name: products set_public_product_updated_at; Type: TRIGGER; Schema: public; Owner: nelson
--

CREATE TRIGGER set_public_product_updated_at BEFORE UPDATE ON public.products FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();


--
-- Name: TRIGGER set_public_product_updated_at ON products; Type: COMMENT; Schema: public; Owner: nelson
--

COMMENT ON TRIGGER set_public_product_updated_at ON public.products IS 'trigger to set value of column "updated_at" to current timestamp on row update';


--
-- Name: shops set_public_shop_updated_at; Type: TRIGGER; Schema: public; Owner: nelson
--

CREATE TRIGGER set_public_shop_updated_at BEFORE UPDATE ON public.shops FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();


--
-- Name: TRIGGER set_public_shop_updated_at ON shops; Type: COMMENT; Schema: public; Owner: nelson
--

COMMENT ON TRIGGER set_public_shop_updated_at ON public.shops IS 'trigger to set value of column "updated_at" to current timestamp on row update';


--
-- Name: users set_public_user_updated_at; Type: TRIGGER; Schema: public; Owner: nelson
--

CREATE TRIGGER set_public_user_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();


--
-- Name: TRIGGER set_public_user_updated_at ON users; Type: COMMENT; Schema: public; Owner: nelson
--

COMMENT ON TRIGGER set_public_user_updated_at ON public.users IS 'trigger to set value of column "updated_at" to current timestamp on row update';


--
-- Name: affiliate_agents affiliate_agents_user_id_858014ed_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.affiliate_agents
    ADD CONSTRAINT affiliate_agents_user_id_858014ed_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_items cart_items_cart_id_54d2714b_fk_carts_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_54d2714b_fk_carts_id FOREIGN KEY (cart_id) REFERENCES public.carts(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_items cart_items_product_id_9398bb89_fk_products_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_9398bb89_fk_products_id FOREIGN KEY (product_id) REFERENCES public.products(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: carts carts_shop_id_b3319ed3_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_shop_id_b3319ed3_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: categories categories_shop_id_7fdd920b_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_shop_id_7fdd920b_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: checkouts checkouts_cart_id_999df4ad_fk_carts_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_cart_id_999df4ad_fk_carts_id FOREIGN KEY (cart_id) REFERENCES public.carts(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: checkouts checkouts_cart_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_cart_id_foreign FOREIGN KEY (cart_id) REFERENCES public.carts(id) ON DELETE CASCADE;


--
-- Name: checkouts checkouts_customer_id_213d2e87_fk_customers_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_customer_id_213d2e87_fk_customers_id FOREIGN KEY (customer_id) REFERENCES public.customers(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: checkouts checkouts_customer_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_customer_id_foreign FOREIGN KEY (customer_id) REFERENCES public.customers(id) ON DELETE CASCADE;


--
-- Name: checkouts checkouts_shipping_profile_id_8c6be142_fk_core_ship; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.checkouts
    ADD CONSTRAINT checkouts_shipping_profile_id_8c6be142_fk_core_ship FOREIGN KEY (shipping_profile_id) REFERENCES public.core_shippingprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_bankaccount core_bankaccount_shop_id_ddadf6ad_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_bankaccount
    ADD CONSTRAINT core_bankaccount_shop_id_ddadf6ad_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_billingplan core_billingplan_user_id_92db090d_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_billingplan
    ADD CONSTRAINT core_billingplan_user_id_92db090d_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_shippingmethod core_shippingmethod_zone_id_51ff5d8c_fk_core_shippingzone_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingmethod
    ADD CONSTRAINT core_shippingmethod_zone_id_51ff5d8c_fk_core_shippingzone_id FOREIGN KEY (zone_id) REFERENCES public.core_shippingzone(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_shippingprofile_shops core_shippingprofile_shippingprofile_id_82b14099_fk_core_ship; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile_shops
    ADD CONSTRAINT core_shippingprofile_shippingprofile_id_82b14099_fk_core_ship FOREIGN KEY (shippingprofile_id) REFERENCES public.core_shippingprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_shippingprofile_shops core_shippingprofile_shops_shop_id_c3842613_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingprofile_shops
    ADD CONSTRAINT core_shippingprofile_shops_shop_id_c3842613_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_shippingzone core_shippingzone_profile_id_92750062_fk_core_ship; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shippingzone
    ADD CONSTRAINT core_shippingzone_profile_id_92750062_fk_core_ship FOREIGN KEY (profile_id) REFERENCES public.core_shippingprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_shopdesign core_shopdesign_shop_id_e959ab4b_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.core_shopdesign
    ADD CONSTRAINT core_shopdesign_shop_id_e959ab4b_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: customers customers_user_id_28f6c6eb_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_user_id_28f6c6eb_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exchange_rate exchange_rate_backend_id_d57e3a62_fk_exchange_; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.exchange_rate
    ADD CONSTRAINT exchange_rate_backend_id_d57e3a62_fk_exchange_ FOREIGN KEY (backend_id) REFERENCES public.exchange_exchangebackend(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_checkoutsession kash_checkoutsession_cart_id_cbb308da_fk_carts_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_cart_id_cbb308da_fk_carts_id FOREIGN KEY (cart_id) REFERENCES public.carts(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_checkoutsession kash_checkoutsession_order_id_bbf7f005_fk_orders_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_order_id_bbf7f005_fk_orders_id FOREIGN KEY (order_id) REFERENCES public.orders(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_checkoutsession kash_checkoutsession_shop_id_2c254b1e_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_shop_id_2c254b1e_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_checkoutsession kash_checkoutsession_user_id_d21678a6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_checkoutsession
    ADD CONSTRAINT kash_checkoutsession_user_id_d21678a6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_fundinghistory kash_fundinghistory_card_id_053f9d3f_fk_kash_virtualcard_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_fundinghistory
    ADD CONSTRAINT kash_fundinghistory_card_id_053f9d3f_fk_kash_virtualcard_id FOREIGN KEY (card_id) REFERENCES public.kash_virtualcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_invitecode kash_invitecode_invited_id_29fe192a_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode
    ADD CONSTRAINT kash_invitecode_invited_id_29fe192a_fk_kash_userprofile_id FOREIGN KEY (invited_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_invitecode kash_invitecode_inviter_id_07e11b31_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_invitecode
    ADD CONSTRAINT kash_invitecode_inviter_id_07e11b31_fk_kash_userprofile_id FOREIGN KEY (inviter_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequest kash_kashrequest_initiator_id_b2a52673_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest
    ADD CONSTRAINT kash_kashrequest_initiator_id_b2a52673_fk_kash_userprofile_id FOREIGN KEY (initiator_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequest_recipients kash_kashrequest_rec_kashrequest_id_8daa10bf_fk_kash_kash; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest_recipients
    ADD CONSTRAINT kash_kashrequest_rec_kashrequest_id_8daa10bf_fk_kash_kash FOREIGN KEY (kashrequest_id) REFERENCES public.kash_kashrequest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequest_recipients kash_kashrequest_rec_userprofile_id_9b486648_fk_kash_user; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest_recipients
    ADD CONSTRAINT kash_kashrequest_rec_userprofile_id_9b486648_fk_kash_user FOREIGN KEY (userprofile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequest kash_kashrequest_recipient_id_823d2981_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequest
    ADD CONSTRAINT kash_kashrequest_recipient_id_823d2981_fk_kash_userprofile_id FOREIGN KEY (recipient_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequestresponse kash_kashrequestresp_request_id_4fd0434d_fk_kash_kash; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequestresponse
    ADD CONSTRAINT kash_kashrequestresp_request_id_4fd0434d_fk_kash_kash FOREIGN KEY (request_id) REFERENCES public.kash_kashrequest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequestresponse kash_kashrequestresp_sender_id_d1e7bcdc_fk_kash_user; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequestresponse
    ADD CONSTRAINT kash_kashrequestresp_sender_id_d1e7bcdc_fk_kash_user FOREIGN KEY (sender_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashrequestresponse kash_kashrequestresp_transaction_id_bcf42fe3_fk_kash_send; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashrequestresponse
    ADD CONSTRAINT kash_kashrequestresp_transaction_id_bcf42fe3_fk_kash_send FOREIGN KEY (transaction_id) REFERENCES public.kash_sendkash(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashtransaction kash_kashtransaction_profile_id_64677415_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction
    ADD CONSTRAINT kash_kashtransaction_profile_id_64677415_fk_kash_userprofile_id FOREIGN KEY (profile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashtransaction kash_kashtransaction_receiver_type_id_ef186451_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction
    ADD CONSTRAINT kash_kashtransaction_receiver_type_id_ef186451_fk_django_co FOREIGN KEY (receiver_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_kashtransaction kash_kashtransaction_sender_id_fb3cfd81_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_kashtransaction
    ADD CONSTRAINT kash_kashtransaction_sender_id_fb3cfd81_fk_kash_userprofile_id FOREIGN KEY (sender_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_sendkash_recipients kash_kashtransaction_userprofile_id_67f5c645_fk_kash_user; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_recipients
    ADD CONSTRAINT kash_kashtransaction_userprofile_id_67f5c645_fk_kash_user FOREIGN KEY (userprofile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_sendkash_paid_recipients kash_kashtransaction_userprofile_id_84a5cf51_fk_kash_user; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_paid_recipients
    ADD CONSTRAINT kash_kashtransaction_userprofile_id_84a5cf51_fk_kash_user FOREIGN KEY (userprofile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_momoaccount kash_momoaccount_profile_id_6e141249_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_momoaccount
    ADD CONSTRAINT kash_momoaccount_profile_id_6e141249_fk_kash_userprofile_id FOREIGN KEY (profile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_notification kash_notification_content_type_id_cc4a1cca_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_notification
    ADD CONSTRAINT kash_notification_content_type_id_cc4a1cca_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_notification kash_notification_profile_id_246c4acb_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_notification
    ADD CONSTRAINT kash_notification_profile_id_246c4acb_fk_kash_userprofile_id FOREIGN KEY (profile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_sendkash kash_sendkash_initiator_id_dba8d30b_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash
    ADD CONSTRAINT kash_sendkash_initiator_id_dba8d30b_fk_kash_userprofile_id FOREIGN KEY (initiator_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_sendkash_paid_recipients kash_sendkash_paid_r_sendkash_id_a241485c_fk_kash_send; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_paid_recipients
    ADD CONSTRAINT kash_sendkash_paid_r_sendkash_id_a241485c_fk_kash_send FOREIGN KEY (sendkash_id) REFERENCES public.kash_sendkash(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_sendkash_recipients kash_sendkash_recipi_sendkash_id_dada7138_fk_kash_send; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_sendkash_recipients
    ADD CONSTRAINT kash_sendkash_recipi_sendkash_id_dada7138_fk_kash_send FOREIGN KEY (sendkash_id) REFERENCES public.kash_sendkash(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_userprofile kash_userprofile_user_id_c72ef6ac_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_userprofile
    ADD CONSTRAINT kash_userprofile_user_id_c72ef6ac_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_virtualcard kash_virtualcard_profile_id_8f77d62e_fk_kash_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_virtualcard
    ADD CONSTRAINT kash_virtualcard_profile_id_8f77d62e_fk_kash_userprofile_id FOREIGN KEY (profile_id) REFERENCES public.kash_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kash_withdrawalhistory kash_withdrawalhistory_card_id_baff692a_fk_kash_virtualcard_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.kash_withdrawalhistory
    ADD CONSTRAINT kash_withdrawalhistory_card_id_baff692a_fk_kash_virtualcard_id FOREIGN KEY (card_id) REFERENCES public.kash_virtualcard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: order_items order_items_order_id_412ad78b_fk_orders_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_412ad78b_fk_orders_id FOREIGN KEY (order_id) REFERENCES public.orders(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: order_items order_items_product_id_dd557d5a_fk_products_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_dd557d5a_fk_products_id FOREIGN KEY (product_id) REFERENCES public.products(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders orders_customer_id_b7016332_fk_customers_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_b7016332_fk_customers_id FOREIGN KEY (customer_id) REFERENCES public.customers(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders orders_shipping_profile_id_ddf93ff4_fk_core_shippingprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_shipping_profile_id_ddf93ff4_fk_core_shippingprofile_id FOREIGN KEY (shipping_profile_id) REFERENCES public.core_shippingprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders orders_shop_id_6c078d53_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_shop_id_6c078d53_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: product_images product_images_product_id_28ebf5f0_fk_products_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_images_product_id_28ebf5f0_fk_products_id FOREIGN KEY (product_id) REFERENCES public.products(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: products_categories products_categories_category_id_a3d618ca_fk_categories_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products_categories
    ADD CONSTRAINT products_categories_category_id_a3d618ca_fk_categories_id FOREIGN KEY (category_id) REFERENCES public.categories(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: products_categories products_categories_product_id_14cbb9b0_fk_products_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products_categories
    ADD CONSTRAINT products_categories_product_id_14cbb9b0_fk_products_id FOREIGN KEY (product_id) REFERENCES public.products(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: products products_shop_id_a08e8f39_fk_shops_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_shop_id_a08e8f39_fk_shops_id FOREIGN KEY (shop_id) REFERENCES public.shops(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qosic_transaction qosic_transaction_content_type_id_d7f2815d_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.qosic_transaction
    ADD CONSTRAINT qosic_transaction_content_type_id_d7f2815d_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qosic_transaction qosic_transaction_initiator_id_6301f752_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.qosic_transaction
    ADD CONSTRAINT qosic_transaction_initiator_id_6301f752_fk_users_id FOREIGN KEY (initiator_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shops shops_affiliate_id_1dd7007f_fk_affiliate_agents_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_affiliate_id_1dd7007f_fk_affiliate_agents_id FOREIGN KEY (affiliate_id) REFERENCES public.affiliate_agents(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shops shops_user_id_b95bae63_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.shops
    ADD CONSTRAINT shops_user_id_b95bae63_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_user_id_f500bee5_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_f500bee5_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_user_id_92473840_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: nelson
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_92473840_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

