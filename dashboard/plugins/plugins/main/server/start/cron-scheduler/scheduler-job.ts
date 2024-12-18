import { jobs } from './predefined-jobs';
import { IApi, SaveDocument } from './index';
import { ErrorHandler } from './error-handler';
import { configuredJobs } from './configured-jobs';

export class SchedulerJob {
  jobName: string;
  saveDocument: SaveDocument;
  context: any;
  logger: any;
  apiClient: any;

  constructor(jobName: string, context) {
    this.jobName = jobName;
    this.context = context;
    this.logger = context.xcyber360.logger;
    this.apiClient = context.xcyber360.api.client.asInternalUser;
    this.saveDocument = new SaveDocument(context);
  }

  public async run() {
    try {
      const { index, status } = (await configuredJobs(this.context, {}))[
        this.jobName
      ];
      if (!status) {
        return;
      }
      const hosts = await this.getApiObjects();
      const jobPromises = hosts.map(async host => {
        try {
          const { status } = (
            await configuredJobs(this.context, {
              host,
              jobName: this.jobName,
            })
          )[this.jobName];
          if (!status) return;
          return await this.getResponses(host);
        } catch (error) {
          ErrorHandler(error, this.logger);
        }
      });
      const data = (await Promise.all(jobPromises))
        .filter(promise => !!promise)
        .flat();
      Array.isArray(data) &&
        !!data.length &&
        (await this.saveDocument.save(data, index));
    } catch (error) {
      ErrorHandler(error, this.logger);
    }
  }

  private async getApiObjects() {
    const { apis } = jobs[this.jobName];
    const hostsResponse: IApi[] =
      await this.context.xcyber360_core.manageHosts.getEntries({
        excludePassword: true,
      });
    if (!hostsResponse.length)
      throw {
        error: 10001,
        message: 'No API host configured in configuration',
      };
    if (apis && apis.length) {
      return this.filterHosts(hostsResponse, apis);
    }
    return hostsResponse;
  }

  private filterHosts(hosts: IApi[], apis: string[]) {
    const filteredHosts = hosts.filter(host => apis.includes(host.id));
    if (filteredHosts.length <= 0) {
      throw {
        error: 10002,
        message: 'No host was found with the indicated ID',
      };
    }
    return filteredHosts;
  }

  private async getResponses(host): Promise<object[]> {
    const { request, params } = jobs[this.jobName];
    const data: object[] = [];

    if (typeof request === 'string') {
      const apiResponse = await this.apiClient.request('GET', request, params, {
        apiHostID: host.id,
      });
      data.push({ ...apiResponse.data, apiName: host.id });
    } else {
      await this.getResponsesForIRequest(host, data);
    }
    return data;
  }

  private async getResponsesForIRequest(host: any, data: object[]) {
    const { request, params } = jobs[this.jobName];
    const fieldName = this.getParamName(
      typeof request !== 'string' && request.request,
    );
    const paramList = await this.getParamList(fieldName, host);
    for (const param of paramList) {
      const paramRequest =
        typeof request !== 'string' && request.request.replace(/\{.+\}/, param);
      if (!!paramRequest) {
        const apiResponse = await this.apiClient.request(
          'GET',
          paramRequest,
          params,
          { apiHostID: host.id },
        );
        data.push({
          ...apiResponse.data,
          apiName: host.id,
          [fieldName]: param,
        });
      }
    }
  }

  private getParamName(request): string {
    const regexResult = /\{(?<fieldName>.+)\}/.exec(request);
    if (regexResult === null)
      throw {
        error: 10003,
        message: `The parameter is not found in the Request: ${request}`,
      };
    // @ts-ignore
    const { fieldName } = regexResult.groups;
    if (fieldName === undefined || fieldName === '')
      throw {
        error: 10004,
        message: `Invalid field in the request: {request: ${request}, field: ${fieldName}}`,
      };
    return fieldName;
  }

  private async getParamList(fieldName, host) {
    const { request } = jobs[this.jobName];
    // @ts-ignore
    const apiResponse = await this.apiClient.request(
      'GET',
      request.params[fieldName].request,
      {},
      { apiHostID: host.id },
    );
    const { affected_items } = apiResponse.data.data;
    if (affected_items === undefined || affected_items.length === 0)
      throw {
        error: 10005,
        message: `Empty response when tried to get the parameters list: ${JSON.stringify(
          apiResponse.data,
        )}`,
      };
    const values = affected_items.map(this.mapParamList);
    return values;
  }

  private mapParamList(item) {
    if (typeof item !== 'object') {
      return item;
    }
    const keys = Object.keys(item);
    if (keys.length > 1 || keys.length < 0)
      throw {
        error: 10006,
        message: `More than one key or none were obtained: ${keys}`,
      };
    return item[keys[0]];
  }
}
