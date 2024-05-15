-- Crea la tabla de usuarios
create table users (
  _name text not null,
  _password varchar(20) not null,
  encryption_keys_ids varchar(20)
); 