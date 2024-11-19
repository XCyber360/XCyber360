
var selectedNode = context.request.queryParams.select

switch (selectedNode) {
  case 'name':
    respond()
      .withStatusCode(200)
      .withFile('cluster/node/select-name.json');
    break;
  default:
    respond()
      .withStatusCode(200)
      .withFile('cluster/node/response-with-everything.json');
    break;
}

// Commented code is used to test the restart only
//
// var storeXcyber360 = stores.open('storeXcyber360');
// var attemptRestart = storeXcyber360.load('attempt');
// var callRestart = storeXcyber360.load('callRestart');
// if (callRestart) {
//   if (attemptRestart < 10) {
//     storeXcyber360.save('attempt', attemptRestart + 1);
//     respond()
//       .withStatusCode(200)
//       .withFile('cluster/cluster-node-info-no-restart.json')
//   } else {
//     storeXcyber360.save('attempt', 0);
//     storeXcyber360.save('callRestart', false);
//     respond()
//       .withStatusCode(200)
//       .withFile('cluster/cluster-node-info.json')
//   }
// } else {
//   respond()
//     .withStatusCode(200)
//     .withFile('cluster/cluster-node-info.json')
// }
