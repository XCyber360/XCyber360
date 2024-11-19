var storeXcyber360 = stores.open('storeXcyber360');
var deleteRolesMapping = storeXcyber360.load('deleteRolesMapping');

switch (deleteRolesMapping) {
  case false:
    respond()
      .withStatusCode(200)
      .withFile('security/roles-mapping/get-rules.json');
    break;
  case true:
    storeXcyber360.save('deleteRolesMapping', false);
    respond()
      .withStatusCode(200)
      .withFile('security/roles-mapping/get-rules-after-delete.json');
    break;
  default:
    respond()
      .withStatusCode(200)
      .withFile('security/roles-mapping/get-rules.json');
    break;
}
