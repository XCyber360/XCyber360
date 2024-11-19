var storeXcyber360 = stores.open('storeXcyber360');
var deleteRole = storeXcyber360.load('deleteRole');

switch (deleteRole) {
  case false:
    respond().withStatusCode(200).withFile('security/roles/get-roles.json');
    break;
  case true:
    storeXcyber360.save('deleteRole', false);
    respond()
      .withStatusCode(200)
      .withFile('security/roles/get-roles-after-delete.json');
    break;
  default:
    respond().withStatusCode(200).withFile('security/roles/get-roles.json');
    break;
}
