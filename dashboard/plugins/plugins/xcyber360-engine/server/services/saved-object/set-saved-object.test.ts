import {
  getInternalSavedObjectsClient,
  getXcyber360CheckUpdatesServices,
} from '../../plugin-services';
import { setSavedObject } from './set-saved-object';

jest.mock('../../plugin-services', () => ({
  getInternalSavedObjectsClient: jest.fn(),
  getXcyber360CheckUpdatesServices: jest.fn(),
}));

const mockedGetInternalObjectsClient =
  getInternalSavedObjectsClient as jest.Mock;
const mockedGetXcyber360CheckUpdatesServices =
  getXcyber360CheckUpdatesServices as jest.Mock;

describe('setSavedObject function', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should return saved object', async () => {
    mockedGetInternalObjectsClient.mockImplementation(() => ({
      create: () => ({ attributes: { hide_update_notifications: true } }),
    }));
    mockedGetXcyber360CheckUpdatesServices.mockImplementation(() => ({
      logger: {
        debug: jest.fn(),
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
      },
    }));

    const response = await setSavedObject(
      'xcyber360-check-updates-user-preferences',
      { hide_update_notifications: true },
      'admin',
    );

    expect(response).toEqual({ hide_update_notifications: true });
  });

  test('should return an error', async () => {
    mockedGetInternalObjectsClient.mockImplementation(() => ({
      create: jest.fn().mockRejectedValue(new Error('setSavedObject error')),
    }));
    mockedGetXcyber360CheckUpdatesServices.mockImplementation(() => ({
      logger: {
        debug: jest.fn(),
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
      },
    }));

    const promise = setSavedObject(
      'xcyber360-check-updates-user-preferences',
      { hide_update_notifications: true },
      'admin',
    );

    await expect(promise).rejects.toThrow('setSavedObject error');
  });
});
