import { useState, useCallback, useEffect, useMemo } from 'react';
import _ from 'lodash';

const variablesEndpoint = `${
  process.env.REACT_APP_AIRFLOW_BASE || 'https://airflow.docker.localhost'
}/api/v1/variables`;

export const checkResponseStatus = (status) => {
  if (status >= 400 && status < 500) {
    throw new Error(400);
  }
  if (status >= 500 && status < 600) {
    throw new Error(500);
  }
  return;
};

const parseOrReturn = (candidate) => {
  try {
    return JSON.parse(candidate);
  } catch {
    return candidate;
  }
};

const extract = (variables) => (type) => {
  const repositoriesVariable = _.filter(variables, {
    key: type,
  });
  if (repositoriesVariable) {
    return _.chain(repositoriesVariable)
      .map((repositoryObject) => parseOrReturn(repositoryObject.value))
      .head()
      .value();
  }
  return null;
};

const useVariables = () => {
  const [storageCredentials, setStorageCredentials] = useState({});
  const [repositories, setRepositories] = useState(null);
  const [variablesStatus, setVariablesStatus] = useState(false);
  const [isLoadingVariables, setIsLoading] = useState(false);
  const [variablesError, setVariablesError] = useState(null);
  const [airflowUserError, setAirflowUserError] = useState(null);
  const [airflowUserName, setAirflowUserName] = useState(null);
  const [airflowPassword, setAirflowPassword] = useState(null);

  const setAirflowCredentials = useCallback(
    (credentials) => {
      setAirflowUserName(credentials.airflowApi_userName);
      setAirflowPassword(credentials.airflowApi_pwd);
    },
    [setAirflowUserName, setAirflowPassword]
  );

  const headers = useMemo(() => {
    if (airflowPassword && airflowUserName) {
      let headers = new Headers();
      headers.append('Content-Type', 'application/json');
      headers.set(
        'Authorization',
        'Basic ' + window.btoa(airflowUserName + ':' + airflowPassword)
      );
      return headers;
    }
  }, [airflowUserName, airflowPassword]);

  const setError = useCallback(
    (error) => {
      switch (error.message) {
        case '400':
          setAirflowUserError(400);
          break;
        default:
          setVariablesError(500);
      }
    },
    [setAirflowUserError, setVariablesError]
  );

  const fetchVariables = useCallback(() => {
    setIsLoading(true);
    try {
      fetch(variablesEndpoint, {
        method: 'GET',
        headers: headers,
      })
        .then((response) => {
          checkResponseStatus(response.status);
          return response;
        })
        .then((response) => response.json())
        .then((json) => {
          if (json.variables) {
            setAirflowUserError(null);
            setVariablesError(null);
            const extractVariable = extract(json.variables);
            const repositories = extractVariable('repositories');
            if (repositories) {
              setRepositories(repositories);
            }
            const storageCredentials = extractVariable('storages');
            if (storageCredentials) {
              setStorageCredentials(storageCredentials);
            }
          } else {
            setError('unknown');
          }
        })
        .catch((error) => {
          setError(error);
        });
    } catch {
      setError('unknown');
    } finally {
      setIsLoading(false);
    }
  }, [headers, setError, setIsLoading]);

  const createVariables = useCallback(
    (variableObject) => {
      if (headers) {
        setVariablesStatus('loading');
        try {
          fetch(variablesEndpoint, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(variableObject),
          })
            .then((response) => {
              checkResponseStatus(response.status);
              setVariablesStatus('success');
              return response;
            })
            .then(() => fetchVariables())
            .catch((error) => {
              setError(error);
              setVariablesStatus('error');
            });
        } catch {
          setError('unknown');
          setVariablesStatus('error');
        }
      }
    },
    [headers, setError, fetchVariables]
  );

  const patchVariables = useCallback(
    (variableObject) => {
      if (headers) {
        const patchURL = `${variablesEndpoint}/${variableObject.key}`;
        setVariablesStatus('loading');
        try {
          fetch(patchURL, {
            method: 'PATCH',
            headers: headers,
            body: JSON.stringify(variableObject),
          })
            .then((response) => {
              checkResponseStatus(response.status);
              setVariablesStatus('success');
              return response;
            })
            .then(() => fetchVariables())
            .catch((error) => {
              setError(error.message);
              setVariablesStatus('error');
            });
        } catch (error) {
          setError(error);
          setVariablesStatus('error');
        }
      }
    },
    [headers, setError, fetchVariables]
  );

  const postVariables = useCallback(
    (variable_key) => (newVariable) => {
      const requestBody = {
        key: variable_key,
        value: JSON.stringify(newVariable),
      };
      if (
        !_.isEmpty(
          variable_key === 'repositories' ? repositories : storageCredentials
        )
      ) {
        patchVariables(requestBody);
      } else {
        createVariables(requestBody);
      }
    },
    [patchVariables, createVariables, repositories, storageCredentials]
  );

  useEffect(() => {
    if (headers) {
      fetchVariables();
      setAirflowUserError(null);
    }
  }, [fetchVariables, headers, setAirflowUserError]);

  useEffect(() => {
    if (variablesStatus === 'success') {
      setTimeout(() => setVariablesStatus(null), 1000);
    }
  }, [variablesStatus]);

  return {
    headers,
    repositories,
    storageCredentials,
    isLoadingVariables,
    variablesError,
    airflowUserError,
    setAirflowCredentials,
    fetchVariables,
    postVariables,
    variablesStatus,
  };
};
export default useVariables;
