set -e

mongo -- "$MONGO_INITDB_DATABASE" <<EOF
  var userDatabase = db.getSiblingDB('userData');
  userDatabase.users.insertOne( { userName: '$MONGO_INVENTORYUSER_USERNAME', pwdHash: '$MONGO_INVENTORYUSER_PWDHASH'} )
  userDatabase.createUser({ 
    user: '$MONGO_INVENTORYAPI_USERNAME',
    pwd: '$MONGO_INVENTORYAPI_PASSWORD',
    roles: [{
      role: 'read',
      db: 'userData'
    }]
  })

  var inventoryDatabase = db.getSiblingDB('$MONGO_INVENTORY_DATABASE')
  inventoryDatabase.createUser({
    user: '$MONGO_INVENTORYAPI_USERNAME',
    pwd: '$MONGO_INVENTORYAPI_PASSWORD',
    roles: [{
      role: 'read',
      db: '$MONGO_INVENTORY_DATABASE'
    }]
  })
  inventoryDatabase.createUser({
    user: '$MONGO_REPORTINGMODULE_USERNAME',
    pwd: '$MONGO_REPORTINGMODULE_PASSWORD',
    roles: [{
      role: 'readWrite',
      db: '$MONGO_INVENTORY_DATABASE'
    }]
  })
EOF