import { UIErrorLog } from '../error-orchestrator/types';

export interface IXcyber360ErrorLogOpts extends Omit<UIErrorLog,'context'> {}
export interface IErrorOpts {
  error: Error;
  message: string;
  code?: number;
}

export interface IXcyber360Error extends Error, IErrorOpts {
  error: Error;
  message: string;
  code?: number;
  logOptions: IXcyber360ErrorLogOpts;
}

export interface IXcyber360ErrorConstructor {
  new (error: Error, info: IXcyber360ErrorInfo): IXcyber360Error;
}

export interface IXcyber360ErrorInfo {
  message: string;
  code?: number;
}
