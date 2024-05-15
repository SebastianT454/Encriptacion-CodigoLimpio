-- Crea la tabla de claves (matrices)
create table encryptionkey (
  ID SERIAL PRIMARY KEY,
  key_name text not null,
  key_value text not null,
  authentication_key varchar(20) not null
);