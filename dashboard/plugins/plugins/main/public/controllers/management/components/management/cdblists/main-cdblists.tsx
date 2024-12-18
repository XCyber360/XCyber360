/*
 * Xcyber360 app - React component for main CDB List view.
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import React, { useState } from 'react';
import WzCDBListsOverview from './views/cdblists-overview';
import WzListEditor from './views/list-editor';

export default function WzCDBList() {
  const [listContent, setListContent] = useState(false);

  return (
    <>
      {(listContent && (
        <WzListEditor
          listContent={listContent}
          clearContent={() => {
            setListContent(false);
          }}
          updateListContent={listContent => {
            setListContent(listContent);
          }}
        />
      )) || (
        <WzCDBListsOverview
          updateListContent={listContent => {
            setListContent(listContent);
          }}
        />
      )}
    </>
  );
}
