import { ErrorFactory } from '../error-factory/error-factory';
import {
  IndexerApiError,
  Xcyber360ReportingError,
  Xcyber360ApiError,
  HttpError,
} from '../error-factory/errors';
import { IXcyber360Error, IXcyber360ErrorConstructor } from '../types';
import Xcyber360Error from '../error-factory/errors/Xcyber360Error';
// error orchestrator
import { UIErrorLog } from '../../error-orchestrator/types';
import { ErrorOrchestratorService } from '../../error-orchestrator/error-orchestrator.service';
import axios, { AxiosError } from 'axios';
import { OpenSearchDashboardsResponse } from '../../../../../../src/core/server/http/router/response';

interface ILogCustomOptions {
  title: string;
  message?: string;
}

interface IUrlRequestedTypes {
  [key: string]: IXcyber360ErrorConstructor;
}

export class ErrorHandler {
 
  /**
   * Receives an error and create return a new error instance then treat the error
   * 
   * @param error error instance
   * @param customLogOptions custom log options to show when the error is presented to the UI (toast|logs|blank-screen)
   * @returns 
   */
  static handleError(error: Error, customLogOptions?: ILogCustomOptions): Error | IXcyber360Error {
    if (!error) {
      throw Error('Error must be defined');
    }
    const errorCreated = this.createError(error);
    this.logError(errorCreated, customLogOptions);
    return errorCreated;
  }

  /**
   * Receives an error and create a new error instance depending on the error type defined or not
   *
   * @param error
   * @returns
   */
  static createError(error: Error | AxiosError | string): IXcyber360Error | Error {
    if (!error) {
      throw Error('Error must be defined');
    }
    if (typeof error === 'string') return new Error(error);
    const errorType = this.getErrorType(error);
    if (errorType)
      return ErrorFactory.create(errorType, { error, message: error.message });
    return error;
  }

  /**
   * Reveives an error and return a new error instance depending on the error type
   *
   * @param error
   * @returns
   */
  private static getErrorType(
    error: Error | AxiosError | OpenSearchDashboardsResponse, // ToDo: Get error types
  ): IXcyber360ErrorConstructor | null {
    let errorType = null;
    // if is http error (axios error) then get new to create a new error instance
    if(this.isHttpError(error)){
      errorType = this.getErrorTypeByConfig(error as AxiosError);
    }
    return errorType;
  }

  /**
   * Check if the error received is an http error (axios error)
   * @param error 
   * @returns 
   */
  static isHttpError(error: Error | IXcyber360Error | AxiosError | OpenSearchDashboardsResponse): boolean {
    return axios.isAxiosError(error);
  }

  /**
   * Get the error type depending on the error config only when the error received is a http error and have the config property
   * @param error 
   * @returns 
   */
  private static getErrorTypeByConfig(error: AxiosError): IXcyber360ErrorConstructor | null {
    const requestedUrlbyErrorTypes: IUrlRequestedTypes = {
      '/api': Xcyber360ApiError,
      '/reports': Xcyber360ReportingError,
      '/elastic': IndexerApiError,
    }

    // get the config object from the error
    const requestedUrl = error.response?.config?.url || error.config?.url;
    if (!requestedUrl) return HttpError;

    const urls = Object.keys(requestedUrlbyErrorTypes);
    for (const url of urls) {
      if(requestedUrl.includes(url)) return requestedUrlbyErrorTypes[url];
    }
    return HttpError;
  }

  /**
   * Check if the parameter received is a string
   * @param error
   */
  static isString(error: Error | string): boolean {
    return typeof error === 'string';
  }

  /**
   * This method log the error depending on the error type and the log options defined in the error class
   * @param error
   */
  private static logError(error: Error | IXcyber360Error, customLogOptions?: ILogCustomOptions) {
    // this is a generic error treatment
    // this condition is for the native error classes
    let defaultErrorLog: UIErrorLog = {
      error: {
        title: customLogOptions?.title ? customLogOptions?.title : `[An error has occurred]`,
        message: customLogOptions?.message ? customLogOptions?.message : error.message,
        error: error,
      },
      level: 'ERROR',
      severity: "UI",
      display: true,
      store: false,
    };
    if (error instanceof Xcyber360Error) {
      defaultErrorLog = {
        ...error.logOptions,
        ...{
          error: {
            title: customLogOptions?.title || error.logOptions.error.title || error.message,
            message: customLogOptions?.message || error.logOptions.error.message || error.stack as string,
            error: error,
          }
        }
      };

    }
    ErrorOrchestratorService.handleError(defaultErrorLog);
  }
}
