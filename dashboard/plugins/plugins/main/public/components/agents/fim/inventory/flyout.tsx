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

import React, { Component } from 'react';
import {
  EuiFlyoutHeader,
  EuiFlyoutBody,
  EuiTitle,
  EuiLoadingContent,
  EuiCallOut,
} from '@elastic/eui';
import { WzRequest } from '../../../../react-services/wz-request';
import { FileDetails } from './fileDetail';
import {
  UI_ERROR_SEVERITIES,
  UIErrorLog,
  UIErrorSeverity,
  UILogLevel,
} from '../../../../react-services/error-orchestrator/types';
import { UI_LOGGER_LEVELS } from '../../../../../common/constants';
import { getErrorOrchestrator } from '../../../../react-services/common-services';
import { WzFlyout } from '../../../common/flyouts';
import { withRouterSearch } from '../../../common/hocs';

export const FlyoutDetail = withRouterSearch(
  class FlyoutDetail extends Component {
    state: {
      currentFile: boolean | { [key: string]: string };
      isLoading: boolean;
      error: boolean;
      type: 'file' | 'registry_key';
    };

    props!: {
      fileName: string;
      agentId: string;
      view: 'inventory' | 'events' | 'extern';
      closeFlyout(): void;
    };

  constructor(props) {
    super(props);
    this.state = {
      currentFile: false,
      isLoading: true,
      error: false,
      type: 'file',
    };
  }

  async componentDidMount() {
    try {
      let currentFile;
      if (
        typeof this.props.item === 'boolean' &&
        typeof this.props.fileName !== undefined
      ) {
        const regex = new RegExp('file=' + '[^&]*');
        const match = window.location.href.match(regex);
        if (match && match[0]) {
          const file = decodeURIComponent(match[0].split('=')[1]);
          const data = await WzRequest.apiReq(
            'GET',
            `/syscheck/${this.props.agentId}`,
            {
              params: {
                q: `file=${file};(type=file,type=registry_key)`,
              },
            },
          );
          currentFile = ((((data || {}).data || {}).data || {})
            .affected_items || [])[0];
        }
      } else if (this.props.item) {
        currentFile = this.props.item;
      } else {
        const file = this.props.fileName;
        const data = await WzRequest.apiReq(
          'GET',
          `/syscheck/${this.props.agentId}`,
          {
            params: {
              q: `file=${file};(type=file,type=registry_key)`,
            },
          },
        );
        currentFile = ((((data || {}).data || {}).data || {}).affected_items ||
          [])[0];
      }
      if (!currentFile) {
        throw new Error('File not found');
      }
      this.setState({ currentFile, type: currentFile.type, isLoading: false });
    } catch (error) {
      this.setState({
        error: `Data could not be fetched for ${this.props.fileName}`,
        currentFile: { file: this.props.fileName },
      });

        const options: UIErrorLog = {
          context: `${FlyoutDetail.name}.componentDidMount`,
          level: UI_LOGGER_LEVELS.ERROR as UILogLevel,
          severity: UI_ERROR_SEVERITIES.BUSINESS as UIErrorSeverity,
          store: true,
          error: {
            error: error,
            message: error.message || error,
            title: error.name,
          },
        };
        getErrorOrchestrator().handleError(options);
      }
    }

  componentWillUnmount() {
    window.location.href = window.location.href.replace(
      new RegExp('&file=' + '[^&]*', 'g'),
      '',
    );
  }

  render() {
    const { type } = this.state;
    return (
      <WzFlyout
        onClose={() => this.props.closeFlyout()}
        flyoutProps={{
          size: 'l',
          'aria-labelledby': this.state.currentFile.file,
          maxWidth: '70%',
          className: 'wz-inventory wzApp',
        }}
      >
        <EuiFlyoutHeader hasBorder className='flyout-header'>
          <EuiTitle size='s'>
            <h2 id={this.state.currentFile.file}>
              {this.state.currentFile.file}
            </h2>
          </EuiTitle>
        </EuiFlyoutHeader>
        {this.state.isLoading && (
          <EuiFlyoutBody className='flyout-body'>
            {(this.state.error && (
              <EuiCallOut
                title={this.state.error}
                color='warning'
                iconType='alert'
              />
            )) || <EuiLoadingContent style={{ margin: 16 }} />}
          </EuiFlyoutBody>
        )}
        {this.state.currentFile && !this.state.isLoading && (
          <EuiFlyoutBody className='flyout-body'>
            <FileDetails
              currentFile={this.state.currentFile}
              type={type}
              {...this.props}
            />
          </EuiFlyoutBody>
        )}
      </WzFlyout>
    );
  }
}
);
