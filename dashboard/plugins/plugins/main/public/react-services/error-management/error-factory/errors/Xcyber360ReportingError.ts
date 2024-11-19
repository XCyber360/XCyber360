import { IXcyber360ErrorInfo, IXcyber360ErrorLogOpts } from '../../types';
import { HttpError } from './HttpError';

export class Xcyber360ReportingError extends HttpError {
  constructor(error: Error, info?: IXcyber360ErrorInfo) {
    super(error, info);
  }
}