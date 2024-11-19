import {
  getAllOptionals,
  getAllOptionalsMacos,
  getDEBAMD64InstallCommand,
  getDEBARM64InstallCommand,
  getLinuxStartCommand,
  getMacOsInstallCommand,
  getMacosStartCommand,
  getRPMAMD64InstallCommand,
  getRPMARM64InstallCommand,
  getWindowsInstallCommand,
  getWindowsStartCommand,
  transformOptionalsParamatersMacOSCommand,
} from './register-agent-os-commands-services';

let test: any;

beforeEach(() => {
  test = {
    optionals: {
      agentGroups: "XCYBER360_AGENT_GROUP='default'",
      agentName: "XCYBER360_AGENT_NAME='test'",
      serverAddress: "XCYBER360_MANAGER='1.1.1.1'",
      xcyber360Password: "XCYBER360_REGISTRATION_PASSWORD='<CUSTOM_PASSWORD>'",
    },
    urlPackage: 'https://test.com/agent.deb',
    xcyber360Version: '4.8.0',
  };
});

describe('getAllOptionals', () => {
  it('should return empty string if optionals is falsy', () => {
    const result = getAllOptionals(null);
    expect(result).toBe('');
  });

  it('should return the correct paramsText', () => {
    const optionals = {
      serverAddress: 'localhost',
      xcyber360Password: 'password',
      agentGroups: 'group1',
      agentName: 'agent1',
      protocol: 'http',
    };
    const result = getAllOptionals(optionals, 'linux');
    expect(result).toBe('localhost password group1 agent1 http ');
  });
});

describe('getDEBAMD64InstallCommand', () => {
  it('should return the correct install command', () => {
    const props = {
      optionals: {
        serverAddress: 'localhost',
        xcyber360Password: 'password',
        agentGroups: 'group1',
        agentName: 'agent1',
        protocol: 'http',
      },
      urlPackage: 'https://example.com/package.deb',
      xcyber360Version: '4.0.0',
    };
    const result = getDEBAMD64InstallCommand(props);
    expect(result).toBe(
      'wget https://example.com/package.deb && sudo localhost password group1 agent1 http dpkg -i ./xcyber360-agent_4.0.0-1_amd64.deb',
    );
  });
});

