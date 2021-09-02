import { useState, useEffect, useCallback } from 'react';
import { checkResponseStatus } from './useVariables';

const reportEndpoint = `${
  process.env.REACT_APP_INVENTORYAPI_BASE ||
  'https://inventory-api.docker.localhost'
}/report`;

const useReports = () => {
  const [reports, setReports] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState({});
  const [token, setToken] = useState(null);

  const fetchReports = useCallback(() => {
    if (token) {
      setIsLoading(true);
      try {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.set('Authorization', `Bearer ${token}`);
        fetch(reportEndpoint, {
          method: 'GET',
          headers: headers,
        })
          .then((response) => {
            checkResponseStatus(response.status);
            return response;
          })
          .then((response) => response.json())
          .then((json) => {
            setReports(json);
            setError(null);
          })
          .catch((error) => {
            setError(error);
            setReports(null);
          });
      } catch {
        setError('unknown');
      } finally {
        setIsLoading(false);
      }
    }
  }, [token, setIsLoading, setError, setReports]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports, filter, token]);

  return { reports, isLoading, error, setFilter, setToken, fetchReports };
};
export default useReports;
