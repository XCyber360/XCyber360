import { getSavedObject } from '../saved-object/get-saved-object';
import { setSavedObject } from '../saved-object/set-saved-object';
import {
  getXcyber360CheckUpdatesServices,
  getXcyber360Core,
} from '../../plugin-services';
import { API_UPDATES_STATUS } from '../../../common/types';
import { getUpdates } from './get-updates';
import { SAVED_OBJECT_UPDATES } from '../../../common/constants';

const mockedGetSavedObject = getSavedObject as jest.Mock;
jest.mock('../saved-object/get-saved-object');

const mockedSetSavedObject = setSavedObject as jest.Mock;
jest.mock('../saved-object/set-saved-object');

const mockedGetXcyber360Core = getXcyber360Core as jest.Mock;
const mockedGetXcyber360CheckUpdatesServices =
  getXcyber360CheckUpdatesServices as jest.Mock;
jest.mock('../../plugin-services');

describe('getUpdates function', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should return available updates from saved object', async () => {
    mockedGetSavedObject.mockImplementation(() => ({
      last_check_date: '2023-09-30T14:00:00.000Z',
      apis_available_updates: [
        {
          api_id: 'api id',
          current_version: '4.3.1',
          status: API_UPDATES_STATUS.UP_TO_DATE,
          last_available_patch: {
            description:
              '## Manager\r\n\r\n### Fixed\r\n\r\n- Fixed a crash when overwrite rules are triggered...',
            published_date: '2022-05-18T10:12:43Z',
            semver: {
              major: 4,
              minor: 3,
              patch: 8,
            },
            tag: 'v4.3.8',
            title: 'Xcyber360 v4.3.8',
          },
        },
      ],
    }));

    mockedGetXcyber360Core.mockImplementation(() => ({
      serverAPIHostEntries: {
        getHostsEntries: jest.fn(() => []),
      },
    }));

    mockedGetXcyber360CheckUpdatesServices.mockImplementation(() => ({
      logger: {
        debug: jest.fn(),
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
      },
    }));

    const updates = await getUpdates();

    expect(getSavedObject).toHaveBeenCalledTimes(1);
    expect(getSavedObject).toHaveBeenCalledWith(SAVED_OBJECT_UPDATES);

    expect(updates).toEqual({
      last_check_date: '2023-09-30T14:00:00.000Z',
      apis_available_updates: [
        {
          api_id: 'api id',
          current_version: '4.3.1',
          status: API_UPDATES_STATUS.UP_TO_DATE,
          last_available_patch: {
            description:
              '## Manager\r\n\r\n### Fixed\r\n\r\n- Fixed a crash when overwrite rules are triggered...',
            published_date: '2022-05-18T10:12:43Z',
            semver: {
              major: 4,
              minor: 3,
              patch: 8,
            },
            tag: 'v4.3.8',
            title: 'Xcyber360 v4.3.8',
          },
        },
      ],
    });
  });

  test('should return available updates from api', async () => {
    mockedSetSavedObject.mockImplementation(() => ({}));
    mockedGetXcyber360Core.mockImplementation(() => ({
      api: {
        client: {
          asInternalUser: {
            request: jest.fn().mockImplementation(() => ({
              data: {
                data: {
                  uuid: '7f828fd6-ef68-4656-b363-247b5861b84c',
                  current_version: '4.3.1',
                  last_available_patch: {
                    description:
                      '## Manager\r\n\r\n### Fixed\r\n\r\n- Fixed a crash when overwrite rules are triggered...',
                    published_date: '2022-05-18T10:12:43Z',
                    semver: {
                      major: 4,
                      minor: 3,
                      patch: 8,
                    },
                    tag: 'v4.3.8',
                    title: 'Xcyber360 v4.3.8',
                  },
                },
              },
            })),
          },
        },
      },
      manageHosts: {
        get: jest.fn(() => [{ id: 'api id' }]),
      },
    }));
    mockedGetXcyber360CheckUpdatesServices.mockImplementation(() => ({
      logger: {
        debug: jest.fn(),
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
      },
    }));

    const updates = await getUpdates(true);

    expect(updates).toEqual({
      last_check_date: expect.any(Date),
      apis_available_updates: [
        {
          api_id: 'api id',
          current_version: '4.3.1',
          status: API_UPDATES_STATUS.AVAILABLE_UPDATES,
          last_available_patch: {
            description:
              '## Manager\r\n\r\n### Fixed\r\n\r\n- Fixed a crash when overwrite rules are triggered...',
            published_date: '2022-05-18T10:12:43Z',
            semver: {
              major: 4,
              minor: 3,
              patch: 8,
            },
            tag: 'v4.3.8',
            title: 'Xcyber360 v4.3.8',
          },
        },
      ],
    });
  });
});
