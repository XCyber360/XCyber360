/*
 * Xcyber360 app - React component for showing the Mitre Att&ck intelligence flyout.
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React, { useRef, Fragment } from 'react';
import { MitreAttackResources } from './resources';
import { ReferencesTable } from './resource_detail_references_table';

import {
  EuiFlyoutHeader,
  EuiTitle,
  EuiText,
  EuiFlexGroup,
  EuiFlyoutBody,
  EuiFlexItem,
  EuiSpacer,
} from '@elastic/eui';
import { Markdown } from '../../../common/util';
import { WzFlyout } from '../../../common/flyouts';

interface DetailFlyoutType {
  details: any;
  closeFlyout: () => { onClick: () => void };
  onSelectResource: (resource: any) => void;
}

export const ModuleMitreAttackIntelligenceFlyout = ({
  details,
  closeFlyout,
  onSelectResource,
}: DetailFlyoutType) => {
  const startReference = useRef(null);

  return (
    <WzFlyout
      onClose={closeFlyout}
      flyoutProps={{ size: 'l', 'aria-labelledby': `` }}
    >
      <EuiFlyoutHeader hasBorder>
        <EuiTitle size='m'>
          <h2 id='flyoutTitle'>Details</h2>
        </EuiTitle>
      </EuiFlyoutHeader>
      <EuiFlyoutBody>
        <div ref={startReference}>
          <EuiFlexGroup>
            {MitreAttackResources[0].mitreFlyoutHeaderProperties.map(
              detailProperty => (
                <EuiFlexItem
                  key={`mitre_att&ck_intelligence_detail_resource_property_${detailProperty.label}`}
                >
                  <div>
                    <strong>{detailProperty.label}</strong>
                  </div>
                  <EuiText>
                    {detailProperty.render
                      ? detailProperty.render(details[detailProperty.id])
                      : details[detailProperty.id]}
                  </EuiText>
                </EuiFlexItem>
              ),
            )}
          </EuiFlexGroup>
        </div>
        <EuiFlexGroup>
          <EuiFlexItem>
            <div>
              <strong>Description</strong>
            </div>
            <EuiText>
              {details.description ? (
                <Markdown markdown={details.description} />
              ) : (
                ''
              )}
            </EuiText>
          </EuiFlexItem>
        </EuiFlexGroup>
        <EuiFlexGroup>
          <EuiFlexItem>
            {MitreAttackResources.filter(item => details[item.id]).map(item => (
              <Fragment key={`resource_${item.id}`}>
                <ReferencesTable
                  referencesName={item.id}
                  referencesArray={details[item.id]}
                  columns={item.tableColumnsCreator()}
                  backToTop={() => {
                    startReference.current?.scrollIntoView();
                  }}
                />
                <EuiSpacer />
              </Fragment>
            ))}
          </EuiFlexItem>
        </EuiFlexGroup>
      </EuiFlyoutBody>
    </WzFlyout>
  );
};
