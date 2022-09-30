cities_table_create = '''CREATE TABLE IF NOT EXISTS 
  cities (
  id int NOT NULL AUTO_INCREMENT,
  stateId int NOT NULL,
  name varchar(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id)
) '''

client_credentials_create = '''CREATE TABLE IF NOT EXISTS
  client_credential (
  id int NOT NULL AUTO_INCREMENT,
  app_id varchar(255) NOT NULL,
  app_key varchar(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id),
  UNIQUE KEY app_id_UNIQUE (app_id),
  UNIQUE KEY app_key_UNIQUE (app_key)
)'''

companies_create = '''
CREATE TABLE IF NOT EXISTS companies (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  address varchar(255) NOT NULL,
  phone varchar(255) NOT NULL,
  uuid varchar(255) NOT NULL,
  city varchar(255) NOT NULL,
  state varchar(255) NOT NULL,
  PRIMARY KEY (id,name),
  UNIQUE KEY uuid_UNIQUE (uuid)
)'''

company_account_create = '''CREATE TABLE IF NOT EXISTS 
  companyaccount (
  id int NOT NULL AUTO_INCREMENT,
  userId int DEFAULT NULL,
  companyId int NOT NULL,
  appId varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
)'''

purchases_create = '''CREATE TABLE IF NOT EXISTS
  compras (
  id int NOT NULL AUTO_INCREMENT,
  fecha date DEFAULT NULL,
  documento varchar(255) DEFAULT NULL,
  tipo varchar(255) DEFAULT NULL,
  referencia varchar(255) DEFAULT NULL,
  nrc varchar(255) DEFAULT NULL,
  nombre varchar(255) DEFAULT NULL,
  compra float DEFAULT NULL,
  iva float DEFAULT NULL,
  guardado datetime DEFAULT NULL,
  documentoId int NOT NULL,
  tipoId int NOT NULL,
  dui varchar(255) NOT NULL,
  comInGra float NOT NULL,
  comInEx float NOT NULL DEFAULT '0',
  intExNoSuj float NOT NULL DEFAULT '0',
  imExNoSuj float NOT NULL DEFAULT '0',
  inGraBie float NOT NULL DEFAULT '0',
  imGravBie float NOT NULL DEFAULT '0',
  imGravSer float NOT NULL DEFAULT '0',
  attachmentId int NOT NULL DEFAULT '3',
  companyUuid varchar(255) NOT NULL,
  PRIMARY KEY (id)
)'''

expenses_create = '''CREATE TABLE IF NOT EXISTS
  gastos (
  id int NOT NULL AUTO_INCREMENT,
  tipo varchar(255) DEFAULT NULL,
  fecha date DEFAULT NULL,
  descripcion varchar(255) DEFAULT NULL,
  guardado datetime DEFAULT NULL,
  monto float DEFAULT NULL,
  companyUuid varchar(255) NOT NULL,
  PRIMARY KEY (id)
)'''

payments_create = '''CREATE TABLE IF NOT EXISTS
  pagos (
  id int NOT NULL AUTO_INCREMENT,
  fecha date DEFAULT NULL,
  tipoPago varchar(255) DEFAULT NULL,
  pago float DEFAULT NULL,
  caja varchar(255) DEFAULT NULL,
  hora time DEFAULT NULL,
  usuario varchar(255) DEFAULT NULL,
  correlativo int DEFAULT NULL,
  anulado varchar(255) DEFAULT NULL,
  iva float DEFAULT NULL,
  tid int DEFAULT NULL,
  companyUuid varchar(255) NOT NULL,
  PRIMARY KEY (id)
)'''

products_create = '''CREATE TABLE IF NOT EXISTS
  productos (
  fecha date DEFAULT NULL,
  hora time DEFAULT NULL,
  producto varchar(255) DEFAULT NULL,
  cantidad float DEFAULT NULL,
  porcion varchar(255) DEFAULT NULL,
  venta varchar(255) DEFAULT NULL,
  tid int DEFAULT NULL,
  id int NOT NULL AUTO_INCREMENT,
  precio float DEFAULT NULL,
  companyUuid varchar(255) NOT NULL,
  PRIMARY KEY (id)
)'''

