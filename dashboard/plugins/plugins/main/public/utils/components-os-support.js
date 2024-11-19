/*
 * Xcyber360 app - Components compatibility operative system
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import { XCYBER360_AGENTS_OS_TYPE, XCYBER360_MODULES_ID } from '../../common/constants';

export const UnsupportedComponents = {
  [XCYBER360_AGENTS_OS_TYPE.LINUX]: [],
  [XCYBER360_AGENTS_OS_TYPE.WINDOWS]: [XCYBER360_MODULES_ID.AUDITING, XCYBER360_MODULES_ID.DOCKER, XCYBER360_MODULES_ID.OPEN_SCAP],
  [XCYBER360_AGENTS_OS_TYPE.DARWIN]: [XCYBER360_MODULES_ID.AUDITING, XCYBER360_MODULES_ID.DOCKER, XCYBER360_MODULES_ID.OPEN_SCAP],
  [XCYBER360_AGENTS_OS_TYPE.SUNOS]: [XCYBER360_MODULES_ID.VULNERABILITIES],
  [XCYBER360_AGENTS_OS_TYPE.OTHERS]: [XCYBER360_MODULES_ID.AUDITING, XCYBER360_MODULES_ID.DOCKER, XCYBER360_MODULES_ID.OPEN_SCAP, XCYBER360_MODULES_ID.VULNERABILITIES]
};
