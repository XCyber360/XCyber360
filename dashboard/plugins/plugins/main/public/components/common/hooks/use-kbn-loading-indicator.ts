/*
 * Xcyber360 app - React hook hidde or show the plugin platform loading indicator
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import { getHttp } from '../../../kibana-services';
import React, { useEffect, useState, useRef } from 'react';
import { BehaviorSubject } from 'rxjs';

export const useKbnLoadingIndicator = (): [
  boolean,
  React.Dispatch<React.SetStateAction<boolean>>,
  boolean
] => {
  const [loading, setLoading] = useState(false);
  const [flag, setFlag] = useState(false);
  const [visible, setVisible] = useState(0);
  const loadingCount$ = useRef(new BehaviorSubject(0))
  
  useEffect(() => {
    getHttp().addLoadingCountSource(loadingCount$.current);
    const subscriber = getHttp() 
      .getLoadingCount$()
      .subscribe((count) => {
        setVisible(count);
        !count && setFlag(false);
      });
    return () => subscriber.unsubscribe();
  }, []);

  useEffect(() => {
    if (loading && visible <= 0) {
      loadingCount$.current.next(loadingCount$.current.value + 1);
      setFlag(true);
    }

    if (!loading && flag && visible > 0) {
      loadingCount$.current.next(loadingCount$.current.value - 1);
    }
  }, [visible, loading]);
  return [loading, setLoading, visible > 0];
};