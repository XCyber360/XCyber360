var storeXcyber360 = stores.open('storeXcyber360');
var attemptRestart = storeXcyber360.load('attempt');

var taskStatus = context.request.queryParams.status;

if (!taskStatus) {
  respond().withStatusCode(200).withFile('tasks/status_in_progress_2.json');
}

if (attemptRestart < 5) {
  storeXcyber360.save('attempt', attemptRestart + 1);

  if (taskStatus === 'In progress') {
    respond().withStatusCode(200).withFile('tasks/status_in_progress_2.json');
  }

  if (taskStatus === 'Done' || taskStatus === 'Failed') {
    respond().withStatusCode(200).withFile('tasks/empty.json');
  }
} else if (attemptRestart < 10) {
  storeXcyber360.save('attempt', attemptRestart + 1);

  if (taskStatus === 'In progress') {
    respond().withStatusCode(200).withFile('tasks/status_in_progress_1.json');
  }

  if (taskStatus === 'Done') {
    respond().withStatusCode(200).withFile('tasks/status_done.json');
  }

  if (taskStatus === 'Failed') {
    respond().withStatusCode(200).withFile('tasks/empty.json');
  }
} else {
  if (taskStatus === 'In progress') {
    respond().withStatusCode(200).withFile('tasks/empty.json');
  }

  if (taskStatus === 'Done') {
    respond().withStatusCode(200).withFile('tasks/status_done.json');
  }

  if (taskStatus === 'Failed') {
    storeXcyber360.save('attempt', 0);
    respond().withStatusCode(200).withFile('tasks/status_failed.json');
  }
}
