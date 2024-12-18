import React, { useEffect, useMemo, useState } from 'react';
import { IntlProvider } from 'react-intl';
import {
  EuiDataGrid,
  EuiPageTemplate,
  EuiToolTip,
  EuiButtonIcon,
  EuiDataGridCellValueElementProps,
  EuiFlexGroup,
  EuiFlyout,
  EuiFlyoutBody,
  EuiFlyoutHeader,
  EuiTitle,
  EuiButtonEmpty,
  EuiPanel,
} from '@elastic/eui';
import { SearchResponse } from '../../../../../../../../src/core/server';
import { HitsCounter } from '../../../../../kibana-integrations/discover/application/components/hits_counter/hits_counter';
import { formatNumWithCommas } from '../../../../../kibana-integrations/discover/application/helpers';
import { getXcyber360CorePlugin } from '../../../../../kibana-services';
import {
  ErrorHandler,
  ErrorFactory,
  HttpError,
} from '../../../../../react-services/error-management';
import './inventory.scss';
import { inventoryTableDefaultColumns } from './config';
import {
  MAX_ENTRIES_PER_QUERY,
  getAllCustomRenders,
} from '../../../../common/data-grid/data-grid-service';
import { DiscoverNoResults } from '../../common/components/no_results';
import { LoadingSpinner } from '../../common/components/loading_spinner';
// common components/hooks
import useSearchBar from '../../../../common/search-bar/use-search-bar';
import { useDataGrid } from '../../../../common/data-grid/use-data-grid';
import { useDocViewer } from '../../../../common/doc-viewer/use-doc-viewer';
import { withErrorBoundary } from '../../../../common/hocs';
import { exportSearchToCSV } from '../../../../common/data-grid/data-grid-service';
import { compose } from 'redux';
import { withVulnerabilitiesStateDataSource } from '../../common/hocs/validate-vulnerabilities-states-index-pattern';
import { ModuleEnabledCheck } from '../../common/components/check-module-enabled';
import {
  VulnerabilitiesDataSourceRepository,
  VulnerabilitiesDataSource,
  tParsedIndexPattern,
  PatternDataSource,
} from '../../../../common/data-source';
import { useDataSource } from '../../../../common/data-source/hooks';
import { IndexPattern } from '../../../../../../../../src/plugins/data/public';
import { wzDiscoverRenderColumns } from '../../../../common/xcyber360-discover/render-columns';
import { DocumentViewTableAndJson } from '../../../../common/xcyber360-discover/components/document-view-table-and-json';
import { WzSearchBar } from '../../../../common/search-bar';

