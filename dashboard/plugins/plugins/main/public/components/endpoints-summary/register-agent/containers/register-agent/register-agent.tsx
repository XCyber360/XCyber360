import React, { useState, useEffect } from 'react';
import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiPanel,
  EuiTitle,
  EuiButtonEmpty,
  EuiPage,
  EuiPageBody,
  EuiSpacer,
  EuiProgress,
  EuiButton,
} from '@elastic/eui';
import { WzRequest } from '../../../../../react-services/wz-request';
import { UI_LOGGER_LEVELS } from '../../../../../../common/constants';
import { UI_ERROR_SEVERITIES } from '../../../../../react-services/error-orchestrator/types';
import { ErrorHandler } from '../../../../../react-services/error-management';
import './register-agent.scss';
import { Steps } from '../steps/steps';
import { InputForm } from '../../../../common/form';
import {
  getGroups,
  getMasterConfiguration,
} from '../../services/register-agent-services';
import { useForm } from '../../../../common/form/hooks';
import { FormConfiguration } from '../../../../common/form/types';
import { useSelector } from 'react-redux';
import {
  withErrorBoundary,
  withGlobalBreadcrumb,
  withRouteResolvers,
  withUserAuthorizationPrompt,
} from '../../../../common/hocs';
import GroupInput from '../../components/group-input/group-input';
import { OsCard } from '../../components/os-selector/os-card/os-card';
import { validateAgentName } from '../../utils/validations';
import { compose } from 'redux';
import { endpointSummary } from '../../../../../utils/applications';
import { getXcyber360CorePlugin } from '../../../../../kibana-services';
import { getErrorOrchestrator } from '../../../../../react-services/common-services';
import {
  enableMenu,
  ip,
  nestedResolve,
  savedSearch,
} from '../../../../../services/resolves';
import NavigationService from '../../../../../react-services/navigation-service';

