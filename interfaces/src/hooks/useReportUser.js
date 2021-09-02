import { useState, useCallback } from 'react';
import superagent from 'superagent';

const authEndpoint = `${
  process.env.REACT_APP_INVENTORYAPI_BASE ||
  'https://inventory-api.docker.localhost'
}/auth`;

const useReportUser = () => {
  const [tokenReportUser, setToken] = useState(null);
  const [isLoadingReportUser, setIsLoading] = useState(false);
  const [reportUserError, setError] = useState(null);

  const loginReportUser = useCallback(
    (credentials) => {
      setIsLoading(true);
      try {
        superagent
          .post(authEndpoint)
          .send({
            userName: credentials.report_userName,
            pwd: credentials.report_pwd,
          })
          .set('Accept', 'application/json')
          .end((error, res) => {
            if (res?.statusCode >= 400) {
              setError(res.statusCode);
            } else if (error) {
              setError(error);
            }
            if (res?.body?.token) {
              setToken(res.body.token);
            }
          });
      } catch {
        setError('network error');
      } finally {
        setIsLoading(false);
      }
    },
    [setIsLoading, setError, setToken]
  );

  return {
    tokenReportUser,
    isLoadingReportUser,
    reportUserError,
    loginReportUser,
  };
};
export default useReportUser;
