import { useEffect, useState } from 'react';
import Xcyber360Error from '../../error-factory/errors/Xcyber360Error';
import { ErrorHandler } from '../error-handler';

/**
 *
 * @param callback
 * @returns
 */
export const useErrorHandler = (callback: Function) => {
  const [res, setRes] = useState(null);
  const [error, setError] = useState<Error|Xcyber360Error|null>(null);
  useEffect(() => {
    const handleCallback =  async () => {
      try {
        let res = await callback();
        setRes(res);
        setError(null);
      } catch (error) {
        if (error instanceof Error) {
          error = ErrorHandler.handleError(error);
        }
        setRes(null);
        setError(error as Error | Xcyber360Error);
      }
    }

    handleCallback();
  }, [])
  
  return [res, error];
};
