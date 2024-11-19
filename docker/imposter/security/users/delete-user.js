var id = context.request.queryParams.user_ids;
var storeXcyber360 = stores.open('storeXcyber360');

storeXcyber360.save('deleteUser', true);

var data = {
  data: {
    affected_items: [
      {
        id: id,
        username: 'test',
        allow_run_as: false,
        roles: [],
      },
    ],
    total_affected_items: 1,
    total_failed_items: 0,
    failed_items: [],
  },
  message: 'Users were successfully deleted',
  error: 0,
};

respond().withStatusCode(200).withData(JSON.stringify(data));
