// To launch this file
// yarn test:jest --testEnvironment node --verbose server/routes/xcyber360-hosts
import supertest from 'supertest';
import { createMockPlatformServer } from '../mocks/platform-server.mock';
import { Xcyber360HostsRoutes } from './xcyber360-hosts';

function noop() {}
const logger = {
  debug: noop,
  info: noop,
  warn: noop,
  error: noop,
};
const context = {
  xcyber360: {
    logger,
  },
  xcyber360_core: {
    configuration: {
      _settings: new Map(),
      logger,
      get: jest.fn(),
      set: jest.fn(),
    },
    manageHosts: {
      getEntries: jest.fn(),
      create: jest.fn(),
    },
    dashboardSecurity: {
      isAdministratorUser: jest.fn(),
    },
  },
};
const mockPlatformServer = createMockPlatformServer(context);

beforeAll(async () => {
  // Register settings
  context.xcyber360_core.configuration._settings.set('hosts', {
    options: {
      arrayOf: {
        id: {},
        url: {},
        port: {},
        username: {},
        password: {},
        run_as: {},
      },
    },
  });
  const registerRoutes = router =>
    Xcyber360HostsRoutes(router, {
      configuration: context.xcyber360_core.configuration,
    });
  await mockPlatformServer.start(registerRoutes);
});

afterAll(async () => {
  await mockPlatformServer.stop();
});

describe('[endpoint] GET /hosts/apis', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it.each`
    storedAPIs
    ${[{
    id: 'default',
    url: 'https://localhost',
    port: 55000,
    username: 'test',
    password: 'test',
    run_as: false,
  }]}
    ${[{
    id: 'default',
    url: 'https://localhost',
    port: 55000,
    username: 'test',
    password: 'test',
    run_as: false,
  }, {
    id: 'default2',
    url: 'https://localhost',
    port: 55000,
    username: 'test',
    password: 'test',
    run_as: false,
  }]}
  `('Get API hosts', async ({ storedAPIs }) => {
    let currentAPIs = storedAPIs;
    context.xcyber360_core.manageHosts.getEntries.mockImplementation(() =>
      currentAPIs.map(currentAPI => ({ ...currentAPI, cluster_info: {} })),
    );
    const response = await supertest(mockPlatformServer.getServerListener())
      .get(`/hosts/apis`)
      .expect(200);

    currentAPIs.forEach((currentAPI, index) => {
      Object.keys(currentAPI).forEach(key => {
        expect(response.body[index][key]).toBe(currentAPI[key]);
      });
      expect(response.body[index].cluster_info).toBeDefined();
    });
  });
});
