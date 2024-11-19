/**
 * @example
 *   HOST = set in configuration
 *   USER = set in user interface
 *
 * ALL_DISABLED
 *   binary 00 = decimal 0 ---> USER 0 y HOST 0
 *
 * USER_NOT_ALLOWED
 *   binary 01 = decimal 1 ---> USER 0 y HOST 1
 *
 * HOST_DISABLED
 *   binary 10 = decimal 2 ---> USER 1 y HOST 0
 *
 * ENABLED
 *   binary 11 = decimal 3 ---> USER 1 y HOST 1
 */
export enum API_USER_STATUS_RUN_AS {
  ALL_DISABLED = 0, // Xcyber360 HOST and USER API user configured with run_as=false or undefined
  USER_NOT_ALLOWED = 1, // Xcyber360 HOST API user configured with run_as=true in configuration but it has not run_as in Xcyber360 API
  HOST_DISABLED = 2, // Xcyber360 HOST API user configured with run_as=false in configuration but it has not run_as in Xcyber360 API
  ENABLED = 3, // Xcyber360 API user configured with run_as=true and allow run_as
}
