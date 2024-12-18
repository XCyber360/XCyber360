/*
 * Xcyber360 app - React component for registering agents.
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

// import { createStore } from 'redux';
// import rootReducers from './reducers/rootReducers';

// export default createStore(rootReducers);

import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers/rootReducers';

const store = createStore(rootReducer, applyMiddleware(thunk));

export default store;
