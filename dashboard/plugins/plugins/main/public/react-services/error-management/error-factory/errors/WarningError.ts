import { IXcyber360ErrorInfo, IXcyber360ErrorLogOpts } from '../../types';
import Xcyber360Error from './Xcyber360Error';

export class WarningError extends Xcyber360Error {
  logOptions: IXcyber360ErrorLogOpts;
  constructor(error: Error, info?: IXcyber360ErrorInfo) {
    super(error, info);
    Object.setPrototypeOf(this, WarningError.prototype);
    this.logOptions = {
      error: {
        message: `[${this.constructor.name}]: ${error.message}`,
        title: `An warning has occurred`,
        error: error,
      },
      level: 'WARNING',
      severity: 'BUSINESS',
      display: true,
      store: false,
    };
  }
}
