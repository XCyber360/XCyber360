/*
 * Xcyber360 app - React component for reporting.
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import { cloneDeep } from 'lodash';

const initialState = {
  isLoading: false,
  isProcessing: false,
  itemList: [],
  showModal: false,
  dataSourceSearchContext: null,
};

const statusReducers = (state = initialState, action) => {
  if (action.type === 'UPDATE_IS_PROCESSING') {
    return {
      ...state,
      isProcessing: action.isProcessing,
      isLoading: action.isProcessing,
    };
  }
  if (action.type === 'UPDATE_LIST_ITEMS_FOR_REMOVE') {
    return {
      ...state,
      itemList: action.itemList,
    };
  }
  if (action.type === 'UPDATE_SHOW_MODAL') {
    return {
      ...state,
      showModal: action.showModal,
    };
  }
  if (action.type === 'CLEAN_INFO') {
    return {
      ...state,
      isLoading: false,
      isProcessing: false,
      itemList: [],
      showModal: false,
    };
  }
  if (action.type === 'UPDATE_REPORTING_DATA_SEARCH_SOURCE_CONTEXT') {
    return {
      ...state,
      dataSourceSearchContext: cloneDeep(action.dataSourceSearchContext),
    };
  }

  return state;
};

export default statusReducers;
