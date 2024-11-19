var storeXcyber360 = stores.open('storeXcyber360');
var deletePolicies = storeXcyber360.load('deletePolicies');

switch (deletePolicies) {
  case false:
    respond()
      .withStatusCode(200)
      .withFile('security/policies/get-policies.json');
    break;
  case true:
    storeXcyber360.save('deletePolicies', false);
    respond()
      .withStatusCode(200)
      .withFile('security/policies/get-policies-after-delete.json');
    break;
  default:
    respond()
      .withStatusCode(200)
      .withFile('security/policies/get-policies.json');
    break;
}