export const RegisterAgent = compose(
  withErrorBoundary,
  withRouteResolvers({ enableMenu, ip, nestedResolve, savedSearch }),
  withGlobalBreadcrumb([
    {
      text: endpointSummary.breadcrumbLabel,
      href: `#${endpointSummary.redirectTo()}`,
    },
    { text: 'Deploy new agent' },
  ]),
  withUserAuthorizationPrompt([
    [{ action: 'agent:create', resource: '*:*:*' }],
  ]),
)(() => {
  const configuration = useSelector(
    (state: { appConfig: { data: any } }) => state.appConfig.data,
  );
  const [xcyber360Version, setXcyber360Version] = useState('');
  const [haveUdpProtocol, setHaveUdpProtocol] = useState<boolean | null>(false);
  const [loading, setLoading] = useState(false);
  const [xcyber360Password, setXcyber360Password] = useState('');
  const [groups, setGroups] = useState([]);
  const [needsPassword, setNeedsPassword] = useState<boolean>(false);

  const initialFields: FormConfiguration = {
    operatingSystemSelection: {
      type: 'custom',
      initialValue: '',
      component: props => {
        return <OsCard {...props} />;
      },
      options: {
        groups,
      },
    },
    serverAddress: {
      type: 'text',
      initialValue: configuration['enrollment.dns'] || '',
      validate:
        getXcyber360CorePlugin().configuration._settings.get('enrollment.dns')
          .validate,
    },
    agentName: {
      type: 'text',
      initialValue: '',
      validate: validateAgentName,
    },

    agentGroups: {
      type: 'custom',
      initialValue: [],
      component: props => {
        return <GroupInput {...props} />;
      },
      options: {
        groups,
      },
    },
  };

  const form = useForm(initialFields);

  const getMasterConfig = async () => {
    const masterConfig = await getMasterConfiguration();
    if (masterConfig?.remote) {
      setHaveUdpProtocol(masterConfig.remote.isUdp);
    }
    return masterConfig;
  };

  const getXcyber360Version = async () => {
    try {
      const result = await WzRequest.apiReq('GET', '/', {});
      return result?.data?.data?.api_version;
    } catch (error) {
      const options = {
        context: `RegisterAgent.getXcyber360Version`,
        level: UI_LOGGER_LEVELS.ERROR,
        severity: UI_ERROR_SEVERITIES.BUSINESS,
        error: {
          error: error,
          message: error.message || error,
          title: `Could not get the Xcyber360 version: ${error.message || error}`,
        },
      };
      getErrorOrchestrator().handleError(options);
      return version;
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const xcyber360Version = await getXcyber360Version();
        const { auth: authConfig } = await getMasterConfig();
        // get xcyber360 password configuration
        let xcyber360Password = '';
        const needsPassword = authConfig?.auth?.use_password === 'yes';
        if (needsPassword) {
          xcyber360Password =
            configuration?.['enrollment.password'] ||
            authConfig?.['authd.pass'] ||
            '';
        }
        const groups = await getGroups();
        setNeedsPassword(needsPassword);
        setXcyber360Password(xcyber360Password);
        setXcyber360Version(xcyber360Version);
        setGroups(groups);
        setLoading(false);
      } catch (error) {
        setXcyber360Version(xcyber360Version);
        setLoading(false);
        const options = {
          context: 'RegisterAgent',
          level: UI_LOGGER_LEVELS.ERROR,
          severity: UI_ERROR_SEVERITIES.BUSINESS,
          display: true,
          store: false,
          error: {
            error: error,
            message: error.message || error,
            title: error.name || error,
          },
        };
        ErrorHandler.handleError(error, options);
      }
    };

    fetchData();
  }, []);

  const osCard = (
    <InputForm {...form.fields.operatingSystemSelection}></InputForm>
  );

  return (
    <div>
      <EuiPage restrictWidth='1000px' style={{ background: 'transparent' }}>
        <EuiPageBody>
          <EuiFlexGroup>
            <EuiFlexItem>
              <EuiPanel className='register-agent-wizard-container'>
                <div className='register-agent-wizard-close'>
                  <EuiButtonEmpty
                    size='s'
                    href={NavigationService.getInstance().getUrlForApp(
                      endpointSummary.id,
                      {
                        path: `#${endpointSummary.redirectTo()}`,
                      },
                    )}
                    iconType='cross'
                  >
                    Close
                  </EuiButtonEmpty>
                </div>
                <EuiFlexGroup>
                  <EuiFlexItem>
                    <EuiTitle>
                      <h2 className='register-agent-wizard-title'>
                        Deploy new agent
                      </h2>
                    </EuiTitle>
                  </EuiFlexItem>
                </EuiFlexGroup>
                <EuiSpacer />
                {loading ? (
                  <>
                    <EuiFlexItem>
                      <EuiProgress size='xs' color='primary' />
                    </EuiFlexItem>
                    <EuiSpacer></EuiSpacer>
                  </>
                ) : (
                  <EuiFlexItem>
                    <Steps
                      form={form}
                      needsPassword={needsPassword}
                      xcyber360Password={xcyber360Password}
                      osCard={osCard}
                      connection={{
                        isUDP: haveUdpProtocol ? true : false,
                      }}
                    />
                  </EuiFlexItem>
                )}
                <EuiFlexGroup
                  justifyContent='flexEnd'
                  style={{ marginRight: '0.3rem' }}
                >
                  <EuiFlexItem grow={false}>
                    <EuiButton
                      className='close-button'
                      fill
                      color='primary'
                      href={NavigationService.getInstance().getUrlForApp(
                        endpointSummary.id,
                        {
                          path: `#${endpointSummary.redirectTo()}`,
                        },
                      )}
                    >
                      Close
                    </EuiButton>
                  </EuiFlexItem>
                </EuiFlexGroup>
              </EuiPanel>
            </EuiFlexItem>
          </EuiFlexGroup>
        </EuiPageBody>
      </EuiPage>
    </div>
  );
});
