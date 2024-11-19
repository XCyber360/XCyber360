import { IXcyber360ErrorInfo, IXcyber360ErrorLogOpts } from '../../types';
import Xcyber360Error from './Xcyber360Error';

export class HttpError extends Xcyber360Error {
  logOptions: IXcyber360ErrorLogOpts;
  constructor(error: Error, info?: IXcyber360ErrorInfo) {
    super(error, info);
    this.logOptions = {
      error: {
        message: `[${this.constructor.name}]: ${error.message}`,
        title: `An error has occurred`,
        error: error,
      },
      level: 'ERROR',
      severity: 'BUSINESS',
      display: true,
      store: false,
    };
  }
}