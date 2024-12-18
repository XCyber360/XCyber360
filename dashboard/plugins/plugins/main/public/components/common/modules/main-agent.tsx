/*
 * Xcyber360 app - Integrity monitoring components
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React, { Component, Fragment } from 'react';
import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiTitle,
  EuiButtonEmpty,
} from '@elastic/eui';
import { euiThemeVars } from '@osd/ui-shared-deps/theme';
import '../../common/modules/module.scss';
import store from '../../../redux/store';
import { FilterHandler } from '../../../utils/filter-handler';
import { AppState } from '../../../react-services/app-state';
import { ReportingService } from '../../../react-services/reporting';
import { XCYBER360_MODULES } from '../../../../common/xcyber360-modules';
import { AgentInfo } from '../../common/welcome/agents-info';
import { compose } from 'redux';
import { withGlobalBreadcrumb } from '../hocs';
import { endpointSummary } from '../../../utils/applications';
import {
  AlertsDataSource,
  AlertsDataSourceRepository,
  PatternDataSource,
  tFilter,
  tParsedIndexPattern,
  useDataSource,
} from '../data-source';
import { useAsyncAction } from '../hooks';
import NavigationService from '../../../react-services/navigation-service';

export class MainModuleAgent extends Component {
  props!: {
    [key: string]: any;
  };
  state: {
    selectView: Boolean;
    loadingReport: Boolean;
    switchModule: Boolean;
    showAgentInfo: Boolean;
  };
  reportingService: ReportingService;
  filterHandler: FilterHandler;

  constructor(props) {
    super(props);
    this.reportingService = new ReportingService();
    this.filterHandler = new FilterHandler(AppState.getCurrentPattern());
    this.state = {
      selectView: false,
      loadingReport: false,
      switchModule: false,
      showAgentInfo: false,
    };
  }

  renderTitle() {
    return (
      <EuiFlexGroup>
        <EuiFlexItem className='wz-module-header-agent-title'>
          <EuiFlexGroup>
            <EuiFlexItem grow={false}>
              <span style={{ display: 'inline-flex' }}>
                <EuiTitle size='s' className='wz-module-header-agent-title-btn'>
                  <h1>
                    <span
                      style={{ color: euiThemeVars.euiColorPrimaryText }}
                      onClick={() => {
                        NavigationService.getInstance().navigate(
                          `/agents?tab=welcome&agent=${this.props.agent.id}`,
                        );
                      }}
                    >
                      <span>
                        &nbsp;{this.props.agent.name}&nbsp;&nbsp;&nbsp;
                      </span>
                    </span>
                  </h1>
                </EuiTitle>
              </span>
            </EuiFlexItem>
            <EuiFlexItem />
            {this.props.section === 'syscollector' && (
              <EuiFlexItem
                grow={false}
                style={{ marginRight: 4, marginTop: 6 }}
              >
                <GenerateSyscollectorReportButton agent={this.props.agent} />
              </EuiFlexItem>
            )}
          </EuiFlexGroup>
        </EuiFlexItem>
      </EuiFlexGroup>
    );
  }

  render() {
    const { agent, section, selectView } = this.props;
    const ModuleTabView = (this.props.tabs || []).find(
      tab => tab.id === selectView,
    );
    return (
      <div
        className={
          this.state.showAgentInfo
            ? 'wz-module wz-module-showing-agent'
            : 'wz-module'
        }
      >
        {agent && agent.os && (
          <Fragment>
            <div className='wz-module-header-agent-wrapper'>
              <div className='wz-module-header-agent'>{this.renderTitle()}</div>
            </div>
            <div>
              <div
                className={
                  this.props.tabs &&
                  this.props.tabs.length &&
                  'wz-module-header-nav'
                }
              >
                {this.state.showAgentInfo && (
                  <div
                    className={
                      !this.props.tabs || !this.props.tabs.length
                        ? 'wz-welcome-page-agent-info'
                        : 'wz-welcome-page-agent-info wz-welcome-page-agent-info-gray'
                    }
                  >
                    <AgentInfo
                      agent={this.props.agent}
                      isCondensed={false}
                      hideActions={true}
                      {...this.props}
                    ></AgentInfo>
                  </div>
                )}
                {this.props.tabs && this.props.tabs.length && (
                  <div className='wz-welcome-page-agent-tabs'>
                    <EuiFlexGroup>
                      {this.props.renderTabs()}
                      <EuiFlexItem
                        grow={false}
                        style={{ marginTop: 6, marginRight: 5 }}
                      >
                        <EuiFlexGroup>
                          {ModuleTabView &&
                            ModuleTabView.buttons &&
                            ModuleTabView.buttons.map(
                              (ModuleViewButton, index) =>
                                typeof ModuleViewButton !== 'string' ? (
                                  <EuiFlexItem key={`module_button_${index}`}>
                                    <ModuleViewButton
                                      {...{
                                        ...this.props,
                                        ...this.props.agentsSelectionProps,
                                      }}
                                      moduleID={section}
                                    />
                                  </EuiFlexItem>
                                ) : null,
                            )}
                        </EuiFlexGroup>
                      </EuiFlexItem>
                    </EuiFlexGroup>
                  </div>
                )}
              </div>
            </div>
            {!['syscollector', 'configuration'].includes(section) &&
              ModuleTabView &&
              ModuleTabView.component && (
                <ModuleTabView.component {...this.props} moduleID={section} />
              )}
          </Fragment>
        )}
      </div>
    );
  }
}

export default compose(
  withGlobalBreadcrumb(({ agent, section }) => {
    if (section === 'welcome') {
      return [
        {
          text: endpointSummary.breadcrumbLabel,
          href: NavigationService.getInstance().getUrlForApp(
            endpointSummary.id,
            {
              path: `#/agents-preview`,
            },
          ),
        },
        { text: agent.id },
      ];
    } else {
      return [
        {
          text: endpointSummary.breadcrumbLabel,
          href: NavigationService.getInstance().getUrlForApp(
            endpointSummary.id,
            {
              path: `#/agents-preview`,
            },
          ),
        },
        { agent: agent },
        {
          text: XCYBER360_MODULES[section].title,
        },
      ];
    }
  }),
)(MainModuleAgent);

export class AgentInventoryDataSource extends AlertsDataSource {
  constructor(id: string, title: string) {
    super(id, title);
  }

  getFixedFilters(): tFilter[] {
    return [
      ...super.getFixedFiltersClusterManager(),
      ...super.getFixedFilters(),
    ];
  }
}

const GenerateSyscollectorReportButton = ({ agent }) => {
  const {
    dataSource,
    fetchFilters,
    isLoading: isDataSourceLoading,
  } = useDataSource<tParsedIndexPattern, PatternDataSource>({
    repository: new AlertsDataSourceRepository(), // this makes only works with alerts index pattern
    DataSource: AgentInventoryDataSource,
  });

  const action = useAsyncAction(async () => {
    const reportingService = new ReportingService();
    const agentID =
      (agent || store.getState().appStateReducers.currentAgentData || {}).id ||
      false;
    await reportingService.startVis2Png('syscollector', agentID, {
      indexPattern: dataSource.indexPattern,
      query: { query: '', language: 'kuery' },
      filters: fetchFilters,
      time: {
        from: 'now-1d/d',
        to: 'now',
      },
    });
  }, [dataSource]);

  return (
    <EuiButtonEmpty
      iconType='document'
      isLoading={action.running}
      isDisabled={isDataSourceLoading}
      onClick={action.run}
    >
      Generate report
    </EuiButtonEmpty>
  );
};