describe('getDEBAMD64InstallCommand', () => {
  it('should return the correct command', () => {
    let expected = `wget ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.xcyber360Password} ${test.optionals.agentGroups} ${test.optionals.agentName} dpkg -i ./xcyber360-agent_${test.xcyber360Version}-1_amd64.deb`;
    const withAllOptionals = getDEBAMD64InstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;

    expected = `wget ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.agentGroups} dpkg -i ./xcyber360-agent_${test.xcyber360Version}-1_amd64.deb`;
    const withServerAddresAndAgentGroupsOptions =
      getDEBAMD64InstallCommand(test);
    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getDEBARM64InstallCommand', () => {
  it('should return the correct command', () => {
    let expected = `wget ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.xcyber360Password} ${test.optionals.agentGroups} ${test.optionals.agentName} dpkg -i ./xcyber360-agent_${test.xcyber360Version}-1_arm64.deb`;
    const withAllOptionals = getDEBARM64InstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;

    expected = `wget ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.agentGroups} dpkg -i ./xcyber360-agent_${test.xcyber360Version}-1_arm64.deb`;
    const withServerAddresAndAgentGroupsOptions =
      getDEBARM64InstallCommand(test);
    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getRPMAMD64InstallCommand', () => {
  it('should return the correct command', () => {
    let expected = `curl -o xcyber360-agent-4.8.0-1.x86_64.rpm ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.xcyber360Password} ${test.optionals.agentGroups} ${test.optionals.agentName} rpm -ihv xcyber360-agent-${test.xcyber360Version}-1.x86_64.rpm`;
    const withAllOptionals = getRPMAMD64InstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;

    expected = `curl -o xcyber360-agent-4.8.0-1.x86_64.rpm ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.agentGroups} rpm -ihv xcyber360-agent-${test.xcyber360Version}-1.x86_64.rpm`;
    const withServerAddresAndAgentGroupsOptions =
      getRPMAMD64InstallCommand(test);
    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getRPMARM64InstallCommand', () => {
  it('should return the correct command', () => {
    let expected = `curl -o xcyber360-agent-4.8.0-1.aarch64.rpm ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.xcyber360Password} ${test.optionals.agentGroups} ${test.optionals.agentName} rpm -ihv xcyber360-agent-${test.xcyber360Version}-1.aarch64.rpm`;
    const withAllOptionals = getRPMARM64InstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;

    expected = `curl -o xcyber360-agent-4.8.0-1.aarch64.rpm ${test.urlPackage} && sudo ${test.optionals.serverAddress} ${test.optionals.agentGroups} rpm -ihv xcyber360-agent-${test.xcyber360Version}-1.aarch64.rpm`;
    const withServerAddresAndAgentGroupsOptions =
      getRPMARM64InstallCommand(test);
    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getLinuxStartCommand', () => {
  it('returns the correct start command for Linux', () => {
    const startCommand = getLinuxStartCommand({});
    const expectedCommand =
      'sudo systemctl daemon-reload\nsudo systemctl enable xcyber360-agent\nsudo systemctl start xcyber360-agent';

    expect(startCommand).toEqual(expectedCommand);
  });
});

// Windows

describe('getWindowsInstallCommand', () => {
  it('should return the correct install command', () => {
    let expected = `Invoke-WebRequest -Uri ${test.urlPackage} -OutFile \$env:tmp\\xcyber360-agent; msiexec.exe /i \$env:tmp\\xcyber360-agent /q ${test.optionals.serverAddress} ${test.optionals.xcyber360Password} ${test.optionals.agentGroups} ${test.optionals.agentName} `;

    const withAllOptionals = getWindowsInstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;

    expected = `Invoke-WebRequest -Uri ${test.urlPackage} -OutFile \$env:tmp\\xcyber360-agent; msiexec.exe /i \$env:tmp\\xcyber360-agent /q ${test.optionals.serverAddress} ${test.optionals.agentGroups} `;
    const withServerAddresAndAgentGroupsOptions =
      getWindowsInstallCommand(test);

    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getWindowsStartCommand', () => {
  it('should return the correct start command', () => {
    const expectedCommand = 'NET START Xcyber360Svc';

    const result = getWindowsStartCommand({});

    expect(result).toEqual(expectedCommand);
  });
});

// MacOS

describe('getAllOptionalsMacos', () => {
  it('should return empty string if optionals is falsy', () => {
    const result = getAllOptionalsMacos(null);
    expect(result).toBe('');
  });

  it('should return the correct paramsValueList', () => {
    const optionals = {
      serverAddress: 'localhost',
      agentGroups: 'group1',
      agentName: 'agent1',
      protocol: 'http',
      xcyber360Password: 'password',
    };
    const result = getAllOptionalsMacos(optionals);
    expect(result).toBe('localhost && group1 && agent1 && http && password');
  });
});

describe('transformOptionalsParamatersMacOSCommand', () => {
  it('should transform the command correctly', () => {
    const command =
      "' serverAddress && agentGroups && agentName && protocol && xcyber360Password";
    const result = transformOptionalsParamatersMacOSCommand(command);
    expect(result).toBe(
      "' && serverAddress && agentGroups && agentName && protocol && xcyber360Password",
    );
  });
});

describe('getMacOsInstallCommand', () => {
  it('should return the correct macOS installation script', () => {
    let expected = `curl -so xcyber360-agent.pkg ${test.urlPackage} && echo "${test.optionals.serverAddress} && ${test.optionals.agentGroups} && ${test.optionals.agentName} && ${test.optionals.xcyber360Password}\" > /tmp/xcyber360_envs && sudo installer -pkg ./xcyber360-agent.pkg -target /`;

    const withAllOptionals = getMacOsInstallCommand(test);
    expect(withAllOptionals).toEqual(expected);

    delete test.optionals.xcyber360Password;
    delete test.optionals.agentName;
    expected = `curl -so xcyber360-agent.pkg ${test.urlPackage} && echo "${test.optionals.serverAddress} && ${test.optionals.agentGroups}" > /tmp/xcyber360_envs && sudo installer -pkg ./xcyber360-agent.pkg -target /`;

    const withServerAddresAndAgentGroupsOptions = getMacOsInstallCommand(test);
    expect(withServerAddresAndAgentGroupsOptions).toEqual(expected);
  });
});

describe('getMacosStartCommand', () => {
  it('returns the correct start command for macOS', () => {
    const startCommand = getMacosStartCommand({});
    expect(startCommand).toEqual(
      'sudo /Library/xcyber360_agent/bin/xcyber360-control start',
    );
  });
});
