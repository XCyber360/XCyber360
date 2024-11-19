/*
 * Xcyber360 app - Module for app initialization
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import packageJSON from '../../../package.json';
import { pluginPlatformTemplate } from '../../integration-files/kibana-template';
import { totalmem } from 'os';
import {
  XCYBER360_PLUGIN_PLATFORM_TEMPLATE_NAME,
  PLUGIN_PLATFORM_NAME,
} from '../../../common/constants';
import _ from 'lodash';

export function jobInitializeRun(context) {
  const PLUGIN_PLATFORM_INDEX =
    context.server.config.opensearchDashboards.index;
  context.xcyber360.logger.info(
    `${PLUGIN_PLATFORM_NAME} index: ${PLUGIN_PLATFORM_INDEX}`,
  );
  context.xcyber360.logger.info(`App revision: ${packageJSON.revision}`);

  try {
    // RAM in MB
    context.xcyber360.logger.debug('Getting the total RAM memory');
    const ram = Math.ceil(totalmem() / 1024 / 1024);
    context.xcyber360.logger.info(`Total RAM: ${ram}MB`);
  } catch (error) {
    context.xcyber360.logger.error(
      `Could not check total RAM due to: ${error.message}`,
    );
  }

  const createKibanaTemplate = () => {
    context.xcyber360.logger.debug(
      `Creating template for ${PLUGIN_PLATFORM_INDEX}`,
    );

    try {
      pluginPlatformTemplate.template = PLUGIN_PLATFORM_INDEX + '*';
    } catch (error) {
      context.xcyber360.logger.error('Exception: ' + error.message);
    }

    return context.core.opensearch.client.asInternalUser.indices.putTemplate({
      name: XCYBER360_PLUGIN_PLATFORM_TEMPLATE_NAME,
      order: 0,
      create: true,
      body: pluginPlatformTemplate,
    });
  };

  const createEmptyKibanaIndex = async () => {
    try {
      context.xcyber360.logger.debug(`Creating ${PLUGIN_PLATFORM_INDEX} index.`);
      await context.core.opensearch.client.asInternalUser.indices.create({
        index: PLUGIN_PLATFORM_INDEX,
      });
      context.xcyber360.logger.info(`${PLUGIN_PLATFORM_INDEX} index created`);
    } catch (error) {
      throw new Error(
        `Error creating ${PLUGIN_PLATFORM_INDEX} index: ${error.message}`,
      );
    }
  };

  const fixKibanaTemplate = async () => {
    try {
      context.xcyber360.logger.debug(`Fixing ${PLUGIN_PLATFORM_INDEX} template`);
      await createKibanaTemplate();
      context.xcyber360.logger.info(`${PLUGIN_PLATFORM_INDEX} template created`);
      await createEmptyKibanaIndex();
    } catch (error) {
      throw new Error(
        `Error creating template for ${PLUGIN_PLATFORM_INDEX}: ${error.message}`,
      );
    }
  };

  const getTemplateByName = async () => {
    try {
      context.xcyber360.logger.debug(
        `Getting ${XCYBER360_PLUGIN_PLATFORM_TEMPLATE_NAME} template`,
      );
      await context.core.opensearch.client.asInternalUser.indices.getTemplate({
        name: XCYBER360_PLUGIN_PLATFORM_TEMPLATE_NAME,
      });
      context.xcyber360.logger.debug(
        `No need to create the ${PLUGIN_PLATFORM_INDEX} template, already exists.`,
      );
      await createEmptyKibanaIndex();
    } catch (error) {
      context.xcyber360.logger.warn(error.message || error);
      return fixKibanaTemplate();
    }
  };

  // Does Kibana index exist?
  const checkKibanaStatus = async () => {
    try {
      context.xcyber360.logger.debug(
        `Checking the existence of ${PLUGIN_PLATFORM_INDEX} index`,
      );
      const response =
        await context.core.opensearch.client.asInternalUser.indices.exists({
          index: PLUGIN_PLATFORM_INDEX,
        });
      if (response.body) {
        context.xcyber360.logger.debug(`${PLUGIN_PLATFORM_INDEX} index exist`);
      } else {
        context.xcyber360.logger.debug(
          `${PLUGIN_PLATFORM_INDEX} index does not exist`,
        );
        // No Kibana index created...
        context.xcyber360.logger.info(`${PLUGIN_PLATFORM_INDEX} index not found`);
        await getTemplateByName();
      }
    } catch (error) {
      context.xcyber360.logger.error(error.message || error);
    }
  };

  // Wait until Elasticsearch js is ready
  const checkStatus = async () => {
    try {
      // TODO: wait until opensearch is ready?
      // await server.plugins.opensearch.waitUntilReady();
      return await checkKibanaStatus();
    } catch (error) {
      context.xcyber360.logger.debug(
        'Waiting for opensearch plugin to be ready...',
      );
      setTimeout(() => checkStatus(), 3000);
    }
  };

  // Check Kibana index and if it is prepared, start the initialization of Xcyber360 App.
  return checkStatus();
}