const InventoryVulsComponent = () => {
  const {
    dataSource,
    filters,
    fetchFilters,
    fixedFilters,
    isLoading: isDataSourceLoading,
    fetchData,
    setFilters,
  } = useDataSource<tParsedIndexPattern, PatternDataSource>({
    DataSource: VulnerabilitiesDataSource,
    repository: new VulnerabilitiesDataSourceRepository(),
  });
  const { searchBarProps } = useSearchBar({
    indexPattern: dataSource?.indexPattern as IndexPattern,
    filters,
    setFilters,
  });
  const { query } = searchBarProps;

  const [results, setResults] = useState<SearchResponse>({} as SearchResponse);
  const [inspectedHit, setInspectedHit] = useState<any>(undefined);
  const [indexPattern, setIndexPattern] = useState<IndexPattern | undefined>(
    undefined,
  );
  const [isExporting, setIsExporting] = useState<boolean>(false);

  const sideNavDocked = getXcyber360CorePlugin().hooks.useDockedSideNav();

  const onClickInspectDoc = useMemo(
    () => (index: number) => {
      const rowClicked = results.hits.hits[index];
      setInspectedHit(rowClicked);
    },
    [results],
  );

  const DocViewInspectButton = ({
    rowIndex,
  }: EuiDataGridCellValueElementProps) => {
    const inspectHintMsg = 'Inspect vulnerability details';
    return (
      <EuiToolTip content={inspectHintMsg}>
        <EuiButtonIcon
          onClick={() => onClickInspectDoc(rowIndex)}
          iconType='inspect'
          aria-label={inspectHintMsg}
        />
      </EuiToolTip>
    );
  };

  const dataGridProps = useDataGrid({
    ariaLabelledBy: 'Vulnerabilities Inventory Table',
    defaultColumns: inventoryTableDefaultColumns,
    renderColumns: wzDiscoverRenderColumns,
    results,
    indexPattern: indexPattern as IndexPattern,
    DocViewInspectButton,
  });

  const { pagination, sorting, columnVisibility } = dataGridProps;

  const docViewerProps = useDocViewer({
    doc: inspectedHit,
    indexPattern: indexPattern as IndexPattern,
  });

  const onClickExportResults = async () => {
    const params = {
      indexPattern: indexPattern as IndexPattern,
      filters: fetchFilters,
      query,
      fields: columnVisibility.visibleColumns,
      pagination: {
        pageIndex: 0,
        pageSize: results.hits.total,
      },
      sorting,
    };
    try {
      setIsExporting(true);
      await exportSearchToCSV(params);
    } catch (error) {
      const searchError = ErrorFactory.create(HttpError, {
        error,
        message: 'Error downloading csv report',
      });
      ErrorHandler.handleError(searchError);
    } finally {
      setIsExporting(false);
    }
  };

  useEffect(() => {
    if (isDataSourceLoading) {
      return;
    }
    setIndexPattern(dataSource?.indexPattern);
    fetchData({ query, pagination, sorting })
      .then(results => {
        setResults(results);
      })
      .catch(error => {
        const searchError = ErrorFactory.create(HttpError, {
          error,
          message: 'Error fetching data',
        });
        ErrorHandler.handleError(searchError);
      });
  }, [
    JSON.stringify(fetchFilters),
    JSON.stringify(query),
    JSON.stringify(pagination),
    JSON.stringify(sorting),
  ]);

  return (
    <IntlProvider locale='en'>
      <>
        <ModuleEnabledCheck />
        <EuiPageTemplate
          className='vulsInventoryContainer'
          restrictWidth='100%'
          fullHeight={true}
          grow
          paddingSize='none'
          pageContentProps={{ color: 'transparent' }}
        >
          <>
            {isDataSourceLoading ? (
              <LoadingSpinner />
            ) : (
              <WzSearchBar
                appName='inventory-vuls'
                {...searchBarProps}
                fixedFilters={fixedFilters}
                showDatePicker={false}
                showQueryInput={true}
                showQueryBar={true}
                showSaveQuery={true}
              />
            )}
            {!isDataSourceLoading && results?.hits?.total === 0 ? (
              <DiscoverNoResults />
            ) : null}
            {!isDataSourceLoading && results?.hits?.total > 0 ? (
              <EuiPanel
                paddingSize='s'
                hasShadow={false}
                hasBorder={false}
                color='transparent'
              >
                <div className='vulsInventoryDataGrid'>
                  <EuiDataGrid
                    {...dataGridProps}
                    className={sideNavDocked ? 'dataGridDockedNav' : ''}
                    toolbarVisibility={{
                      additionalControls: (
                        <>
                          <HitsCounter
                            hits={results?.hits?.total}
                            showResetButton={false}
                            tooltip={
                              results?.hits?.total &&
                              results?.hits?.total > MAX_ENTRIES_PER_QUERY
                                ? {
                                    ariaLabel: 'Warning',
                                    content: `The query results has exceeded the limit of ${formatNumWithCommas(
                                      MAX_ENTRIES_PER_QUERY,
                                    )} hits. To provide a better experience the table only shows the first ${formatNumWithCommas(
                                      MAX_ENTRIES_PER_QUERY,
                                    )} hits.`,
                                    iconType: 'alert',
                                    position: 'top',
                                  }
                                : undefined
                            }
                          />
                          <EuiButtonEmpty
                            disabled={
                              results?.hits?.total === 0 ||
                              !columnVisibility?.visibleColumns?.length
                            }
                            size='xs'
                            iconType='exportAction'
                            color='primary'
                            isLoading={isExporting}
                            className='euiDataGrid__controlBtn'
                            onClick={onClickExportResults}
                          >
                            Export Formated
                          </EuiButtonEmpty>
                        </>
                      ),
                    }}
                  />
                </div>
              </EuiPanel>
            ) : null}
            {inspectedHit && (
              <EuiFlyout onClose={() => setInspectedHit(undefined)} size='m'>
                <EuiFlyoutHeader>
                  <EuiTitle>
                    <h2>Vulnerability details</h2>
                  </EuiTitle>
                </EuiFlyoutHeader>
                <EuiFlyoutBody>
                  <EuiFlexGroup direction='column'>
                    <DocumentViewTableAndJson
                      document={inspectedHit}
                      indexPattern={indexPattern}
                      renderFields={getAllCustomRenders(
                        inventoryTableDefaultColumns,
                        wzDiscoverRenderColumns,
                      )}
                    />
                  </EuiFlexGroup>
                </EuiFlyoutBody>
              </EuiFlyout>
            )}
          </>
        </EuiPageTemplate>
      </>
    </IntlProvider>
  );
};

export const InventoryVuls = compose(
  withErrorBoundary,
  withVulnerabilitiesStateDataSource,
)(InventoryVulsComponent);
