/*
 * Xcyber360 app - Component for the module generate reports
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React from 'react';
import { useAsyncAction } from '../../hooks';
import { getUiSettings } from '../../../../kibana-services';
import { ReportingService } from '../../../../react-services';
import $ from 'jquery';
import { WzButton } from '../../../common/buttons';
import { connect } from 'react-redux';

const mapStateToProps = state => ({
  dataSourceSearchContext: state.reportingReducers.dataSourceSearchContext,
});

export const ButtonModuleGenerateReport = connect(mapStateToProps)(
  ({ agent, moduleID, dataSourceSearchContext }) => {
    const disabledReport = ![
      !dataSourceSearchContext?.isSearching,
      dataSourceSearchContext?.totalResults,
      dataSourceSearchContext?.indexPattern,
    ].every(Boolean);
    const totalResults = dataSourceSearchContext?.totalResults;
    const action = useAsyncAction(async () => {
      const reportingService = new ReportingService();
      const isDarkModeTheme = getUiSettings().get('theme:darkMode');
      if (isDarkModeTheme) {
        //Patch to fix white text in dark-mode pdf reports
        const defaultTextColor = '#DFE5EF';

        //Patch to fix dark backgrounds in visualizations dark-mode pdf reports
        const $labels = $(
          '.euiButtonEmpty__text, .echLegendItem, div.mtrVis__value ~ div',
        );
        const $vizBackground = $('.echChartBackground');
        const defaultVizBackground = $vizBackground.css('background-color');

        try {
          $labels.css('color', 'black');
          $vizBackground.css('background-color', 'transparent');
          await reportingService.startVis2Png(moduleID, agent?.id || false);
          $vizBackground.css('background-color', defaultVizBackground);
          $labels.css('color', defaultTextColor);
        } catch (e) {
          $labels.css('color', defaultTextColor);
          $vizBackground.css('background-color', defaultVizBackground);
        }
      } else {
        await reportingService.startVis2Png(moduleID, agent?.id || false);
      }
    }, [agent]);

    return (
      <WzButton
        buttonType='empty'
        iconType='document'
        isLoading={action.running}
        onClick={action.run}
        isDisabled={disabledReport}
        tooltip={
          disabledReport && totalResults === 0
            ? {
                position: 'top',
                content: 'No results match for this search criteria.',
              }
            : undefined
        }
      >
        Generate report
      </WzButton>
    );
  },
);