suppliers_create = '''CREATE TABLE IF NOT EXISTS 
  proveedores (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(255) DEFAULT NULL,
  nrc varchar(255) DEFAULT NULL,
  guardado datetime DEFAULT NULL,
  companyUuid varchar(255) NOT NULL,
  PRIMARY KEY (id)
)'''

roles_create = '''CREATE TABLE IF NOT EXISTS 
  roles (
  id int NOT NULL AUTO_INCREMENT,
  roleName varchar(255) NOT NULL,
  PRIMARY KEY (id,roleName),
  UNIQUE KEY id_UNIQUE (id),
  UNIQUE KEY roleName_UNIQUE (roleName)
)'''

state_create = '''CREATE TABLE IF NOT EXISTS 
  states (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id),
  UNIQUE KEY name_UNIQUE (name)
)'''

status_create = '''CREATE TABLE IF NOT EXISTS 
  status (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(45) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id),
  UNIQUE KEY name_UNIQUE (name)
)'''

tickets_create = '''CREATE TABLE IF NOT EXISTS
  tickets (
  id int NOT NULL AUTO_INCREMENT,
  fecha date DEFAULT NULL,
  hora time DEFAULT NULL,
  total float DEFAULT NULL,
  tipo varchar(255) DEFAULT NULL,
  documento varchar(255) DEFAULT NULL,
  puntosLealtad varchar(255) DEFAULT NULL,
  correlativo int DEFAULT NULL,
  descuentoTotal float DEFAULT NULL,
  propina float DEFAULT NULL,
  descuentoLealtad float DEFAULT NULL,
  servicioDomicilio float DEFAULT NULL,
  cliente varchar(255) DEFAULT NULL,
  mesa varchar(255) DEFAULT NULL,
  anulado varchar(255) DEFAULT NULL,
  mesero varchar(255) DEFAULT NULL,
  tid int DEFAULT NULL,
  companyUuid varchar(255) NOT NULL,
  docTipo varchar(255) NOT NULL,
  docTipoId int NOT NULL,
  docId varchar(45) NOT NULL,
  numResolucion varchar(255) NOT NULL,
  docSerie varchar(255) NOT NULL,
  venEx float NOT NULL DEFAULT '0',
  venNoSuj float NOT NULL DEFAULT '0',
  venGrabLoc float NOT NULL DEFAULT '0',
  venCueTerNoDom float NOT NULL DEFAULT '0',
  anexoNum int NOT NULL DEFAULT '0',
  nrc varchar(255) NOT NULL,
  nombre varchar(255) NOT NULL,
  dui varchar(255) NOT NULL,
  maqNum varchar(45) NOT NULL DEFAULT '',
  venIntExNoSujProp float NOT NULL DEFAULT '0',
  expDenCA float NOT NULL DEFAULT '0',
  expFueCA float NOT NULL DEFAULT '0',
  expSer float NOT NULL DEFAULT '0',
  venZoFra float NOT NULL DEFAULT '0',
  tax float NOT NULL DEFAULT '0',
  PRIMARY KEY (id)
)'''

users_create = '''CREATE TABLE IF NOT EXISTS 
  users (
  id int NOT NULL AUTO_INCREMENT,
  email varchar(255) NOT NULL,
  lastName varchar(255) NOT NULL,
  passwordSalt varchar(255) NOT NULL,
  passwordHash varchar(255) NOT NULL,
  createdDate datetime NOT NULL,
  firstName varchar(255) NOT NULL,
  status varchar(255) NOT NULL,
  loginTries int NOT NULL DEFAULT '0',
  roleId int NOT NULL DEFAULT '1',
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id),
  UNIQUE KEY email_UNIQUE (email)
)'''