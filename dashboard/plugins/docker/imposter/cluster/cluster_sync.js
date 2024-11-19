
var storeXcyber360 = stores.open('storeXcyber360');
var attemptRestart = storeXcyber360.load('attempt');


if(attemptRestart < 5){
    storeXcyber360.save('attempt', attemptRestart + 1);
    respond()
        .withStatusCode(200)
        .withFile('cluster/cluster_sync_no_sync.json')
} else {
    storeXcyber360.save('attempt', 0);
    respond()
        .withStatusCode(200)
        .withFile('cluster/cluster_sync.json')
}
