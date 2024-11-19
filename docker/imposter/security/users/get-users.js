var storeXcyber360 = stores.open('storeXcyber360');
var deleteUser = storeXcyber360.load('deleteUser');

switch (deleteUser) {
  case false:
    respond().withStatusCode(200).withFile('security/users/get-users.json');
    break;
  case true:
    storeXcyber360.save('deleteUser', false);
    respond()
      .withStatusCode(200)
      .withFile('security/users/get-users-after-delete.json');
    break;
  default:
    respond().withStatusCode(200).withFile('security/users/get-users.json');
    break;
}
