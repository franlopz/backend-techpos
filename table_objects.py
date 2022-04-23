from peewee import Table

ProductoDB = Table('productos', ('fecha', 'hora', 'producto',
                   'cantidad', 'precio', 'porcion', 'venta', 'tid', 'id'))

PagoDB = Table('pagos', ('fecha', 'hora', 'tipoPago', 'pago',
               'cajo', 'usuario', 'correlativo', 'anulado', 'iva', 'tid', 'id'))

TicketsDB = Table('tickets', ('fecha', 'hora', 'total', 'tipo', 'documento', 'puntosLealtad', 'correlativo',
                  'descuentoTotal', 'servicioDomicilio', 'cliente', 'mesa', 'anulado', 'mesero', 'tid', 'id'))

ComprasDB = Table('compras', ('fecha', 'documento', 'tipo', 'referencia', 'nrc', 'nombre', 'compra', 'iva', 'guardado', 'id', 'documentoId',
                  'tipoId', 'dui', 'comInGra', 'comInEx', 'intExNoSuj', 'imExNoSuj', 'inGraBie', 'imGravBie', 'imGravSer', 'attachmentId'))

ProveedoresDB = Table('proveedores', ('nombre', 'nrc', 'guardado', 'id'))

GastosDB = Table('gastos', ('descripcion', 'fecha',
                 'guardado', 'id', 'monto', 'tipo'))

usersDB = Table('users', ('id', 'email', 'firstName', 'lastName',
                          'passwordSalt', 'passwordHash', 'createdDate',
                          'status', 'loginTries', 'roleId'))

rolesDB = Table('roles', ('id', 'roleName'))

companyaccountDB = Table('companyaccount', ('id', 'userId', 'companyId'))

companiesDB = Table('companies', ('id', 'name', 'address', 'phone', 'uuid', 'city', 'state'))

citiesDB = Table('cities',('id','stateId','name'))

stateDB = Table('states',('id','name'))